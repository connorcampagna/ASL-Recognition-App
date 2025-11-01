# Expected Behaviors for handy-fingers

This document defines the expected behavior of the app under various conditions. Use it as a reference for testing and debugging.

---

## 🖐️ Finger Counting

### No Hands Detected
- **Display**: Empty frame or "Waiting for hands..." message.
- **Counts**: L: —, R: —, Total: 0

### One Hand Detected (Right)
- **Input**: Right hand with 3 fingers extended.
- **Display**: 
  - R: 3
  - Total: 3
  - Left hand count not shown.

### One Hand Detected (Left)
- **Input**: Left hand with 5 fingers extended.
- **Display**:
  - L: 5
  - Total: 5
  - Right hand count not shown.

### Two Hands Detected
- **Input**: Left hand (2 fingers), Right hand (4 fingers).
- **Display**:
  - L: 2, R: 4
  - Total: 6

### Closed Fists (Both Hands)
- **Input**: Both hands with 0 fingers.
- **Display**:
  - L: 0, R: 0
  - Total: 0
  - **Easter egg**: After ~0.5s, "calm palms ✌️" appears.

---

## � ASL Recognition

### Sign Detection
- **Behavior**: Displays detected ASL sign with confidence indicator.
- **Input**: ASL sign held steady for ~1 second.
- **Display**: Large letter/number with confidence bar.

### High Confidence (>85%)
- **Input**: Clear ASL number "5" (open hand, palm forward).
- **Display**: Large "5" in green with 90% confidence bar.

### Medium Confidence (70-85%)
- **Input**: ASL letter "L" (thumb + index extended).
- **Display**: "L" in blue with 75% confidence bar.

### Low Confidence (<70%)
- **Input**: Ambiguous hand position.
- **Display**: "?" (UNKNOWN) or no display if below threshold.

### Spell Mode
- **Behavior**: Build words by adding recognized letters.
- **Actions**:
  1. Sign "H" → Press SPACE → "H" added to word
  2. Sign "I" → Press SPACE → Word shows "HI"
  3. Press BACKSPACE → Word shows "H"
  4. Press ENTER → Word cleared

---

## 🎛️ Focus Mode

### Enabled with `--focus`
- **Video feed**: Dimmed to 40% brightness.
- **Counts**: Total only, displayed in very large font (scale 5.0).
- **Position**: Centered horizontally and vertically.
- **Landmarks**: Points only (no skeleton connections).

### Disabled (Default)
- **Video feed**: Full brightness.
- **Counts**: L, R (top corners), Total (bottom-center).
- **Landmarks**: Full skeleton with connections.

---

## 🎥 Video Recording

### `--record output.mp4`
- **Behavior**: Saves processed frames to `output.mp4`.
- **Format**: MP4V codec, 30 FPS, same resolution as capture.
- **Overlay**: All HUD elements included in recording.

### Headless Mode (`--no-video`)
- **Behavior**: No window displayed, processing continues in background.
- **Use case**: Testing, CI, background counting.
- **Exit**: Ctrl+C to stop.

---

## 🔧 Calibration

### First Run
- **Trigger**: Config file missing or `first_run_complete: false`.
- **Steps**:
  1. Prompt: "Which is your dominant hand? [left/right]"
  2. Capture sample frame.
  3. Assess lighting (dim/normal/bright).
  4. Save to `~/.handy-fingers/connorcampagna.json`.

### Subsequent Runs
- **Behavior**: Skip calibration, load saved config.

### Force Recalibrate (`--recalibrate`)
- **Behavior**: Run wizard again, overwrite existing config.

---

## 🐛 Error Handling

### Camera Access Denied
- **Error**: `CameraError: Cannot access camera device 0.`
- **Exit code**: 1
- **Message**: Clear instructions for checking permissions.

### Camera Read Failure (Mid-Session)
- **Error**: `CameraError: Failed to read frame from camera.`
- **Behavior**: App exits gracefully with error message.

### Invalid Device ID
- **Command**: `handy-fingers --device 99`
- **Error**: Same as "Camera Access Denied".

### Config Parse Error
- **Behavior**: Log warning, use default config.
- **Message**: `⚠️  Config read error: <details>. Using defaults.`

---

## ⚡ Performance

### Target FPS
- **Goal**: 30 FPS on typical laptops (2020+ hardware).
- **Conditions**: 1280x720, no downscaling, 1–2 hands.

### Downscaling (`--downscale 0.5`)
- **Effect**: Process at half resolution (640x360).
- **Trade-off**: Lower CPU usage, slightly reduced accuracy.
- **FPS gain**: ~50% increase on lower-end hardware.

### Smoothing Window
- **Default**: 5 frames (median filter).
- **Effect**: Stable counts, ~0.16s latency at 30 FPS.
- **Edge case**: Rapid gesture changes may lag slightly.

---

## 🎨 Watermark

### Enabled with `--watermark`
- **Text**: "by connorcampagna"
- **Position**: Bottom-right corner.
- **Style**: Gray, small font, low opacity.

### Disabled (Default)
- **Behavior**: No watermark shown.

---

## 🔐 Privacy

### Data Storage
- **Config**: `~/.handy-fingers/connorcampagna.json` (local only).
- **Video**: Only saved if `--record` used.
- **Network**: No network requests, all processing local.

### Camera Access
- **Scope**: Read-only, released on exit.
- **Permissions**: Respects OS-level camera permissions.

---

**Use this document as a testing checklist to verify all expected behaviors.** ✅
