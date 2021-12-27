from hashlib import sha256
from typing import Optional

from ecdsa import SigningKey
from json import dumps, loads
from block import Blockchain
from transaction import Transaction, TransItem


class Wallet:
    def __init__(self, blockchain: Blockchain):
        """
        Initializes a new wallet with no addresses
        :return: None
        """
        self.is_running = False
        self.private_key = None
        self.public_key = None
        self.password_hash = None
        self.prev_out_transactions: list[tuple[str, str]] = []
        self.prev_in_transactions: list[tuple[str, str]] = []
        self.total_balance = 0
        self.blockchain = blockchain

    def start(self):
        print("Loading wallet address")
        with open("wallet.json", "r") as f:
            data = loads(f.read())
        if data:
            # transform backup private_key to bytes from hex
            self.private_key = SigningKey.from_string(bytes.fromhex(data["private_key"]))
            self.public_key = self.private_key.verifying_key
            self.password_hash = data["password"]
        else:
            print("Wallet address not found, creating new address")
            self.private_key = SigningKey.generate()
            self.public_key = self.private_key.verifying_key
            self.password_hash = sha256("demo123".encode()).hexdigest()
        print("Wallet address loaded")
        self.is_running = True

    def stop(self):
        print("Saving wallet addresses")
        with open("wallet.json", "w") as f:
            data = {
                "private_key": self.private_key.to_string().hex(),
                "password": self.password_hash,
            }
            f.write(dumps(data, sort_keys=True))
        print("Wallet saved")
        self.is_running = False

    def balance(self):
        """
        Returns the balance of the wallet
        :return: The balance of the wallet
        """
        if not self.is_running:
            print("Wallet is not running")
            return
        for height, block in self.blockchain.chain.items():
            for trans in block.transactions:
                for inpt in trans.inputs:
                    if self.public_key.to_string().hex() == inpt.address:
                        self.total_balance -= inpt.value
                        self.prev_out_transactions.append((height, trans.hash))
                for outp in trans.outputs:
                    if self.public_key.to_string().hex() == outp.address:
                        self.total_balance += outp.value
                        self.prev_in_transactions.append((height, trans.hash))
                self.total_balance += self.total_balance

    def send(self, amount, recipient_public_key, fee=0):
        """
        Sends an amount of money to a recipient
        :param fee:
        :param amount: The amount of money to be sent
        :param recipient_public_key: The public key of the recipient
        :return: None
        """
        if not self.is_running:
            print("Wallet is not running")
            return
        if self.balance() >= amount:
            transactions = []
            amnt_from_trans = 0
            outputs = []
            if self.total_balance >= amount:
                for height, trans in self.prev_in_transactions:
                    transaction = self.blockchain.get_transaction(height, trans)
                    transactions.append(transaction)
                    # amnt_from_trans += transaction.get_adr_output(adr.public_key.to_string().hex())
                    outputs.append(transaction.get_adr_output(self.public_key.to_string().hex()))
                    if amnt_from_trans >= amount:
                        inputs = [TransItem(output.address, output.value, trans) for output in outputs]
                        if amnt_from_trans == amount:
                            outputs = [TransItem(recipient_public_key, None, amount)]
                        else:
                            outputs = [
                                TransItem(recipient_public_key, None, amount),
                                TransItem(self.public_key.to_string().hex(), None, (amnt_from_trans - amount)),
                            ]
                        t = Transaction(inputs, outputs, fee)
                        t.sign_transaction(self.private_key)
                        self.blockchain.add_transaction(t)
        else:
            print("Not enough money to send")
