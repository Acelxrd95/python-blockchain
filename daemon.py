from json import loads, dumps
from typing import Optional

import config
from block import Blockchain


class Daemon:
    def __init__(self, config_file):
        self.config = config_file
        self.logger = config_file.logger
        self.logger.info('Daemon initialized')
        self.blockchain: Optional[Blockchain] = None

    def run(self):
        self.logger.info('Daemon started')
        self.blockchain = self.load_blockchain()

    def stop(self):
        self.save_blockchain()
        self.logger.info('Daemon stopped')

    def load_blockchain(self):
        self.logger.info('Loading blockchain')
        with open("yeetcoin.json", "r") as f:
            data = loads(f.read())
        if data:
            blockchain = Blockchain(data['chain'])
        else:
            self.logger.info('Blockchain not found, creating new one')
            blockchain = Blockchain()
        self.logger.info('Blockchain loaded')
        return blockchain

    def save_blockchain(self):
        self.logger.info('Saving blockchain')
        with open("yeetcoin.json", "w") as f:
            data = {}
            for height, block in self.blockchain.chain.items():
                data.update({height: block.to_dict()})
            f.write(dumps(data, sort_keys=True))
        self.logger.info('Blockchain saved')


if __name__ == '__main__':
    daemon = Daemon(config)
    daemon.run()
    daemon.stop()
