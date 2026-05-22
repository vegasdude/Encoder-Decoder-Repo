#!/usr/bin/env python3
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

def choose_mode():
    print("
Select mode:")
    print("1. base64")
    print("2. base64url")
    print("3. hex")
    print("4. caesar")
    print("5. hash")
    choice = input("Enter choice: ").strip()

    return {
        "1": "base64",
        "2": "base64url",
        "3": "hex",
        "4": "caesar",
        "5": "hash",
    }.get(choice, "base64")

def main():
    print("Advanced Encoding / Decoding Tool")
    print("1. Encode file")
    print("2. Decode file")
    print("3. Exit")

    action = input("Choose action: ").strip()
    if action == "3":
        return

    input_file = input("Input file path: ").strip()
    output_file = input("Output file path: ").strip()
    mode = choose_mode()

    shift = 3
    if mode == "caesar":
        try:
            shift = int(input("Shift value (default 3): ").strip() or "3")
        except ValueError:
            shift = 3

    compress = False
    decompress = False

    if action == "1" and mode in {"base64", "base64url", "hex"}:
        compress = input("Compress before encoding? (y/n): ").strip().lower() == "y"

    if action == "2" and mode in {"base64", "base64url", "hex"}:
        decompress = input("Decompress after decoding? (y/n): ").strip().lower() == "y"

    text = Path(input_file).read_text(encoding="utf-8").strip()

    if action == "1":
        result = encode(text, mode, shift=shift, compress=compress)
    elif action == "2":
        if mode == "hash":
            raise ValueError("Hash cannot be decoded")
        result = decode(text, mode, shift=shift, decompress=decompress)
    else:
        print("Invalid action")
        return

    Path(output_file).write_text(result, encoding="utf-8")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
