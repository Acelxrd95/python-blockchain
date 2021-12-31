from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, chain: dict) -> None:
        self.chain = chain
        # TODO: change to priority queue
        self.ether = []

    @classmethod
    def from_json(cls, json_data) -> "Blockchain":
        """
        Create a blockchain from a json string

        Parameters
        ----------
        json_data : str
            The json string to create the blockchain from

        Returns
        -------
        Blockchain
            The blockchain created from the json string

        TODO
        ----
        - Process Json string
        """
        chain = {}
        return cls(chain)

    @classmethod
    def generate(cls) -> "Blockchain":
        """
        Generate a new blockchain

        Returns
        -------
        Blockchain
            The new blockchain

        TODO
        ----
        - Add genesis block
        """
        chain = {}
        return cls(chain)

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
        return self.chain[-1]

    @property
    def block_reached(self) -> bool:
        """
        Check if the block target size has been reached

        Returns
        -------
        bool
            True if the block target size has been reached, False otherwise
        """
        if len(self.ether) >= 16:
            return True
        return False

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the ether

        Parameters
        ----------
        transaction : Transaction
            The transaction to add to the ether
        """
        self.ether.append(transaction)

    def add_block(self, block: Block) -> None:
        """
        Add a block to the blockchain

        Parameters
        ----------
        block : Block
            The block to add to the blockchain
        """
        self.chain.update({self.height + 1: block})
