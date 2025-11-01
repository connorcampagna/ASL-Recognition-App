# Demo Scenarios for handy-fingers

These are fun scripts to film short GIFs/videos showcasing the app's features.

---

## 🎬 Scenario 1: Basic Counting

**Duration**: 10 seconds  
**Mode**: Default

**Actions**:
1. Start with closed fists (0 fingers).
2. Slowly open left hand (0 → 5).
3. Open right hand (5 → 10).
4. Close right hand (10 → 5).
5. Close left hand (5 → 0).

**Voiceover**: "Count from 0 to 10 and back with both hands."

---

## 🎬 Scenario 2: Spell Mode

**Duration**: 20 seconds  
**Mode**: `--spell-mode`

**Actions**:
1. Sign letter "H" - hold steady (1 second).
2. Press SPACE to add "H" to word.
3. Sign letter "I" - hold steady.
4. Press SPACE to add "I".
5. Word displayed: "HI"
6. Sign number "5" - hold steady.
7. Press SPACE to add "5".
8. Word displayed: "HI5"
9. Press ENTER to clear and start new word.

**Voiceover**: "Spell mode: build words letter-by-letter with ASL."

---

## 🎬 Scenario 3: Focus Mode

**Duration**: 8 seconds  
**Mode**: `--focus`

**Actions**:
1. Start with left hand showing 3 fingers.
2. Right hand shows 4 fingers.
3. Total "7" appears large and centered.
4. Slowly change counts to 5 + 5 = 10.

**Voiceover**: "Focus mode: high-contrast, distraction-free counting."

---

## 🎬 Scenario 4: Easter Egg

**Duration**: 5 seconds  
**Mode**: Default

**Actions**:
1. Show both hands with closed fists (0 + 0).
2. Hold for ~1 second.
3. "calm palms ✌️" appears on screen.
4. Open hands to resume normal counting.

**Voiceover**: "Hidden easter egg: both hands at zero."

---

## 🎬 Scenario 5: Calibration Wizard

**Duration**: 20 seconds  
**Mode**: `--recalibrate`

**Actions**:
1. Launch app with `--recalibrate`.
2. Terminal shows prompts:
   - "Which is your dominant hand? [left/right]"
   - Type `right`, press Enter.
   - "Assessing lighting conditions..."
   - Show hand to camera.
   - "Lighting: normal ✓"
3. App starts normally.

**Voiceover**: "First-run calibration adapts to your setup."

---

## 📹 Recording Tips

### Command to Record

```bash
handy-fingers --spell-mode --watermark --record demo.mp4
```

### Convert to GIF

```bash
ffmpeg -i demo.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" demo.gif
```

### Best Practices

- **Lighting**: Bright, even lighting works best.
- **Background**: Solid, contrasting background (avoid clutter).
- **Hand position**: Center both hands in frame.
- **Movement**: Slow, deliberate gestures for clarity.
- **Duration**: Keep clips under 15 seconds for social media.

---

## 🎥 Platform-Specific Notes

### macOS
- Use **QuickTime Player** to trim clips.
- Export as 1080p for best quality.

### Windows
- Use **Photos** app or **VLC** for trimming.

### Linux
- Use **ffmpeg** or **Kdenlive** for editing.

---

**Happy filming!** 🎬✨
