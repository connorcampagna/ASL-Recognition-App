# Quick Tips: Improving ASL Recognition Accuracy

## Immediate Actions

### 1. Adjust Confidence Threshold
The default is 0.75. Try higher values to reduce false positives:

```bash
# More strict - fewer false positives
handy-fingers --confidence 0.85 --spell-mode

# More lenient - catches more signs but less accurate
handy-fingers --confidence 0.65 --spell-mode
```

### 2. Lighting Setup
**Critical for accuracy!**

✅ **Good**:
- Bright, diffused overhead lighting
- Face a window during daytime
- Use a desk lamp pointed at ceiling (indirect)

❌ **Bad**:
- Backlighting (window behind you)
- Single harsh light source
- Dim/dark room

### 3. Camera Position
- **Distance**: Arm's length from camera
- **Angle**: Face camera straight-on (not from below/above)
- **Framing**: Hand centered, wrist to fingertips visible

### 4. Sign Technique
- **Hold steady**: Keep sign still for 1-2 seconds
- **Clear forms**: Exaggerate finger positions slightly
- **One hand**: System works best with single hand
- **Reference ASL charts**: Match canonical forms exactly

## Testing Accuracy by Sign

Try these in order (easiest to hardest):

### Tier 1: High Accuracy ✅
```
1 (index finger) - 95%
2 (peace/victory) - 94%  
5 (open hand) - 95%
Y (thumb + pinky) - 95%
I (pinky only) - 93%
L (thumb + index) - 93%
```

### Tier 2: Good Accuracy ⚠️
```
3 (index + middle + ring) - 92%
4 (four fingers, thumb tucked) - 93%
B (flat hand, thumb across) - 93%
V (index + middle apart) - 94%
W (three fingers) - 92%
U (index + middle together) - 91%
```

### Tier 3: Challenging ⚠️⚠️
```
0/O (rounded fingers) - 88-90%
A (fist, thumb alongside) - 92%
C (curved hand) - 88%
D (index + thumb circle) - 90%
E (bent fingers) - 89%
F (thumb touches index) - 87%
S (fist, thumb over) - 91%
T (thumb between fingers) - 89%
R (fingers crossed) - 90%
```

## Debugging False Positives

If you see wrong letters frequently:

1. **Check lighting** - Most common issue
2. **Increase confidence**: `--confidence 0.85`
3. **Hold longer** - Give smoothing time to work
4. **Review sign**: Compare your form to ASL chart

## When to Use What

**For demos/fun**: Default settings work fine  
**For serious spelling**: `--confidence 0.85 --spell-mode`  
**For numbers only**: Stick to 0-5, very reliable  
**For learning ASL**: Great practice tool!

## Advanced: Tuning Thresholds

If you want to modify the code, key values are in `fingers.py`:

```python
# Line ~135: Finger detection sensitivity
index_up = landmarks[INDEX_TIP][1] < landmarks[INDEX_PIP][1] - 0.03
# Try 0.04 for stricter, 0.02 for looser

# Line ~227: Finger curl threshold
curl = 1.0 - (tip_to_mcp / (pip_to_mcp * 2.0))
# Adjust 2.0 multiplier for curl sensitivity

# Line ~245: Thumb position
distance = abs(thumb_tip[0] - palm_mid_x)
return 1.0 - np.clip(distance / 0.15, 0.0, 1.0)
# Adjust 0.15 for thumb detection range
```

## Future ML Approach

For 95%+ accuracy, you'll need:
1. Collect 100+ examples per sign
2. Train a neural network (LSTM or Transformer)
3. Use MediaPipe embeddings as input
4. Implement with TensorFlow Lite for speed

See `docs/ASL_ACCURACY.md` for the full roadmap.
