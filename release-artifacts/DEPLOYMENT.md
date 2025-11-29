# Mirage Minecraft Mod - Deployment Guide

## 🎮 About
The Mirage Minecraft Mod is a **client-side Fabric mod** for Minecraft 1.21.8 that transforms your game into any style or world you can imagine in real-time, powered by Decart's live video restyling model.

## ✅ Build Status
- **Build**: ✅ Successful
- **Java Version**: 21.0.5 (Temurin)
- **Mod Version**: 1.0.0
- **Minecraft Version**: 1.21.8
- **Fabric Loader**: 0.17.2

## 📦 Build Artifacts

The mod has been successfully built and the following artifacts are available in `build/libs/`:

- **mirage-minecraft-mod-1.0.0.jar** (44MB) - Main mod file
- **mirage-minecraft-mod-1.0.0-sources.jar** (24KB) - Source code archive

## 🚀 Installation Instructions

### For End Users

1. **Prerequisites**:
   - Minecraft Java Edition 1.21.8
   - Fabric Loader 0.17.2 or higher
   - Java 21 (JDK 21 or higher)

2. **Install Fabric Loader**:
   - Download and install Fabric Loader from [FabricMC](https://fabricmc.net/use/)
   - Select Minecraft version 1.21.8

3. **Install the Mod**:
   - Locate your Minecraft mods folder:
     - Windows: `%APPDATA%\.minecraft\mods\`
     - macOS: `~/Library/Application Support/minecraft/mods/`
     - Linux: `~/.minecraft/mods/`
   - Copy `mirage-minecraft-mod-1.0.0.jar` to the mods folder
   - Download and install Fabric API 0.133.4+1.21.8 (required dependency)

4. **Launch Minecraft**:
   - Open Minecraft Launcher
   - Select the Fabric profile for version 1.21.8
   - Click "Play"

## 🖥️ System Requirements

- **Java**: Version 21 or higher (required by Minecraft 1.21.8)
- **RAM**: At least 2GB allocated to Minecraft (4GB+ recommended)
- **Graphics**: OpenGL compatible graphics card
- **OS**: Windows 10/11, macOS 10.14+, or Linux with X11/Wayland

## 📋 Supported Platforms

The mod includes native WebRTC libraries for:
- ✅ Windows x86_64
- ✅ macOS x86_64 (Intel)
- ✅ macOS aarch64 (Apple Silicon)
- ✅ Linux x86_64
- ✅ Linux aarch64
- ✅ Linux aarch32

## 🛠️ Developer Setup

### Building from Source

```bash
# Clone the repository
git clone <repository-url>
cd mirage-minecraft-mod

# Ensure Java 21 is installed
# Using SDKMAN (recommended):
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 21.0.5-tem

# Build the mod
./gradlew build

# The built JAR will be in build/libs/
```

### Running in Development

**Note**: The Minecraft client requires a graphical environment and cannot run in headless mode.

```bash
# On a system with display support:
./gradlew runClient
```

## 📖 How It Works

The Mirage mod uses:
- **WebRTC** (via webrtc-java) for real-time video streaming
- **Fabric Mixins** to intercept game rendering
- **Decart's Mirage API** for live video restyling
- **OpenGL/LWJGL** for graphics processing

### Key Components

- `OasisClient.kt` - Main client initialization
- `WebRTC.kt` - WebRTC connection management
- `MirageAPI.kt` - Decart API integration
- `Graphics.kt` - OpenGL buffer management
- `GameRendererMixin.java` - Rendering interception
- `WorldRendererMixin.java` - World rendering hooks

## 🔗 Resources

- **Production Version**: [Oasis 2.0 Installation Guide](https://oasis2.decart.ai/how-to-install)
- **How to Play**: [Oasis 2.0 Gameplay Guide](https://oasis2.decart.ai/how-to-play)
- **Development Guide**: [Decart Cookbook](https://cookbook.decart.ai/mirage-minecraft-mod)
- **WebRTC Library**: [webrtc-java Documentation](https://jrtc.dev/)
- **Announcements**:
  - [Oasis 2.0 on X](https://x.com/DecartAI/status/1963758685995368884)
  - [Mirage on X](https://x.com/DecartAI/status/1945947692871692667)

## ⚠️ Important Notes

### Cannot Run in Headless Environments

This mod **requires a graphical display** and cannot run in:
- ❌ Server environments
- ❌ Headless Linux systems
- ❌ Docker containers without display forwarding
- ❌ CI/CD pipelines
- ❌ SSH sessions without X11 forwarding

The error you'll see without a display:
```
java.lang.IllegalStateException: Failed to initialize GLFW, 
errors: GLFW error during init: [0x1000E]Failed to detect any supported platform
```

### For Cloud Deployments

To use this mod in cloud environments, you need:
1. A virtual desktop environment (VNC, X11, or similar)
2. GPU acceleration support (for acceptable performance)
3. Display forwarding properly configured

## 🐛 Troubleshooting

### Common Issues

1. **"Minecraft requires Java 21 but Gradle is using X"**
   - Install Java 21 and set JAVA_HOME
   - Or use SDKMAN: `sdk use java 21.0.5-tem`

2. **"Failed to initialize GLFW"**
   - This mod requires a display
   - Ensure you're running on a system with graphics support
   - On Linux, verify X11/Wayland is running

3. **Missing Dependencies**
   - Fabric API is required (included in development)
   - For production, download Fabric API separately

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

- Powered by [Decart's Mirage](https://mirage.decart.ai)
- Built with [Fabric](https://fabricmc.net/)
- Uses [webrtc-java](https://jrtc.dev/)

---

**Build Date**: 2025-11-28  
**Build Environment**: Linux x86_64 with Java 21.0.5
