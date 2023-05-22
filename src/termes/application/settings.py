import os
import secrets

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite+aiosqlite://:memory:"
PASSWORD_HASH_SALT = os.getenv("PASSWORD_HASH_SALT") or secrets.token_hex(32)
TOKEN_HASH_SALT = os.getenv("TOKEN_HASH_SALT") or secrets.token_hex(32)
SESSION_LIFETIME = int(os.getenv("SESSION_LIFETIME") or 86400)
SESSION_TOKEN_LENGTH = int(os.getenv("SESSION_TOKEN_LENGTH") or 32)
