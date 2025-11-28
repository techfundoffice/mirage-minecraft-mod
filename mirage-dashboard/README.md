# 🎨 Mirage Workflow Dashboard

A beautiful React.js dashboard for managing AI-powered video transformations using the Mirage ComfyUI workflow.

## 🌟 Features

- 📤 **Drag & Drop Video Upload** - Easy video file upload interface
- 🎨 **Style Selection** - Choose from multiple transformation styles (Minecraft, Anime, Cyberpunk, Enhanced)
- 📊 **Real-time Progress** - Live job status tracking with progress bars
- 💾 **Download Results** - Instant download of transformed videos
- 📈 **Analytics Dashboard** - View statistics and job history
- 🔄 **Auto-refresh** - Automatic polling for job updates
- 🎯 **RESTful API** - Complete REST API backend with Flask

## 🚀 Live Dashboard

**🌐 Frontend**: https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai  
**🔧 API**: https://5000-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai

## 📸 Screenshots

### Main Dashboard
- Upload interface with style selector
- Real-time statistics cards
- Job queue with status indicators

### Features
- ✅ Drag & drop video upload
- ✅ 4 transformation styles
- ✅ Real-time progress tracking
- ✅ One-click download
- ✅ Job history & management

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons
- **CSS3** - Custom responsive styling

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin support
- **Python 3.12** - Backend processing
- **ComfyUI Integration** - Video workflow engine

## 📦 Installation

### Prerequisites
```bash
# Node.js 18+ and npm
node --version  # Should be 18+
npm --version

# Python 3.10+
python3 --version
```

### Setup

```bash
# Clone and navigate
cd /home/user/webapp/mirage-dashboard

# Install frontend dependencies
npm install

# Install backend dependencies  
pip3 install flask flask-cors

# Create required directories
mkdir -p logs server/uploads server/outputs
```

## 🚀 Running the Dashboard

### Option 1: Quick Start (Recommended)

```bash
./start.sh
```

This starts both the API server (port 5000) and React frontend (port 5173).

### Option 2: Manual Start

**Terminal 1 - API Server:**
```bash
cd /home/user/webapp/mirage-dashboard
python3 server/api_server.py
```

**Terminal 2 - React Frontend:**
```bash
cd /home/user/webapp/mirage-dashboard
npm run dev
```

### Option 3: Production Build

```bash
# Build for production
npm run build

# Serve with a static server
npm install -g serve
serve -s dist
```

## 📖 Usage Guide

### 1. Upload a Video

1. Open the dashboard in your browser
2. Select a transformation style (Minecraft, Anime, Cyberpunk, or Enhanced)
3. Click "Choose Video File" or drag & drop a video
4. Click "Start Transformation"

### 2. Monitor Progress

- View real-time status in the Jobs section
- Watch the progress bar fill up
- Check the statistics cards at the top

### 3. Download Results

- Once completed, click the "Download Result" button
- Video downloads automatically as MP4

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
```

Returns API server status and configuration.

### Get Available Styles
```http
GET /api/styles
```

Returns list of available transformation styles.

### Upload Video
```http
POST /api/upload
Content-Type: multipart/form-data

Body: { video: <file> }
```

Uploads a video file and returns filename.

### Create Job
```http
POST /api/jobs
Content-Type: application/json

