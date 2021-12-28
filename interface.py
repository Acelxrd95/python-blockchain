# from daemon import Daemon
# from wallet import Wallet
# import config
#
# daemon = Daemon(config)
#
# daemon.run()
# wallet = Wallet(daemon.blockchain)
# wallet.start()
# wallet.send(5, "1bdd29e7a42ac1de57d7b342d8f9b20cd83e9ff094dad4b5d39d98534499584f14866922d355b341c33a5ecc1bff73c1")
# daemon.blockchain.create_block()
# wallet.balance()
# print(wallet.total_balance)
# wallet.stop()
# daemon.stop()

import eel

eel.init("web")
eel.conslog("Hello")
eel.start("index.html", size=(None, 716), close_callback=lambda *args: exit())
# eel.start("index.html", size=(None, 747), close_callback=lambda *args: exit())
