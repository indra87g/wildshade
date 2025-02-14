from cryptography.fernet import Fernet
import hashlib
import hmac
import base64
import json

SECRET_KEY = b"very-secret"
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)


def generate_signature(data: str) -> str:
    """Generate HMAC signature for given data."""
    return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()


def encrypt_data(data: dict) -> str:
    """Encrypt data before saved to file."""
    json_data = json.dumps(data)
    encrypted = cipher.encrypt(json_data.encode())
    signature = generate_signature(json_data)
    return base64.urlsafe_b64encode(encrypted).decode() + "." + signature


def decrypt_data(encrypted_data: str) -> dict:
    """Decrypt and verify data."""
    try:
        encrypted_part, signature = encrypted_data.rsplit(".", 1)
        decrypted = cipher.decrypt(base64.urlsafe_b64decode(encrypted_part)).decode()

        if generate_signature(decrypted) != signature:
            raise ValueError("Data has been tampered!")

        return json.loads(decrypted)
    except Exception:
        return None
