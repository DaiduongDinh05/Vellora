from app.config import settings
from cryptography.fernet import Fernet

f = Fernet((settings.FERNET_KEY).encode())

def encrypt_address(address: str) -> str:
    if not address:
        return ""
    return f.encrypt(address.encode()).decode()

def decrypt_address(token: str) -> str:
    if not token:
        return ""
    return f.decrypt(token.encode()).decode()