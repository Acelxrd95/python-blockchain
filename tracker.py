import socket
from logging import getLogger, StreamHandler, Formatter, INFO
from json import loads, dumps
from peer import Peer

check_alive = Peer.check_alive

# create logger
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(INFO)
logger.addHandler(handler)
# client list
clients = []
# define connection info
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
s.settimeout(30)
logger.info("Tracker started on %s:%s" % (HOST, PORT))
while True:
    try:
        conn, addr = s.accept()
    except socket.timeout:
        continue
    logger.info(f"Connection from {str(addr)}")
    # check that clients are alive
    for client in clients:
        if not check_alive(client[0], client[1]):
            logger.info(f"Client {str(client)} is dead")
            # remove client from dictionary
            clients.pop(clients.index(client))
    # send alive clients to client
    conn.send(dumps(clients).encode())
    try:
        client = conn.recv(1024)
        if client:
            clients.append(loads(client.decode()))
    except socket.timeout:
        logger.info(f"Client {str(addr)} timed out")
    else:
        # announce_client(client)
        conn.close()
    # append client to list
    logger.info(f"Clients: {str(clients)}")
    logger.info("---------------------------------")
