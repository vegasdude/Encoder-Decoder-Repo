#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from crypto_utils import encode, decode, metadata_for, verify_metadata

def process_encode(input_dir, output_dir, mode, shift=3, compress=False, password=None):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if file.is_file() and file.suffix.lower() in {".txt", ".md", ".csv", ".log"}:
            text = file.read_text(encoding="utf-8").strip()
            encoded, raw = encode(text, mode, shift=shift, compress=compress, password=password)

            out_file = output_dir / f"{file.stem}.enc.txt"
            meta_file = output_dir / f"{file.stem}.json"

            out_file.write_text(encoded, encoding="utf-8")
            meta = metadata_for(str(file), mode, shift, compress, raw, encoded)
            meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")

def process_decode(input_dir, output_dir, mode, shift=3, decompress=False, password=None, verify=False):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if file.is_file() and file.name.endswith(".enc.txt"):
            base = file.name.replace(".enc.txt", "")
            meta_file = input_dir / f"{base}.json"
            out_file = output_dir / f"{base}.txt"

            text = file.read_text(encoding="utf-8").strip()

            if meta_file.exists():
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                mode = meta.get("mode", mode)
                shift = meta.get("shift", shift)
                decompress = meta.get("compressed", decompress)

            result = decode(text, mode, shift=shift, decompress=decompress, password=password)
            out_file.write_text(result, encoding="utf-8")

            if verify and meta_file.exists():
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                ok, actual = verify_metadata(result.encode("utf-8"), meta)
                status = "OK" if ok else "FAILED"
                print(f"{file.name}: {status}")
                if not ok:
                    print(f"  expected: {meta.get('sha256')}")
                    print(f"  actual:   {actual}")

def main():
    parser = argparse.ArgumentParser(description="Batch encoding/decoding tool")
    parser.add_argument("action", choices=["encode", "decode"])
    parser.add_argument("-i", "--input", required=True, help="Input folder")
    parser.add_argument("-o", "--output", required=True, help="Output folder")
    parser.add_argument("-m", "--mode", choices=["base64", "base64url", "hex", "caesar", "hash", "aes"], default="base64")
    parser.add_argument("--shift", type=int, default=3)
    parser.add_argument("--compress", action="store_true")
    parser.add_argument("--decompress", action="store_true")
    parser.add_argument("--password", default=None)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    if args.action == "encode":
        process_encode(args.input, args.output, args.mode, shift=args.shift, compress=args.compress, password=args.password)
    else:
        process_decode(args.input, args.output, args.mode, shift=args.shift, decompress=args.decompress, password=args.password, verify=args.verify)

if __name__ == "__main__":
    main()
