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
        data = {key: val for key, val in self.__dict__.items() if val is not None and key != "signature"}
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
        print(self.to_json())
        self.signature = private_key.sign(self.to_json().encode(), sigencode=sigencode_string).hex()

    def verify(self):
        """
        verifies the transaction with the given public key

        Parameters
        ----------
        public_key : str
            the public key to verify the transaction with
        """
        print(self.to_json())
        return VerifyingKey.from_string(bytearray.fromhex(self.sender)).verify(
            bytearray.fromhex(self.signature), self.to_json().encode(), sigdecode=sigdecode_string
        )


# x.to_string().hex()
# 'c9784d344ae4f812fc4719476874277e4fec6dbbe3b23cd4'
# x.verifying_key.to_string().hex()
# 'a34fa1904ecc6535dfe7f778cda72896cc5594437d729f85990503ff08727d67c7fcb29e8079a456af1b300db643dce1'
# {
#     "amount": 2,
#     "fee": 0,
#     "recipient": "a34fa1904ecc6535dfe7f778cda72896cc5594437d729f85990503ff08727d67c7fcb29e8079a456af1b300db643dce1",
#     "sender": "612cc49836a4c01ca1f3fbe71972fac29c79e654ac60a48c132d0c5f69cd84cc6997a7e8d4d1173462fb2a6372ea7150",
#     "timestamp": 1641047959.261593,
# }
