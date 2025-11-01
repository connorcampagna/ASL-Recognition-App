"""
app.py
~~~~~~
CLI entrypoint and application wiring.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import cv2
import typer

from . import __version__
from .calibration import CalibrationWizard, load_config, save_config
from .fingers import ASLRecognizer
from .landmarks import LandmarkDetector
from .overlay import Overlay
from .video import CameraError, VideoCapture

app = typer.Typer(
    help="🤟  ASL Recognizer: Real-time American Sign Language recognition.",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"handy-fingers {__version__}")
        raise typer.Exit()


@app.command()
def main(
    device: int = typer.Option(0, "--device", "-d", help="Camera device ID."),
    width: int = typer.Option(1280, "--width", help="Capture width."),
    height: int = typer.Option(720, "--height", help="Capture height."),
    downscale: float = typer.Option(1.0, "--downscale", help="Processing scale (0.5 = half)."),
    min_conf: float = typer.Option(0.7, "--min-conf", help="Detection confidence [0, 1]."),
    confidence: float = typer.Option(0.75, "--confidence", help="ASL recognition confidence threshold."),
    focus: bool = typer.Option(False, "--focus", help="Focus mode: large sign display."),
    spell_mode: bool = typer.Option(False, "--spell-mode", help="Enable word spelling mode."),
    watermark: bool = typer.Option(False, "--watermark", help="Show 'by connorcampagna' watermark."),
    recalibrate: bool = typer.Option(False, "--recalibrate", help="Force re-run calibration."),
    no_video: bool = typer.Option(False, "--no-video", help="Headless mode (testing)."),
    record: Optional[Path] = typer.Option(None, "--record", help="Record to video file."),
    version: bool = typer.Option(
        False, "--version", callback=version_callback, is_eager=True, help="Show version."
    ),
) -> None:
    """
    Launch the ASL recognition application.
    
    Press ESC or 'q' to exit.
    Press SPACE to add letter to word (spell mode).
    Press BACKSPACE to delete last letter.
    Press ENTER to clear word.
    """
    # Load or run calibration
    config = load_config()
    
    try:
        with VideoCapture(device, width, height, downscale) as video:
            if not config.get("first_run_complete") or recalibrate:
                wizard = CalibrationWizard(video)
                config = wizard.run()
                save_config(config)
            
            # Initialize components
            detector = LandmarkDetector(min_detection_confidence=min_conf)
            recognizer = ASLRecognizer(smoothing_window=7, confidence_threshold=confidence)
            overlay = Overlay(focus_mode=focus, show_watermark=watermark)
            
            # Spell mode state
            current_word = []
            last_letter = None
            frames_since_change = 0
            
            # Optional video writer
            writer = None
            if record and not no_video:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                writer = cv2.VideoWriter(str(record), fourcc, 30.0, (width, height))
                typer.echo(f"📹 Recording to {record}", err=True)
            
            with detector:
                for frame_rgb in video.frames():
                    hands = detector.detect(frame_rgb)
                    
                    # Recognize ASL signs
                    detected_sign = None
                    sign_confidence = 0.0
                    
                    if hands:
                        # Use first detected hand
                        hand = hands[0]
                        is_right = hand.label == "Right"
                        sign, conf = recognizer.recognize_with_smoothing(hand.landmarks, is_right)
                        
                        if conf >= confidence:
                            detected_sign = sign
                            sign_confidence = conf
                            
                            # Spell mode: track letter changes
                            if spell_mode:
                                if sign != last_letter and sign.value not in ["?", "SPACE"]:
                                    frames_since_change += 1
                                    if frames_since_change > 15:  # Hold for 0.5s
                                        last_letter = sign
                                        frames_since_change = 0
                                else:
                                    frames_since_change = 0
                    
                    # Prepare display frame (RGB → BGR for OpenCV)
                    display_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                    
                    if focus:
                        display_frame = overlay.apply_focus_dim(display_frame)
                    
                    # Draw landmarks
                    overlay.draw_landmarks(display_frame, hands, show_connections=not focus)
                    
                    # Draw ASL sign
                    overlay.draw_asl_sign(display_frame, detected_sign, sign_confidence)
                    
                    # Draw spelled word if in spell mode
                    if spell_mode:
                        overlay.draw_spelled_word(display_frame, current_word)
                    
                    # Watermark
                    overlay.draw_watermark(display_frame)
                    
                    # Record if enabled
                    if writer:
                        writer.write(display_frame)
                    
                    # Display (unless headless)
                    if not no_video:
                        cv2.imshow("handy-fingers", display_frame)
                        
                        key = cv2.waitKey(1) & 0xFF
                        if key in [27, ord("q")]:  # ESC or 'q'
                            break
                        elif key == ord(" ") and spell_mode and last_letter:  # SPACE: add letter
                            current_word.append(last_letter)
                            last_letter = None
                        elif key == 8 and spell_mode and current_word:  # BACKSPACE: delete last letter
                            current_word.pop()
                        elif key == 13 and spell_mode:  # ENTER: clear word
                            current_word = []
                            last_letter = None
            
            # Cleanup
            if writer:
                writer.release()
            if not no_video:
                cv2.destroyAllWindows()
            
            typer.echo("\n👋 Goodbye!", err=True)
    
    except CameraError as e:
        typer.echo(f"❌ Camera error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Interrupted by user.", err=True)
        sys.exit(130)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
