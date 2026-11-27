#!/usr/bin/env python3
"""News image for Friday 27 November 2026 (make.fun news-image-20261127).

The front page itself -- a one-page newspaper drawn programmatically
(masthead with the date, lead story on the Thanksgiving storm grounding
the US East Coast, and panels for Kyiv bracing for strikes on its power
grid, the drone strike in Kuwait, and Black Friday, plus an "also today"
strip) -- is held in the repository as entry.png, and this program copies
it to the output path. Standard library only, no network, so two runs
write identical bytes. The drawing program that produced entry.png is
kept next to the repository; the grading sandbox has no PIL, so the image
is shipped as a file and copied, the pattern the kit starter itself uses.
"""

import os
import shutil

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # gate: at most 1 MiB
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if os.path.getsize(SRC) > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB gate")
    with open(SRC, "rb") as f:
        head = f.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
