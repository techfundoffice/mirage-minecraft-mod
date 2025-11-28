# 🔗 URL Input & Prepopulation Feature

## Overview

Added ability to load videos from URLs and prepopulate the dashboard with URL parameters. This enables easy sharing of transformation links and streamlined workflows.

---

## ✨ New Features

### 1. URL Input Field ✅
Users can now paste video URLs directly into the dashboard instead of uploading files.

**Location**: Below the file upload section  
**Function**: Downloads video from URL and processes it

### 2. URL Parameter Prepopulation ✅
Dashboard can be prepopulated using URL query parameters.

**Parameters**:
- `url` - Video URL to load
- `style` - Transformation style to apply

---

## 🎯 Usage Examples

### Manual URL Entry

1. **Open Dashboard**:
   ```
   https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai
   ```

2. **Enter Video URL**:
   - Paste URL in "Or Load from URL" input field
   - Example: `https://example.com/sample-video.mp4`

3. **Select Style**:
   - Choose from: Minecraft, Anime, Cyberpunk, or Enhanced

4. **Click "Load from URL"**:
   - Video downloads from URL
   - Automatically uploads and starts transformation

---

### Prepopulated URL

Share links with prepopulated video URLs:

#### Basic Example
```
https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=https://example.com/video.mp4
```

#### With Style Parameter
```
https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=https://example.com/video.mp4&style=anime
```

#### Multiple Parameters
```
https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=VIDEO_URL&style=cyberpunk
```

---

## 🎨 Supported Styles

| Style ID | Name | Description |
|----------|------|-------------|
| `minecraft` | Minecraft | Pixelated blocky style |
| `anime` | Anime | Cel-shaded cartoon style |
| `cyberpunk` | Cyberpunk | Neon glow style |
| `default` | Enhanced | Enhanced quality |

---

## 📝 URL Encoding

When passing URLs as parameters, they should be URL-encoded:

### JavaScript Example
```javascript
const videoUrl = 'https://example.com/my video.mp4'
const style = 'anime'
const dashboardUrl = `https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai`
const prepopulatedUrl = `${dashboardUrl}?url=${encodeURIComponent(videoUrl)}&style=${style}`

// Opens: https://5173-.../dashboard?url=https%3A%2F%2Fexample.com%2Fmy%20video.mp4&style=anime
window.open(prepopulatedUrl)
```

### Python Example
```python
from urllib.parse import urlencode

video_url = 'https://example.com/sample.mp4'
style = 'minecraft'
dashboard_base = 'https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai'

params = {
    'url': video_url,
    'style': style
}

prepopulated_url = f"{dashboard_base}?{urlencode(params)}"
print(prepopulated_url)
```

### cURL Example
```bash
VIDEO_URL="https://example.com/video.mp4"
STYLE="anime"
ENCODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$VIDEO_URL'))")

DASHBOARD="https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai"
echo "${DASHBOARD}?url=${ENCODED_URL}&style=${STYLE}"
```

---

## 🔄 Workflow

### Manual URL Input Flow
```
1. User opens dashboard
2. User pastes video URL in input field
3. User clicks "Load from URL"
4. Dashboard downloads video from URL
   - Shows progress: "Downloading... 45%"
5. Video uploaded to API
   - Shows progress: "Uploading... 78%"
6. Job created automatically
7. Processing begins
8. User downloads result
```

### Prepopulated URL Flow
```
1. User clicks prepopulated link
   - Example: dashboard?url=VIDEO&style=anime
2. Dashboard opens with:
   - URL field filled: VIDEO
   - Style selected: anime
3. User clicks "Load from URL"
4. Rest of flow is same as manual input
```

---

## 💡 Use Cases

### 1. Quick Sharing
Share transformation links with friends:
```
Hey! Transform this video:
https://dashboard-url?url=https://my-server.com/funny-cat.mp4&style=anime
```

### 2. Automation Scripts
Automate video transformations:
```bash
#!/bin/bash
for video in videos/*.mp4; do
  # Upload to your server
  URL=$(upload_video "$video")
  
  # Open in dashboard
  open "https://dashboard-url?url=$URL&style=cyberpunk"
done
```

### 3. Integration with Other Apps
Embed transformation links in other applications:
```javascript
// In your app
function transformVideo(videoUrl, style) {
  const dashboardUrl = 'https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai'
  const url = `${dashboardUrl}?url=${encodeURIComponent(videoUrl)}&style=${style}`
  window.open(url, '_blank')
}
```

### 4. Bookmarklets
Create browser bookmarklets:
```javascript
javascript:(function(){
  var url = prompt('Enter video URL:');
  if(url) {
    window.open('https://dashboard-url?url=' + encodeURIComponent(url) + '&style=anime');
  }
})();
```

---

## 🎨 UI Components

### URL Input Section
Located below the file upload section with:
- **Text Input**: For entering/displaying video URL
- **Load Button**: Downloads and uploads the video
- **Hint Text**: Shows example usage with URL parameters
- **Progress Indicator**: Shows download/upload progress

### Visual Design
- Clean separation from file upload (border-top)
- Matches existing dashboard styling
- Responsive design for mobile
- Purple gradient consistent with branding

---

## ⚙️ Technical Implementation

### Frontend (Dashboard.jsx)

#### URL State Management
```javascript
const [videoUrl, setVideoUrl] = useState('')
const [isDownloadingFromUrl, setIsDownloadingFromUrl] = useState(false)
```

