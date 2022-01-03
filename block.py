import random
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pickle import dumps

from datastructs import Array
from transaction import Transaction


@dataclass
class BlockHeader:
    """
    BlockHeader

    Attributes
    ----------
    previous_hash : str
        The hash of the previous block in the chain.
    miner_address : str
        The address of the miner who mined the block.
    difficulty: int
        The difficulty of the block.
    timestamp : int
        The time the block was mined.
    height: int
        The height of the block.
    nonce : int
        The nonce used to generate the hash.
    block_size: int
        The number of transactions in the block.
    hash : str
        The hash of the block.
    """

    previous_hash: str = None
    miner_address: str = None
    difficulty: int = None
    timestamp: int = None
    height: int = None
    nonce: int = None
    block_size: int = None
    hash: str = None

    def __str__(self) -> str:
        """Returns the string representation of the block header."""
        return "BlockHeader: " + str(self.__dict__)


class Block:
    """
    The block class is used to create a block in the blockchain.

    Attributes
    ----------
    header : BlockHeader
        The block header.
    transactions : list[Transaction]
        The list of transactions in the block.
    """

    def __init__(self, header: BlockHeader, transactions: list[Transaction]) -> None:
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
        transactions = Array(
            Transaction,
            len(json_data["transactions"]),
            [Transaction.from_json(t) for t in json_data["transactions"]],
        )
        return cls(header, transactions)

    @classmethod
    def create(
        cls,
        previous_hash: str,
        miner_address: str,
        difficulty: int,
        height: int,
        transactions: Array,
    ) -> "Block":
        """
        Create a new block

        Parameters
        ----------
        previous_hash : str
            The hash of the previous block in the chain.
        miner_address : str
            The address of the miner who mined the block.
        difficulty: int
            The difficulty of the block.
        height: int
            The height of the block.
        transactions : list[Transaction]
            The list of transactions in the block.

        Returns
        -------
        Block
            The block instance created
        """
        header = BlockHeader()
        header.previous_hash = previous_hash
        header.miner_address = miner_address
        header.difficulty = difficulty
        header.timestamp = datetime.now().timestamp()
        header.height = height
        transactions = Array(Transaction, len(transactions), transactions)
        return cls(header, transactions)

    @property
    def hash(self) -> str:
        """Returns the hash of the block."""
        return self.header.hash

    def to_dict(self) -> dict:
        """Returns the block as a dict"""
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

    def hash_block(self) -> None:
        """Calculate the hash of the block header"""
        self.header.hash = sha256(dumps(self.header.__dict__)).hexdigest()

    def proof_of_work(self, isfound: callable) -> None:
        """
        Proof of work algorithm.

        Parameters
        ----------
        isfound : callable
            A function that returns True if the block is found.
        """
        start, end = 0, 1000000
        while True:
            nonce_list = [i for i in range(start, end)]
            for i in nonce_list:
                if isfound():
                    return False
                n = random.choice(nonce_list)
                self.header.nonce = n
                self.hash_block()
                if (
                    self.header.hash[: self.header.difficulty]
                    == "0" * self.header.difficulty
                ):
                    return True
            else:
                start = end
                end = end * 2
