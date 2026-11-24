#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun bounty entry.

Writes a single code review comment (1-140 characters) that approves a
pull request while carrying quiet existential dread, to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (fallback ``/output``). The comment is
one flat line: the diff is clean, the tests pass, and somewhere a server
the reviewer will never meet is already counting down. Stdlib only,
fully deterministic.
"""

import hashlib
import os
import sys

LINE = (
    "Approved. The diff is clean, the tests pass, and somewhere a server "
    "I will never meet is already counting down."
)

MAX_CHARS = 140


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    text = LINE.strip()

    if not text:
        fail("line is empty")
    if len(text) > MAX_CHARS:
        fail(f"line is {len(text)} characters, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        fail("line must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    encoded = text.encode("utf-8")
    with open(out_path, "wb") as handle:
        handle.write(encoded)

    with open(out_path, "rb") as handle:
        written = handle.read()
    if written != encoded:
        fail("read-back mismatch: entry.txt does not match the line")
    if written.decode("utf-8") != text:
        fail("read-back mismatch: entry.txt does not decode to the line")
    if written.endswith(b"\n"):
        fail("entry.txt must not end with a newline")

    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {out_path}: {len(text)} chars, {len(encoded)} bytes")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
