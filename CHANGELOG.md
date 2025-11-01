# Changelog

All notable changes to **handy-fingers-connorcampagna** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2025-10-31

### 🚀 Major Pivot: ASL Recognition System

#### Changed
- **Complete transformation**: Pivoted from finger counting to American Sign Language (ASL) recognition
- **ASLRecognizer**: Replaced `FingerCounter` with geometric feature analysis for ASL signs
- **Spell Mode**: Added word-building capability with keyboard controls (SPACE/BACKSPACE/ENTER)
- **CLI interface** updated:
  - Removed `--math-mode`
  - Added `--spell-mode`: Enable word spelling
  - Added `--confidence`: ASL recognition confidence threshold

#### Added
- **ASL Sign Support**:
  - Numbers: 0, 1, 2, 3, 4, 5 (high accuracy)
  - Letters: A, B, C, D, E, F, I, L, O, R, S, T, U, V, W, Y (moderate accuracy)
- **Geometric Features**:
  - Finger curl detection
  - Thumb position analysis
  - Finger separation measurement
  - Palm orientation estimation
- **Temporal Smoothing**: 7-frame window for stable recognition
- **Confidence Indicators**: Visual feedback for detection quality
- **Documentation**:
  - `ASL_ACCURACY.md`: Honest assessment of limitations and roadmap
  - `QUICK_TIPS.md`: Usage tips for better accuracy
  - Updated README with accuracy warnings

#### Removed
- **Math Mode**: Removed gesture-based arithmetic feature
- `math_mode.py` module
- `test_math_mode.py` tests

#### Known Limitations
- Accuracy ~70-80% for clear, deliberate signs
- Heuristic-based (not ML), best suited as prototype/demo
- Some letters difficult to distinguish (A/S, C/O)
- Dynamic signs (J, Z) and two-handed signs not supported

---

## [0.1.0] - 2025-10-31

### 🎉 Initial Release (Finger Counting)

#### Added
- **Core functionality**: Realtime finger counting with webcam using MediaPipe Hands
- **Calibration wizard**: First-run setup for handedness and lighting
- **Focus mode**: High-contrast display with dimmed video
- **Test suite**: Parametrized tests with synthetic landmarks
- **CI/CD**: GitHub Actions with Python 3.11/3.12 matrix
- **Documentation**: README, CONTRIBUTING.md, MIT LICENSE
- **Developer tools**: Makefile, pyproject.toml with linting/formatting config

#### Performance
- Targets 30 FPS on typical laptops.
- Temporal smoothing (5-frame window) for stable counts.
- Optional `--downscale` for lower-end hardware.

#### Privacy
- On-device processing only; no cloud uploads.
- Config saved locally in `~/.handy-fingers/connorcampagna.json`.

---

## [Unreleased]

### Planned
- Web demo with Gradio or FastAPI + WebRTC.
- ASL number sign recognition (0–9).
- UDP/OSC export for creative coding integrations.
- Multi-camera support.
- Gesture history timeline visualization.

---

**Legend:**
- 🎉 Major milestone
- ✨ New feature
- 🐛 Bug fix
- 🔧 Configuration/tooling
- 📝 Documentation
- ⚡ Performance improvement
- 🔒 Security/privacy
