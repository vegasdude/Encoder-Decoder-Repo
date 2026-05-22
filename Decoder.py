#!/usr/bin/env python3
import argparse
import base64
import zlib
from pathlib import Path

def caesar_shift(text, shift):
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return "".join(out)

def decode(text, mode, shift=3, decompress=False):
    if mode == "caesar":
        return caesar_shift(text, -shift)

    if mode == "base64":
        data = base64.b64decode(text.encode("ascii"))
    elif mode == "base64url":
        data = base64.urlsafe_b64decode(text.encode("ascii"))
    elif mode == "hex":
        data = bytes.fromhex(text)
    else:
        raise ValueError("Hash cannot be decoded")

    if decompress:
        data = zlib.decompress(data)

    return data.decode("utf-8")

def main():
    parser = argparse.ArgumentParser(description="Advanced text decoder")
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-m", "--mode", choices=["base64", "base64url", "hex", "caesar"], default="base64")
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--decompress", action="store_true")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8").strip()
    result = decode(text, args.mode, shift=args.shift, decompress=args.decompress)
    Path(args.output).write_text(result, encoding="utf-8")

if __name__ == "__main__":
    main()
