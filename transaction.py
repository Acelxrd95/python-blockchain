from dataclasses import dataclass
from datetime import datetime
from json import dumps
import inspect

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

    amount: float = None
    data: dict = None
    fee: int = None
    recipient: str = None
    sender: str = None
    signature: str = None
    timestamp: datetime = None

    @property
    def size(self):
        """returns the size of the transaction in bytes"""
        return len(dumps(self.data))

    @classmethod
    def from_json(cls, json_data: dict):
        """
        creates a transaction from a json string

        Parameters
        ----------
        json_data : dict
            the json string to create the transaction from

        Returns
        -------
        Transaction
            the transaction created from the json string
        """
        return cls(
            **{
                key: (json_data[key] if val.default == val.empty else json_data.get(key, val.default))
                for key, val in inspect.signature(Transaction).parameters.items()
            }
        )

    def sign(self, private_key: SigningKey):
        """
        signs the transaction with the given private key

        Parameters
        ----------
        private_key :
            the private key to sign the transaction with
        """
        self.signature = private_key.sign(self.data)
