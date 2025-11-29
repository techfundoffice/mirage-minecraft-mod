#!/usr/bin/env python3
"""
Demo Mode - Mirage ComfyUI Workflow
Demonstrates the workflow without requiring API key
Uses mock transformation for testing
"""

import sys
import cv2
import numpy as np
from pathlib import Path

def apply_demo_transform(frame, style="minecraft"):
    """Apply a demo transformation effect"""
    
    if style == "minecraft":
        # Pixelate effect (blocky like Minecraft)
        h, w = frame.shape[:2]
        block_size = 16
        
        # Downsample
        temp = cv2.resize(frame, (w // block_size, h // block_size), interpolation=cv2.INTER_LINEAR)
        # Upsample back
        output = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        
        # Increase saturation
        hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        output = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    elif style == "anime":
        # Anime/cartoon effect
        # Bilateral filter for smooth colors
        output = cv2.bilateralFilter(frame, 9, 75, 75)
        
        # Edge detection
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 9, 2)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Combine
        output = cv2.bitwise_and(output, edges)
        
    elif style == "cyberpunk":
        # Cyberpunk neon effect
        # Increase blue channel
        output = frame.copy()
        output[:, :, 0] = np.clip(output[:, :, 0] * 1.5, 0, 255)  # Blue
        output[:, :, 1] = np.clip(output[:, :, 1] * 0.8, 0, 255)  # Green
        
        # Add glow
        blur = cv2.GaussianBlur(output, (21, 21), 0)
        output = cv2.addWeighted(output, 0.7, blur, 0.3, 0)
        
    else:
        # Default: slight contrast/saturation boost
        output = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
    
    return output

def process_video(input_path, output_path, style="minecraft"):
    """Process video with demo transformation"""
    
    print("="*60)
    print("🎨 Mirage ComfyUI Demo Mode")
    print("="*60)
    print(f"📥 Input:  {input_path}")
    print(f"📤 Output: {output_path}")
    print(f"🎭 Style:  {style}")
    print("="*60)
    print()
    
    # Open input video
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        print(f"❌ Error: Could not open video: {input_path}")
        return False
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"📊 Video Info:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Total Frames: {total_frames}")
    print()
    
    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    if not out.isOpened():
        print(f"❌ Error: Could not create output video: {output_path}")
        cap.release()
        return False
    
    print("🔄 Processing...")
    print()
    
    # Process frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply transformation
        transformed = apply_demo_transform(frame, style)
        
        # Write frame
        out.write(transformed)
        
        frame_count += 1
        
        # Progress indicator
        if frame_count % 10 == 0 or frame_count == total_frames:
            progress = (frame_count / total_frames) * 100
            bar_length = 40
            filled = int(bar_length * frame_count / total_frames)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r   [{bar}] {progress:.1f}% ({frame_count}/{total_frames} frames)", end='')
    
    print()  # New line after progress
    
    # Cleanup
    cap.release()
    out.release()
    
    print()
    print("="*60)
    print(f"✅ Success! Video transformed and saved to:")
    print(f"   {output_path}")
    print("="*60)
    print()
    print("📝 Note: This is a demo transformation using local effects.")
    print("   For full AI-powered transformation, use the Mirage API:")
    print("   python3 run_mirage_headless.py -i input.mp4 -k YOUR_API_KEY")
    print()
    
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Demo mode for Mirage ComfyUI (no API key required)"
    )
    parser.add_argument(
        "-i", "--input",
        default="test_input.mp4",
        help="Input video file (default: test_input.mp4)"
    )
    parser.add_argument(
        "-o", "--output",
        default="demo_output.mp4",
        help="Output video file (default: demo_output.mp4)"
    )
    parser.add_argument(
        "-s", "--style",
        choices=["minecraft", "anime", "cyberpunk", "default"],
        default="minecraft",
        help="Demo style effect (default: minecraft)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)
    
    # Process video
    output_path = Path(args.output)
    try:
        success = process_video(input_path, output_path, args.style)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
