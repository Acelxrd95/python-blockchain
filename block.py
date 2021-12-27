from hashlib import sha256
from json import dumps

import inputs as inputs

from transaction import Transaction, TransItem


class Blockchain:
    def __init__(self, chain: dict = None):
        self.chain = {}
        if chain is None:
            self.create_genesis_block()
        else:
            self.load_chain(chain)
        self.ether = []
        self.current_block = None

    @property
    def height(self):
        return len(self.chain)

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def block_reached(self):
        if len(self.ether) >= 16:
            return True
        return False

    def load_chain(self, chain):
        for height, block in chain.items():
            self.chain.update({height: Block(data=block)})

    def serialize(self):
        serialized_chain = {}
        for _, block in self.chain.items():
            serialized_chain.update({block.height: block.serialize()})
        return {
            "chain": serialized_chain,
        }

    def is_valid(self):
        for i in range(len(self.chain) - 1):
            if self.chain[i].hash != self.chain[i + 1].previous_hash:
                return False
        return True

    def mine(self):
        """
        This function serves as an interface to add transactions to the blockchain after
        the user adds them
        :return:
        """
        self.create_block()

    def get_transaction(self, transaction_hash, block_id):
        block = self.chain[block_id]
        for transaction in block.transactions:
            if transaction.hash == transaction_hash:
                return transaction
        return None

    def __repr__(self):
        return dumps(self.chain)

    def add_transaction(self, transaction: Transaction):
        """
        Create a new transaction to go into the next mined Block
        :param transaction: <Transaction>
        :return:
        """
        self.ether.append(transaction)

    def create_block(self):
        block = Block(self.height + 1, self.ether, self.chain[-1].hash)
        self.ether = []
        self.chain.update({block.height: block})

    def create_genesis_block(self):
        inpt = TransItem("0", 10, "0")
        outpt = TransItem(
            "55125ef59d79ad15db027b35c0b6644ef68c022fc58153176695e64632daf0eb7a9f1d666df202f2da7facbaea21cdd8", 10, "0"
        )
        transact = Transaction([inpt], [outpt], 0)
        block = Block(0, [transact], "0")
        self.chain.update({block.height: block})


class Block:
    def __init__(self, height=None, transactions=None, previous_hash=None, data=None):
        if data is None:
            if height is None or transactions is None or previous_hash is None:
                raise ValueError("height, transactions and previous_hash are required")
            self.previous_hash = previous_hash
            self.transactions = transactions
            self.height = height
            self.timestamp = 0
            self.proof = 0
            self.difficulty = 0
            self.confirmations = 0
            self.size = 0
            self.block_reward = 0
            self.fee_reward = 0
            self.miner = 0
            self.hash = 0
        else:
            self.load_block(data)

    def load_block(self, data):
        self.previous_hash = data["previous_hash"]
        self.transactions = [Transaction(data=transaction) for transaction in data["transactions"]]
        self.height = data["height"]
        self.timestamp = data["timestamp"]
        self.proof = data["proof"]
        self.difficulty = data["difficulty"]
        self.confirmations = data["confirmations"]
        self.size = data["size"]
        self.block_reward = data["block_reward"]
        self.fee_reward = data["fee_reward"]
        self.miner = data["miner"]
        self.hash = data["hash"]

    def generate_hash(self):
        serialized_transactions = [transaction.serialize() for transaction in self.transactions]
        block_string = dumps(
            {
                "height": self.height,
                "timestamp": self.timestamp,
                "proof": self.proof,
                "previous_hash": self.previous_hash,
                "transactions": serialized_transactions,
                "difficulty": self.difficulty,
                "confirmations": self.confirmations,
                "size": self.size,
                "block_reward": self.block_reward,
                "fee_reward": self.fee_reward,
                "miner": self.miner,
                "hash": self.hash,
            }
        )
        return sha256(block_string.encode()).hexdigest()

    def serialize(self):
        serialized_transactions = [transaction.serialize() for transaction in self.transactions]
        return {
            "height": self.height,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "transactions": serialized_transactions,
            "difficulty": self.difficulty,
            "confirmations": self.confirmations,
            "size": self.size,
            "block_reward": self.block_reward,
            "fee_reward": self.fee_reward,
            "miner": self.miner,
            "hash": self.hash,
        }
