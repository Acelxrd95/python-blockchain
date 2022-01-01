import random
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pickle import dumps

from transaction import Transaction


@dataclass
class BlockHeader:
    previous_hash = None
    miner_address = None
    difficulty = None
    timestamp = None
    height = None
    nonce = None
    block_size = None
    hash = None

    def __str__(self):
        return "BlockHeader: " + str(self.__dict__)


class Block:
    def __init__(self, header: BlockHeader, transactions: list[Transaction]):
        self.header: BlockHeader = header
        self.transactions: list[Transaction] = transactions

    @classmethod
    def from_json(cls, json_data: dict) -> "Block":
        """
        Create a block from a json dict
        Parameters
        ----------
        json_data : dict
            The json dict to create the block from

        Returns
        -------
        Block
            The block instance created from the json dict
        """
        header = BlockHeader()
        header.previous_hash = json_data["previous_hash"]
        header.miner_address = json_data["miner_address"]
        header.difficulty = json_data["difficulty"]
        header.timestamp = json_data["timestamp"]
        header.height = json_data["height"]
        header.hash = json_data["hash"]
        header.nonce = json_data["nonce"]
        header.block_size = json_data["block_size"]
        transactions = [Transaction.from_json(t) for t in json_data["transactions"]]

        return cls(header, transactions)

    @classmethod
    def create(
        cls, previous_hash: str, miner_address: str, difficulty: int, height: int, transactions: list[Transaction]
    ):
        """Create a new block"""
        header = BlockHeader()
        header.previous_hash = previous_hash
        header.miner_address = miner_address
        header.difficulty = difficulty
        header.timestamp = datetime.now().timestamp()
        header.height = height
        transactions = transactions
        # header.size = len(transactions)
        return cls(header, transactions)

    @property
    def hash(self):
        return self.header.hash

    def to_dict(self):
        transactions = []
        return {
            "previous_hash": self.header.previous_hash,
            "miner_address": self.header.miner_address,
            "difficulty": self.header.difficulty,
            "timestamp": self.header.timestamp,
            "height": self.header.height,
            "hash": self.header.hash,
            "nonce": self.header.nonce,
            "block_size": self.header.block_size,
            "transactions": [t.to_dict() for t in self.transactions],
        }

    def hash_block(self):
        """Calculate the hash of the block header"""
        self.header.hash = sha256(dumps(self.header.__dict__)).hexdigest()

    def proof_of_work(self, isfound: callable):
        start, end = 0, 1000000
        while True:
            nonce_list = [i for i in range(start, end)]
            for i in nonce_list:
                if isfound():
                    return False
                n = random.choice(nonce_list)
                self.header.nonce = n
                self.hash_block()
                if self.header.hash[: self.header.difficulty] == "0" * self.header.difficulty:
                    return True
            else:
                start = end
                end = end * 2
