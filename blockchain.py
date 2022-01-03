from datetime import datetime
from datastructs import Queue
from block import Block
from transaction import Transaction


class Blockchain:
    """
    The main class for the blockchain.

    Attributes
    ----------
    chain : dict
        The chain containing all the valid blocks
    ether : Queue[Transaction]
        The list of transactions in the ether
    """

    def __init__(self, chain: dict) -> None:
        self.chain = chain
        self.ether = Queue()

    @classmethod
    def from_json(cls, json_data: dict) -> "Blockchain":
        """
        Create a blockchain from a json string

        Parameters
        ----------
        json_data : dict
            The json dictionary to create the blockchain from

        Returns
        -------
        Blockchain
            The blockchain instance created from the json string
        """
        chain = {height: Block.from_json(block) for height, block in json_data.items()}
        return cls(chain)

    @classmethod
    def generate(cls) -> "Blockchain":
        """
        Generate a new blockchain

        Returns
        -------
        Blockchain
            The new blockchain
        """
        chain = cls({})
        chain.genesis()
        return chain

    def to_dict(self) -> dict:
        """
        Convert the blockchain to a json string

        Returns
        -------
        str
            The blockchain converted to a json string
        """
        json_data = {height: block.to_dict() for height, block in self.chain.items()}
        return json_data

    @property
    def height(self) -> int:
        """
        Get the height of the blockchain

        Returns
        -------
        int
            The height of the blockchain
        """
        return len(self.chain)

    @property
    def last_block(self) -> Block:
        """
        Get the last block in the blockchain

        Returns
        -------
        Block
            The last block in the blockchain
        """
        return self.chain[str(self.height)]

    @property
    def block_reached(self) -> bool:
        """
        Check if the block target size has been reached

        Returns
        -------
        bool
            True if the block target size has been reached, False otherwise
        """
        if len(self.ether) >= 1:  # DEV: Change to 16 or 32
            return True
        return False

    def calc_reward(self) -> float:
        """
        Calculate the reward for the last block

        Returns
        -------
        float
            The reward for the last block
        """
        total_reward = 17179869183
        max_reward = 50
        reward = total_reward / self.height ** 2
        if reward > max_reward:
            reward = max_reward
        return reward

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the ether

        Parameters
        ----------
        transaction : Transaction
            The transaction to add to the ether
        """
        self.ether.enqueue(transaction)

    def add_block(self, block: Block) -> None:
        """
        Add a block to the blockchain

        Parameters
        ----------
        block : Block
            The block to add to the blockchain
        """
        self.chain.update({str(self.height + 1): block})

    def get_chaininfo(self) -> tuple[int, str]:
        """
        Get the chain information

        Returns
        -------
        tuple[int, str]
            The chain information
        """
        return self.height, self.last_block.hash

    def genesis(self) -> bool:
        """
        Creates the genesis block

        Returns
        -------
        bool
            True if the genesis block was created, False otherwise
        """
        if self.height == 0:
            tsx = Transaction()
            tsx.sender = "0"
            tsx.recipient = "612cc49836a4c01ca1f3fbe71972fac29c79e654ac60a48c132d0c5f69cd84cc6997a7e8d4d1173462fb2a6372ea7150"
            tsx.amount = 1000
            tsx.nonce = 0
            tsx.timestamp = datetime.now().timestamp()

            genesis = Block.create(
                "0",
                "0",
                0,
                0,
                [tsx],
            )
            genesis.hash_block()
            self.add_block(genesis)
            return True
        else:
            return False
