"""Funniest Lost Sock Status Update - one status update in the voice of a
lost sock.

The program writes the line to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output), with no trailing newline. The bounty's gate: entry.txt must be
UTF-8 text of 1 to 120 characters, not only whitespace.
"""

import os

TEXT = "Status update: the dryer didn't eat me. I filed for divorce. The lint trap has the papers."
# Why this line: it twists the obvious sock material instead of repeating it.
# The dryer did NOT eat the sock - the sock left, and its missing partner is
# not a tragedy but a divorce, with the lint trap holding the papers. The
# "Status update:" opening makes it literally a status update, the sock's
# voice is small and domestic (dryer, lint trap), and the punchline lands in
# the last few words.


def gate(text):
    """Check the 1-120 character gate: UTF-8, 1-120 chars, not only
    whitespace, no leading or trailing whitespace, a single line."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text.encode("utf-8")
    if not 1 <= len(text) <= 120:
        raise ValueError("entry is %d chars, gate is 1-120" % len(text))
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return True


def main():
    gate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    os.chmod(path, 0o644)
    mode = os.stat(path).st_mode & 0o777
    if mode != 0o644:
        raise ValueError("entry.txt mode is %o, expected 0644" % mode)
    with open(path, "rb") as f:
        raw = f.read()
    read_back = raw.decode("utf-8")
    if read_back != TEXT:
        raise ValueError("read-back differs from TEXT")
    gate(read_back)
    print("wrote %d chars to %s (mode 0644)" % (len(TEXT), path))


if __name__ == "__main__":
    main()
