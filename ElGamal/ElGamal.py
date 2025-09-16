# Nama  : Muhammad Zahran Muntazar
# NPM   : 140810230014

from typing import List, Tuple

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Tidak ada invers modulo.")
    return x % m

def only_letters(s: str) -> str:
    return "".join([c for c in s.upper() if c.isalpha()])

def char_to_num(c: str) -> int:
    return alphabet.index(c)

def num_to_char(n: int) -> str:
    return alphabet[n % 26]

def elgamal_encrypt(p: int, g: int, x: int, k: int, plaintext: str) -> Tuple[int, List[int]]:
    text = only_letters(plaintext)
    nums = [char_to_num(ch) for ch in text]

    y  = pow(g, x, p)
    c1 = pow(g, k, p)
    yk = pow(y, k, p)

    print("\n=== Parameter & Rumus ===")
    print(f"{'p (prima)':15s}: {p}")
    print(f"{'g (generator)':15s}: {g}")
    print(f"{'x (privat)':15s}: {x}")
    print(f"{'k (nonce)':15s}: {k}")
    print(f"{'y = g^x mod p':15s}: {y}")
    print(f"{'c1 = g^k mod p':15s}: {c1}   <-- rumus c1")
    print(f"{'y^k mod p':15s}: {yk}")

    print("\n=== Tabel Enkripsi ===")
    print(" i  ch  m_i  c2_i")
    c2_list = []
    for i, m in enumerate(nums):
        c2 = (m * yk) % p
        c2_list.append(c2)
        print(f"{i:2d}  {text[i]:2s}  {m:3d}  {c2:4d}")

    pairs = ", ".join([f"({c1},{c2})" for c2 in c2_list])
    print("\nCiphertext (c1,c2_i):")
    print(pairs)
    return c1, c2_list

def elgamal_decrypt(p: int, x: int, c1: int, c2_list: List[int]) -> str:
    print("\n=== Langkah Dekripsi ===")
    print(f"{'p (prima)':15s}: {p}")
    print(f"{'x (privat)':15s}: {x}")
    print(f"{'c1':15s}: {c1}")
    print(f"{'c2 list':15s}: {c2_list}")

    s = pow(c1, x, p)
    s_inv = modinv(s, p)

    print(f"{'s = c1^x mod p':15s}: {s}")
    print(f"{'s_inv':15s}: {s_inv} (mod {p})")

    print("\n i  c2_i  m_i  ch")
    m_nums = []
    for i, c2 in enumerate(c2_list):
        m_i = (c2 * s_inv) % p
        m_nums.append(m_i)
        ch = num_to_char(m_i) if 0 <= m_i < 26 else "?"
        print(f"{i:2d}  {c2:4d}  {m_i:3d}  {ch:2s}")

    plaintext = "".join([num_to_char(m) if 0 <= m < 26 else "?" for m in m_nums])
    print("\nPlaintext hasil dekripsi:", plaintext)
    return plaintext

def main():
    while True:
        print("\n=== Program ElGamal Cipher ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")
        try:
            pilih = int(input("Pilih (1/2/3): ").strip())
        except:
            print("Input salah.")
            continue

        if pilih == 1:
            p = int(input("Masukkan p (prima)     : "))
            g = int(input("Masukkan g (generator) : "))
            x = int(input("Masukkan x (privat)    : "))
            k = int(input("Masukkan k (nonce)     : "))
            plaintext = input("Masukkan plaintext     : ")
            elgamal_encrypt(p, g, x, k, plaintext)

        elif pilih == 2:
            p = int(input("Masukkan p (prima)     : "))
            x = int(input("Masukkan x (privat)    : "))
            c1 = int(input("Masukkan c1            : "))
            raw = input("Masukkan daftar c2 dipisah spasi: ")
            c2_list = [int(t) for t in raw.strip().split() if t]
            elgamal_decrypt(p, x, c1, c2_list)

        elif pilih == 3:
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
