#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
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

def encode_data(text, mode, shift=3, compress=False):
    raw = text.encode("utf-8")

    if compress:
        raw = zlib.compress(raw)

    if mode == "base64":
        return base64.b64encode(raw).decode("ascii")
    if mode == "base64url":
        return base64.urlsafe_b64encode(raw).decode("ascii")
    if mode == "hex":
        return raw.hex()
    if mode == "caesar":
        if compress:
            raise ValueError("Caesar cipher cannot be used with compression")
        return caesar_shift(text, shift)
    if mode == "hash":
        return hashlib.sha256(raw).hexdigest()

    raise ValueError(f"Unsupported mode: {mode}")

def decode_data(text, mode, shift=3, compressed=False):
    if mode == "base64":
        raw = base64.b64decode(text.encode("ascii"))
    elif mode == "base64url":
        raw = base64.urlsafe_b64decode(text.encode("ascii"))
    elif mode == "hex":
        raw = bytes.fromhex(text)
    elif mode == "caesar":
        if compressed:
            raise ValueError("Caesar cipher cannot be used with compression")
        return caesar_shift(text, -shift)
    elif mode == "hash":
        raise ValueError("Hash is one-way and cannot be decoded")
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    if compressed:
        raw = zlib.decompress(raw)

    return raw.decode("utf-8")

def process_file(input_path, output_path, mode, action, shift=3, compress=False, decompressed=False):
    text = Path(input_path).read_text(encoding="utf-8")

    if action == "encode":
        result = encode_data(text, mode, shift=shift, compress=compress)
    else:
        result = decode_data(text, mode, shift=shift, compressed=decompressed)

    Path(output_path).write_text(result, encoding="utf-8")

def batch_process(folder, mode, action, shift=3, compress=False, decompressed=False):
    folder = Path(folder)
    output_dir = folder / "output"
    output_dir.mkdir(exist_ok=True)

    for item in folder.iterdir():
        if item.is_file() and item.name != "toolkit.py":
            out_file = output_dir / f"{item.stem}.{action}.txt"
            try:
                process_file(item, out_file, mode, action, shift=shift, compress=compress, decompressed=decompressed)
            except Exception as e:
                print(f"Skipped {item.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Advanced encoding/decoding toolkit")
    parser.add_argument("action", choices=["encode", "decode"])
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-m", "--mode", choices=["base64", "base64url", "hex", "caesar", "hash"], default="base64")
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--compress", action="store_true", help="Compress before encoding")
    parser.add_argument("--decompress", action="store_true", help="Decompress after decoding")
    parser.add_argument("--batch", help="Batch process all files in a folder")
    args = parser.parse_args()

    if args.batch:
        batch_process(args.batch, args.mode, args.action, shift=args.shift, compress=args.compress, decompressed=args.decompress)
    else:
        if not args.input or not args.output:
            parser.error("input and output are required unless --batch is used")
        process_file(args.input, args.output, args.mode, args.action, shift=args.shift, compress=args.compress, decompressed=args.decompress)

if __name__ == "__main__":
    main()
