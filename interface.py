from daemon import Daemon
from wallet import Wallet


daemon = Daemon()

daemon.run()
wallet = Wallet(daemon.blockchain)
daemon.stop()
