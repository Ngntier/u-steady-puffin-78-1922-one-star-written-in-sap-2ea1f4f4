"""One Star, Written in Sap — a one-line 1-star review by a houseplant.

The program writes the review line exactly, with no trailing newline,
to entry.txt inside MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import unicodedata

ENTRY = (
    "One star. He waters me whenever his phone reminds him, "
    "vents to me like I'm his therapist, and still wonders why "
    "I lean toward the window \u2014 I'm not reaching for the sun, "
    "I'm trying to leave."
)


def validate(text):
    """Check the entry against the gate: 1-279 chars, one line, clean."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= 279:
        raise ValueError("entry must be 1-279 characters, got %d" % len(text))
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    for ch in text:
        if ch in "\n\r\u2028\u2029":
            raise ValueError("entry must be a single line")
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
        if unicodedata.category(ch) == "Cf":
            raise ValueError("entry must not contain format characters")
    # Valid UTF-8 round-trip.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry failed UTF-8 round-trip")


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("entry.txt is not byte-identical to the intended text")


if __name__ == "__main__":
    main()
