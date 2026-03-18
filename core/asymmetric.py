import base64
import json
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class AsymmetricCipher:
    def generate_keys(self, key_size: int = 2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def save_private_key(self, private_key, filename: str):
        with open(filename, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    def save_public_key(self, public_key, filename: str):
        with open(filename, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

    def load_private_key(self, filename: str):
        with open(filename, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def load_public_key(self, filename: str):
        with open(filename, "rb") as f:
            return serialization.load_pem_public_key(f.read())

    def encrypt_text(self, public_key, message: str) -> str:
        ciphertext = public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode("utf-8")

    def decrypt_text(self, private_key, encrypted_b64: str) -> str:
        ciphertext = base64.b64decode(encrypted_b64.encode("utf-8"))
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode("utf-8")

    def hybrid_encrypt_text(self, public_key, plaintext: str) -> str:
        aes_key = os.urandom(32)

        from core.symmetric import SymmetricCipher
        symmetric = SymmetricCipher()
        iv, ciphertext = symmetric.encrypt_with_raw_key(plaintext.encode("utf-8"), aes_key)

        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        payload = {
            "encrypted_key": base64.b64encode(encrypted_key).decode(),
            "iv": base64.b64encode(iv).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
        }
        return json.dumps(payload, indent=2)

    def hybrid_decrypt_text(self, private_key, payload_str: str) -> str:
        payload = json.loads(payload_str)

        encrypted_key = base64.b64decode(payload["encrypted_key"])
        iv = base64.b64decode(payload["iv"])
        ciphertext = base64.b64decode(payload["ciphertext"])

        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        from core.symmetric import SymmetricCipher
        symmetric = SymmetricCipher()
        plaintext = symmetric.decrypt_with_raw_key(iv, ciphertext, aes_key)
        return plaintext.decode("utf-8")