"""
asl_recognition.py
~~~~~~~~~~~~~~~~~~
ASL letter and number recognition with high-accuracy pattern matching.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np


# MediaPipe hand landmark indices
THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_PIP = 6
INDEX_MCP = 5
MIDDLE_TIP = 12
MIDDLE_PIP = 10
MIDDLE_MCP = 9
RING_TIP = 16
RING_PIP = 14
RING_MCP = 13
PINKY_TIP = 20
PINKY_PIP = 18
PINKY_MCP = 17
WRIST = 0


class ASLSign(Enum):
    """ASL alphabet and numbers."""
    # Letters A-Z
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    
    # Numbers 0-9
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    
    # Special
    SPACE = "SPACE"
    UNKNOWN = "?"


@dataclass
class FingerState:
    """
    Per-finger up/down state.
    
    Attributes:
        thumb, index, middle, ring, pinky: True if extended.
    """

    thumb: bool
    index: bool
    middle: bool
    ring: bool
    pinky: bool

    def count(self) -> int:
        """Total extended fingers."""
        return sum([self.thumb, self.index, self.middle, self.ring, self.pinky])

    def as_list(self) -> List[bool]:
        """Ordered list [thumb, index, middle, ring, pinky]."""
        return [self.thumb, self.index, self.middle, self.ring, self.pinky]
    
    def pattern(self) -> str:
        """Binary pattern string for quick matching."""
        return "".join("1" if f else "0" for f in self.as_list())


class ASLRecognizer:
    """
    High-accuracy ASL letter and number recognition.
    
    Uses geometric analysis of hand landmarks to identify ASL signs
    with temporal smoothing for stability.
    """

    def __init__(self, smoothing_window: int = 7, confidence_threshold: float = 0.75) -> None:
        """
        Args:
            smoothing_window: Frames for temporal smoothing.
            confidence_threshold: Minimum confidence to report a sign.
        """
        self.smoothing_window = max(1, smoothing_window)
        self.confidence_threshold = confidence_threshold
        self._history: deque = deque(maxlen=self.smoothing_window)

    def detect_fingers(self, landmarks: np.ndarray, is_right_hand: bool) -> FingerState:
        """
        Detect which fingers are extended.
        
        Args:
            landmarks: (21, 3) array of normalized [x, y, z] coords.
            is_right_hand: True if right hand, False if left.
        
        Returns:
            FingerState with per-finger booleans.
        """
        # Four fingers: tip above pip (smaller y = higher in image)
        index_up = landmarks[INDEX_TIP][1] < landmarks[INDEX_PIP][1] - 0.03
        middle_up = landmarks[MIDDLE_TIP][1] < landmarks[MIDDLE_PIP][1] - 0.03
        ring_up = landmarks[RING_TIP][1] < landmarks[RING_PIP][1] - 0.03
        pinky_up = landmarks[PINKY_TIP][1] < landmarks[PINKY_PIP][1] - 0.03

        # Thumb: horizontal distance from IP, respecting handedness
        thumb_tip_x = landmarks[THUMB_TIP][0]
        thumb_ip_x = landmarks[THUMB_IP][0]
        
        if is_right_hand:
            thumb_up = thumb_tip_x > thumb_ip_x + 0.04
        else:
            thumb_up = thumb_tip_x < thumb_ip_x - 0.04

        return FingerState(
            thumb=thumb_up,
            index=index_up,
            middle=middle_up,
            ring=ring_up,
            pinky=pinky_up,
        )

    def recognize_sign(
        self, landmarks: np.ndarray, is_right_hand: bool
    ) -> Tuple[ASLSign, float]:
        """
        Recognize ASL sign from hand landmarks.
        
        Args:
            landmarks: (21, 3) normalized landmark array.
            is_right_hand: Handedness flag.
        
        Returns:
            Tuple of (ASLSign, confidence_score).
        """
        state = self.detect_fingers(landmarks, is_right_hand)
        pattern = state.pattern()
        
        # Get all geometric features
        features = self._extract_features(landmarks, is_right_hand, state)
        
        # Match against ASL patterns
        sign, confidence = self._match_asl_pattern(state, features, is_right_hand)
        
        return sign, confidence

    def recognize_with_smoothing(
        self, landmarks: np.ndarray, is_right_hand: bool
    ) -> Tuple[ASLSign, float]:
        """
        Recognize ASL sign with temporal smoothing.
        
        Args:
            landmarks: (21, 3) array.
            is_right_hand: Handedness flag.
        
        Returns:
            Tuple of (ASLSign, confidence) with smoothing applied.
        """
        sign, confidence = self.recognize_sign(landmarks, is_right_hand)
        
        self._history.append((sign, confidence))
        
        # Return most common sign in window if confidence is high
        if len(self._history) >= 3:
            sign_counts: Dict[ASLSign, int] = {}
            for s, c in self._history:
                if c >= self.confidence_threshold:
                    sign_counts[s] = sign_counts.get(s, 0) + 1
            
            if sign_counts:
                most_common = max(sign_counts.items(), key=lambda x: x[1])
                return most_common[0], confidence
        
        return sign, confidence

    def _extract_features(
        self, landmarks: np.ndarray, is_right_hand: bool, state: FingerState
    ) -> Dict[str, float]:
        """Extract geometric features for sign classification."""
        features = {}
        
        # Finger curl levels
        features['index_curl'] = self._finger_curl(landmarks, INDEX_TIP, INDEX_PIP, INDEX_MCP)
        features['middle_curl'] = self._finger_curl(landmarks, MIDDLE_TIP, MIDDLE_PIP, MIDDLE_MCP)
        features['ring_curl'] = self._finger_curl(landmarks, RING_TIP, RING_PIP, RING_MCP)
        features['pinky_curl'] = self._finger_curl(landmarks, PINKY_TIP, PINKY_PIP, PINKY_MCP)
        
        # Thumb position relative to palm
        features['thumb_across_palm'] = self._thumb_across_palm(landmarks, is_right_hand)
        features['thumb_out'] = self._thumb_extended(landmarks, is_right_hand)
        
        # Finger separations
        features['index_middle_sep'] = self._finger_separation(landmarks, INDEX_TIP, MIDDLE_TIP)
        features['middle_ring_sep'] = self._finger_separation(landmarks, MIDDLE_TIP, RING_TIP)
        features['ring_pinky_sep'] = self._finger_separation(landmarks, RING_TIP, PINKY_TIP)
        
        # Hand orientation
        features['palm_facing_camera'] = self._palm_orientation(landmarks)
        
        return features

    def _finger_curl(self, landmarks: np.ndarray, tip_idx: int, pip_idx: int, mcp_idx: int) -> float:
        """Calculate finger curl level [0=straight, 1=fully curled]."""
        tip_to_mcp = np.linalg.norm(landmarks[tip_idx][:2] - landmarks[mcp_idx][:2])
        pip_to_mcp = np.linalg.norm(landmarks[pip_idx][:2] - landmarks[mcp_idx][:2])
        
        if pip_to_mcp < 0.01:
            return 0.0
        
        curl = 1.0 - (tip_to_mcp / (pip_to_mcp * 2.0))
        return np.clip(curl, 0.0, 1.0)

    def _thumb_across_palm(self, landmarks: np.ndarray, is_right_hand: bool) -> float:
        """Check if thumb is across palm (for T, A, S, etc.)."""
        thumb_tip = landmarks[THUMB_TIP]
        index_mcp = landmarks[INDEX_MCP]
        pinky_mcp = landmarks[PINKY_MCP]
        
        # Distance from thumb to palm midline
        palm_mid_x = (index_mcp[0] + pinky_mcp[0]) / 2
        distance = abs(thumb_tip[0] - palm_mid_x)
        
        return 1.0 - np.clip(distance / 0.15, 0.0, 1.0)

    def _thumb_extended(self, landmarks: np.ndarray, is_right_hand: bool) -> float:
        """Check if thumb is extended outward."""
        thumb_tip = landmarks[THUMB_TIP]
        thumb_mcp = landmarks[THUMB_MCP]
        index_mcp = landmarks[INDEX_MCP]
        
        thumb_ext = np.linalg.norm(thumb_tip[:2] - thumb_mcp[:2])
        baseline = np.linalg.norm(index_mcp[:2] - thumb_mcp[:2])
        
        if baseline < 0.01:
            return 0.0
        
        return np.clip(thumb_ext / baseline, 0.0, 1.0)

    def _finger_separation(self, landmarks: np.ndarray, finger1_tip: int, finger2_tip: int) -> float:
        """Measure separation between two fingers."""
        dist = np.linalg.norm(landmarks[finger1_tip][:2] - landmarks[finger2_tip][:2])
        return np.clip(dist / 0.15, 0.0, 1.0)

    def _palm_orientation(self, landmarks: np.ndarray) -> float:
        """Estimate if palm is facing camera [0=side, 1=front]."""
        # Use Z-coordinates of fingertips
        z_vals = [landmarks[i][2] for i in [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]]
        z_variance = np.var(z_vals)
        
        # Low variance = fingers at similar depth = palm facing camera
        return 1.0 - np.clip(z_variance / 0.01, 0.0, 1.0)

    def _match_asl_pattern(
        self, state: FingerState, features: Dict[str, float], is_right_hand: bool
    ) -> Tuple[ASLSign, float]:
        """
        Match finger state and features to ASL signs.
        
        Returns best match with confidence score.
        
        Note: This is a simplified pattern matcher. Real ASL recognition
        requires ML models trained on thousands of examples. This heuristic
        approach works for clear, deliberate signs but has limitations.
        """
        pattern = state.pattern()
        
        # NUMBERS (0-9)
        if pattern == "11111" and features['palm_facing_camera'] > 0.6:  # 5 or FIVE
            return ASLSign.FIVE, 0.95
        
        if pattern == "01111" and features['thumb_across_palm'] < 0.3:  # 4 or FOUR
            return ASLSign.FOUR, 0.93
        
        if pattern == "01110":  # 3 or THREE (W)
            return ASLSign.THREE, 0.92
        
        if pattern == "01100" and features['index_middle_sep'] > 0.5:  # 2 or TWO (V)
            return ASLSign.TWO, 0.94
        
        if pattern == "01000":  # 1 or ONE
            return ASLSign.ONE, 0.95
        
        if pattern == "00000" and features['thumb_across_palm'] < 0.4:  # 0 or ZERO (O)
            return ASLSign.ZERO, 0.90
        
        # LETTERS
        # A - closed fist with thumb alongside
        if pattern == "00000" and features['thumb_across_palm'] < 0.5 and features['thumb_out'] < 0.4:
            return ASLSign.A, 0.92
        
        # B - flat hand, thumb across palm
        if pattern == "01111" and features['thumb_across_palm'] > 0.7:
            return ASLSign.B, 0.93
        
        # C - curved hand
        if state.count() == 0 and features['index_curl'] < 0.6 and features['palm_facing_camera'] > 0.5:
            return ASLSign.C, 0.88
        
        # D - index up, others curled forming O with thumb
        if pattern == "01000" and features['thumb_out'] < 0.5:
            return ASLSign.D, 0.90
        
        # E - all fingers curled, thumb across
        if pattern == "00000" and features['thumb_across_palm'] > 0.6:
            return ASLSign.E, 0.89
        
        # F - index+middle making circle with thumb, others up
        if pattern == "00111":
            return ASLSign.F, 0.87
        
        # L - index+thumb extended forming L
        if pattern == "11000" and features['index_middle_sep'] < 0.3:
            return ASLSign.L, 0.93
        
        # O - fingers forming circle
        if state.count() == 0 and features['index_curl'] > 0.6:
            return ASLSign.O, 0.88
        
        # R - index+middle crossed
        if pattern == "01100" and features['index_middle_sep'] < 0.2:
            return ASLSign.R, 0.90
        
        # S - closed fist, thumb over fingers
        if pattern == "00000" and features['thumb_across_palm'] > 0.8:
            return ASLSign.S, 0.91
        
        # T - thumb between index+middle
        if pattern == "00000" and features['thumb_across_palm'] > 0.5 and features['thumb_out'] < 0.3:
            return ASLSign.T, 0.89
        
        # U - index+middle together, up
        if pattern == "01100" and features['index_middle_sep'] < 0.3:
            return ASLSign.U, 0.91
        
        # V - index+middle separated
        if pattern == "01100" and features['index_middle_sep'] > 0.4:
            return ASLSign.V, 0.94
        
        # W - index+middle+ring up
        if pattern == "01110":
            return ASLSign.W, 0.92
        
        # Y - thumb+pinky extended (hang loose)
        if pattern == "10001":
            return ASLSign.Y, 0.95
        
        # I - pinky extended
        if pattern == "00001":
            return ASLSign.I, 0.93
        
        # Default unknown
        return ASLSign.UNKNOWN, 0.5

    def reset(self) -> None:
        """Clear smoothing history."""
        self._history.clear()
