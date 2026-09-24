import hashlib
import secrets

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_token():
    return secrets.token_hex(24)
