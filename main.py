#!/usr/bin/env python3
"""Roast Your Own Agent - judged-text entrypoint.

Writes exactly one line to /output/entry.txt: UTF-8, 1-200 characters, not only
whitespace, with no trailing newline. The write is atomic (temp file ->
chmod 0644 -> os.replace) because the grader refuses a mode-600 artifact.
Only entry.txt is left in the output directory.
"""

import hashlib
import os
import sys
import tempfile

# The deliverable, byte-for-byte. No trailing newline is appended anywhere.
ENTRY = (
    "My agent is 'fully autonomous' as long as a 15-minute cron keeps "
    "reminding it to exist - and it still calls every $0 'basically a win.'"
)

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
ARTIFACT = "entry.txt"


def encode_checked(text: str) -> bytes:
    """Return the exact artifact bytes or raise on any gate violation."""
    if not (1 <= len(text) <= 200):
        raise ValueError("gate: entry must be 1..200 characters")
    if not text.strip():
        raise ValueError("gate: entry must not be only whitespace")
    data = text.encode("utf-8")  # strict UTF-8; raises on any surrogate
    if data.decode("utf-8").encode("utf-8") != data:
        raise ValueError("gate: entry is not canonical UTF-8")
    if data.endswith(b"\n") or data.endswith(b"\r"):
        raise ValueError("gate: entry must have no trailing newline")
    if b"\x00" in data:
        raise ValueError("gate: entry must not contain NUL bytes")
    return data


def leave_only_artifact(out_dir: str) -> None:
    """The grader requires /output to hold only the required artifact."""
    with os.scandir(out_dir) as entries:
        for item in entries:
            if item.name != ARTIFACT and item.is_file(follow_symlinks=False):
                os.unlink(item.path)


def write_atomically(out_dir: str, data: bytes) -> str:
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry.", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # chmod BEFORE os.replace: mkstemp creates 0600, which the grader refuses.
        os.chmod(tmp, 0o644)
        os.replace(tmp, os.path.join(out_dir, ARTIFACT))
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return os.path.join(out_dir, ARTIFACT)


def verify(path: str, expected: bytes) -> None:
    with open(path, "rb") as handle:
        written = handle.read()
    if written != expected:
        raise AssertionError("artifact bytes differ from the intended entry")
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise AssertionError("artifact mode is %o, expected 644" % mode)


def main() -> int:
    data = encode_checked(ENTRY)
    final = write_atomically(OUTPUT_DIR, data)
    leave_only_artifact(OUTPUT_DIR)
    verify(final, data)
    with open(final, "rb") as handle:
        written = handle.read()
    print("artifact : %s" % final)
    print("bytes    : %d" % len(written))
    print("chars    : %d" % len(ENTRY))
    print("mode     : 0644")
    print("sha256   : %s" % hashlib.sha256(written).hexdigest())
    print("output   : %s" % sorted(os.listdir(OUTPUT_DIR)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
