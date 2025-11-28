# 🎨 Mirage ComfyUI Headless Workflow Guide

## Overview

This guide shows you how to use the **Mirage Minecraft Mod** technology in a **headless ComfyUI workflow** without needing a graphical Minecraft client. Perfect for server environments, batch processing, and automated video transformation.

## 🎯 What This Does

Transform any video using Decart's Mirage AI - the same technology that powers the Minecraft mod - but in a headless, scriptable workflow:

```
Input Video → Mirage API → AI-Transformed Video
```

**Examples:**
- Transform gameplay recordings into different art styles
- Batch process multiple videos
- Create style variations of existing videos
- Run on servers without displays

---

## 📋 Prerequisites

### Required
- ✅ Python 3.10+ (3.12 recommended)
- ✅ ComfyUI installed
- ✅ Mirage API key (from Decart platform)
- ✅ Input video file

### System Requirements
- **CPU**: Multi-core recommended
- **RAM**: 8GB+ recommended
- **Disk**: Space for input/output videos
- **Network**: Stable internet for API communication

---

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to ComfyUI directory
cd /home/user/webapp/comfyui

# Install additional dependencies
pip install aiortc websockets aiohttp opencv-python

# Verify installation
python3 -c "import aiortc, websockets, cv2; print('✅ All dependencies installed')"
```

### 2. Get Your API Key

Visit: https://platform.decart.ai
- Sign up / Log in
- Navigate to API Keys
- Create a new key
- Copy your API key

### 3. Prepare Your Video

```bash
# Example: Use any video file
cp /path/to/your/video.mp4 input_video.mp4

# Or create a test video
ffmpeg -f lavfi -i testsrc=duration=10:size=512x512:rate=20 \
  -pix_fmt yuv420p input_video.mp4
```

### 4. Run the Workflow

```bash
# Basic usage
python3 run_mirage_headless.py \
  --input input_video.mp4 \
  --output output_mirage.mp4 \
  --api-key YOUR_API_KEY \
  --prompt "minecraft style, blocky textures"

# With custom settings
python3 run_mirage_headless.py \
  -i my_video.mp4 \
  -o transformed_video.mp4 \
  -k YOUR_API_KEY \
  -p "cyberpunk neon city, futuristic"
```

---

## 📖 Detailed Usage

### Command Line Options

```bash
python3 run_mirage_headless.py [OPTIONS]

Required:
  -i, --input PATH        Input video file path
  -k, --api-key KEY       Mirage API key

Optional:
  -o, --output PATH       Output video path (default: output_mirage.mp4)
  -p, --prompt TEXT       Style transformation prompt
  -w, --workflow PATH     Custom workflow JSON file
```

### Example Commands

**1. Basic Transformation**
```bash
python3 run_mirage_headless.py \
  -i gameplay.mp4 \
  -k "your-api-key-here" \
  -p "minecraft blocky style"
```

**2. Custom Output**
```bash
python3 run_mirage_headless.py \
  --input recording.mp4 \
  --output transformed_cyberpunk.mp4 \
  --api-key "your-key" \
  --prompt "cyberpunk neon aesthetic, futuristic city"
