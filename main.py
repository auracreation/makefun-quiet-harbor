import os
from pathlib import Path


TEXT = (
    "She trails a hand in the warm bathwater. "
    "On the stool beside the tub is the old towel, soft where it has been washed so often. "
    "A thread has worked loose from the hem and curls on the wood. "
    "Through the wall she hears a cupboard closing, then the light footsteps of someone going upstairs. "
    "The pipes give a little tick. After a while, another. "
    "She lifts her hand. "
    "Water follows the curve of her wrist, gathers at her elbow, and falls. "
    "The surface moves toward the sides of the tub and back, each return a little lower, "
    "until the pale ceiling lies in it again."
)

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
(output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))
