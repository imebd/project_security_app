import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class DigitalSignature:
    def sign_text(self, private_key, text: str) -> str:
        signature = private_key.sign(
            text.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode("utf-8")

    def verify_text_signature(self, public_key, text: str, signature_b64: str) -> bool:
        signature = base64.b64decode(signature_b64.encode("utf-8"))
        try:
            public_key.verify(
                signature,
                text.encode("utf-8"),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def sign_file(self, private_key, filepath: str) -> bytes:
        with open(filepath, "rb") as f:
            data = f.read()

        return private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def verify_signature(self, public_key, filepath: str, signature: bytes) -> bool:
        with open(filepath, "rb") as f:
            data = f.read()

        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False