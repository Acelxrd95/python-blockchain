from dataclasses import dataclass
from datetime import datetime
from json import dumps

from ecdsa import SigningKey


@dataclass
class Transaction:
    """
    Transaction class

    Attributes
    ----------
    sender : str
        Sender of the transaction
    recipient : str
        Recipient of the transaction
    amount : int
        Amount of the transaction
    timestamp: datetime
        Timestamp of the transaction
    fee: int
        Fee of the transaction
    data: dict
        Extra data of the transaction
    signature : str
        Signature of the transaction
    """

    sender: str = None
    recipient: str = None
    amount: float = None
    timestamp: datetime = None
    fee: int = None
    signature: str = None
    data: dict = None

    @property
    def size(self):
        """returns the size of the transaction in bytes"""
        return len(dumps(self.data))

    def sign(self, private_key: SigningKey):
        """
        signs the transaction with the given private key

        Parameters
        ----------
        private_key :
            the private key to sign the transaction with
        """
        self.signature = private_key.sign(self.data)
