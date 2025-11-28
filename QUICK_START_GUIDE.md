# 🎮 Quick Start Guide - Run Mirage Minecraft Mod NOW!

## 🚀 Get Playing in 5 Steps

### Step 1: Download the Mod (2 minutes)
```bash
# Open your terminal and run:
curl -L -O https://github.com/techfundoffice/mirage-minecraft-mod/releases/download/v1.0.0/mirage-minecraft-mod-1.0.0.jar
```

**Or download via browser:**
👉 https://github.com/techfundoffice/mirage-minecraft-mod/releases/download/v1.0.0/mirage-minecraft-mod-1.0.0.jar

---

### Step 2: Install Java 21 (5 minutes)

**Windows:**
```powershell
# Download and install from:
https://adoptium.net/temurin/releases/?version=21
```

**macOS:**
```bash
brew install openjdk@21
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install openjdk-21-jdk
```

**Verify Installation:**
```bash
java -version
# Should show: openjdk version "21.x.x"
```

---

### Step 3: Install Fabric Loader (3 minutes)

1. **Download Fabric Installer:**
   👉 https://fabricmc.net/use/installer/

2. **Run the installer:**
   - Select Minecraft version: **1.21.8**
   - Select Loader version: **0.17.2** or higher
   - Click "Install"

3. **Verify:** Open Minecraft Launcher, you should see "Fabric" profile

---

### Step 4: Install Fabric API (2 minutes)

**Download Fabric API:**
👉 https://modrinth.com/mod/fabric-api/version/0.133.4+1.21.8

**Or use this direct link:**
```bash
curl -L -O https://cdn.modrinth.com/data/P7dR8mSH/versions/nfbslshR/fabric-api-0.133.4%2B1.21.8.jar
```

**Move to mods folder:**
- **Windows**: `%APPDATA%\.minecraft\mods\`
- **macOS**: `~/Library/Application Support/minecraft/mods/`
- **Linux**: `~/.minecraft/mods/`

---

### Step 5: Install Mirage Mod & Launch! (2 minutes)

1. **Move the downloaded JAR** to your Minecraft mods folder (same as Step 4)

2. **Launch Minecraft:**
   - Open Minecraft Launcher
   - Select "Fabric 1.21.8" profile
   - Click "Play"

3. **Verify mod is loaded:**
   - On the main menu, click "Mods"
   - You should see "Mirage Minecraft Mod 1.0.0"

4. **Start playing!**
   - Create or load a world
   - The mod will begin transforming your gameplay in real-time

---

## 🎨 Using the Mod

Once in-game:
1. The mod connects to Decart's Mirage API automatically
2. Your gameplay is streamed and transformed in real-time
3. Choose different visual styles from the menu
4. Experience Minecraft like never before!

For detailed usage instructions:
👉 https://oasis2.decart.ai/how-to-play

---

## 🐛 Troubleshooting

### "Java version error"
```bash
# Make sure Java 21 is active:
java -version

# If wrong version, set JAVA_HOME:
export JAVA_HOME=/path/to/java21
```

### "Fabric not found"
- Re-run Fabric installer
- Ensure you selected Minecraft 1.21.8

### "Mod not loading"
- Check the JAR is in the correct mods folder
- Verify Fabric API is also installed
- Check logs: `.minecraft/logs/latest.log`

### "Game crashes on startup"
- Update graphics drivers
- Allocate more RAM to Minecraft (4GB+ recommended)
- Check compatibility with other mods

---

## 📊 System Requirements

**Minimum:**
- CPU: Intel Core i5 or equivalent
- RAM: 4GB (8GB recommended)
- GPU: OpenGL 4.5 compatible
- OS: Windows 10, macOS 10.14, or Linux

**Recommended:**
- CPU: Intel Core i7 or better
- RAM: 8GB+
- GPU: NVIDIA GTX 1060 or AMD equivalent
- Internet: Stable broadband (for AI streaming)

---

## 🔗 Quick Links

- **Download Mod**: https://github.com/techfundoffice/mirage-minecraft-mod/releases/download/v1.0.0/mirage-minecraft-mod-1.0.0.jar
- **Fabric Loader**: https://fabricmc.net/use/installer/
- **Fabric API**: https://modrinth.com/mod/fabric-api/version/0.133.4+1.21.8
- **Java 21**: https://adoptium.net/temurin/releases/?version=21
- **How to Play**: https://oasis2.decart.ai/how-to-play
- **Support**: https://github.com/techfundoffice/mirage-minecraft-mod/issues

---

## ⏱️ Total Setup Time: ~15 minutes

You'll be playing in no time! 🎮✨

---

## 💡 Pro Tips

1. **Allocate more RAM**: In Minecraft Launcher → Installations → Edit → More Options → JVM Arguments:
   ```
   -Xmx4G -Xms4G
   ```

2. **Better Performance**: 
   - Install Sodium mod for better FPS
   - Lower render distance if experiencing lag
   - Close other applications

3. **Recording**: The mod works great with:
   - OBS Studio
   - ShareX
   - Minecraft's built-in screenshot (F2)

---

**Ready to transform your Minecraft world? Let's go!** 🚀
