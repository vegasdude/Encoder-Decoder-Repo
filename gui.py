import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_utils import encode, decode
from pathlib import Path

def run():
    path = filedialog.askopenfilename(title="Select input file")
    if not path:
        return
    mode = mode_var.get()
    action = action_var.get()
    shift = int(shift_var.get() or "3")
    compress = compress_var.get()
    decompress = decompress_var.get()

    out = filedialog.asksaveasfilename(title="Save output as")
    if not out:
        return

    text = Path(path).read_text(encoding="utf-8").strip()

    try:
        if action == "encode":
            result = encode(text, mode, shift=shift, compress=compress)
        else:
            result = decode(text, mode, shift=shift, decompress=decompress)
        Path(out).write_text(result, encoding="utf-8")
        messagebox.showinfo("Done", f"Saved to {out}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Encoding / Decoding Tool")

action_var = tk.StringVar(value="encode")
mode_var = tk.StringVar(value="base64")
shift_var = tk.StringVar(value="3")
compress_var = tk.BooleanVar(value=False)
decompress_var = tk.BooleanVar(value=False)

tk.Label(root, text="Action").grid(row=0, column=0, sticky="w")
tk.Radiobutton(root, text="Encode", variable=action_var, value="encode").grid(row=0, column=1)
tk.Radiobutton(root, text="Decode", variable=action_var, value="decode").grid(row=0, column=2)

tk.Label(root, text="Mode").grid(row=1, column=0, sticky="w")
tk.OptionMenu(root, mode_var, "base64", "base64url", "hex", "caesar", "hash").grid(row=1, column=1, columnspan=2, sticky="ew")

tk.Label(root, text="Shift").grid(row=2, column=0, sticky="w")
tk.Entry(root, textvariable=shift_var).grid(row=2, column=1, columnspan=2, sticky="ew")

tk.Checkbutton(root, text="Compress", variable=compress_var).grid(row=3, column=1, sticky="w")
tk.Checkbutton(root, text="Decompress", variable=decompress_var).grid(row=3, column=2, sticky="w")

tk.Button(root, text="Run", command=run).grid(row=4, column=0, columnspan=3, sticky="ew")

root.mainloop()
