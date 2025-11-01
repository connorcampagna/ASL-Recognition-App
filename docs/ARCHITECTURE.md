# handy-fingers Architecture

## High-Level Overview

```
                    ┌─────────────────┐
                    │     app.py      │  CLI entrypoint (Typer)
                    │   (main loop)   │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌───────────┐    ┌──────────────┐  ┌─────────────┐
    │  Video    │    │  Calibration │  │   Overlay   │
    │  Capture  │    │    Wizard    │  │  (Drawing)  │
    └─────┬─────┘    └──────────────┘  └─────────────┘
          │
          │ RGB frames
          ▼
    ┌──────────────┐
    │  Landmark    │  MediaPipe Hands wrapper
    │  Detector    │
    └──────┬───────┘
           │
           │ List[Hand] with (label, landmarks, confidence)
           │
           ├─────────────────┬─────────────────┐
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐  ┌─────────────┐
    │   Finger    │   │   Math      │  │   Overlay   │
    │   Counter   │   │   Mode      │  │   (HUD)     │
    └─────────────┘   └─────────────┘  └─────────────┘
    • Handedness      • Gestures →    • Landmarks
    • Smoothing         Operations    • Counts
    • Count [0..5]    • Expressions   • Math expr
```

## Data Flow

1. **VideoCapture** reads frames from webcam (BGR → RGB).
2. **LandmarkDetector** processes frames → `List[Hand]`.
3. **FingerCounter** counts extended fingers per hand (with smoothing).
4. **ASLRecognizer** analyzes geometric features → recognizes ASL signs with confidence scores.
5. **Overlay** draws landmarks, counts, and expressions on frame.
6. **app.py** displays result with OpenCV or records to file.

## Module Responsibilities

| Module          | Purpose                                      | Key Classes/Functions          |
|-----------------|----------------------------------------------|--------------------------------|
| `video.py`      | Webcam I/O, frame preprocessing             | `VideoCapture`                 |
| `landmarks.py`  | Hand detection (MediaPipe wrapper)          | `LandmarkDetector`, `Hand`     |
| `fingers.py`    | ASL recognition with geometric analysis     | `ASLRecognizer`, `ASLSign`, `FingerState` |
| `calibration.py`| First-run wizard, config persistence        | `CalibrationWizard`            |
| `overlay.py`    | Drawing utilities (landmarks, signs, words) | `Overlay`                      |
| `app.py`        | CLI entrypoint, wiring, main loop           | `main()`, Typer app            |

## Design Principles

1. **Separation of Concerns**: Each module has a single, clear responsibility.
2. **Geometric Features**: ASL recognition uses finger curl, separation, palm orientation analysis.
3. **Context Managers**: Resources (camera, detector) use `__enter__`/`__exit__`.
4. **Type Safety**: Full type hints throughout.
5. **Fail-Safe**: Overlay never crashes on missing data; degrades gracefully.
6. **Honest Documentation**: Clear about heuristic limitations vs ML approaches.

## Testing Strategy

- **Unit tests**: Pure logic (`fingers.py` ASL patterns) with synthetic data.
- **Integration tests**: CLI with `--no-video` for headless verification.
- **Fixtures**: JSON landmark data in `tests/assets/` for determinism.

## Extension Points

Want to add a feature? Here's where to start:

- **New ASL sign**: Add pattern to `ASLRecognizer._match_asl_pattern()`.
- **Custom overlay**: Extend `Overlay` with new `draw_*()` methods.
- **ML recognition**: Replace geometric features with trained model in `fingers.py`.
- **Output export**: Hook into `app.py` main loop to send signs via UDP/OSC.
- **Web demo**: Use `landmarks.py` and `fingers.py` as-is; new frontend in `web/`.

---

**This architecture balances simplicity, testability, and extensibility.** 🏗️✨
