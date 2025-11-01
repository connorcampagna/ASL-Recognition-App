# ASL Recognition Accuracy Notes

## Current Status

The current ASL recognizer uses **geometric heuristics** (finger positions, angles, distances) to identify signs. This approach has **significant limitations**:

### What Works Well ✅
- **Numbers 0-5**: High accuracy (90%+) for clear, deliberate signs
- **Simple letters**: Y, I, V, W, L - these have distinctive finger patterns
- **Temporal smoothing**: Reduces jitter and false positives

### What Struggles ❌
- **Letters with subtle differences**: A vs S, C vs O, R vs U
- **Hand orientation**: Many signs require specific palm angles
- **Dynamic signs**: J, Z require motion (not supported)
- **Two-handed signs**: H, N, X (not implemented)
- **Variations in hand size/shape**: Thresholds tuned for "average" hands

## Why It's Hard

Real ASL recognition requires:

1. **Machine Learning Models**: Trained on thousands of labeled examples
2. **Temporal Features**: Many signs involve motion paths
3. **Context**: Some signs look identical without sentence context
4. **Regional Variations**: ASL has dialects and personal styles
5. **Lighting/Camera Quality**: Affects landmark detection accuracy

## Improving Accuracy

### Short-term (Heuristic Improvements)
1. **Adjust thresholds**: Tune curl/separation values for your hand
2. **Better lighting**: Bright, even lighting helps MediaPipe
3. **Deliberate signs**: Hold signs clearly for 1-2 seconds
4. **Camera angle**: Face camera straight-on, hand centered

### Medium-term (Better Features)
1. **Angle-based features**: Use bone angles instead of just distances
2. **Fingertip trajectories**: Track movement for dynamic signs
3. **Two-hand support**: Detect relative positions of both hands
4. **Calibration per user**: Learn your specific hand geometry

### Long-term (ML Approach)
1. **Dataset collection**: Record labeled examples of each sign
2. **Train classifier**: Use TensorFlow/PyTorch LSTM or Transformer
3. **Real-time inference**: Deploy model with MediaPipe
4. **Continuous improvement**: Collect edge cases and retrain

## Recommended Usage

For best results with the current system:

1. **Focus on numbers**: 0-5 work reliably for counting
2. **Use spell mode for simple words**: Y-E-S, H-I, etc.
3. **Increase confidence threshold**: `--confidence 0.85` reduces false positives
4. **Practice signs**: Review ASL references to match canonical forms
5. **Good lighting**: Essential for landmark detection

## References

- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- [ASL Fingerspelling Guide](https://www.lifeprint.com/asl101/fingerspelling/)
- [Sign Language Recognition Papers](https://paperswithcode.com/task/sign-language-recognition)

## Contributing

If you'd like to improve accuracy:
1. Share your test results (which signs work/fail)
2. Suggest threshold adjustments
3. Contribute ML-based recognition (see STRETCH_GOALS.md)

---

**Bottom line**: This is a **demo/prototype** of ASL recognition. For production use, consider:
- [Google's MediaPipe Gesture Recognition](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer)
- Commercial ASL APIs (Sign All, SignTime, etc.)
- ML-based custom models
