import random
import os

class RSA:
    alphabet1 = "abcdefghijklmnopqrstuvwxyz"
    alphabet2 = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    @staticmethod
    def text_to_base10(text, alphabet):
        """Convert a base-N string to a base-10 integer."""
        base = len(alphabet)
        value = 0
        for char in text:
            value = value * base + alphabet.index(char)
        return value

    @staticmethod
    def base10_to_text(number, alphabet):
        """Convert a base-10 integer to a base-N string."""
        base = len(alphabet)
        if number == 0:
            return alphabet[0]
        chars = []
        while number > 0:
            chars.append(alphabet[number % base])
            number //= base
        return ''.join(reversed(chars))

    @staticmethod
    def is_prime(n):
        """Check if a number is prime using trial division."""
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a, b):
        """Compute the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def modular_inverse(a, m):
        """Find the modular inverse of a mod m using the Extended Euclidean Algorithm."""
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1

    def generate_keys(self, text1, text2):
        """Generate RSA keys."""
        p = self.text_to_base10(text1, self.alphabet1) % (10**200)
        q = self.text_to_base10(text2, self.alphabet1) % (10**200)

        print(f"Converted p: {p}")
        print(f"Converted q: {q}")

        # Ensure p and q are large enough
        if p < 10**200 or q < 10**200:
            raise ValueError("Input strings are too short. The primes must be at least 200 digits long.")

        # Make p and q odd if they are even, then find the next prime
        p = p if p % 2 else p + 1
        q = q if q % 2 else q + 1
        while not self.is_prime(p):
            p += 2
        while not self.is_prime(q):
            q += 2

        n = p * q
        r = (p - 1) * (q - 1)

        # Find e
        e = 10**398 + 1
        while self.gcd(e, r) != 1:
            e += 2

        # Find d (modular inverse of e mod r)
        d = self.modular_inverse(e, r)

        # Save public and private keys
        with open("public.txt", "w") as pub_file:
            pub_file.write(f"{n}\n{e}\n")
        with open("private.txt", "w") as priv_file:
            priv_file.write(f"{n}\n{d}\n")

    def encrypt(self, input_file, output_file):
        """Encrypt a file using the RSA algorithm."""
        with open("public.txt", "r") as pub_file:
            n = int(pub_file.readline().strip())
            e = int(pub_file.readline().strip())

        with open(input_file, "rb") as fin:
            plaintext_binary = fin.read()
        plaintext = plaintext_binary.decode("utf-8")

        block_size = 216  # log_70(10^400) ≈ 216
        encrypted_blocks = []
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i+block_size]
            block_number = self.text_to_base10(block, self.alphabet2)
            encrypted_block = pow(block_number, e, n)
            encrypted_blocks.append(self.base10_to_text(encrypted_block, self.alphabet2) + "$")

        with open(output_file, "wb") as fout:
            fout.write(''.join(encrypted_blocks).encode("utf-8"))

    def decrypt(self, input_file, output_file):
        """Decrypt a file using the RSA algorithm."""
        with open("private.txt", "r") as priv_file:
            n = int(priv_file.readline().strip())
            d = int(priv_file.readline().strip())

        with open(input_file, "rb") as fin:
            encrypted_binary = fin.read()
        encrypted_text = encrypted_binary.decode("utf-8")

        blocks = encrypted_text.split("$")
        decrypted_blocks = []
        for block in blocks:
            if not block:
                continue
            block_number = self.text_to_base10(block, self.alphabet2)
            decrypted_block = pow(block_number, d, n)
            decrypted_blocks.append(self.base10_to_text(decrypted_block, self.alphabet2))

        with open(output_file, "wb") as fout:
            fout.write(''.join(decrypted_blocks).encode("utf-8"))



def main():
    rsa = RSA()

    # Hardcoded long strings for key generation
    string1 = "z" * 500  # A 300-character string of 'z'
    string2 = "y" * 500  # A 300-character string of 'y'

    print("Generating keys...")
    rsa.generate_keys(string1, string2)
    print("Keys generated and saved to 'public.txt' and 'private.txt'.")

    # Create a plaintext file (1000 characters from alphabet2)
    original_text = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!\t\n\r" * 15
    )[:1000]  # Repeat alphabet2 to reach 1000 characters
    plaintext_file = "plaintext.txt"
    with open(plaintext_file, "wb") as file:
        file.write(original_text.encode("utf-8"))
    print(f"Plaintext file '{plaintext_file}' created.")

    # Encrypt the plaintext file
    encrypted_file = "encrypted.txt"
    print("Encrypting plaintext...")
    rsa.encrypt(plaintext_file, encrypted_file)
    print(f"Encrypted text saved to '{encrypted_file}'.")

    # Decrypt the encrypted file
    decrypted_file = "decrypted.txt"
    print("Decrypting encrypted text...")
    rsa.decrypt(encrypted_file, decrypted_file)
    print(f"Decrypted text saved to '{decrypted_file}'.")

    # Verify the decrypted file matches the original plaintext
    with open(plaintext_file, "rb") as fin:
        original_content = fin.read().decode("utf-8")
    with open(decrypted_file, "rb") as fout:
        decrypted_content = fout.read().decode("utf-8")

    if original_content == decrypted_content:
        print("Success! Decrypted text matches the original plaintext.")
    else:
        print("Error: Decrypted text does not match the original plaintext.")

    # Cleanup (optional)
    # os.remove(plaintext_file)
    # os.remove(encrypted_file)
    # os.remove(decrypted_file)
    # os.remove("public.txt")
    # os.remove("private.txt")


if __name__ == "__main__":
    main()
