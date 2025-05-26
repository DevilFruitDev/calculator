# 🛠️ Installation Guide

Get Calc-Arcade running on your machine in just a few minutes! This guide covers everything from system requirements to troubleshooting common issues.

## 📋 System Requirements

### **Minimum Requirements**
- **Python 3.6 or higher** (Python 3.8+ recommended)
- **Operating System**: Windows 10, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **RAM**: 512 MB available
- **Storage**: 50 MB free space
- **Display**: 1024x768 resolution minimum

### **Recommended Setup**
- **Python 3.9+** for optimal performance
- **1920x1080** resolution for best visual experience
- **Emoji font support** (comes with most modern systems)

## 🚀 Quick Installation

### **Method 1: Download Release (Easiest)**

1. **Go to the [Releases page](https://github.com/yourusername/calc-arcade/releases)**
2. **Download** the latest `calc-arcade-v1.0.zip`
3. **Extract** the zip file to your desired location
4. **Open terminal/command prompt** in that folder
5. **Run**: `python main.py`

**Done!** Your calculator should launch immediately. 🎉

### **Method 2: Clone from Source (For Developers)**

```bash
# Clone the repository
git clone https://github.com/yourusername/calc-arcade.git

# Navigate to the project directory
cd calc-arcade

# Install dependencies (if any)
pip install -r requirements.txt

# Launch the calculator
python main.py
```

### **Method 3: Direct Download**

If you don't have Git installed:

1. **Click** the green "Code" button on the GitHub page
2. **Select** "Download ZIP"
3. **Extract** the downloaded file
4. **Open terminal** in the extracted folder
5. **Run**: `python main.py`

## 🐍 Python Installation Help

### **Windows**

1. **Download Python** from [python.org](https://www.python.org/downloads/)
2. **Check** "Add Python to PATH" during installation
3. **Verify** installation: Open Command Prompt and type `python --version`

### **macOS**

```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
```

### **Linux (Ubuntu/Debian)**

```bash
# Update package list
sudo apt update

# Install Python 3
sudo apt install python3 python3-pip

# Verify installation
python3 --version
```

## ✅ Verification Steps

After installation, verify everything works:

### **1. Test Basic Launch**
```bash
python main.py
```
You should see the calculator window open with the Game Boy-style interface.

### **2. Test Calculations**
- Try basic math: `2 + 2` → Should show `4`
- Test functions: `sin(30)` → Should show `0.5` (in DEG mode)
- Check easter eggs: `42` → Face should show 😎

### **3. Test Mode Switching**
- Click **"ARCADE MODE"** button
- Interface should toggle between retro and basic styles

### **4. Run Tests (Optional but Recommended)**
```bash
# Test calculator logic
python tests/test_calculator.py

# Should show: "Success rate: 100.0%"

# Test UI components  
python tests/test_ui.py

# Should show: "Success rate: 96.7%"
```

## 🎮 Optional Enhancements

### **Enable Pixel Font (For Authentic Look)**

**Windows:**
1. Download a pixel font like "Press Start 2P" from Google Fonts
2. Install the font by double-clicking the `.ttf` file
3. Restart Calc-Arcade for enhanced visuals

**macOS/Linux:**
```bash
# The calculator will automatically fall back to system fonts
# No additional action needed
```

### **Create Desktop Shortcut**

**Windows:**
1. Right-click on `main.py`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Rename to "Calc-Arcade"

**macOS:**
```bash
# Create an alias
ln -s /path/to/calc-arcade/main.py ~/Desktop/calc-arcade
```

**Linux:**
```bash
# Create a .desktop file
cat > ~/Desktop/calc-arcade.desktop << EOF
[Desktop Entry]
Name=Calc-Arcade
Exec=python3 /path/to/calc-arcade/main.py
Icon=/path/to/calc-arcade/assets/icons/app_icon.png
Type=Application
EOF
```

## 🚨 Troubleshooting

### **Common Issues & Solutions**

#### **"Python is not recognized as an internal or external command"**
**Problem**: Python not in PATH  
**Solution**: 
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to your system PATH

#### **"No module named tkinter"**
**Problem**: tkinter not installed (rare on most systems)  
**Solution**:
```bash
# Linux only (tkinter comes with Python on Windows/macOS)
sudo apt-get install python3-tk
```

#### **Calculator window appears but looks broken**
**Problem**: Missing emoji font support  
**Solution**: 
- Update your system fonts
- On older systems, some emojis might appear as boxes (functionality still works)

#### **Tests fail with import errors**
**Problem**: Python path issues  
**Solution**:
```bash
# Run from the project root directory
cd calc-arcade
python tests/test_calculator.py
```

#### **Calculator is slow or laggy**
**Problem**: System resources or Python version  
**Solutions**:
- Switch to **Basic Mode** (less animations)
- Upgrade to Python 3.8+
- Close other heavy applications

#### **Face expressions not showing**
**Problem**: Emoji font not available  
**Solution**: 
- Install a system emoji font
- The calculator will still work perfectly, just without emoji faces

### **Performance Optimization**

For the smoothest experience:

1. **Use Basic Mode** on older computers
2. **Close unnecessary applications** 
3. **Update Python** to the latest version
4. **Run from SSD** if available

### **Getting Help**

If you're still having trouble:

1. **Check the [Issues page](https://github.com/yourusername/calc-arcade/issues)** for similar problems
2. **Create a new issue** with:
   - Your operating system and version
   - Python version (`python --version`)
   - Error messages (if any)
   - Steps you tried

3. **Include system info**:
```bash
python --version
python -c "import sys; print(sys.platform)"
python -c "import tkinter; print('tkinter works')"
```

## 🎉 You're All Set!

Once installed, check out the **[Usage Guide](usage.md)** to master all the features and discover the hidden easter eggs!

**Enjoy calculating in style!** 🚀

---

### **Next Steps**
- 📖 **[Learn how to use all features →](usage.md)**
- 🎨 **[Explore the visual showcase →](features.md)**
- 🛠️ **[Contribute to development →](development.md)**