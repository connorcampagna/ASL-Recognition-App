# Screenshot Placeholders

This directory should contain demo screenshots/GIFs for the README.

## Required Images

1. **basic_mode.png** (or .gif)
   - Shows per-hand counts and total
   - One or two hands visible with landmarks

2. **spell_mode.png** (or .gif)
   - Spell mode with word displayed
   - Expression visible (e.g., "3 + 2 = 5")

3. **focus_mode.png** (or .gif)
   - Focus mode enabled
   - Large centered digit, dimmed video

## How to Create

Use `handy-fingers --record demo.mp4` to record, then:

```bash
# Extract frame as PNG
ffmpeg -i demo.mp4 -ss 00:00:03 -vframes 1 basic_mode.png

# Convert to GIF
ffmpeg -i demo.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" basic_mode.gif
```

Place files here and update README image paths.
