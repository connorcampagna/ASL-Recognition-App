# 🤟 handy-fingers-connorcampagna

[![CI](https://github.com/connorcampagna/handy-fingers-connorcampagna/actions/workflows/ci.yml/badge.svg)](https://github.com/connorcampagna/handy-fingers-connorcampagna/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> **Real-time American Sign Language (ASL) recognition using your webcam.**

Recognize ASL letters and numbers, spell words with signs, all on-device with no cloud required.

⚠️ **Prototype Notice**: This uses geometric heuristics for sign recognition. Accuracy is **moderate** (~70-80% for clear signs). For production use, consider ML-based approaches. See [ASL_ACCURACY.md](./docs/ASL_ACCURACY.md) for details.

---

## ✨ Features

- 🎥 **Live webcam feed** with hand landmark detection (MediaPipe)
- 🤟 **ASL Recognition**: Letters A-Z (partial) and numbers 0-9
- ✍️ **Spell Mode**: Build words letter-by-letter with sign language
- 🎛️ **Calibration wizard** on first run (handedness, lighting baseline)
- 🌙 **Focus Mode**: Large sign display with confidence indicators
- 📊 **Confidence threshold**: Filter out uncertain detections
- 🎨 **Clean OOP design**: testable, extensible, well-documented
- 🔒 **Privacy-first**: all processing happens locally
- 🐧 **Cross-platform**: macOS, Linux, Windows

### Currently Supported Signs

**Numbers**: 0, 1, 2, 3, 4, 5 ✅ (High accuracy)  
**Letters**: A, B, C, D, E, F, I, L, O, R, S, T, U, V, W, Y ⚠️ (Moderate accuracy)  
**Coming Soon**: G, H, J, K, M, N, P, Q, X, Z, numbers 6-9

---

## 🚀 Quickstart

### Prerequisites

- Python 3.11 or 3.12
- Webcam (built-in or USB)
- (Linux) `libgl1-mesa-glx` and `libglib2.0-0` for OpenCV GUI

### Install

```bash
# Clone the repo
git clone https://github.com/connorcampagna/handy-fingers-connorcampagna.git
cd handy-fingers-connorcampagna

# Install in editable mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

### Run

```bash
# Basic ASL recognition
handy-fingers

# With spell mode (build words)
handy-fingers --spell-mode

# Focus mode (large sign display)
handy-fingers --focus --spell-mode

# Adjust confidence threshold
handy-fingers --confidence 0.85

# Custom camera device
handy-fingers --device 1
```

**Controls:**
- **ESC** or **q**: Exit
- **SPACE**: Add current letter to word (spell mode)
- **BACKSPACE**: Delete last letter
- **ENTER**: Clear word

---

## � Using ASL Recognition

### Basic Mode

Shows detected ASL sign with confidence indicator in real-time.

### Spell Mode (`--spell-mode`)

Build words letter-by-letter:

1. **Sign a letter** - Hold the sign steady for ~1 second
2. **Press SPACE** - Add the recognized letter to your word
3. **Repeat** - Build your word one letter at a time
4. **BACKSPACE** - Remove last letter if you make a mistake
5. **ENTER** - Clear word and start over

**Tips for Better Accuracy:**
- ✅ Hold signs **clearly and deliberately** for 1-2 seconds
- ✅ Use **bright, even lighting**
- ✅ Keep hand **centered** in frame
- ✅ Face camera **straight-on**
- ✅ Start with **numbers** (0-5) - they're most accurate
- ⚠️ Some letters look similar (A/S, C/O) - be patient
- 📖 See [ASL_ACCURACY.md](./docs/ASL_ACCURACY.md) for detailed info

---

## 🎬 Recording a Demo

Record video output with `--record`:

```bash
handy-fingers --spell-mode --record demo.mp4
```

Convert to GIF with ffmpeg:

```bash
ffmpeg -i demo.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" demo.gif
```

---

## 🏗️ Architecture

```
┌──────────────┐
│   app.py     │  CLI entrypoint, wiring
└──────┬───────┘
       │
       ├─► VideoCapture     (video.py)
       ├─► LandmarkDetector (landmarks.py)
       ├─► ASLRecognizer    (fingers.py)
       ├─► Overlay          (overlay.py)
       └─► CalibrationWizard (calibration.py)
```

### Modules

- **`video.py`**: Webcam I/O with preprocessing and downscaling.
- **`landmarks.py`**: MediaPipe Hands wrapper; outputs `Hand` objects with landmarks.
- **`fingers.py`**: ASL sign recognition using geometric feature analysis with temporal smoothing.
- **`calibration.py`**: First-run wizard; saves settings to `~/.handy-fingers/`.
- **`overlay.py`**: Drawing utilities (landmarks, signs, spelled words, confidence indicators).

---

## 🐛 Troubleshooting

### macOS: "Camera busy" or permission denied

1. **System Preferences** → **Security & Privacy** → **Camera**  
2. Ensure Terminal (or your IDE) has camera access.

### Windows: Driver quirks

- Update webcam drivers via Device Manager.
- Try `--device 0` or `--device 1` to cycle devices.

### Linux: "cannot open camera"

Install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0

# Fedora
sudo dnf install mesa-libGL glib2
```

### Performance: Low FPS

Use `--downscale 0.5` to process at half resolution:

```bash
handy-fingers --downscale 0.5
```

---

## 🧪 Testing

Run the test suite:

```bash
make test

# With coverage
make test-cov
```

Tests include:
- **`test_fingers.py`**: ASL sign recognition with synthetic landmarks and temporal smoothing.

Fixtures in `tests/assets/` provide deterministic landmark data.

---

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for style guidelines and PR workflow.

**Quick summary:**
- Use **type hints** everywhere.
- Format with **black** and **isort**.
- Lint with **ruff**.
- Write tests before submitting PRs.

---

## 📄 License

[MIT License](./LICENSE) © 2025 Connor Campagna

---

## 🔐 Privacy & Ethics

All processing happens **on-device**. No images or data leave your machine. The app:
- Does not record by default (use `--record` explicitly).
- Can be run with `--no-video` for headless testing.
- Respects your camera feed as a local-only resource.

---

## 🎨 Why?

Because sign language recognition is fascinating, and because I wanted a repo that felt uniquely *mine*—not a cookie-cutter tutorial clone. This project emphasizes:
- Clean separation of concerns
- Testable, pure functions
- Thoughtful UX touches (calibration, focus mode, spell mode)
- Privacy-first design
- Honest documentation about limitations

Enjoy! 🤟✨

---

## 📸 Screenshots

### Basic Mode
![ASL recognition](./docs/screenshots/basic_mode.png)
*Real-time ASL sign detection with confidence indicators.*

### Spell Mode
![Spell mode in action](./docs/screenshots/spell_mode.png)
*Build words letter-by-letter using ASL signs.*

### Focus Mode
![Focus mode with large sign](./docs/screenshots/focus_mode.png)
*Large, high-contrast sign display for clear viewing.*

---

## 🛠️ Development

```bash
# Install dev dependencies
make install-dev

# Format code
make format

# Lint
make lint

# Run with spell mode
handy-fingers --spell-mode --watermark
```

---

## 🎁 Stretch Goals (TODOs)

- [ ] **ML-based recognition** Train LSTM/Transformer for 95%+ accuracy
- [ ] **Complete alphabet** Add remaining letters (G, H, J, K, M, N, P, Q, X, Z)
- [ ] **Dynamic signs** Support J, Z (require motion)
- [ ] **Two-handed signs** Implement H, N, X
- [ ] **Web demo** via Gradio or FastAPI + WebRTC  
- [ ] **UDP/OSC export** for creative coding (e.g., TouchDesigner, Processing)
- [ ] **Gesture history timeline** Visual trace of signs over time

---

**Made with ❤️ by Connor Campagna** | [GitHub](https://github.com/connorcampagna)
