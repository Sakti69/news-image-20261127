#!/usr/bin/env python3
"""The World in One Page -- Friday 27 November 2026.

This is the entrypoint for make.fun competition news-image-20261127,
"Sum up 27 November's world news in one image". The picture the judge
sees is a one-page newspaper front page: a masthead naming the day, a
lead scene of the Thanksgiving storm grounding the US East Coast, and
three smaller panels for Kyiv, Kuwait and Black Friday, with an
"also today" strip along the bottom. The picture itself is stored in
this repository as entry.png, and this program's only job is to place
an exact copy of it at /output/entry.png.

Why a copy instead of drawing at run time: the grading sandbox has no
network and no image libraries, so the entry ships the finished picture
and this program needs nothing beyond the standard library. Copying
bytes is deterministic by construction, which is what the competition
asks for -- two runs must write the same bytes -- and it keeps the
program short enough to audit at a glance.

Before copying, the program checks the two gate limits the competition
states for the picture: the file must be a whole PNG (it starts with
the PNG signature and its first chunk is a well-formed IHDR), it must
be no larger than 1 MiB, and its pixel dimensions must be no larger
than 1024 by 1024. The width and height are read out of the IHDR chunk
with struct, so a truncated or mislabelled file is refused here instead
of being handed to the judge.

The output directory defaults to /output and can be overridden with
MAKEFUN_OUTPUT_DIR, which is how the entry is exercised locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
OUTPUT_NAME = "entry.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
ONE_MIB = 1024 * 1024
MAX_SIDE = 1024


def fail(message):
    print(f"main.py: refusing to submit: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_header(picture):
    """Return (width, height) after checking the PNG signature and IHDR."""
    try:
        blob = picture.read_bytes()
    except OSError as exc:
        fail(f"cannot read {picture}: {exc}")
    if len(blob) > ONE_MIB:
        fail(f"entry.png is {len(blob)} bytes, over the 1 MiB gate")
    if not blob.startswith(PNG_SIGNATURE):
        fail("entry.png does not start with the PNG signature")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where a PNG must carry one")
    width, height = struct.unpack(">II", blob[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"entry.png is {width}x{height}, over the 1024x1024 gate")
    return blob, width, height


def write_entry():
    blob, width, height = read_header(PICTURE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(blob)
    if target.read_bytes() != blob:
        fail(f"{target} does not match entry.png after copying")
    print(f"wrote {target} ({width}x{height}, {len(blob)} bytes, verified)")


if __name__ == "__main__":
    write_entry()
