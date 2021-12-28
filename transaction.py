from datetime import datetime
from hashlib import sha256
from json import dumps


class TransItem:
    def __init__(self, address, value, trans_reference=None):
        self.address = address
        self.value = value
        self.trans_reference = trans_reference

    def serialize(self):
        if self.trans_reference is None:
            return {
                "address": self.address,
                "value": self.value,
            }
        return {
            "address": self.address,
            "value": self.value,
            "trans_reference": self.trans_reference,
        }


class Transaction:
    def __init__(self, inputs: list[TransItem] = None, outputs: list[TransItem] = None, fee=None, data=None):
        if data is None:
            if inputs is None or outputs is None or fee is None:
                raise ValueError("Transaction must have inputs, outputs, and fee")
            self.inputs = inputs
            self.outputs = outputs
            self.fee = fee
            self.signature = None
            self.timestamp = datetime.now()
            self.hash = self.generate_hash()
            for outpt in self.outputs:
                outpt.trans_reference = self.hash
        else:
            self.load_transaction(data)

    @property
    def size(self):
        return 0

    @property
    def total_output(self):
        return sum([outpt.value for outpt in self.outputs])

    @property
    def total_input(self):
        return sum([inpt.value for inpt in self.inputs])

    def get_adr_output(self, address):
        for outpt in self.outputs:
            if outpt.address == address:
                return outpt

    def sign_transaction(self, private_key):
        self.signature = private_key.sign(self.hash.encode()).hex()

    def load_transaction(self, data):
        self.inputs = [TransItem(*list(inpt.values())) for inpt in data["inputs"]]
        self.outputs = [TransItem(*list(outpt.values())) for outpt in data["outputs"]]
        self.fee = data["fee"]
        self.timestamp = datetime.fromtimestamp(data["timestamp"])
        self.hash = data["hash"]
        self.signature = data["signature"]

    def serialize(self):
        return {
            "inputs": [inpt.serialize() for inpt in self.inputs],
            "outputs": [outpt.serialize() for outpt in self.outputs],
            "fee": self.fee,
            "timestamp": self.timestamp.timestamp(),
            "hash": self.hash,
            "signature": self.signature,
        }

    def generate_hash(self):
        block_string = dumps(
            {
                "inputs": [inpt.serialize() for inpt in self.inputs],
                "outputs": [outpt.serialize() for outpt in self.outputs],
                "fee": self.fee,
                "timestamp": self.timestamp.timestamp(),
            }
        )
        return sha256(block_string.encode()).hexdigest()
