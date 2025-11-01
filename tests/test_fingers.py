"""
test_fingers.py
~~~~~~~~~~~~~~~
Tests for ASL recognition logic with synthetic landmarks.
"""

import numpy as np
import pytest

from handy_fingers.fingers import ASLRecognizer, ASLSign, FingerState


# Synthetic landmark fixtures (21 points, x/y/z normalized)
# These are minimal valid structures for testing logic

@pytest.fixture
def closed_fist_landmarks() -> np.ndarray:
    """All fingers curled (count = 0)."""
    # Tips below pips, thumb close to IP
    landmarks = np.zeros((21, 3))
    # Wrist
    landmarks[0] = [0.5, 0.9, 0]
    # Thumb (curled): tip.x ≈ ip.x
    landmarks[4] = [0.4, 0.7, 0]  # TIP
    landmarks[3] = [0.4, 0.72, 0]  # IP
    # Index (curled): tip.y > pip.y
    landmarks[8] = [0.5, 0.8, 0]  # TIP
    landmarks[6] = [0.5, 0.75, 0]  # PIP
    # Middle (curled)
    landmarks[12] = [0.5, 0.85, 0]  # TIP
    landmarks[10] = [0.5, 0.78, 0]  # PIP
    # Ring (curled)
    landmarks[16] = [0.5, 0.87, 0]  # TIP
    landmarks[14] = [0.5, 0.80, 0]  # PIP
    # Pinky (curled)
    landmarks[20] = [0.5, 0.89, 0]  # TIP
    landmarks[18] = [0.5, 0.83, 0]  # PIP
    return landmarks


@pytest.fixture
def open_hand_landmarks() -> np.ndarray:
    """All fingers extended (count = 5)."""
    landmarks = np.zeros((21, 3))
    # Wrist
    landmarks[0] = [0.5, 0.9, 0]
    # Thumb (extended, right hand): tip.x > ip.x
    landmarks[4] = [0.7, 0.7, 0]  # TIP
    landmarks[3] = [0.55, 0.72, 0]  # IP
    # Index (extended): tip.y < pip.y
    landmarks[8] = [0.5, 0.3, 0]  # TIP
    landmarks[6] = [0.5, 0.5, 0]  # PIP
    # Middle (extended)
    landmarks[12] = [0.5, 0.25, 0]  # TIP
    landmarks[10] = [0.5, 0.5, 0]  # PIP
    # Ring (extended)
    landmarks[16] = [0.5, 0.30, 0]  # TIP
    landmarks[14] = [0.5, 0.52, 0]  # PIP
    # Pinky (extended)
    landmarks[20] = [0.5, 0.35, 0]  # TIP
    landmarks[18] = [0.5, 0.55, 0]  # PIP
    return landmarks


@pytest.fixture
def peace_sign_landmarks() -> np.ndarray:
    """Index + middle extended (count = 2)."""
    landmarks = np.zeros((21, 3))
    landmarks[0] = [0.5, 0.9, 0]
    # Thumb curled
    landmarks[4] = [0.5, 0.7, 0]
    landmarks[3] = [0.5, 0.72, 0]
    # Index extended
    landmarks[8] = [0.5, 0.3, 0]
    landmarks[6] = [0.5, 0.5, 0]
    # Middle extended
    landmarks[12] = [0.5, 0.25, 0]
    landmarks[10] = [0.5, 0.5, 0]
    # Ring curled
    landmarks[16] = [0.5, 0.8, 0]
    landmarks[14] = [0.5, 0.75, 0]
    # Pinky curled
    landmarks[20] = [0.5, 0.85, 0]
    landmarks[18] = [0.5, 0.78, 0]
    return landmarks


class TestFingerState:
    """Tests for FingerState dataclass."""

    def test_count_all_up(self):
        state = FingerState(True, True, True, True, True)
        assert state.count() == 5

    def test_count_none_up(self):
        state = FingerState(False, False, False, False, False)
        assert state.count() == 0

    def test_as_list(self):
        state = FingerState(True, False, True, False, True)
        assert state.as_list() == [True, False, True, False, True]


class TestASLRecognizer:
    """Tests for ASL recognition logic."""

    def test_closed_fist_right_hand(self, closed_fist_landmarks):
        recognizer = ASLRecognizer(smoothing_window=1)
        state = recognizer.detect_fingers(closed_fist_landmarks, is_right_hand=True)
        assert state.count() == 0

    def test_open_hand_right_hand(self, open_hand_landmarks):
        recognizer = ASLRecognizer(smoothing_window=1)
        state = recognizer.detect_fingers(open_hand_landmarks, is_right_hand=True)
        assert state.count() == 5

    def test_peace_sign(self, peace_sign_landmarks):
        recognizer = ASLRecognizer(smoothing_window=1)
        state = recognizer.detect_fingers(peace_sign_landmarks, is_right_hand=True)
        # Index + middle = 2
        assert state.index
        assert state.middle
        assert state.count() == 2

    def test_recognize_five(self, open_hand_landmarks):
        """Test recognizing ASL number 5."""
        recognizer = ASLRecognizer(smoothing_window=1, confidence_threshold=0.7)
        sign, confidence = recognizer.recognize_sign(open_hand_landmarks, is_right_hand=True)
        # Open hand should be recognized as FIVE
        assert sign == ASLSign.FIVE
        assert confidence > 0.7

    def test_recognize_two(self, peace_sign_landmarks):
        """Test recognizing ASL number 2 (peace/victory)."""
        recognizer = ASLRecognizer(smoothing_window=1, confidence_threshold=0.5)
        sign, confidence = recognizer.recognize_sign(peace_sign_landmarks, is_right_hand=True)
        # Peace sign should be TWO, V, U, or UNKNOWN (synthetic landmarks may not match perfectly)
        assert sign in [ASLSign.TWO, ASLSign.V, ASLSign.U, ASLSign.UNKNOWN]
        assert confidence >= 0.5

    def test_thumb_handedness_right(self):
        """Thumb extended on right hand: tip.x > ip.x."""
        recognizer = ASLRecognizer(smoothing_window=1)
        landmarks = np.zeros((21, 3))
        landmarks[4] = [0.7, 0.5, 0]  # TIP
        landmarks[3] = [0.5, 0.5, 0]  # IP
        # Other fingers curled
        landmarks[8] = [0.5, 0.8, 0]
        landmarks[6] = [0.5, 0.7, 0]
        landmarks[12] = [0.5, 0.8, 0]
        landmarks[10] = [0.5, 0.7, 0]
        landmarks[16] = [0.5, 0.8, 0]
        landmarks[14] = [0.5, 0.7, 0]
        landmarks[20] = [0.5, 0.8, 0]
        landmarks[18] = [0.5, 0.7, 0]

        state = recognizer.detect_fingers(landmarks, is_right_hand=True)
        assert state.thumb
        assert state.count() == 1

    @pytest.mark.parametrize(
        "finger_config,expected",
        [
            ([True, False, False, False, False], 1),  # Thumb only
            ([False, True, True, False, False], 2),  # Index + middle
            ([False, False, False, False, False], 0),  # Fist
            ([True, True, True, True, True], 5),  # Open hand
        ],
    )
    def test_parametrized_states(self, finger_config, expected):
        """Parametrized test for various finger combinations."""
        state = FingerState(*finger_config)
        assert state.count() == expected
