# handy-fingers-connorcampagna 🤟

**Status**: 0.2.0 - ASL Recognition System  
**Author**: Connor Campagna  
**License**: MIT

---

## 📦 What's Inside

- **Core app**: `src/handy_fingers/` (6 modules)
- **Tests**: `tests/` with fixtures
- **Docs**: README, CHANGELOG, CONTRIBUTING, accuracy guides
- **CI/CD**: GitHub Actions with Python 3.11/3.12 matrix
- **Tools**: Makefile, pyproject.toml, requirements.txt

---

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Run basic ASL recognition
handy-fingers

# With spell mode (build words)
handy-fingers --spell-mode

# Run tests
make test
```

---

## 🎯 Features

✅ Real-time ASL recognition (letters & numbers)  
✅ Spell mode (build words with signs)  
✅ Geometric feature analysis (finger curl, separation, palm orientation)  
✅ Temporal smoothing (7-frame window)  
✅ Confidence indicators  
✅ Calibration wizard (handedness, lighting)  
✅ Focus mode (large sign display)  
✅ Video recording (`--record`)  
✅ Headless mode (`--no-video`)  
✅ Clean OOP design, fully typed  
✅ 100% local processing (privacy-first)

---

## � Accuracy

⚠️ **Prototype**: Uses geometric heuristics (~70-80% accuracy)  
✅ **Best**: Numbers 0-5 (90-95%)  
⚠️ **Moderate**: Most letters (70-85%)  

See `docs/ASL_ACCURACY.md` for details and ML roadmap.

---

## 🛠️ Development

```bash
make install-dev  # Install with dev dependencies
make format       # Format with black + isort
make lint         # Lint with ruff
make test         # Run pytest
make demo         # Run with --spell-mode --watermark
```

---

## 🔗 Links

- [README.md](./README.md) - Full documentation
- [CHANGELOG.md](./CHANGELOG.md) - Version history
- [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
- [LICENSE](./LICENSE) - MIT License
- [examples/](./examples/) - Demo scripts

---

**Made with ❤️ by Connor Campagna**