Body: {
  "input_file": "filename.mp4",
  "style": "minecraft"
}
```

Creates a new transformation job.

### List Jobs
```http
GET /api/jobs
```

Returns all jobs with their status.

### Get Job Status
```http
GET /api/jobs/{job_id}
```

Get detailed status of a specific job.

### Download Result
```http
GET /api/jobs/{job_id}/download
```

Download the transformed video file.

### Get Statistics
```http
GET /api/stats
```

Returns dashboard statistics (total, completed, processing, failed).

## 🎨 Available Styles

### Minecraft
- Pixelated blocks (16x16 grid)
- Enhanced saturation
- Classic blocky aesthetic
- Best for: Gaming content, retro look

### Anime
- Cel-shading effect
- Edge detection
- Smooth gradients
- Best for: Animation style, artistic videos

### Cyberpunk
- Neon blue glow
- Enhanced blue channel
- Futuristic tones
- Best for: Sci-fi content, night scenes

### Enhanced (Default)
- Contrast boost
- Saturation enhancement
- Balanced improvement
- Best for: General videos

## 📁 Project Structure

```
mirage-dashboard/
├── public/              # Static assets
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx      # Main dashboard component
│   │   └── Dashboard.css      # Dashboard styles
│   ├── App.jsx         # Root component
│   ├── App.css         # Global styles
│   └── main.jsx        # Entry point
├── server/
│   ├── api_server.py   # Flask API server
│   ├── uploads/        # Uploaded videos
│   └── outputs/        # Processed videos
├── logs/               # Server logs
├── start.sh            # Quick start script
├── package.json        # npm configuration
└── vite.config.js      # Vite configuration
```

## 🔧 Configuration

### API URL
Update the API URL in `src/components/Dashboard.jsx`:
```javascript
const API_URL = 'http://localhost:5000/api'
```

### Ports
- Frontend: `5173` (Vite default)
- Backend: `5000` (Flask default)

Change in:
- `vite.config.js` for frontend
- `server/api_server.py` for backend

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill processes on ports
lsof -ti:5000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### CORS Issues
Ensure Flask-CORS is installed and enabled in `api_server.py`.

### Upload Fails
Check that `server/uploads/` directory exists and has write permissions.

### Jobs Not Processing
1. Verify ComfyUI path in `api_server.py`
2. Check that `run_demo.py` is executable
3. View logs in `logs/api.log`

### Frontend Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🔐 Security Notes

### For Production:
1. Add authentication/authorization
2. Validate file uploads (size, type)
3. Rate limit API endpoints
4. Use HTTPS
5. Sanitize user inputs
6. Add CSRF protection
7. Use environment variables for secrets

### Current Implementation:
- ⚠️ No authentication (demo only)
- ⚠️ No file size limits
- ⚠️ In-memory job storage

## 📊 Performance

### Recommended Specs:
- **CPU**: 2+ cores
- **RAM**: 4GB+
- **Disk**: 10GB+ free space
- **Network**: Stable connection for polling

### Optimization Tips:
1. Increase polling interval for many jobs
2. Implement pagination for job list
3. Add Redis for job queue
4. Use WebSockets instead of polling
5. Implement job cleanup (delete old jobs)

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY server ./server
COPY ../comfyui ../comfyui
RUN pip install flask flask-cors
EXPOSE 5000
CMD ["python3", "server/api_server.py"]
```

### Cloud Deployment
- **Frontend**: Deploy to Vercel, Netlify, or Cloudflare Pages
- **Backend**: Deploy to AWS Lambda, Google Cloud Run, or Heroku
- **Storage**: Use S3 for videos instead of local filesystem

## 📝 Development

### Run in Development Mode

```bash
# Frontend (auto-reload)
npm run dev

# Backend (auto-reload)
export FLASK_ENV=development
python3 server/api_server.py
```

### Build for Production

```bash
npm run build
# Output in dist/
```

### Linting

```bash
npm run lint
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Same as Mirage Minecraft Mod

## 🔗 Related Projects

- **Mirage Minecraft Mod**: https://github.com/techfundoffice/mirage-minecraft-mod
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Decart Platform**: https://platform.decart.ai

## 💡 Future Enhancements

- [ ] WebSocket for real-time updates
- [ ] User authentication
- [ ] Video preview before processing
- [ ] Custom style parameters
- [ ] Batch processing
- [ ] Job scheduling
- [ ] Video thumbnails
- [ ] Progress notifications
- [ ] Export workflow configurations
- [ ] Integration with Mirage API (production)

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: See guides in parent repository
- **Community**: Join Decart AI Discord

---

**Built with ❤️ for the Mirage Minecraft Mod project**

---

## 🎉 Quick Links

- 🌐 **Live Dashboard**: https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai
- 🔧 **API Endpoint**: https://5000-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai
- 📚 **Main Project**: https://github.com/techfundoffice/mirage-minecraft-mod
- 🚀 **Release**: https://github.com/techfundoffice/mirage-minecraft-mod/releases/tag/v1.0.0

**Start transforming videos now!** 🎬✨
