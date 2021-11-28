from datetime import datetime
from hashlib import sha256
from json import dumps


class Blockchain:
    def __init__(self):
        self.chain = []
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

    def __repr__(self):
        return dumps(self.chain)

    def create_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount sent
        :return:
        """
        self.ether.append(Transaction(sender, recipient, amount))

    def create_block(self):
        block = Block(self.height + 1, self.ether, self.chain[-1].hash)
        self.ether = []
        current_block = block
        self.chain.append(block)


class Block:
    def __init__(self, height, transactions, previous_hash):
        self.height = height
        self.timestamp = 0
        self.proof = 0
        self.previous_hash = previous_hash
        self.transactions = []
        self.difficulty = 0
        self.confirmations = 0
        self.size = 0
        self.block_reward = 0
        self.fee_reward = 0
        self.miner = 0
        self.hash = 0

    def generate_hash(self):
        block_string = dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = 0
        self.recipient = 0
        self.sent_amount = 0
        self.timestamp = datetime.now()

    @property
    def fee(self):
        return self.sent_amount / 0.1

    @property
    def received_amount(self):
        return self.sent_amount - self.fee

    @property
    def size(self):
        return 0

    @property
    def hash(self):
        return 0

    def sign(self, private_key):
        pass