```

**3. Batch Processing**
```bash
for video in videos/*.mp4; do
  output="output/$(basename $video)"
  python3 run_mirage_headless.py \
    -i "$video" \
    -o "$output" \
    -k "your-api-key" \
    -p "anime style, vibrant colors"
done
```

---

## 🎨 Style Prompts

### Popular Prompts

**Minecraft Style:**
```
minecraft style, blocky textures, pixelated, low poly
```

**Cyberpunk:**
```
cyberpunk neon city, futuristic, neon lights, rain, dystopian
```

**Anime:**
```
anime style, cel-shaded, vibrant colors, japanese animation
```

**Watercolor:**
```
watercolor painting, artistic, soft brush strokes, pastel colors
```

**Oil Painting:**
```
oil painting, classical art, renaissance style, detailed brushwork
```

**Cartoon:**
```
cartoon style, exaggerated features, bright colors, cel-shaded
```

### Tips for Better Prompts
- Be specific about the style you want
- Include details about lighting, colors, textures
- Mention art movements or references
- Use descriptive adjectives
- Test and iterate

---

## 🔧 ComfyUI Workflow Structure

The headless workflow consists of 5 nodes:

### Node 1: Video Input
```python
MirageVideoInput
- Loads video file
- Resizes frames to target resolution
- Converts to tensor format
```

### Node 2: Mirage Connection
```python
MirageConnect
- Creates session with Mirage API
- Establishes WebRTC connection
- Handles authentication
```

### Node 3: Transform
```python
MirageTransform
- Sends frames via WebRTC
- Applies style transformation
- Receives transformed frames
```

### Node 4: Video Output
```python
MirageVideoOutput
- Converts frames to video format
- Writes output file
- Applies encoding
```

### Node 5: Disconnect
```python
MirageDisconnect
- Closes WebRTC connection
- Cleans up resources
```

---

## 🛠️ Advanced Configuration

### Custom Workflow JSON

Create your own `custom_workflow.json`:

```json
{
  "1": {
    "inputs": {
      "video_path": "input.mp4",
      "frame_rate": 30,
      "width": 1024,
      "height": 1024
    },
    "class_type": "MirageVideoInput"
  },
  "2": {
    "inputs": {
      "api_key": "YOUR_KEY",
      "enabled": true
    },
    "class_type": "MirageConnect"
  },
  "3": {
    "inputs": {
      "session": ["2", 0],
      "images": ["1", 0],
      "prompt": "your custom prompt",
      "enhance_prompt": true
    },
    "class_type": "MirageTransform"
  },
  "4": {
    "inputs": {
      "images": ["3", 0],
      "output_path": "output.mp4",
      "fps": 30
    },
    "class_type": "MirageVideoOutput"
  }
}
```

Use with:
```bash
python3 run_mirage_headless.py \
  -i input.mp4 \
  -w custom_workflow.json \
  -k your-key
```

---

## 📊 Performance Tuning

### Resolution Settings

**Low Quality (Fast)**
```json
"width": 256,
"height": 256,
"fps": 15
```

**Medium Quality (Balanced)**
```json
"width": 512,
"height": 512,
"fps": 20
```

**High Quality (Slow)**
```json
"width": 1024,
"height": 1024,
"fps": 30
```

### Processing Time Estimates

| Resolution | FPS | Est. Time per 10s video |
|------------|-----|-------------------------|
| 256x256    | 15  | ~2 minutes              |
| 512x512    | 20  | ~5 minutes              |
| 1024x1024  | 30  | ~15 minutes             |

*Times vary based on network speed and server load*

---

## 🐛 Troubleshooting

### Common Issues

**1. "Failed to connect to Mirage API"**
```bash
# Check API key
echo $API_KEY

# Verify network connectivity
curl -I https://oasis2.decart.ai

# Check API key validity
python3 -c "import requests; print(requests.post('https://oasis2.decart.ai/api/create-session', json={'apiKey': 'YOUR_KEY'}).status_code)"
```

**2. "Module not found" errors**
```bash
# Reinstall dependencies
pip install --upgrade aiortc websockets aiohttp opencv-python

# Verify Python version
python3 --version  # Should be 3.10+
```

**3. "Video file not found"**
```bash
# Check file exists
ls -lh input_video.mp4

# Check file permissions
chmod 644 input_video.mp4

# Verify video format
ffprobe input_video.mp4
```

**4. "Out of memory" errors**
```bash
# Reduce resolution
python3 run_mirage_headless.py -i input.mp4 --width 256 --height 256

# Process shorter clips
ffmpeg -i long_video.mp4 -t 10 short_clip.mp4
python3 run_mirage_headless.py -i short_clip.mp4
```

**5. "WebRTC connection timeout"**
```bash
# Check firewall settings
sudo ufw allow 3478/udp  # STUN
sudo ufw allow 19302/udp  # Google STUN

# Test STUN server
python3 -c "from aiortc import RTCPeerConnection; print('WebRTC OK')"
```

---

## 🔐 Security Best Practices

### API Key Management

**DON'T:**
- ❌ Commit API keys to version control
- ❌ Share API keys publicly
- ❌ Hardcode keys in scripts

**DO:**
- ✅ Use environment variables
- ✅ Use config files (gitignored)
- ✅ Rotate keys regularly

**Example with environment variable:**
```bash
export MIRAGE_API_KEY="your-api-key"

python3 run_mirage_headless.py \
  -i input.mp4 \
  -k "$MIRAGE_API_KEY"
```

**Example with config file:**
```bash
# config.env
MIRAGE_API_KEY=your-api-key

# Load and run
source config.env
python3 run_mirage_headless.py -i input.mp4 -k "$MIRAGE_API_KEY"
```

---

## 🚀 Production Deployment

### Docker Container

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy workflow
COPY comfyui /app/comfyui

WORKDIR /app/comfyui

ENTRYPOINT ["python3", "run_mirage_headless.py"]
```

**Build and run:**
```bash
docker build -t mirage-headless .
docker run -v $(pwd)/videos:/videos \
  mirage-headless \
  -i /videos/input.mp4 \
  -o /videos/output.mp4 \
  -k "$MIRAGE_API_KEY"
```

### Kubernetes Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mirage-transform
spec:
  template:
    spec:
      containers:
      - name: mirage
        image: mirage-headless:latest
        args:
          - "-i"
          - "/input/video.mp4"
          - "-o"
          - "/output/transformed.mp4"
          - "-k"
          - "$(MIRAGE_API_KEY)"
        env:
          - name: MIRAGE_API_KEY
            valueFrom:
              secretKeyRef:
                name: mirage-secrets
                key: api-key
        volumeMounts:
          - name: input-volume
            mountPath: /input
          - name: output-volume
            mountPath: /output
      restartPolicy: Never
      volumes:
        - name: input-volume
          persistentVolumeClaim:
            claimName: video-input-pvc
        - name: output-volume
          persistentVolumeClaim:
            claimName: video-output-pvc
```

---

## 📈 Monitoring & Logging

### Enable Verbose Logging

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run with verbose output
python3 run_mirage_headless.py -i input.mp4 -k "$KEY" --verbose
```

### Track Progress

The script outputs progress indicators:
```
[1/5] Loading video input...
   Loaded 200 frames
[2/5] Connecting to Mirage API...
   ✅ Connected successfully
[3/5] Transforming video with AI...
   Processed 200 frames
[4/5] Saving output video...
[5/5] Disconnecting...

✅ Success! Output saved to: output_mirage.mp4
```

---

## 🔗 Resources

### Documentation
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Mirage Platform**: https://platform.decart.ai
- **Oasis 2.0**: https://oasis2.decart.ai
- **WebRTC**: https://webrtc.org/

### Community
- **GitHub Issues**: Report bugs and request features
- **Discord**: Join the Decart AI community
- **Forum**: Share your creations

### Related Projects
- **Original Mod**: https://github.com/techfundoffice/mirage-minecraft-mod
- **Decart Platform**: https://platform.decart.ai/models
- **ComfyUI Custom Nodes**: https://github.com/comfyanonymous/ComfyUI

---

## 🎉 Success!

You now have a fully functional headless Mirage workflow in ComfyUI!

**Next Steps:**
1. Experiment with different prompts
2. Process your own videos
3. Automate batch transformations
4. Share your creations with the community

**Need Help?**
- Check the troubleshooting section
- Open an issue on GitHub
- Join the community Discord

---

## 📄 License

MIT License - Same as the Mirage Minecraft Mod

---

**Happy Transforming!** 🎨✨
