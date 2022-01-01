from dataclasses import dataclass
from datetime import datetime
from json import dumps
import inspect

from ecdsa import SigningKey, VerifyingKey


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

    def to_dict(self, include_signature: bool = False) -> dict:
        """
        returns the transaction as a dict

        Parameters
        ----------
        include_signature : bool
            whether to include the signature in the dict

        Returns
        -------
        dict
            the transaction as a dict
        """
        data = {
            key: (val if val.default == val.empty else getattr(self, key))
            for key, val in inspect.signature(Transaction).parameters.items()
        }
        if include_signature:
            data["signature"] = self.signature
        return data

    def to_json(self, include_signature: bool = False) -> str:
        """
        returns the transaction as a json string

        Parameters
        ----------
        include_signature : bool
            whether to include the signature in the json string

        Returns
        -------
        str
            the transaction as a json string
        """
        return dumps(self.to_dict(include_signature))

    def sign(self, private_key: SigningKey):
        """
        signs the transaction with the given private key

        Parameters
        ----------
        private_key :
            the private key to sign the transaction with
        """
        self.signature = private_key.sign(self.to_json())

    def verify(self, public_key: str):
        """
        verifies the transaction with the given public key

        Parameters
        ----------
        public_key : str
            the public key to verify the transaction with
        """
        return VerifyingKey.from_string(public_key).verify(self.signature, self.to_json())
