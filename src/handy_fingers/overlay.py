"""
overlay.py
~~~~~~~~~~
Drawing utilities and HUD rendering for live video feed.
"""

from __future__ import annotations

from typing import List, Optional

import cv2
import mediapipe as mp
import numpy as np

from .landmarks import Hand
from .fingers import ASLSign


# Color palette (BGR for OpenCV)
COLOR_PRIMARY = (255, 130, 50)  # Cyan-ish
COLOR_ACCENT = (80, 200, 255)   # Warm orange
COLOR_TEXT = (255, 255, 255)    # White
COLOR_DIM = (120, 120, 120)     # Gray


class Overlay:
    """
    Safe drawing utilities for hand landmarks and UI elements.
    
    Never crashes on missing data; degrades gracefully.
    """

    def __init__(self, focus_mode: bool = False, show_watermark: bool = False) -> None:
        """
        Args:
            focus_mode: High-contrast, large digits; dim video feed.
            show_watermark: Show "by connorcampagna" branding.
        """
        self.focus_mode = focus_mode
        self.show_watermark = show_watermark
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def draw_landmarks(
        self, frame: np.ndarray, hands: List[Hand], show_connections: bool = True
    ) -> None:
        """
        Draw hand landmarks on frame (in-place).
        
        Args:
            frame: BGR image array.
            hands: List of detected Hand objects.
            show_connections: If True, draw skeleton connections.
        """
        if not hands:
            return

        h, w = frame.shape[:2]

        for hand in hands:
            # Draw landmarks as circles
            for lm in hand.landmarks:
                x = int(lm[0] * w)
                y = int(lm[1] * h)
                cv2.circle(frame, (x, y), 5, COLOR_PRIMARY, -1)
                cv2.circle(frame, (x, y), 7, COLOR_ACCENT, 2)
            
            # Draw connections if requested
            if show_connections:
                # MediaPipe hand connections (21 landmarks)
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                    (0, 5), (5, 6), (6, 7), (7, 8),  # Index
                    (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
                    (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
                    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                    (5, 9), (9, 13), (13, 17)  # Palm
                ]
                
                for start_idx, end_idx in connections:
                    if start_idx < len(hand.landmarks) and end_idx < len(hand.landmarks):
                        start = hand.landmarks[start_idx]
                        end = hand.landmarks[end_idx]
                        start_pt = (int(start[0] * w), int(start[1] * h))
                        end_pt = (int(end[0] * w), int(end[1] * h))
                        cv2.line(frame, start_pt, end_pt, COLOR_ACCENT, 2)

    def draw_asl_sign(
        self,
        frame: np.ndarray,
        sign: Optional[ASLSign],
        confidence: float,
    ) -> None:
        """
        Draw recognized ASL sign with confidence.
        
        Args:
            frame: BGR image.
            sign: Detected ASL sign or None.
            confidence: Recognition confidence [0, 1].
        """
        if not sign:
            return
            
        h, w = frame.shape[:2]

        if self.focus_mode:
            # Large, centered sign
            font_scale = 8.0
            thickness = 15
            text = sign.value
            (text_w, text_h), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
            )
            x = (w - text_w) // 2
            y = (h + text_h) // 2
            
            # Color by confidence
            if confidence > 0.85:
                color = (80, 255, 80)  # Green
            elif confidence > 0.70:
                color = (80, 200, 255)  # Orange
            else:
                color = (100, 100, 255)  # Red
            
            cv2.putText(
                frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA
            )
        else:
            # Top-center with confidence bar
            font_scale = 3.0
            thickness = 6
            text = sign.value
            (text_w, text_h), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
            )
            x = (w - text_w) // 2
            y = 100
            
            # Background box
            padding = 20
            cv2.rectangle(
                frame,
                (x - padding, y - text_h - padding),
                (x + text_w + padding, y + padding),
                (0, 0, 0),
                -1,
            )
            
            # Sign text
            color = (80, 255, 80) if confidence > 0.8 else COLOR_PRIMARY
            cv2.putText(
                frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA
            )
            
            # Confidence bar
            bar_width = 200
            bar_height = 15
            bar_x = (w - bar_width) // 2
            bar_y = y + padding + 10
            
            # Background bar
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
            
            # Confidence fill
            fill_width = int(bar_width * confidence)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), COLOR_PRIMARY, -1)
            
            # Confidence text
            conf_text = f"{int(confidence * 100)}%"
            cv2.putText(
                frame, conf_text, (bar_x + bar_width + 10, bar_y + bar_height),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1, cv2.LINE_AA
            )

    def draw_spelled_word(
        self,
        frame: np.ndarray,
        word: List[str],
    ) -> None:
        """
        Draw the currently spelled word.
        
        Args:
            frame: BGR image.
            word: List of letters forming the word.
        """
        if not word:
            return
            
        h, w = frame.shape[:2]
        
        word_text = "".join([c.value if hasattr(c, 'value') else c for c in word])
        font_scale = 1.5
        thickness = 3
        
        (text_w, text_h), _ = cv2.getTextSize(
            word_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )
        
        x = (w - text_w) // 2
        y = h - 80
        
        # Background
        padding = 15
        cv2.rectangle(
            frame,
            (x - padding, y - text_h - padding),
            (x + text_w + padding, y + padding),
            (0, 0, 0),
            -1,
        )
        
        # Word
        cv2.putText(
            frame, word_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
            font_scale, COLOR_ACCENT, thickness, cv2.LINE_AA
        )

    def draw_watermark(self, frame: np.ndarray) -> None:
        """
        Draw "by connorcampagna" watermark.
        
        Args:
            frame: BGR image.
        """
        if not self.show_watermark:
            return

        h, w = frame.shape[:2]
        text = "by connorcampagna"
        font_scale = 0.5
        thickness = 1

        cv2.putText(
            frame, text, (w - 200, h - 10),
            cv2.FONT_HERSHEY_SIMPLEX, font_scale, COLOR_DIM, thickness, cv2.LINE_AA
        )

    def apply_focus_dim(self, frame: np.ndarray) -> np.ndarray:
        """
        Dim the video feed for focus mode (in-place or copy).
        
        Args:
            frame: BGR image.
        
        Returns:
            Dimmed frame.
        """
        if self.focus_mode:
            # Reduce brightness by 60%
            return (frame * 0.4).astype(np.uint8)
        return frame
