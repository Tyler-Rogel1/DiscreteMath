import math
import sys
from millers import isPrime


def convert_to_base10(input_str, alphabet):
    """Converts a string to a base-10 number using the given alphabet."""
    base = len(alphabet)
    result = 0
    for char in input_str:
        pos = alphabet.find(char)
        if pos != -1:
            result = result * base + pos
    return result


def convert_from_base10(number, alphabet):
    """Converts a base-10 number to a string using the given alphabet."""
    base = len(alphabet)
    result = []
    while number != 0:
        result.append(alphabet[number % base])
        number //= base
    result.reverse()
    return ''.join(result)


def modular_inverse(a, n):
    """Finds the modular inverse of a with respect to n."""
    t, new_t = 0, 1
    r, new_r = n, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        return "a is not invertible"
    if t < 0:
        t += n
    return t


class RSA:
    """Class implementing RSA encryption and decryption."""

    def generate_keys(self, prime_str1, prime_str2):
        """
        Generates RSA keys based on two input strings.
        Saves public key to `public.txt` and private key to `private.txt`.
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        prime1 = convert_to_base10(prime_str1, alphabet)
        prime2 = convert_to_base10(prime_str2, alphabet)

        if prime1 < 10**200 or prime2 < 10**200:
            print("Input strings are too short!")
            sys.exit(1)

        prime1 %= 10**200
        prime2 %= 10**200

        if prime1 % 2 == 0:
            prime1 += 1
        if prime2 % 2 == 0:
            prime2 += 1

        while not isPrime(prime1):
            prime1 += 2
        while not isPrime(prime2):
            prime2 += 2

        modulus = prime1 * prime2
        totient = (prime1 - 1) * (prime2 - 1)

        public_exponent = 65539
        while math.gcd(public_exponent, totient) != 1:
            public_exponent += 1

        private_exponent = modular_inverse(public_exponent, totient)

        with open("public.txt", 'w') as pub_file:
            pub_file.write(f"{modulus}\n{public_exponent}\n")

        with open("private.txt", 'w') as priv_file:
            priv_file.write(f"{modulus}\n{private_exponent}\n")

    def encrypt(self, input_file, output_file):
        """Encrypts the content of input_file and writes to output_file."""
        with open(input_file, "rb") as fin:
            plaintext = fin.read().decode("utf-8")

        alphabet = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        with open("public.txt", "r") as pub_file:
            modulus = int(pub_file.readline())
            public_exponent = int(pub_file.readline())

        block_size = 216
        num_blocks = math.ceil(len(plaintext) / block_size)

        with open(output_file, "wb") as fout:
            for i in range(num_blocks):
                block = plaintext[i * block_size:(i + 1) * block_size]
                block_num = convert_to_base10(block, alphabet)
                encrypted_block = pow(block_num, public_exponent, modulus)
                encrypted_text = convert_from_base10(encrypted_block, alphabet)
                fout.write(encrypted_text.encode("utf-8"))
                fout.write(b"$")

    def decrypt(self, input_file, output_file):
        """Decrypts the content of input_file and writes to output_file."""
        with open(input_file, "rb") as fin:
            ciphertext = fin.read().decode("utf-8")

        alphabet = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        blocks = ciphertext.split("$")

        decrypted_blocks = []
        for block in blocks:
            if block:
                decrypted_blocks.append(convert_to_base10(block, alphabet))

        with open("private.txt", 'r') as priv_file:
            modulus, private_exponent = map(int, priv_file.readlines())

        plaintext_blocks = []
        for block in decrypted_blocks:
            decrypted_block = pow(block, private_exponent, modulus)
            plaintext = convert_from_base10(decrypted_block, alphabet)
            plaintext_blocks.append(plaintext)

        with open(output_file, 'wb') as fout:
            fout.write(''.join(plaintext_blocks).encode("utf-8"))


def main():
    rsa = RSA()

    prime_input1 = "hello" * 200
    prime_input2 = "orange" * 200

    rsa.generate_keys(prime_input1, prime_input2)

    rsa.encrypt("message.txt", "encrypted.txt")
    rsa.decrypt("encrypted.txt", "decrypted.txt")
    rsa.decrypt("TylerEncrypted.txt", "TylerDecrypted.txt")


if __name__ == "__main__":
    main()
