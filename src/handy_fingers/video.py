"""
video.py
~~~~~~~~
Webcam capture pipeline with frame preprocessing and context management.
"""

from __future__ import annotations

import sys
from typing import Generator, Optional

import cv2
import numpy as np


class CameraError(Exception):
    """Raised when camera access fails or device is unavailable."""

    pass


class VideoCapture:
    """
    Context-managed webcam capture with preprocessing pipeline.
    
    Handles device opening, resolution setting, frame scaling,
    and graceful cleanup.
    """

    def __init__(
        self,
        device_id: int = 0,
        width: int = 1280,
        height: int = 720,
        downscale: float = 1.0,
    ) -> None:
        """
        Args:
            device_id: Camera device index (0 = default).
            width: Desired capture width.
            height: Desired capture height.
            downscale: Processing scale factor (0.5 = half resolution).
        """
        self.device_id = device_id
        self.width = width
        self.height = height
        self.downscale = downscale
        self._cap: Optional[cv2.VideoCapture] = None

    def __enter__(self) -> VideoCapture:
        """Open the camera device and configure settings."""
        self._cap = cv2.VideoCapture(self.device_id)
        
        if not self._cap.isOpened():
            raise CameraError(
                f"Cannot access camera device {self.device_id}. "
                f"Check permissions and device availability."
            )
        
        # Request desired resolution (actual may differ by hardware)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        # Verify what we actually got
        actual_w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"📷 Camera opened: {actual_w}x{actual_h}", file=sys.stderr)
        
        return self

    def __exit__(self, *args) -> None:
        """Release camera resources."""
        if self._cap:
            self._cap.release()
            print("📷 Camera released", file=sys.stderr)

    def frames(self) -> Generator[np.ndarray, None, None]:
        """
        Yield preprocessed frames continuously.
        
        Yields:
            RGB numpy arrays ready for landmark detection.
        
        Raises:
            CameraError: If frame read fails.
        """
        if not self._cap:
            raise CameraError("VideoCapture not initialized. Use as context manager.")
        
        while True:
            ret, frame = self._cap.read()
            
            if not ret:
                raise CameraError("Failed to read frame from camera.")
            
            # Apply downscaling if requested
            if self.downscale != 1.0:
                new_w = int(frame.shape[1] * self.downscale)
                new_h = int(frame.shape[0] * self.downscale)
                frame = cv2.resize(frame, (new_w, new_h))
            
            # Convert BGR → RGB for MediaPipe
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            yield frame_rgb

    def read_one(self) -> Optional[np.ndarray]:
        """
        Read a single frame (useful for testing).
        
        Returns:
            RGB frame or None if read fails.
        """
        if not self._cap:
            return None
        
        ret, frame = self._cap.read()
        if not ret:
            return None
        
        if self.downscale != 1.0:
            new_w = int(frame.shape[1] * self.downscale)
            new_h = int(frame.shape[0] * self.downscale)
            frame = cv2.resize(frame, (new_w, new_h))
        
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
