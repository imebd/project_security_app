import hashlib


class HashManager:
    def calculate_sha256(self, filepath: str) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def calculate_text_sha256(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def verify_hash(self, filepath: str, expected_hash: str) -> bool:
        current_hash = self.calculate_sha256(filepath)
        return current_hash == expected_hash.strip()

    def simulate_modification(self, filepath: str) -> None:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("\n[MODIFICATION SIMULÉE]")