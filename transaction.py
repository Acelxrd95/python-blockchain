import inspect
from dataclasses import dataclass
from datetime import datetime
from json import dumps

from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigencode_string, sigdecode_string


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
    data: dict
        Extra data of the transaction
    signature : str
        Signature of the transaction
    """

    amount: float = None
    data: dict = None
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
                key: (
                    json_data[key]
                    if val.default == val.empty
                    else json_data.get(key, val.default)
                )
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
            key: val
            for key, val in self.__dict__.items()
            if val is not None and key != "signature"
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

    def sign(self, private_key: SigningKey) -> None:
        """
        signs the transaction with the given private key

        Parameters
        ----------
        private_key :
            the private key to sign the transaction with
        """
        self.signature = private_key.sign(
            self.to_json().encode(), sigencode=sigencode_string
        ).hex()

    def verify(self) -> bool:
        """
        verifies the transaction with the given public key

        Returns
        -------
        bool
            True if the transaction is valid, False otherwise
        """
        return VerifyingKey.from_string(bytearray.fromhex(self.sender)).verify(
            bytearray.fromhex(self.signature),
            self.to_json().encode(),
            sigdecode=sigdecode_string,
        )
