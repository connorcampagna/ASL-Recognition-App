# Security Policy for handy-fingers-connorcampagna

## 🔒 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | ❌ (Deprecated)    |

---

## 🔐 Security Considerations

### Privacy
- **On-device processing**: All hand detection and counting happens locally. No data leaves your machine.
- **No telemetry**: The app does not collect or transmit usage data.
- **Camera access**: Only used during active sessions; released on exit.

### Video Recording
- **Opt-in**: Recording only happens with `--record` flag.
- **Local storage**: Recordings saved to user-specified path.

### Configuration
- **Storage**: `~/.handy-fingers/<handle>.json` contains only:
  - Dominant hand preference.
  - Lighting baseline (brightness value).
  - No sensitive data.

### Dependencies
- **Pinned versions**: `requirements.txt` locks specific versions to prevent supply chain attacks.
- **Minimal footprint**: Only essential libraries (OpenCV, MediaPipe, Typer).

---

## ✅ Best Practices

When using **handy-fingers**:
- Review camera permissions on your OS.
- Run in a trusted environment (avoid public/shared machines for recordings).
- Keep dependencies updated: `pip install --upgrade -e ".[dev]"`

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE). Use at your own risk.

---

**Thank you for helping keep handy-fingers secure!** 🖐️🔒
