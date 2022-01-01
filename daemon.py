import json
import os
import time
import random
from datetime import datetime
from logging import RootLogger
from threading import Thread
from typing import Optional, Any

from block import Block
from blockchain import Blockchain
from peer import Peer, Protocol, preset_protocols
from transaction import Transaction
from wallet import Wallet


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
        self.validator = None
        self.logger = logger
        self.blockchain: Optional[Blockchain] = None
        self.wallet: Optional[Wallet] = None
        self.peer: Optional[Peer] = None
        self.mining = False
        self.mining_thread = None

    def ismining(self) -> bool:
        """
        Returns if the daemon is mining

        Returns
        -------
        bool
            True if the daemon is mining, False otherwise
        """
        return self.mining

    def start(self) -> None:
        """This method is used to run the daemon"""
        self.load()
        self.peer = Peer(self.blockchain)
        self.update_blockchain()
        self.logger.info("Daemon started")

    def stop(self) -> None:
        """This method is used to stop the daemon"""
        self.save()
        self.logger.info("Daemon stopped")

    def load(self) -> None:
        """Loads the blockchain and the wallet"""
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
        if notfound:
            # if it doesn't, create a new blockchain
            self.blockchain = Blockchain.generate()
            self.logger.info("Blockchain was not found or was empty, a new one was generated")
        self.logger.info("Loading wallet")
        # check if the file key.pem exists in data folder
        notfound = True
        if os.path.isfile("data/key.pem"):
            with open("data/key.pem", "rb") as f:
                data = f.read()
                # check if the file key.pem is empty, if not load the wallet
                if data:
                    notfound = False
                    self.wallet = Wallet.from_private_key(data)
                    self.logger.info("Wallet loaded")
        if notfound == True:
            # if it doesn't, create a new wallet
            self.wallet = Wallet.generate()
            self.logger.info("Wallet was not found or was empty, a new one was generated")

    def save(self):
        """Saves the blockchain and the wallet"""
        self.logger.info("Saving blockchain")
        with open("data/blockchain.json", "w") as f:
            json.dump(self.blockchain.to_dict(), f)
        self.logger.info("Saving wallet")
        with open("data/key.pem", "wb") as f:
            f.write(self.wallet.private_key.to_pem())

    def balance(self) -> float:
        """
        Returns the balance of the wallet

        Returns
        -------
        float
            The balance of the wallet
        """
        return self.get_balance(self.wallet.public_key)

    def get_balance(self, public_key: str) -> float:
        balance = 0
        for height, block in self.blockchain.chain.items():
            for transaction in block.transactions:
                if transaction.sender == public_key:
                    balance -= transaction.amount
                if transaction.recipient == public_key:
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
        transaction.timestamp = datetime.now().timestamp()
        transaction.sign(self.wallet.private_key)
        self.blockchain.add_transaction(transaction)
        self.logger.info("Transaction sent")
        return True

    def create_block(self) -> Block:
        block = Block.create(
            self.blockchain.last_block.hash,
            self.wallet.public_key,
            self.calculate_difficulty(),
            self.blockchain.height + 1,
            self.blockchain.ether,
        )
        self.blockchain.ether = []
        return block

    def blockfound(self, height: int) -> bool:
        if self.blockchain.height == height:
            return True
        else:
            return False

    def mine(self) -> bool:
        """
        Mines the current block

        Returns
        -------
        bool
            True if the block was mined, False otherwise
        """
        block = self.create_block()
        for transaction in block.transactions:
            if not self.validate_transaction(transaction):
                block.transactions.remove(transaction)
        if len(block.transactions) == 0:
            self.logger.info("No transactions to mine")
            return False
        nonce = block.proof_of_work(lambda: self.blockfound(block.header.height))
        if nonce:
            block = self.reward(block, self.wallet.public_key)
            prot = preset_protocols["new-block"]
            prot.data = block.to_dict()
            self.peer.broadcast(prot)
            self.blockchain.add_block(block)
            return True
        else:
            return False

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Validates a transaction

        Parameters
        ----------
        transaction : Transaction
            The transaction to validate

        Returns
        -------
        bool
            True if the transaction is valid, False otherwise
        """
        if transaction.amount < 0:
            return False
        if transaction.amount + transaction.fee > self.get_balance(transaction.sender):
            return False
        if not transaction.verify():
            return False
        return True

    def reward(self, block, miner_address: str):
        reward_tsx = Transaction()
        reward_tsx.sender = "0"
        reward_tsx.recipient = miner_address
        reward_tsx.amount = sum([transaction.fee for transaction in block.transactions]) + self.blockchain.calc_reward()
        reward_tsx.fee = 0
        reward_tsx.timestamp = datetime.now().timestamp()
        reward_tsx.signature = ""
        block.transactions.insert(0, reward_tsx)
        return block

    def wallet_history(self):
        """
        Returns all the transactions associated with this wallet

        Returns
        -------
        list
            A list of all the transactions associated with this wallet
        """
        transactions = []
        for height, block in self.blockchain.chain.items():
            for transaction in block.transactions:
                tsx = [
                    transaction.sender,
                    transaction.recipient,
                    transaction.amount,
                    transaction.fee,
                    transaction.timestamp,
                ]
                if transaction.sender == self.wallet.public_key:
                    transactions.append(tsx)
                if transaction.recipient == self.wallet.public_key:
                    transactions.append(tsx)
        return transactions

    def start_mining(self, js_logger: callable, enbl_btn: callable):
        js_logger("Starting mining")
        self.mining = True
        enbl_btn(True)
        self.mining_thread = Thread(target=self.mineloop, args=([lambda: self.ismining(), js_logger]))
        self.mining_thread.start()

    def stop_mining(self, js_logger: callable, enbl_btn: callable):
        js_logger("Stopping mining")
        enbl_btn(False)
        self.mining = False
        self.mining_thread.join()

    def mineloop(self, isrunning: callable, js_logger: callable):
        while isrunning():
            self.update_blockchain()
            if self.blockchain.block_reached:
                if self.mine():
                    js_logger("Block mined")
            else:
                x = 5  # DEV increase time
                js_logger(f"Required blocksize still not reached. Sleeping for {x} seconds")
                time.sleep(x)

    def calculate_difficulty(self) -> int:
        """
        Calculate the mining difficulty

        Returns
        -------
        int
            The mining difficulty
        """
        if self.blockchain.height % 10 == 0 or self.blockchain.height == 0:
            return round(len(self.peer.peers) / 100) if len(self.peer.peers) > 100 else 1
        else:
            return self.blockchain.last_block.header.difficulty

    def update_blockchain(self) -> None:
        self.peer.get_longest_chain(self.blockchain.get_chaininfo())


if __name__ == "__main__":
    from config import logger

    daemon = Daemon(logger)
    daemon.start()
    print(daemon.wallet.public_key)
    daemon.save()
    daemon.stop()
