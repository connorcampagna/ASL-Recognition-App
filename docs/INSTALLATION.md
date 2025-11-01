# Installation & Setup Guide

Complete setup instructions for **handy-fingers-connorcampagna** on macOS, Linux, and Windows.

---

## 📋 Prerequisites

### All Platforms

- **Python**: 3.11 or 3.12
  - Check: `python3 --version`
  - Install: [python.org/downloads](https://www.python.org/downloads/)
- **pip**: Latest version
  - Upgrade: `python3 -m pip install --upgrade pip`
- **Webcam**: Built-in or USB camera

### Platform-Specific

#### macOS
- **Xcode Command Line Tools** (for some dependencies):
  ```bash
  xcode-select --install
  ```

#### Linux (Ubuntu/Debian)
- **System libraries** for OpenCV:
  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-dev libgl1-mesa-glx libglib2.0-0
  ```

#### Linux (Fedora/RHEL)
- **System libraries**:
  ```bash
  sudo dnf install python3-devel mesa-libGL glib2
  ```

#### Windows
- **Visual C++ Redistributable** (usually pre-installed):
  - Download from [Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe) if needed.

---

## 🚀 Installation

### Method 1: From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/connorcampagna/handy-fingers-connorcampagna.git
cd handy-fingers-connorcampagna

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### Method 2: Development Mode

For contributors or local development:

```bash
# Clone and install with dev dependencies
git clone https://github.com/connorcampagna/handy-fingers-connorcampagna.git
cd handy-fingers-connorcampagna

# Use the setup script
python3 setup_dev.py

# Or manually:
pip install -e ".[dev]"
```

### Method 3: PyPI (Future)

Once published to PyPI:

```bash
pip install handy-fingers-connorcampagna
```

---

## ✅ Verification

### 1. Check Installation

```bash
# Should print version
handy-fingers --version

# Or
python3 -m handy_fingers --version
```

### 2. Run Smoke Test

```bash
# Basic mode (opens camera window)
handy-fingers

# Headless test (no window, exits after 5s)
timeout 5s handy-fingers --no-video
```

### 3. Run Test Suite

```bash
# If installed with dev dependencies
pytest tests/ -v

# Or via Makefile
make test
```

---

## 🔧 Troubleshooting

### Issue: `ImportError: No module named 'cv2'`

**Cause**: OpenCV not installed.

**Fix**:
```bash
pip install opencv-python
```

### Issue: `ImportError: No module named 'mediapipe'`

**Cause**: MediaPipe not installed.

**Fix**:
```bash
pip install mediapipe
```

### Issue: Camera Permission Denied (macOS)

**Cause**: Terminal/IDE lacks camera access.

**Fix**:
1. **System Preferences** → **Security & Privacy** → **Camera**
2. Enable access for Terminal/VS Code/PyCharm.
3. Restart terminal/IDE.

### Issue: `error: Microsoft Visual C++ 14.0 or greater is required` (Windows)

**Cause**: Missing C++ build tools.

**Fix**:
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022).
2. Select "Desktop development with C++".
3. Retry installation.

### Issue: Low FPS / Laggy Video

**Cause**: Insufficient processing power or high resolution.

**Fix**:
```bash
# Process at half resolution
handy-fingers --downscale 0.5

# Lower capture resolution
handy-fingers --width 640 --height 480
```

### Issue: No Hands Detected

**Cause**: Poor lighting or camera angle.

**Fix**:
- Ensure bright, even lighting.
- Position hands in center of frame.
- Try lowering detection confidence:
  ```bash
  handy-fingers --min-conf 0.5
  ```

### Issue: `ModuleNotFoundError` for Local Imports

**Cause**: Not installed in editable mode.

**Fix**:
```bash
# From repo root
pip install -e .
```

---

## 🎓 Next Steps

### For Users

1. **Run calibration**: First launch will prompt for setup.
2. **Try spell mode**:
   ```bash
   handy-fingers --spell-mode
   ```
3. **Record a demo**:
   ```bash
   handy-fingers --spell-mode --record my_demo.mp4
   ```

### For Developers

1. **Explore architecture**: Read `docs/ARCHITECTURE.md`.
2. **Run linters**:
   ```bash
   make lint
   make format-check
   ```
3. **Contribute**: See `CONTRIBUTING.md`.

---

## 📦 Uninstallation

```bash
# If installed with pip
pip uninstall handy-fingers-connorcampagna

# Remove config (optional)
rm -rf ~/.handy-fingers/
```

---

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/connorcampagna/handy-fingers-connorcampagna/issues)
- **Discussions**: [GitHub Discussions](https://github.com/connorcampagna/handy-fingers-connorcampagna/discussions)
- **Email**: connor@example.com (replace with real email)

---

**Happy finger counting!** 🖐️✨
