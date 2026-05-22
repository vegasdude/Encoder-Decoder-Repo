#!/usr/bin/env python3
import argparse
import base64
import hashlib
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

def encode(text, mode, shift=3, compress=False):
    data = text.encode("utf-8")

    if compress and mode in {"base64", "base64url", "hex"}:
        data = zlib.compress(data)

    if mode == "base64":
        return base64.b64encode(data).decode("ascii")
    if mode == "base64url":
        return base64.urlsafe_b64encode(data).decode("ascii")
    if mode == "hex":
        return data.hex()
    if mode == "caesar":
        if compress:
            raise ValueError("Compression is not supported with Caesar cipher")
        return caesar_shift(text, shift)
    if mode == "hash":
        return hashlib.sha256(data).hexdigest()

    raise ValueError("Unsupported mode")

def main():
    parser = argparse.ArgumentParser(description="Advanced text encoder")
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-m", "--mode", choices=["base64", "base64url", "hex", "caesar", "hash"], default="base64")
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--compress", action="store_true")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    result = encode(text, args.mode, shift=args.shift, compress=args.compress)
    Path(args.output).write_text(result, encoding="utf-8")

if __name__ == "__main__":
    main()
