import os
from pathlib import Path


TEXT = (
    "She trails a hand in the warm bathwater. "
    "On the stool beside the tub, a towel has been folded with the worn patch hidden underneath. "
    "Through the wall she hears a cupboard being closed and the light footsteps of someone going upstairs. "
    "She lifts her hand. "
    "Water follows the curve of her wrist, gathers at her elbow, and falls. "
    "The surface moves toward the sides of the tub and back, each return a little lower, "
    "until the pale ceiling lies in it again."
)

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
(output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))
