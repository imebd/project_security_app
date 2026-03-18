import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class CertificateManager:
    def generate_self_signed_certificate(
        self,
        common_name: str,
        organization: str = "ENSA Fes",
        country: str = "MA",
        days_valid: int = 365
    ):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days_valid))
            .sign(private_key, hashes.SHA256())
        )

        return private_key, cert

    def save_private_key(self, private_key, filename: str):
        with open(filename, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    def save_certificate(self, cert, filename: str):
        with open(filename, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    def load_certificate(self, filename: str):
        with open(filename, "rb") as f:
            return x509.load_pem_x509_certificate(f.read())

    def get_certificate_info(self, cert) -> str:
        return (
            f"Sujet : {cert.subject}\n"
            f"Émetteur : {cert.issuer}\n"
            f"Numéro de série : {cert.serial_number}\n"
            f"Valide à partir de : {cert.not_valid_before}\n"
            f"Valide jusqu'à : {cert.not_valid_after}\n"
            f"Signature hash : SHA256\n"
        )