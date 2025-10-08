# Nama  : Muhammad Zahran Muntazar
# NPM   : 140810230014

import os, sys, struct, argparse

try:
    from PIL import Image
except Exception as e:
    print("Harap install Pillow: pip install pillow")
    sys.exit(1)

MAGIC = b"STG1"
VERSION = 1
BITS_PER_CHANNEL = 2  # 2 bit LSB per channel (R,G,B)

def _bytes_to_bits(data: bytes):
    for byte in data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1

def _bits_to_bytes(bits):
    out = bytearray()
    cur = 0
    for i, b in enumerate(bits):
        cur = (cur << 1) | (b & 1)
        if (i + 1) % 8 == 0:
            out.append(cur)
            cur = 0
    return bytes(out)

def _capacity_bytes(img):
    w, h = img.size
    channels = 3  # gunakan RGB 
    total_bits = w * h * channels * BITS_PER_CHANNEL
    return total_bits // 8

def _embed_bits(img, bits):
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    px = img.load()
    use_alpha = (len(img.getbands()) == 4)
    bit_iter = iter(bits)
    w, h = img.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            r, g, b = p[0], p[1], p[2]

            def take2():
                try:
                    b1 = next(bit_iter)
                    b2 = next(bit_iter)
                    return (b1 << 1) | b2
                except StopIteration:
                    return None

            v = take2()
            if v is None:
                px[x, y] = (r, g, b, p[3]) if use_alpha else (r, g, b)
                return img
            r = (r & ~3) | v

            v = take2()
            if v is None:
                px[x, y] = (r, g, b, p[3]) if use_alpha else (r, g, b)
                return img
            g = (g & ~3) | v

            v = take2()
            if v is None:
                px[x, y] = (r, g, b, p[3]) if use_alpha else (r, g, b)
                return img
            b = (b & ~3) | v

            px[x, y] = (r, g, b, p[3]) if use_alpha else (r, g, b)
    return img

def _extract_bits(img):
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][0:3]
            for chan in (r, g, b):
                v = chan & 3
                yield (v >> 1) & 1
                yield v & 1

def build_payload_text(text: str) -> bytes:
    data = text.encode("utf-8")
    header = MAGIC + struct.pack(">B", VERSION) + struct.pack(">B", 0) + struct.pack(">I", len(data))
    return header + data

def build_payload_file(path: str) -> bytes:
    name = os.path.basename(path).encode("utf-8")
    blob = open(path, "rb").read()
    header = MAGIC + struct.pack(">B", VERSION) + struct.pack(">B", 1) + struct.pack(">H", len(name)) + name + struct.pack(">I", len(blob))
    return header + blob

def parse_payload(blob: bytes):
    i = blob.find(MAGIC)
    if i < 0:
        raise ValueError("MAGIC tidak ditemukan. Bukan stego.")
    blob = blob[i:]
    ver = blob[4]
    ptype = blob[5]
    idx = 6
    if ptype == 0:
        n = struct.unpack(">I", blob[idx:idx+4])[0]; idx += 4
        data = blob[idx:idx+n]
        return {"type":"text","text":data.decode("utf-8",errors="replace")}
    elif ptype == 1:
        name_len = struct.unpack(">H", blob[idx:idx+2])[0]; idx += 2
        name = blob[idx:idx+name_len].decode("utf-8",errors="replace"); idx += name_len
        size = struct.unpack(">I", blob[idx:idx+4])[0]; idx += 4
        data = blob[idx:idx+size]
        return {"type":"file","name":name,"data":data}
    else:
        raise ValueError("Tipe payload tidak dikenal.")

def encode(cover_path, out_path, text=None, file_path=None):
    if (text is None) == (file_path is None):
        raise ValueError("Pilih salah satu: text atau file.")
    img = Image.open(cover_path)
    payload = build_payload_text(text) if text is not None else build_payload_file(file_path)
    cap = _capacity_bytes(img)
    if len(payload) + 16 > cap:
        raise ValueError(f"Kapasitas kurang. Payload {len(payload)} byte, kapasitas {cap} byte.")
    bits = list(_bytes_to_bits(payload))
    stego = _embed_bits(img.copy(), bits)
    stego.save(out_path)
    return cap, len(payload)

