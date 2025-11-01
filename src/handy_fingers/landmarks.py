"""
landmarks.py
~~~~~~~~~~~~
Hand detection abstraction using MediaPipe Hands.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import mediapipe as mp
import numpy as np


@dataclass
class Hand:
    """
    Detected hand with landmarks and metadata.
    
    Attributes:
        label: "Left" or "Right" (from camera perspective).
        landmarks: 21 (x, y, z) normalized coordinates.
        confidence: Detection confidence [0, 1].
    """

    label: str  # "Left" or "Right"
    landmarks: np.ndarray  # shape (21, 3)
    confidence: float


class LandmarkDetector:
    """
    Context-managed hand landmark detector.
    
    Wraps MediaPipe Hands with sensible defaults and clean API.
    """

    def __init__(
        self,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.5,
        max_num_hands: int = 2,
    ) -> None:
        """
        Args:
            min_detection_confidence: Threshold for initial detection.
            min_tracking_confidence: Threshold for tracking across frames.
            max_num_hands: Maximum hands to detect (1 or 2).
        """
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.max_num_hands = max_num_hands
        self._detector: Optional[mp.solutions.hands.Hands] = None

    def __enter__(self) -> LandmarkDetector:
        """Initialize MediaPipe Hands detector."""
        self._detector = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
        return self

    def __exit__(self, *args) -> None:
        """Release detector resources."""
        if self._detector:
            self._detector.close()

    def detect(self, frame_rgb: np.ndarray) -> List[Hand]:
        """
        Detect hands in an RGB frame.
        
        Args:
            frame_rgb: RGB numpy array (H, W, 3).
        
        Returns:
            List of Hand objects (0, 1, or 2 hands).
        """
        if not self._detector:
            raise RuntimeError("Detector not initialized. Use as context manager.")
        
        # MediaPipe expects writable=False for performance
        frame_rgb.flags.writeable = False
        results = self._detector.process(frame_rgb)
        frame_rgb.flags.writeable = True
        
        if not results.multi_hand_landmarks:
            return []
        
        hands = []
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Extract label (Left/Right) and score
            if results.multi_handedness and len(results.multi_handedness) > idx:
                classification = results.multi_handedness[idx].classification[0]
                label = classification.label
                score = classification.score
            else:
                # Fallback if handedness detection fails
                label = "Right"
                score = 0.5
            
            # Convert landmarks to numpy array - access attributes directly
            landmarks_array = np.array(
                [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
            )
            
            hands.append(Hand(label=label, landmarks=landmarks_array, confidence=score))
        
        return hands
