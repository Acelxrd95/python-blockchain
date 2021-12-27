from daemon import Daemon
from wallet import Wallet
import config

daemon = Daemon(config)

daemon.run()
wallet = Wallet(daemon.blockchain)
wallet.start()
wallet.balance()
print(wallet.total_balance)
wallet.stop()
daemon.stop()
