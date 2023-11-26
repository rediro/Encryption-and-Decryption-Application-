import tkinter as tk
from tkinter import ttk
import random
import math

class RSAApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Encryption/Decryption using RSA")

        # Create labels and entry widgets
        ttk.Label(master, text="Enter Message:").grid(row=0, column=0, padx=10, pady=10)
        self.message_entry = ttk.Entry(master, width=50)
        self.message_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create buttons
        ttk.Button(master, text="Encrypt", command=self.encrypt_message).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(master, text="Decrypt", command=self.decrypt_message).grid(row=1, column=1, padx=10, pady=10)

        # Create text widget for displaying results
        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=2, columnspan=2, padx=10, pady=10)

        # Initialize RSA
        self.prime = set()
        self.primefiller()
        self.setkeys()

    def primefiller(self):
        # Function to fill the set of prime numbers
        seive = [True] * 250
        seive[0] = False
        seive[1] = False
        for i in range(2, 250):
            for j in range(i * 2, 250, i):
                seive[j] = False

        for i in range(len(seive)):
            if seive[i]:
                self.prime.add(i)

    def setkeys(self):
        prime1 = self.pickrandomprime()
        prime2 = self.pickrandomprime()

        n = prime1 * prime2
        fi = (prime1 - 1) * (prime2 - 1)

        e = 2
        while True:
            if math.gcd(e, fi) == 1:
                break
            e += 1

        self.public_key = e
        self.n = n  # Save n for later use in encryption/decryption

        d = 2
        while True:
            if (d * e) % fi == 1:
                break
            d += 1

        self.private_key = d

    def pickrandomprime(self):
        k = random.randint(0, len(self.prime) - 1)
        it = iter(self.prime)
        for _ in range(k):
            next(it)

        ret = next(it)
        self.prime.remove(ret)
        return ret

    def encrypt_message(self):
        message = self.message_entry.get()
        coded = self.encoder(message)
        encrypted_message = ''.join(str(p) for p in coded)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Encrypted Message:\n{encrypted_message}")

    def decrypt_message(self):
        message = self.message_entry.get()
        coded = self.encoder(message)
        decoded_message = ''.join(str(p) for p in self.decoder(coded))
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Decrypted Message:\n{decoded_message}")

    def encrypt(self, message):
        e = self.public_key
        encrypted_text = 1
        while e > 0:
            encrypted_text *= message
            encrypted_text %= self.n
            e -= 1
        return encrypted_text

    def decrypt(self, encrypted_text):
        d = self.private_key
        decrypted = 1
        while d > 0:
            decrypted *= encrypted_text
            decrypted %= self.n
            d -= 1
        return decrypted

    def encoder(self, message):
        encoded = []
        for letter in message:
            encoded.append(self.encrypt(ord(letter)))
        return encoded

    def decoder(self, encoded):
        s = ''
        for num in encoded:
            s += chr(self.decrypt(num))
        return s

def main():
    root = tk.Tk()
    app = RSAApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()

