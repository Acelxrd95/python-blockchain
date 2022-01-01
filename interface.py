from daemon import Daemon
import json

# TODO: add error messages

import eel
from config import logger

daemon = Daemon(logger)
daemon.start()


@eel.expose
def get_balance():
    return daemon.balance()


@eel.expose
def get_history():
    return daemon.wallet_history()


@eel.expose
def get_chain():
    return json.dumps(daemon.blockchain.to_dict())


@eel.expose
def send_crypto(recipient, amount, fee=0):
    return daemon.send(recipient, int(amount), int(fee))


@eel.expose
def mine(state):
    if state:
        daemon.start_mining(eel.logger, eel.enable_mining_button)
    else:
        daemon.stop_mining(eel.logger, eel.enable_mining_button)


def close():
    daemon.stop()
    exit()


eel.init("web")
eel.start("index.html", size=(None, None), close_callback=lambda *args: close())
