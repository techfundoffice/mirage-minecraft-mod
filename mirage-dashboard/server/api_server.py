#!/usr/bin/env python3
"""
Mirage Workflow API Server
Flask API to manage video transformation workflows
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import subprocess
import uuid
import json
import time
from pathlib import Path
from datetime import datetime
from threading import Thread

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent / 'outputs'
COMFYUI_PATH = Path(__file__).parent.parent.parent / 'comfyui'

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Job storage (in-memory for demo, use Redis/DB in production)
jobs = {}

class Job:
    def __init__(self, job_id, input_file, style):
        self.id = job_id
        self.input_file = input_file
        self.output_file = None
        self.style = style
        self.status = 'pending'  # pending, processing, completed, failed
        self.progress = 0
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
        self.error = None

def run_workflow(job_id, input_path, output_path, style):
    """Run the ComfyUI workflow in background"""
    job = jobs[job_id]
    job.status = 'processing'
    
    try:
        # Run demo workflow
        cmd = [
            'python3',
            str(COMFYUI_PATH / 'run_demo.py'),
            '-i', str(input_path),
            '-o', str(output_path),
            '-s', style
        ]
        
        # Execute workflow
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            job.status = 'completed'
            job.output_file = str(output_path.name)
            job.progress = 100
            job.completed_at = datetime.now().isoformat()
        else:
            job.status = 'failed'
            job.error = result.stderr or 'Unknown error'
            
    except Exception as e:
        job.status = 'failed'
        job.error = str(e)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'comfyui_path': str(COMFYUI_PATH),
        'upload_folder': str(UPLOAD_FOLDER),
        'output_folder': str(OUTPUT_FOLDER)
    })

@app.route('/api/styles', methods=['GET'])
def get_styles():
    """Get available transformation styles"""
    styles = [
        {
            'id': 'minecraft',
            'name': 'Minecraft',
            'description': 'Pixelated blocky style with 16x16 blocks',
            'thumbnail': '/styles/minecraft.jpg'
        },
        {
            'id': 'anime',
            'name': 'Anime',
            'description': 'Cel-shaded cartoon style with edge detection',
            'thumbnail': '/styles/anime.jpg'
        },
        {
            'id': 'cyberpunk',
            'name': 'Cyberpunk',
            'description': 'Neon glow with blue/purple tones',
            'thumbnail': '/styles/cyberpunk.jpg'
        },
        {
            'id': 'default',
            'name': 'Enhanced',
            'description': 'Enhanced contrast and saturation',
            'thumbnail': '/styles/default.jpg'
        }
    ]
    return jsonify(styles)

@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Upload video file"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_FOLDER / unique_filename
    
    # Save file
    file.save(str(file_path))
    
    return jsonify({
        'filename': unique_filename,
        'path': str(file_path),
        'size': os.path.getsize(file_path)
    })

@app.route('/api/upload-url', methods=['POST'])
def upload_from_url():
    """Download video from URL and save it"""
    import requests
    
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Download video from URL
        response = requests.get(video_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Determine file extension from URL or Content-Type
        file_ext = '.mp4'  # default
        if video_url.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
            file_ext = Path(video_url).suffix
        elif 'content-type' in response.headers:
            content_type = response.headers['content-type']
            if 'mp4' in content_type:
                file_ext = '.mp4'
            elif 'webm' in content_type:
                file_ext = '.webm'
            elif 'quicktime' in content_type:
                file_ext = '.mov'
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_FOLDER / unique_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return jsonify({
            'filename': unique_filename,
            'path': str(file_path),
            'size': os.path.getsize(file_path)
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to download video: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing video: {str(e)}'}), 500

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new transformation job"""
    data = request.json
    
    input_filename = data.get('input_file')
    style = data.get('style', 'minecraft')
    
    if not input_filename:
        return jsonify({'error': 'Input file required'}), 400
    
    input_path = UPLOAD_FOLDER / input_filename
    if not input_path.exists():
        return jsonify({'error': 'Input file not found'}), 404
    
    # Create job
    job_id = str(uuid.uuid4())
    output_filename = f"{job_id}_output.mp4"
    output_path = OUTPUT_FOLDER / output_filename
    
    job = Job(job_id, input_filename, style)
    jobs[job_id] = job
    
    # Start processing in background
    thread = Thread(target=run_workflow, args=(job_id, input_path, output_path, style))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'created_at': job.created_at
    }), 201

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    job_list = []
    for job_id, job in jobs.items():
        job_list.append({
            'id': job.id,
            'input_file': job.input_file,
            'output_file': job.output_file,
            'style': job.style,
            'status': job.status,
            'progress': job.progress,
            'created_at': job.created_at,
            'completed_at': job.completed_at,
            'error': job.error
        })
    
    return jsonify(job_list)

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get job status"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'id': job.id,
        'input_file': job.input_file,
        'output_file': job.output_file,
        'style': job.style,
        'status': job.status,
        'progress': job.progress,
        'created_at': job.created_at,
        'completed_at': job.completed_at,
        'error': job.error
    })

@app.route('/api/jobs/<job_id>/download', methods=['GET'])
def download_result(job_id):
    """Download processed video"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    if job.status != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    output_path = OUTPUT_FOLDER / job.output_file
    if not output_path.exists():
        return jsonify({'error': 'Output file not found'}), 404
    
    return send_file(
        str(output_path),
        mimetype='video/mp4',
        as_attachment=True,
        download_name=f"mirage_{job.style}_{job.output_file}"
    )

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get workflow statistics"""
    total_jobs = len(jobs)
    completed = sum(1 for j in jobs.values() if j.status == 'completed')
    processing = sum(1 for j in jobs.values() if j.status == 'processing')
    failed = sum(1 for j in jobs.values() if j.status == 'failed')
    
    return jsonify({
        'total_jobs': total_jobs,
        'completed': completed,
        'processing': processing,
        'failed': failed,
        'pending': total_jobs - completed - processing - failed
    })

if __name__ == '__main__':
    print("🚀 Starting Mirage Workflow API Server...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")
    print(f"📁 ComfyUI path: {COMFYUI_PATH}")
    print("🌐 Server running on http://localhost:5000")
    print("📝 API docs: http://localhost:5000/api/health")
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
