#!/usr/bin/env python3
import argparse
import base64
import hashlib
from pathlib import Path

def encode_text(text: str, mode: str) -> str:
    if mode == "base64":
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    if mode == "hex":
        return text.encode("utf-8").hex()

    if mode == "caesar":
        shift = 3
        out = []
        for ch in text:
            if "a" <= ch <= "z":
                out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
            elif "A" <= ch <= "Z":
                out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
            else:
                out.append(ch)
        return "".join(out)

    if mode == "hash":
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    raise ValueError(f"Unsupported mode: {mode}")

def main():
    parser = argparse.ArgumentParser(description="Encode text files")
    parser.add_argument("-i", "--input", required=True, help="Input text file")
    parser.add_argument("-o", "--output", required=True, help="Output encoded file")
    parser.add_argument("-m", "--mode", choices=["base64", "hex", "caesar", "hash"], default="base64")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    encoded = encode_text(text, args.mode)
    Path(args.output).write_text(encoded, encoding="utf-8")

if __name__ == "__main__":
    main()
