from hashlib import sha256
from json import dumps
import datetime

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
        # TODO: add mining logic here
        self.create_block()

    def get_transaction(self, block_id, transaction_hash):
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
        block = Block(self.ether, list(self.chain.values())[-1].hash)
        self.ether = []
        self.chain.update({block.height: block})

    def create_genesis_block(self):
        inpt = TransItem("0", 10, None)
        outpt = TransItem(
            "6091dd2b91c627b042ccb3e3e4a28c2fdc4daf51b6aee1cdf671983b431604af0bf9102bdcda7e952e4fa9e583df072b", 10, "0"
        )
        transact = Transaction([inpt], [outpt], 0)
        block = Block([transact], "0")
        self.chain.update({self.height: block})


class Block:
    def __init__(self, transactions=None, previous_hash=None, data=None):
        if data is None:
            if transactions is None or previous_hash is None:
                raise ValueError("transactions and previous_hash are required")
            self.previous_hash = previous_hash
            self.transactions = transactions
            self.timestamp = datetime.datetime.now()
            self.difficulty = 0  # TODO: calculate difficulty
            self.size = None  # TODO: calculate size
            self.fee_reward = 0
            for trans in self.transactions:
                self.fee_reward += trans.fee
            self.block_reward = 0  # TODO: Calculate block reward
            self.miner = None  # TODO: figure out the miner
            self.hash = None
        else:
            self.load_block(data)

    def load_block(self, data):
        self.previous_hash = data["previous_hash"]
        self.transactions = [Transaction(data=transaction) for transaction in data["transactions"]]
        self.timestamp = datetime.datetime.fromtimestamp(data["timestamp"])
        self.difficulty = data["difficulty"]
        self.size = data["size"]
        self.block_reward = data["block_reward"]
        self.fee_reward = data["fee_reward"]
        self.miner = data["miner"]
        self.hash = data["hash"]

    def generate_hash(self):
        serialized_transactions = [transaction.serialize() for transaction in self.transactions]
        block_string = dumps(
            {
                "timestamp": self.timestamp.timestamp(),
                "previous_hash": self.previous_hash,
                "transactions": serialized_transactions,
                "difficulty": self.difficulty,
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
            "timestamp": self.timestamp.timestamp(),
            "previous_hash": self.previous_hash,
            "difficulty": self.difficulty,
            "size": self.size,
            "block_reward": self.block_reward,
            "fee_reward": self.fee_reward,
            "miner": self.miner,
            "hash": self.hash,
            "transactions": serialized_transactions,
        }
