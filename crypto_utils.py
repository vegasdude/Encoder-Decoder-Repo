import base64
import hashlib
import zlib

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
