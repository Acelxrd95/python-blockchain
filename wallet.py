from hashlib import sha256
from typing import Optional

import private as private
from ecdsa import SigningKey
from json import dumps, loads


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.password_hash = None

    @classmethod
    def from_private_key(cls, private_key, password):
        wallet = cls()
        wallet.private_key = SigningKey.from_pem(private_key)
        wallet.public_key = wallet.private_key.verifying_key.to_string().hex()
        return wallet

    @classmethod
    def generate(cls, password):
        wallet = cls()
        wallet.private_key = SigningKey.generate()
        wallet.public_key = wallet.private_key.verifying_key.to_string().hex()
        wallet.password_hash = sha256(password.encode()).hexdigest()
        return wallet
