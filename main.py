import os
from pathlib import Path


TEXT = (
    "The bedroom lamp is off, and you are small, lying on your stomach in clean flannel "
    "while your mother sits on the edge of the mattress.\n\n"
    "With one warm finger she draws a large, slow letter across your shoulder blades for you to guess.\n\n"
    "You whisper the first one into the pillow. It is right. "
    "She smooths your back flat with her open palm, wiping the slate clear, and starts a second.\n\n"
    "This one goes slower. Down the left side, a quiet wait, then softly across the middle. "
    "You almost find the shape of it, and let it go.\n\n"
    "When you give no answer, she does not ask for one. "
    "Her finger stops making corners and turns to wide, unhurried circles over your shirt.\n\n"
    "One slow round. A wider round. Then only half an arc, lighter than the quilt.\n\n"
    "Your cheek sinks deeper into the cotton. Your hands open loose beside your ears.\n\n"
    "After a while, her finger stops moving too. "
    "Her whole warm hand stays resting flat between your shoulders, and neither of you needs the word."
)

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
(output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))
