# Stretch Goals & Future Ideas

This document tracks ambitious features that could be added in future releases.

---

## 🌐 Web Demo

**Goal**: Browser-based finger counter using WebRTC.

**Technologies**:
- **Backend**: FastAPI or Flask with WebRTC signaling.
- **Frontend**: HTML5 Canvas + MediaPipe Hands (TensorFlow.js).
- **Deployment**: Hosted on Vercel/Netlify.

**Benefits**:
- No installation required.
- Demo-able link for sharing.

**Challenges**:
- Browser camera permissions.
- Latency optimization.

**Status**: 🟡 Scaffold in `web/` directory.

---

## 🔢 Number Sign Recognition (0–9)

**Goal**: Map finger patterns to ASL number signs (0–9).

**Approach**:
1. Define landmark patterns for each digit.
2. Add lookup table in `fingers.py`.
3. Debounce transitions (hold for 0.5s to confirm).
4. Display detected number as large digit.

**Use case**: Quick number input without keyboard.

**Status**: 🟡 Stub in `fingers.py` with `TODO` comment.

---

## 📡 UDP/OSC Export

**Goal**: Stream finger counts to creative coding apps (TouchDesigner, Processing, Max/MSP).

**Approach**:
1. Add `--osc-host` and `--osc-port` flags.
2. Send OSC messages on count change:
   - `/handy/left <count>`
   - `/handy/right <count>`
   - `/handy/total <count>`
3. Use `python-osc` library.

**Use case**: Live performances, installations, VJ setups.

**Status**: 🟡 Stub in `app.py` with `TODO` comment.

---

## 📹 Multi-Camera Support

**Goal**: Use separate cameras for left and right hands.

**Approach**:
1. Add `--left-device` and `--right-device` flags.
2. Spawn two `VideoCapture` instances.
3. Merge frames side-by-side or process separately.

**Use case**: High-accuracy setups, stereo vision experiments.

**Status**: 🔴 Design phase.

---

## 📊 Gesture History Timeline

**Goal**: Visualize gesture changes over time.

**Approach**:
1. Store last 30 seconds of counts in a circular buffer.
2. Render timeline at bottom of frame (sparkline-style).
3. Color-code by hand (blue = left, orange = right).

**Use case**: Review patterns, debug temporal smoothing.

**Status**: 🔴 Design phase.

---

## 🤖 Gesture Macros

**Goal**: Map custom gestures to keyboard shortcuts or scripts.

**Approach**:
1. Config file with gesture definitions:
   ```json
   {
     "gestures": {
       "thumbs_up": {"action": "key", "value": "space"},
       "peace_sign": {"action": "shell", "value": "open https://github.com"}
     }
   }
   ```
2. Trigger actions on gesture hold (1s).

**Use case**: Hands-free computer control.

**Status**: 🔴 Design phase.

---

## 🎨 Custom Themes

**Goal**: User-defined color schemes and UI layouts.

**Approach**:
1. Theme JSON with color palette and font sizes.
2. Load via `--theme <path>`.
3. Preset themes: `dark`, `light`, `neon`, `minimal`.

**Use case**: Accessibility, personal preference.

**Status**: 🔴 Design phase.

---

## 🧪 Synthetic Data Generator

**Goal**: Generate synthetic landmark datasets for training/testing.

**Approach**:
1. Script in `tools/generate_landmarks.py`.
2. Parameterize hand poses (angles, distances).
3. Export to JSON or CSV.

**Use case**: Unit tests, benchmarking, ML experiments.

**Status**: 🔴 Wishlist.

---

## 🔐 Gesture Authentication

**Goal**: Use unique gesture sequences as "passwords".

**Approach**:
1. Record a gesture sequence (e.g., 3 → 1 → 5).
2. Compare input against stored pattern with tolerance.
3. Unlock feature or trigger action.

**Use case**: Fun proof-of-concept, security demos.

**Status**: 🔴 Wishlist.

---

**Legend**:
- 🟢 In progress
- 🟡 Stubbed or scaffolded
- 🔴 Design/wishlist phase

---

**Want to work on one of these?** See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines!
