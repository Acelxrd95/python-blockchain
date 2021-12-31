from hashlib import sha256
from typing import Optional

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
        wallet.private_key = private_key
        wallet.public_key = private_key.public_key
        return wallet

    @classmethod
    def generate(cls, password):
        wallet = cls()
        wallet.private_key = SigningKey.generate()
        wallet.public_key = wallet.private_key.verifying_key
        wallet.password_hash = sha256(password.encode()).hexdigest()
        return wallet
