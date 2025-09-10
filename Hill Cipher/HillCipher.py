# Nama  : Muhammad Zahran Muntazar
# NPM   : 140810230014
# Kelas : B

import numpy as np
from math import gcd

MOD = 26
A_ORD = ord('A')

def clean_text(s: str) -> str:
    return ''.join(ch for ch in s.upper() if 'A' <= ch <= 'Z')

def to_nums(s: str) -> np.ndarray:
    return np.array([ord(c) - A_ORD for c in s], dtype=int)

def to_text(arr: np.ndarray) -> str:
    return ''.join(chr((int(x) % MOD) + A_ORD) for x in arr)

def chunk_vectorize(nums: np.ndarray, n: int) -> np.ndarray:
    m = len(nums)
    if m % n != 0:
        pad = n - (m % n)
        nums = np.concatenate([nums, np.full(pad, ord('X')-A_ORD, dtype=int)])
    return nums.reshape(-1, n).T

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int | None:
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

# Determinan & Invers Matriks
def minor(mat: np.ndarray, i: int, j: int) -> np.ndarray:
    return np.delete(np.delete(mat, i, axis=0), j, axis=1)

def det_int(mat: np.ndarray) -> int:
    n = mat.shape[0]
    if n == 1:
        return int(mat[0, 0])
    if n == 2:
        return int(mat[0, 0]*mat[1, 1] - mat[0, 1]*mat[1, 0])
    total = 0
    for j in range(n):
        total += ((-1) ** j) * mat[0, j] * det_int(minor(mat, 0, j))
    return int(total)

def adjugate(mat: np.ndarray) -> np.ndarray:
    n = mat.shape[0]
    cof = np.zeros_like(mat, dtype=int)
    for i in range(n):
        for j in range(n):
            cof[i, j] = ((-1) ** (i + j)) * det_int(minor(mat, i, j))
    return cof.T

def mat_inv_mod(mat: np.ndarray, mod: int) -> np.ndarray | None:
    det = det_int(mat) % mod
    inv_det = modinv(det, mod)
    if inv_det is None:
        return None
    adj = adjugate(mat) % mod
    return (inv_det * adj) % mod

# Hill Cipher
def encrypt(plain: str, K: np.ndarray) -> str:
    n = K.shape[0]
    pnums = to_nums(clean_text(plain))
    P = chunk_vectorize(pnums, n)
    C = (K.dot(P)) % MOD
    return to_text(C.T.reshape(-1))

def decrypt(cipher: str, K: np.ndarray) -> str:
    n = K.shape[0]
    K_inv = mat_inv_mod(K, MOD)
    if K_inv is None:
        raise ValueError("Kunci tidak invertible modulo 26.")
    cnums = to_nums(clean_text(cipher))
    C = chunk_vectorize(cnums, n)
    P = (K_inv.dot(C)) % MOD
    return to_text(P.T.reshape(-1))

def find_key_from_pt_ct(plain: str, cipher: str, n: int) -> np.ndarray:
    pnums = to_nums(clean_text(plain))
    cnums = to_nums(clean_text(cipher))
    if len(pnums) < n*n or len(cnums) < n*n:
        raise ValueError(f"Butuh minimal {n*n} huruf PT & CT.")

    P_all = chunk_vectorize(pnums, n)
    C_all = chunk_vectorize(cnums, n)
    m = P_all.shape[1]

    for start in range(0, m - n + 1):
        P_sub = P_all[:, start:start+n]
        C_sub = C_all[:, start:start+n]
        P_inv = mat_inv_mod(P_sub, MOD)
        if P_inv is not None:
            K = (C_sub.dot(P_inv)) % MOD
            return K.astype(int)

    raise ValueError("Tidak ditemukan submatriks P yang invertible.")

# Input matriks 
def input_key_matrix(n: int) -> np.ndarray:
    print(f"Masukkan matriks kunci {n}x{n} (tiap baris dipisahkan spasi):")
    vals = []
    for i in range(n):
        row = input(f"Baris {i+1}: ").split()
        vals.extend(int(x) for x in row)
    K = np.array(vals, dtype=int).reshape(n, n) % MOD

    d = det_int(K) % MOD
    if gcd(d, MOD) != 1:
        raise ValueError("Kunci tidak invertible (gcd(det,26) ≠ 1).")
    return K

# Menu
def print_matrix(K: np.ndarray):
    print("[")
    for row in K:
        print("  [ " + "  ".join(f"{int(x):2d}" for x in row) + " ]")
    print("]")

def main():

    while True:
        print("===================================================")
        print("                PROGRAM HILL CIPHER                ")
        print("===================================================")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Mencari Kunci PT & CT")
        print("0. Keluar")
        print("---------------------------------------------------")
        choice = input("Pilih menu (0-3): ").strip()

        if choice == '1':
            try:
                n = int(input("Ukuran matriks kunci n: "))
                K = input_key_matrix(n)
                print("\nMatriks kunci:")
                print_matrix(K)
                pt = input("Plaintext : ")
                print("Ciphertext:", encrypt(pt, K), "\n")
            except Exception as e:
                print("Error:", e, "\n")

        elif choice == '2':
            try:
                n = int(input("Ukuran matriks kunci n: "))
                K = input_key_matrix(n)
                print("\nMatriks kunci:")
                print_matrix(K)
                ct = input("Ciphertext: ")
                print("Plaintext :", decrypt(ct, K), "\n")
            except Exception as e:
                print("Error:", e, "\n")

        elif choice == '3':
            try:
                n = int(input("Ukuran matriks kunci n: "))
                pt = input("Plaintext  : ")
                ct = input("Ciphertext : ")
                K_found = find_key_from_pt_ct(pt, ct, n)
                print("\nKunci ditemukan:")
                print_matrix(K_found)
                print()
            except Exception as e:
                print("Error:", e, "\n")

        elif choice == '0':
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()