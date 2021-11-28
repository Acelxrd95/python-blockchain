from wallet import Wallet
from template import *

yeetcoin = Blockchain()
Alice = Wallet("Alice")
Bob = Wallet("Bob")

Alice.balance += 100

transaction = Alice.send(50, Bob.public_key)
yeetcoin.create_transaction(transaction["sender"], transaction["recipient"], transaction["amount"])
transaction = Alice.send(10, Bob.public_key)
yeetcoin.create_transaction(transaction["sender"], transaction["recipient"], transaction["amount"])
yeetcoin.mine()
print(yeetcoin)