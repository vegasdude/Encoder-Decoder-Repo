#!/usr/bin/env python3
import argparse
from encoder import encode
from decoder import decode
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Unified encoding/decoding toolkit")
    parser.add_argument("action", choices=["encode", "decode"])
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-m", "--mode", choices=["base64", "base64url", "hex", "caesar", "hash"], default="base64")
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--compress", action="store_true")
    parser.add_argument("--decompress", action="store_true")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8").strip()

    if args.action == "encode":
        result = encode(text, args.mode, shift=args.shift, compress=args.compress)
    else:
        result = decode(text, args.mode, shift=args.shift, decompress=args.decompress)

    Path(args.output).write_text(result, encoding="utf-8")

if __name__ == "__main__":
    main()
