from hashlib import sha256
from json import dumps
from datetime import datetime

class Input:
    def __init__(self, address, value, trans_reference):
        self.address = address
        self.value= value
        self.trans_reference = trans_reference


class Output:
    def __init__(self, address, value, trans_reference):
        self.address = address
        self.value= value
        self.trans_reference = trans_reference


class Transaction:
    def __init__(self, inputs: Input, outputs: Output, fee):
        self.inputs = inputs
        self.outputs = outputs
        self.fee = fee
        self.timestamp = datetime.now()
        self.hash = self.generate_hash()

    @property
    def size(self):
        return 0

    @property
    def total_output(self):
        # yeetcoin
        return 0

    @property
    def total_input(self):
        return sum([input.amount for input in self.inputs])

    def generate_hash(self):
        block_string = dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
