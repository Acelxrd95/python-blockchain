from hashlib import sha256
from nacl.public import PrivateKey, Box
from nacl.signing import SigningKey
import json
import nacl.utils


class Wallet:
    def __init__(self, password):
        """
        Initializes a Wallet object with a zero balance
        :return: None
        """
        self.private_key = SigningKey.generate()
        self.public_key = self.private_key.verify_key
        self.balance = 0
        self.password_hash = sha256(password.encode()).hexdigest()

    def send(self, amount, recipient_public_key):
        """
        Sends an amount of money to a recipient
        :param amount: The amount of money to be sent
        :param recipient_public_key: The public key of the recipient
        :return: None
        """
        if self.balance >= amount:
            self.balance -= amount
            transaction = {"sender": self.public_key.key_to_bin(),
                           "recipient": recipient_public_key.key_to_bin(),
                           "amount": amount}
            signed = self.private_key.sign(json.dumps(transaction).encode())
            transaction["signature"] = signed.signature.hex()
            return transaction
        else:
            print("Not enough money to send")
