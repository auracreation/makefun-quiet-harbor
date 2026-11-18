import os
from pathlib import Path


TEXT = (
    "The evening barge passed through before dusk, and the lockkeeper has walked home along the grass path.\n\n"
    "Deep underneath, quiet water feeds into the chamber without a splash, rising in wide, smooth swirls "
    "that touch the mossy wall and lose their turn.\n\n"
    "Little by little, the wet band along the stone disappears as the water comes up to meet it.\n\n"
    "An alder leaf floating by the iron ladder turns once, slows, and rests still against the side.\n\n"
    "Now the lock and the long canal above it stand at one even level.\n\n"
    "With no hand on the heavy wooden beam, the two tall gates ease apart on their hinges "
    "and float a thumb's width open on the dark, flat water."
)

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
(output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))
