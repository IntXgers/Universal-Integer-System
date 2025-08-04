# universal_integer_system/src/transports/security.py
import os
import json
from cryptography.fernet import Fernet


class SetUpEncryption:
    """Encryption and security setup"""
    def __init__ (self):
        key = os.environ.get ('ENCRYPTION_KEY')
        if not key:
            raise ValueError ("Set ENCRYPTION_KEY env var")
        self.fernet = Fernet (key)

    def encrypt_json (self,data: dict) -> bytes:
        return self.fernet.encrypt (json.dumps (data).encode ())

    def decrypt_json (self,encrypted: bytes) -> dict:
        return json.loads (self.fernet.decrypt (encrypted))
