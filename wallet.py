from hashlib import sha256
from typing import Optional

from ecdsa import SigningKey
from json import dumps, loads
from block import Transaction


class Wallet:
    def __init__(self, blockchain):
        """
        Initializes a new wallet with no addresses
        :return: None
        """
        self.addresses = []
        self.total_balance = 0
        self.blockchain = blockchain


    def start(self):
        print('Loading wallet addresses')
        with open("wallet.json", "r") as f:
            data = loads(f.read())
        if data:
            for address in data:
                self.addresses.append(Address(address))
        else:
            print('Wallet addresses not found, creating new address')
            self.addresses.append(Address())
        print('Wallet addresses loaded')

    def stop(self):
        print('Saving wallet addresses')
        with open("wallet.json", "w") as f:
            data = []
            for address in self.addresses:
                data.append({
                    "private_key": address.private_key.to_string().hex(),
                    "password": address.password_hash,
                })
            f.write(dumps(data, sort_keys=True))
        print('Blockchain saved')

    def balance(self):
        """
        Returns the balance of the wallet
        :return: The balance of the wallet
        """

        for block in self.blockchain:
            for trans in block.transactions:
                for inpt in trans.inputs:
                    for adr in self.addresses:
                        if adr.public_key == inpt.address:
                            adr.balance -= inpt



    def send(self, amount, recipient_public_key):
        """
        Sends an amount of money to a recipient
        :param amount: The amount of money to be sent
        :param recipient_public_key: The public key of the recipient
        :return: None
        """
        if self.balance() >= amount:
            transactions = []
            for adr in self.addresses:
                if adr.balance >= amount:
                    for trans in adr.prev_transactions:
                        pass  # if prev_transactions
            # self.balance -= amount
            # transaction = {"sender": self.public_key.to_string().hex(),
            #                "recipient": recipient_public_key.to_string().hex(),
            #                "amount": amount}
            # signed = self.private_key.sign(json.dumps(transaction).encode())
            # transaction["signature"] = signed.signature.hex()
            # return transaction
        else:
            print("Not enough money to send")

    def create_address(self):
        self.addresses.append(Address(blockchain=self.blockchain))

class Address:
    def __init__(self, backup: Optional[dict] = None, blockchain=None):
        """
        Initializes an Address object
        :return: None
        """
        if backup is None:
            self.private_key = SigningKey.generate()
            self.public_key = self.private_key.verifying_key
            self.password_hash = sha256("demo123".encode()).hexdigest()
        else:
            self.private_key = SigningKey.from_string(bytes(backup['private_key']))
            self.public_key = self.private_key.verifying_key
            self.password_hash = backup['password']
        self.prev_transactions: list[Transaction] = self.get_transactions()
        self.total_balance = 0

if __name__ == "__main__":
    wallet = Wallet("")
    wallet.start()
    wallet.stop()
