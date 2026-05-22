#!/usr/bin/env python3
import argparse
import base64
from pathlib import Path

def decode_text(text: str, mode: str) -> str:
    if mode == "base64":
        return base64.b64decode(text.encode("ascii")).decode("utf-8")

    if mode == "hex":
        return bytes.fromhex(text).decode("utf-8")

    if mode == "caesar":
        shift = 3
        out = []
        for ch in text:
            if "a" <= ch <= "z":
                out.append(chr((ord(ch) - 97 - shift) % 26 + 97))
            elif "A" <= ch <= "Z":
                out.append(chr((ord(ch) - 65 - shift) % 26 + 65))
            else:
                out.append(ch)
        return "".join(out)

    raise ValueError(f"Unsupported mode: {mode}")

def main():
    parser = argparse.ArgumentParser(description="Decode text files")
    parser.add_argument("-i", "--input", required=True, help="Input encoded file")
    parser.add_argument("-o", "--output", required=True, help="Output decoded file")
    parser.add_argument("-m", "--mode", choices=["base64", "hex", "caesar"], default="base64")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8").strip()
    decoded = decode_text(text, args.mode)
    Path(args.output).write_text(decoded, encoding="utf-8")

if __name__ == "__main__":
    main()