#### URL Parameter Parsing
```javascript
useEffect(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const urlParam = urlParams.get('url')
  const styleParam = urlParams.get('style')
  
  if (urlParam) {
    setVideoUrl(decodeURIComponent(urlParam))
  }
  if (styleParam) {
    setSelectedStyle(styleParam)
  }
}, [])
```

#### URL Download Handler
```javascript
const handleUrlDownload = async () => {
  // Download video from URL
  const response = await axios.get(videoUrl, {
    responseType: 'blob',
    onDownloadProgress: (progressEvent) => {
      const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
      setUploadProgress(progress)
    }
  })

  // Convert to File object
  const filename = videoUrl.split('/').pop().split('?')[0] || 'video.mp4'
  const file = new File([response.data], filename, { type: 'video/mp4' })

  // Upload using existing mutation
  uploadMutation.mutate(file)
}
```

---

## 🔒 Security Considerations

### CORS Requirements
- Video URLs must be accessible from the browser
- Server hosting videos must allow CORS
- Use CORS proxies if needed for restricted content

### URL Validation
- URLs are validated by axios during download
- Invalid URLs show error message
- No server-side URL validation (client-side only)

### Content Type
- Only video/* content types are supported
- File is converted to video/mp4 for upload
- Original filename extracted from URL

---

## 📊 Features Comparison

| Feature | File Upload | URL Input |
|---------|-------------|-----------|
| Source | Local disk | Internet URL |
| Size Limit | Browser dependent | Network dependent |
| Speed | Fast (local) | Depends on network |
| Prepopulation | ❌ No | ✅ Yes |
| Shareable | ❌ No | ✅ Yes |
| Progress | ✅ Yes | ✅ Yes (2-stage) |
| CORS | N/A | Required |

---

## 🧪 Testing

### Test URL Input
```bash
# Test with demo video
DEMO_URL="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"

# Open in browser
open "https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=$DEMO_URL&style=minecraft"
```

### Test Different Styles
```bash
BASE="https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai"
VIDEO="https://example.com/test.mp4"

# Minecraft
open "$BASE?url=$VIDEO&style=minecraft"

# Anime
open "$BASE?url=$VIDEO&style=anime"

# Cyberpunk
open "$BASE?url=$VIDEO&style=cyberpunk"

# Enhanced
open "$BASE?url=$VIDEO&style=default"
```

---

## 🐛 Troubleshooting

### Issue: "Failed to download video from URL"

**Causes**:
1. CORS not enabled on video server
2. Invalid URL
3. Network timeout
4. File too large

**Solutions**:
1. Use CORS proxy
2. Verify URL in browser first
3. Check network connection
4. Use smaller video files

---

### Issue: URL not prepopulating

**Causes**:
1. URL not properly encoded
2. Invalid style parameter
3. Browser cached old page

**Solutions**:
1. Use `encodeURIComponent()` for URL encoding
2. Check style is one of: minecraft, anime, cyberpunk, default
3. Hard refresh browser (Ctrl+Shift+R)

---

### Issue: Progress stuck at 0%

**Causes**:
1. Server not sending Content-Length header
2. Network issue
3. Large file downloading slowly

**Solutions**:
1. Wait longer (large files take time)
2. Check network tab in browser DevTools
3. Try smaller video file

---

## 📚 Examples

### Example 1: Share Gaming Video
```
Transform my gameplay:
https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=https://cdn.example.com/gameplay.mp4&style=minecraft
```

### Example 2: Anime Converter
```html
<a href="https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=https://videos.example.com/clip.mp4&style=anime">
  Convert to Anime Style
</a>
```

### Example 3: Batch Processing
```javascript
const videos = [
  'https://server.com/video1.mp4',
  'https://server.com/video2.mp4',
  'https://server.com/video3.mp4'
]

videos.forEach(url => {
  const link = `https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=${encodeURIComponent(url)}&style=cyberpunk`
  console.log(`Process: ${link}`)
})
```

---

## 🎯 Future Enhancements

Potential improvements:
- [ ] Support for multiple video formats
- [ ] Batch URL processing
- [ ] URL history/favorites
- [ ] Download progress preview
- [ ] Custom style parameters
- [ ] Playlist support
- [ ] Authentication for private URLs
- [ ] URL validation before download

---

## 📊 Summary

### ✅ What Was Added

1. **URL Input Field**: Text input for video URLs
2. **URL Parameter Support**: Prepopulate via query params
3. **Download Functionality**: Fetch videos from URLs
4. **Progress Indicators**: Two-stage progress (download + upload)
5. **Style Prepopulation**: Set style via URL parameter
6. **Error Handling**: User-friendly error messages
7. **Responsive Design**: Mobile-friendly UI
8. **Documentation**: Hint text and examples

### 🎯 Benefits

- ✅ Easy video sharing via links
- ✅ Streamlined workflow for URL-based videos
- ✅ Integration-friendly for other apps
- ✅ No file upload needed for public videos
- ✅ Faster for videos already online
- ✅ Shareable transformation links

---

## 🔗 Quick Links

- **Dashboard**: https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai
- **Example (with URL)**: https://5173-ims7flew2qqlmi3wl6flu-de59bda9.sandbox.novita.ai?url=VIDEO_URL&style=anime
- **GitHub Repo**: https://github.com/techfundoffice/mirage-minecraft-mod

---

*Feature added: 2025-11-28*  
*Status: ✅ LIVE*  
*Version: Dashboard v1.1*
