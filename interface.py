from daemon import Daemon
import json

# TODO: add error messages

import eel
from config import logger

daemon = Daemon(logger)
daemon.start()


@eel.expose
def get_balance():
    """Get the balance of the wallet"""
    return daemon.balance()


@eel.expose
def get_history():
    """Gets the history of the wallet"""
    return daemon.wallet_history()


@eel.expose
def get_chain():
    """Get the chain of the blockchain"""
    return json.dumps(daemon.blockchain.to_dict())


@eel.expose
def send_crypto(recipient, amount):
    """Send crypto to a recipient"""
    return daemon.send(recipient, int(amount))


@eel.expose
def mine(state):
    """Mine a block"""
    if state:
        daemon.start_mining(eel.logger, eel.enable_mining_button)
    else:
        daemon.stop_mining(eel.logger, eel.enable_mining_button)


def close():
    """Close the daemon"""
    daemon.stop()
    exit()


eel.init("web")
eel.start("index.html", size=(None, None), close_callback=lambda *args: close())
