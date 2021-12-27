# from wallet import Wallet
# from block import *
from ecdsa import SigningKey

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

x = SigningKey.generate()
transaction = dumps({"sender": "Alice", "recipient": "Bob", "amount": 10}).encode("utf-8")
signature = x.sign(transaction)
print(signature)
print(x.verifying_key.verify(signature, transaction))
# x.verifying_key.
print(loads(transaction.decode("utf-8")))
