from datetime import datetime
from typing import Optional
import json
import os
from logging import RootLogger
from typing import Optional

from blockchain import Blockchain
from wallet import Wallet
from peer import Peer
from transaction import Transaction
from block import Block


class Daemon:
    """
    Daemon class

    This class is used to interact with the wallet and the blockchain


        wallet (Wallet): The wallet of the node
        blockchain (Blockchain): The blockchain of the node
    """

    def __init__(self, logger: [RootLogger]) -> None:
        """
        Initialize the daemon

        Parameters
        ----------
        logger : [RootLogger]
            The logger of the node
        """
        self.logger = logger
        self.blockchain: Optional[Blockchain] = None
        self.wallet: Optional[Wallet] = None
        self.peer: Optional[Peer] = None

    def run(self) -> None:
        """
        This method is used to run the daemon

        TODO
        ----
        - Start the daemon
        - Load the blockchain
        - Load the wallet
        """
        self.logger.info("Daemon started")
        self.load()

    def stop(self) -> None:
        """
        This method is used to stop the daemon

        TODO
        ----
        - Stop the daemon
        - Save the blockchain
        - Save the wallet
        """
        self.logger.info("Daemon stopped")

    def load(self) -> None:
        """
        Loads the blockchain and the wallet

        TODO
        ----
        - Load the blockchain
        - Load the wallet
        """
        self.logger.info("Loading blockchain")
        # check if the file blockchain.json exists in data folder
        notfound = True
        if os.path.isfile("data/blockchain.json"):
            with open("data/blockchain.json", "r") as f:
                data = json.load(f)
                # check if the file blockchain.json is empty, if not load the blockchain
                if data:
                    notfound = False
                    self.blockchain = Blockchain.from_json(data)
                    self.logger.info("Blockchain loaded")
        if notfound == True:
            # if it doesn't, create a new blockchain
            self.blockchain = Blockchain.generate()
            self.logger.info("Blockchain was not found or was empty, a new one was generated")
        # TODO: check if blockchain is uptodate

        self.logger.info("Loading wallet")
        # check if the file key.pem exists in data folder
        notfound = True
        if os.path.isfile("data/key.pem"):
            with open("data/key.pem", "r") as f:
                data = f.read()
                # check if the file key.pem is empty, if not load the wallet
                if data:
                    notfound = False
                    # DEBUG change the password to something else
                    self.wallet = Wallet.from_private_key(data, "demo123")
                    self.logger.info("Wallet loaded")
        if notfound == True:
            # if it doesn't, create a new wallet
            self.wallet = Wallet.generate("demo123")
            self.logger.info("Wallet was not found or was empty, a new one was generated")

    def save(self):
        """
        Saves the blockchain and the wallet

        TODO
        ----
        - Save the blockchain
        - Save the wallet
        """
        self.logger.info("Saving blockchain")
        with open("data/blockchain.json", "w") as f:
            json.dump(self.blockchain.to_json(), f)
        self.logger.info("Saving wallet")
        with open("data/key.pem", "w") as f:
            f.write(self.wallet.private_key)

    def balance(self) -> float:
        """
        Returns the balance of the wallet

        Returns
        -------
        float
            The balance of the wallet
        """
        balance = 0
        for height, block in self.blockchain.chain:
            for transaction in block.transactions:
                if transaction.sender == self.wallet.public_key:
                    balance -= transaction.amount
                if transaction.recipient == self.wallet.public_key:
                    balance += transaction.amount
        return balance

    def send(self, recipient: str, amount: float, fee: float = 0) -> bool:
        """
        Sends a transaction to the recipient

        Parameters
        ----------
        recipient : str
            The recipient of the transaction
        amount : float
            The amount of the transaction
        fee : float
            The fee for the transaction

        Returns
        -------
        bool
            True if the transaction was sent, False otherwise
        """
        if self.balance() < amount + fee:
            self.logger.info("Not enough balance")
            return False
        transaction = Transaction()
        transaction.sender = self.wallet.public_key
        transaction.recipient = recipient
        transaction.amount = amount
        transaction.fee = fee
        transaction.timestamp = datetime.now()
        transaction.sign(self.wallet.private_key)
        self.blockchain.add_transaction(transaction)
        self.logger.info("Transaction sent")
        return True

    def create_block(self) -> Block:
        block = Block.create(
            self.blockchain.last_block.hash,
            self.wallet.public_key,
            0,
            self.blockchain.height + 1,
            self.blockchain.ether,
        )
        self.blockchain.ether = []
        return block

    def mine(self) -> bool:
        """
        Mines the current block

        Returns
        -------
        bool
            True if the block was mined, False otherwise

        TODO: implement proof of stake algorithm
        """
        # block = self.create_block()
        # if block.mine(self.blockchain.difficulty):
        #     self.blockchain.add_block(block)
        #     self.logger.info("Block mined")
        #     return True
        # else:
        #     self.logger.info("Block not mined")
        #     return False
        self.blockchain.add_block(self.create_block())
        return True
