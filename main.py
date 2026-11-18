import os
from pathlib import Path


TEXT = (
    "Supper is over, and you are small, lying on your back in the middle of the wooden canoe "
    "on a folded wool blanket still warm from the day.\n\n"
    "Someone has laid a dry flannel shirt across your legs. It smells of woodsmoke and pine.\n\n"
    "In the bow and stern, two quiet voices speak now and then down the boat, low and unhurried, "
    "about nothing that needs an answer from you.\n\n"
    "At first both paddles dip and pull, sending one long, even hum through the planks beneath your back.\n\n"
    "Inside the sheltered cove, the front paddle comes in and lies flat. "
    "The back paddle dips once more. A while later, half a stroke. Then it rests across the knees too.\n\n"
    "The canoe keeps gliding on what it already has. "
    "Water falls off the resting blade: one drop. Half a minute later, one more. After that, none.\n\n"
    "The wood touches the low dock without a sound. "
    "Warm arms slide under you, blanket and all, and your cheek settles on a wool shoulder.\n\n"
    "You stay asleep all the way up the path into the house."
)

output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
(output_dir / "entry.txt").write_bytes(TEXT.encode("utf-8"))
