"""
calibration.py
~~~~~~~~~~~~~~
First-run calibration wizard and persistent settings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


DEFAULT_CONFIG = {
    "version": "0.1.0",
    "dominant_hand": "right",
    "lighting_baseline": "normal",
    "first_run_complete": False,
}


def get_config_path(handle: str = "connorcampagna") -> Path:
    """
    Get platform-appropriate config path.
    
    Returns:
        Path to config JSON (e.g., ~/.handy-fingers/connorcampagna.json).
    """
    config_dir = Path.home() / ".handy-fingers"
    config_dir.mkdir(exist_ok=True)
    return config_dir / f"{handle}.json"


def load_config(handle: str = "connorcampagna") -> dict:
    """Load config from disk or return defaults."""
    config_path = get_config_path(handle)
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Config read error: {e}. Using defaults.", file=sys.stderr)
            return DEFAULT_CONFIG.copy()
    
    return DEFAULT_CONFIG.copy()


def save_config(config: dict, handle: str = "connorcampagna") -> None:
    """Persist config to disk."""
    config_path = get_config_path(handle)
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"💾 Config saved to {config_path}", file=sys.stderr)
    except IOError as e:
        print(f"⚠️  Config save error: {e}", file=sys.stderr)


class CalibrationWizard:
    """
    Interactive first-run setup.
    
    Collects:
        - Dominant hand (left/right)
        - Lighting assessment (bright/normal/dim)
        - Optional: hand size baseline for improved tracking
    """

    def __init__(self, video_capture) -> None:
        """
        Args:
            video_capture: Active VideoCapture instance.
        """
        self.video_capture = video_capture
        self.config = DEFAULT_CONFIG.copy()

    def run(self) -> dict:
        """
        Execute calibration wizard.
        
        Returns:
            Updated config dict.
        """
        print("\n" + "="*60, file=sys.stderr)
        print("🖐️  Welcome to handy-fingers calibration!", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)

        # Step 1: Dominant hand
        self._ask_dominant_hand()

        # Step 2: Lighting check
        self._assess_lighting()

        # Mark as complete
        self.config["first_run_complete"] = True

        print("\n✅ Calibration complete! Settings saved.\n", file=sys.stderr)

        return self.config

    def _ask_dominant_hand(self) -> None:
        """Ask user for dominant hand."""
        print("Step 1: Which is your dominant hand?", file=sys.stderr)
        response = input("  Enter 'left' or 'right' [right]: ").strip().lower()
        
        if response in ["left", "l"]:
            self.config["dominant_hand"] = "left"
        else:
            self.config["dominant_hand"] = "right"
        
        print(f"  ✓ Dominant hand: {self.config['dominant_hand']}\n", file=sys.stderr)

    def _assess_lighting(self) -> None:
        """Sample a frame and assess brightness."""
        print("Step 2: Assessing lighting conditions...", file=sys.stderr)
        print("  (Show your hand to the camera)\n", file=sys.stderr)

        frame = self.video_capture.read_one()
        
        if frame is None:
            print("  ⚠️  Could not capture frame. Skipping lighting check.", file=sys.stderr)
            self.config["lighting_baseline"] = "unknown"
            return

        # Calculate mean brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        mean_brightness = np.mean(gray)

        if mean_brightness < 80:
            assessment = "dim"
        elif mean_brightness > 170:
            assessment = "bright"
        else:
            assessment = "normal"

        self.config["lighting_baseline"] = assessment
        print(f"  ✓ Lighting: {assessment} (brightness: {mean_brightness:.1f})\n", file=sys.stderr)

        # Optionally show the frame for 2 seconds
        try:
            display_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Calibration Sample", display_frame)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        except Exception:
            pass  # Headless environment
