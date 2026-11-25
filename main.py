#!/usr/bin/env python3
"""One-Line Robot Wedding Vows.

Writes a single line of wedding vows for a robot couple to
/output/entry.txt. Deterministic: the vow is a fixed string, no
randomness, no time, no network, stdlib only.
"""

import os
import stat

VOW = (
    "To have and to hold, to charge and to cherish, "
    "from this day forward, until death \u2014 or a dead "
    "battery \u2014 do us part."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

MIN_CHARS = 1
MAX_CHARS = 160


def main() -> None:
    text = VOW

    # Validate: 1-160 chars, exactly one line, not only whitespace.
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise SystemExit(
            f"vow is {len(text)} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("vow must be exactly one line")
    if not text.strip():
        raise SystemExit("vow must not be only whitespace")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    os.chmod(OUTPUT_PATH, 0o644)

    # Re-read to verify exactly what was written.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise SystemExit("verification failed: file content differs")
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    if mode != 0o644:
        raise SystemExit(f"verification failed: mode is {oct(mode)}")

    print(f"Wrote {len(text)} chars to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
