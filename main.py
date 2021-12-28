# from wallet import Wallet
# from block import *
import time

from ecdsa import SigningKey
from hashlib import sha256, sha512
from random import randint, choice

# from pickle import dumps, loads
from json import dumps, loads

# yeetcoin = Blockchain()
# Alice = Wallet("Alice")
# Bob = Wallet("Bob")
#
# Alice.balance += 100
#
# transaction = Alice.send(50, Bob.public_key)
# yeetcoin.create_transaction(transaction["sender"], transaction["recipient"], transaction["amount"])
# transaction = Alice.send(10, Bob.public_key)
# yeetcoin.create_transaction(transaction["sender"], transaction["recipient"], transaction["amount"])
# yeetcoin.mine()
# print(yeetcoin)

# x = SigningKey.generate()
# print(x.to_string().hex())
# print(x.verifying_key.to_string().hex())

# b8dd4bacec2c023be474a3043e2cc0c6c1059dca5b0712a6
# 1bdd29e7a42ac1de57d7b342d8f9b20cd83e9ff094dad4b5d39d98534499584f14866922d355b341c33a5ecc1bff73c1

# signature = x.sign(transaction)
# print(signature)
# print(x.verifying_key.verify(signature, transaction))
# # x.verifying_key.
# print(loads(transaction.decode("utf-8")))


block = {
    "height": 0,
    "timestamp": 0,
    "proof": 0,
    "previous_hash": "0",
    "difficulty": 0,
    "confirmations": 0,
    "size": 0,
    "block_reward": 0,
    "fee_reward": 0,
    "miner": 0,
    "hash": 0,
    "transactions": [
        {
            "inputs": [{"address": "0", "value": 10}],
            "outputs": [
                {
                    "address": "6091dd2b91c627b042ccb3e3e4a28c2fdc4daf51b6aee1cdf671983b431604af0bf9102bdcda7e952e4fa9e583df072b",
                    "value": 10,
                    "trans_reference": "2543ac794cb0478c4608590f0cb18992f0be329c7aed00478455cb77e7effe04",
                }
            ],
            "fee": 0,
            "timestamp": 1640625932.233715,
            "hash": "2543ac794cb0478c4608590f0cb18992f0be329c7aed00478455cb77e7effe04",
            "signature": None,
        }
    ],
}
begin = time.time()
numbers = [_ for _ in range(0, 1000001)]
i = randint(0, 100000)
for _ in range(100000):
    i = choice(numbers)
    block.update({"nonce": i})
    _hash = sha256(dumps(block).encode("utf-8")).hexdigest()
    # print(_hash)
    if _hash[:4] == "000000":
        print(_hash)
        print("found", i)
        print(len(numbers))
        break
end = time.time() - begin
print(end)
