# Nama  : Muhammad Zahran Muntazar
# NPM   : 140810230014
# Kelas : B
class VigenereCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def prepare_text(self, text):
        return ''.join(text.split()).upper()

    def extend_key(self, text, key):
        key = key.upper()
        return (key * (len(text) // len(key) + 1))[:len(text)]

    def encrypt(self, plaintext, key):
        plaintext = self.prepare_text(plaintext)
        key = self.extend_key(plaintext, key)
        rows = {"PT": [], "nPT": [], "K": [], "nK": [], "SUM": [], "CT": []}

        for p, k in zip(plaintext, key):
            p_idx = self.alphabet.index(p)
            k_idx = self.alphabet.index(k)
            c_idx = (p_idx + k_idx) % 26
            rows["PT"].append(p)
            rows["nPT"].append(p_idx)
            rows["K"].append(k)
            rows["nK"].append(k_idx)
            rows["SUM"].append(c_idx)
            rows["CT"].append(self.alphabet[c_idx])

        return rows, ''.join(rows["CT"])

    def decrypt(self, ciphertext, key):
        ciphertext = self.prepare_text(ciphertext)
        key = self.extend_key(ciphertext, key)
        rows = {"CT": [], "nCT": [], "K": [], "nK": [], "DIFF": [], "PT": []}

        for c, k in zip(ciphertext, key):
            c_idx = self.alphabet.index(c)
            k_idx = self.alphabet.index(k)
            p_idx = (c_idx - k_idx) % 26
            rows["CT"].append(c)
            rows["nCT"].append(c_idx)
            rows["K"].append(k)
            rows["nK"].append(k_idx)
            rows["DIFF"].append(p_idx)
            rows["PT"].append(self.alphabet[p_idx])

        return rows, ''.join(rows["PT"])

def format_row(label, data):
    return f"{label:<12}: " + " ".join(f"{str(x):>3}" for x in data)

def print_table_enkripsi(rows):
    print("\n=== Tabel Enkripsi ===")
    print(format_row("PT", rows["PT"]))
    print(format_row("n(PT)", rows["nPT"]))
    print(format_row("K", rows["K"]))
    print(format_row("n(K)", rows["nK"]))
    print(format_row("(nPT+nK)", rows["SUM"]))
    print(format_row("CT", rows["CT"]))

def print_table_dekripsi(rows):
    print("\n=== Tabel Dekripsi ===")
    print(format_row("CT", rows["CT"]))
    print(format_row("n(CT)", rows["nCT"]))
    print(format_row("K", rows["K"]))
    print(format_row("n(K)", rows["nK"]))
    print(format_row("(nCT-nK)", rows["DIFF"]))
    print(format_row("PT", rows["PT"]))


def main():
    cipher = VigenereCipher()

    while True:
        print("\n=== Program Vigenere Cipher ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            plaintext = input("Masukkan Plaintext : ")
            key = input("Masukkan Kunci     : ")
            rows, hasil = cipher.encrypt(plaintext, key)
            print_table_enkripsi(rows)
            print(f"\nCiphertext: {hasil}\n")

        elif pilihan == "2":
            ciphertext = input("Masukkan Ciphertext: ")
            key = input("Masukkan Kunci     : ")
            rows, hasil = cipher.decrypt(ciphertext, key)           
            print_table_dekripsi(rows)
            print(f"\nPlaintext: {hasil}\n")

        elif pilihan == "3":
            print("Selesai, terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