def decode(stego_path, out_dir):
    img = Image.open(stego_path)
    bits = list(_extract_bits(img))
    blob = _bits_to_bytes(bits)
    meta = parse_payload(blob)
    if meta["type"] == "text":
        return {"mode":"text","text":meta["text"]}
    else:
        os.makedirs(out_dir, exist_ok=True)
        outpath = os.path.join(out_dir, meta["name"] or "payload.bin")
        with open(outpath, "wb") as f:
            f.write(meta["data"])
        return {"mode":"file","path":outpath, "size":len(meta["data"])}

def ensure_dirs():
    base = os.path.dirname(os.path.abspath(__file__))
    cover = os.path.join(base, "Cover Object")
    stego = os.path.join(base, "Stego Object")
    os.makedirs(cover, exist_ok=True)
    os.makedirs(stego, exist_ok=True)
    return cover, stego


def _resolve_user_path(input_str, default_dir):
    p = input_str.strip().strip('"').strip("'")
    # If absolute path exists, use it
    if os.path.isabs(p) and os.path.exists(p):
        return p
    # If relative path exists as given, use it
    if os.path.exists(p):
        return p
    # Otherwise join with default_dir
    return os.path.join(default_dir, p)


def menu():
    cover_dir, stego_dir = ensure_dirs()
    while True:
        print("\n=== Steganografi LSB (CLI) ===")
        print("1. Encode")
        print("2. Decode")
        print("3. Keluar")
        try:
            choice = input("Pilih menu [1/2/3]: ").strip()
        except EOFError:
            break

        if choice == "1":
            print("\n1) Sisipkan Teks\n2) Sisipkan File")
            sub = input("Pilih [1/2]: ").strip()
            cover_name = input("Masukkan Nama File Cover Object (contoh: cover_1.png): ").strip()
            cover_path = _resolve_user_path(cover_name, cover_dir)
            if not os.path.exists(cover_path):
                print("✗ Cover tidak ditemukan:", cover_path)
                continue
            out_name = os.path.splitext(os.path.basename(cover_name))[0] + "_stego.png"
            out_path = os.path.join(stego_dir, out_name)
            try:
                if sub == "1":
                    msg = input("Masukkan Pesan: ")
                    cap, used = encode(cover_path, out_path, text=msg)
                    print(f"✓ Berhasil. Pesan tersisip → {out_path}")
                else:
                    fpath = input("Masukkan path file yang disisipkan (relatif/absolut): ").strip()
                    fpath_r = _resolve_user_path(fpath, os.path.dirname(cover_path))
                    cap, used = encode(cover_path, out_path, file_path=fpath_r)
                    print(f"✓ Berhasil. File tersisip → {out_path}")
            except Exception as e:
                print("✗ Gagal:", e)

        elif choice == "2":
            stego_name = input("Masukkan Nama File Stego Object (contoh: cover_1_stego.png): ").strip()
            stego_path = _resolve_user_path(stego_name, stego_dir)
            if not os.path.exists(stego_path):
                print("✗ Stego tidak ditemukan:", stego_path)
                continue
            outdir = os.path.join(stego_dir, "decoded")
            try:
                res = decode(stego_path, outdir)
                if res["mode"] == "text":
                    print("✓ Pesan Terbaca:")
                    print(res["text"])
                else:
                    print(f"✓ File Terbaca → {res['path']} ({res['size']} bytes)")
            except Exception as e:
                print("✗ Gagal:", e)

        elif choice == "3":
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Menu tidak dikenal.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        menu()
    else:
        parser = argparse.ArgumentParser(description="Steganografi LSB 2-bit (CLI & fungsi)")
        sub = parser.add_subparsers(dest="cmd", required=True)
        p1 = sub.add_parser("encode")
        p1.add_argument("--cover", required=True)
        p1.add_argument("--out", required=True)
        g = p1.add_mutually_exclusive_group(required=True)
        g.add_argument("--text")
        g.add_argument("--file")
        p2 = sub.add_parser("decode")
        p2.add_argument("--stego", required=True)
        p2.add_argument("--outdir", default="decoded")
        args = parser.parse_args()
        if args.cmd == "encode":
            cap, used = encode(args.cover, args.out, text=args.text, file_path=args.file)
            print("OK encode →", args.out)
        else:
            res = decode(args.stego, args.outdir)
            print("OK decode →", res)
