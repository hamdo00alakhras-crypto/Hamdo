import hashlib
import secrets
import base64


def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"pbkdf2_sha256${salt}${base64.b64encode(hashed).decode('utf-8')}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, salt, hash_b64 = hashed_password.split('$')
        if algorithm != 'pbkdf2_sha256':
            return False
        stored_hash = base64.b64decode(hash_b64)
        computed_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return secrets.compare_digest(stored_hash, computed_hash)
    except Exception:
        return False
