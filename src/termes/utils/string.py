import hashlib


def sha256(string: str, *, salt: str | None = None, encoding: str = "utf-8") -> str:
    if salt is None:
        return hashlib.sha256(string.encode(encoding)).hexdigest()
    return hashlib.sha256((string + salt).encode(encoding)).hexdigest()
