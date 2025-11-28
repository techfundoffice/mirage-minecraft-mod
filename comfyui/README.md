# 🎨 Mirage ComfyUI Integration

## Headless Video Transformation with Mirage API

Transform videos using Decart's Mirage AI in a headless ComfyUI workflow - no Minecraft or GUI required!

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install aiortc websockets aiohttp opencv-python

# 2. Run transformation
python3 run_mirage_headless.py \
  --input test_input.mp4 \
  --output output.mp4 \
  --api-key YOUR_MIRAGE_API_KEY \
  --prompt "minecraft style, blocky textures"
```

---

## 📁 Project Structure

```
comfyui/
├── custom_nodes/
│   └── mirage_integration/
│       ├── __init__.py          # Node registration
│       └── nodes.py             # Custom ComfyUI nodes
├── run_mirage_headless.py       # Headless runner script
├── mirage_workflow.json         # Sample workflow
├── test_input.mp4               # Test video file
└── README.md                    # This file
```

---

## 🔧 Custom Nodes

### 1. MirageVideoInput
Loads video files and prepares frames for processing

**Inputs:**
- `video_path`: Path to input video
- `frame_rate`: Target frame rate
- `width`: Frame width
- `height`: Frame height

**Outputs:**
- `IMAGE`: Tensor of video frames

### 2. MirageConnect
Establishes connection to Mirage API

**Inputs:**
- `api_key`: Your Mirage API key
- `enabled`: Enable/disable connection

**Outputs:**
- `MIRAGE_SESSION`: Active session object

### 3. MirageTransform
Transforms video using AI style transfer

**Inputs:**
- `session`: Mirage session from MirageConnect
- `images`: Video frames to transform
- `prompt`: Style description
- `enhance_prompt`: Auto-enhance prompt

**Outputs:**
- `IMAGE`: Transformed video frames

### 4. MirageVideoOutput
Saves transformed frames as video file

**Inputs:**
- `images`: Transformed frames
- `output_path`: Output file path
- `fps`: Output frame rate

### 5. MirageDisconnect
Closes Mirage session and cleans up

**Inputs:**
- `session`: Mirage session to close

---

## 📖 Usage Examples

### Basic Command Line

```bash
python3 run_mirage_headless.py \
  -i input_video.mp4 \
  -o output_video.mp4 \
  -k "your-api-key" \
  -p "anime style, vibrant colors"
```

### With Custom Workflow

```bash
python3 run_mirage_headless.py \
  -i video.mp4 \
  -w custom_workflow.json \
  -k "your-api-key"
```

### Batch Processing

```bash
#!/bin/bash
for video in videos/*.mp4; do
  output="transformed/$(basename $video)"
  python3 run_mirage_headless.py \
    -i "$video" \
    -o "$output" \
    -k "$MIRAGE_API_KEY" \
    -p "cyberpunk neon city"
done
```

---

## 🎨 Style Prompt Examples

**Minecraft:**
```
minecraft style, blocky textures, pixelated, low poly
```

**Cyberpunk:**
```
cyberpunk neon city, futuristic, rain, neon lights, dystopian
```

**Anime:**
```
anime style, cel-shaded, vibrant colors, japanese animation
```

**Watercolor:**
```
watercolor painting, artistic, soft brush strokes, pastel colors
```

---

## 🔧 Configuration

### Workflow JSON Structure

```json
{
  "1": {
    "inputs": {
      "video_path": "input.mp4",
      "frame_rate": 20,
      "width": 512,
      "height": 512
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
      "prompt": "your prompt",
      "enhance_prompt": false
    },
    "class_type": "MirageTransform"
  }
}
```

---

## 🐛 Troubleshooting

### Module Not Found
```bash
pip install --upgrade aiortc websockets aiohttp opencv-python
```

### Connection Timeout
```bash
# Check network
ping oasis2.decart.ai

# Verify API key
curl -X POST https://oasis2.decart.ai/api/create-session \
  -H "Content-Type: application/json" \
  -d '{"apiKey":"YOUR_KEY"}'
```

### Video Not Loading
```bash
# Verify video file
ffprobe input.mp4

# Check permissions
chmod 644 input.mp4
```

---

## 🔗 Resources

- **Full Guide**: See `../COMFYUI_MIRAGE_GUIDE.md`
- **Mirage Platform**: https://platform.decart.ai
- **Original Mod**: https://github.com/techfundoffice/mirage-minecraft-mod
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI

---

## 📄 License

MIT License - Same as Mirage Minecraft Mod

---

**Created from the Mirage Minecraft Mod technology**
**Powered by Decart AI** 🚀
