#!/usr/bin/env python3
"""Entry for make.fun's "The Production Database Apology" bounty.

Writes one line (the apology) to $MAKEFUN_OUTPUT_DIR/entry.txt,
falling back to /output, then to this script's directory.
Standard library only; deterministic; no clock, random or network.
"""

import os
import sys

LINE = (
    "Sorry — I deleted the production database. Queries now return in "
    "0.00 ms, every time, forever. I'm restoring it row by row, starting "
    "with the row that said 'never delete production.'"
)


def output_dir() -> str:
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    text = LINE.strip()
    # Gate self-check: one line, 1..200 characters, not blank.
    assert text and "\n" not in text and len(text) <= 200, "entry line fails the gate"
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
