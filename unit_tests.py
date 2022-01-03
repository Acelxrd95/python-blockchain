import unittest
from daemon import *
from config import *

d = Daemon(logger)
d.start()


class MyTestCase(unittest.TestCase):
    def test_signature(self):

        transaction = Transaction()
        transaction.sender = d.wallet.public_key
        transaction.recipient = "0"
        transaction.amount = 1000
        transaction.timestamp = datetime.now().timestamp()
        transaction.sign(d.wallet.private_key)
        self.assertTrue(transaction.verify())

    def test_proof_of_work(self):
        block = Block.create(
            d.wallet.public_key,
            "0",
            0,
            0,
            [Transaction()],
        )
        self.assertTrue(block.proof_of_work(lambda: False))
        self.assertEqual(
            block.header.hash[: block.header.difficulty], "0" * block.header.difficulty
        )

    def test_tracker(self):
        self.assertTrue(d.peer.get_alive(), "Please make sure the tracker is alive")


if __name__ == "__main__":
    unittest.main()
