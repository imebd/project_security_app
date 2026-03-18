import base64
import os
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCipher:
    def __init__(self, iterations: int = 100000):
        self.iterations = iterations

    def generate_aes_key(self) -> str:
        key = os.urandom(32)
        return base64.b64encode(key).decode()

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )
        return kdf.derive(password.encode("utf-8"))

    def encrypt_text(self, plaintext: str, password: str) -> str:
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        data = plaintext.encode("utf-8")
        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        blob = salt + iv + ciphertext
        return base64.b64encode(blob).decode("utf-8")

    def decrypt_text(self, encrypted_b64: str, password: str) -> str:
        blob = base64.b64decode(encrypted_b64.encode("utf-8"))
        salt = blob[:16]
        iv = blob[16:32]
        ciphertext = blob[32:]

        key = self._derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return plaintext.decode("utf-8")

    def encrypt_file(self, input_file: str, output_file: str, password: str) -> None:
        with open(input_file, "rb") as f:
            data = f.read()

        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(password, salt)

        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        with open(output_file, "wb") as f:
            f.write(salt + iv + ciphertext)

    def decrypt_file(self, input_file: str, output_file: str, password: str) -> None:
        with open(input_file, "rb") as f:
            blob = f.read()

        salt = blob[:16]
        iv = blob[16:32]
        ciphertext = blob[32:]

        key = self._derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()

        with open(output_file, "wb") as f:
            f.write(data)

    def encrypt_with_raw_key(self, plaintext: bytes, raw_key: bytes) -> tuple[bytes, bytes]:
        iv = os.urandom(16)

        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(algorithms.AES(raw_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return iv, ciphertext

    def decrypt_with_raw_key(self, iv: bytes, ciphertext: bytes, raw_key: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(raw_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()