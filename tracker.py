import logging
import socket

# create logger
logger = logging.getLogger("tracker")
logger.setLevel(logging.DEBUG)
# client dictionary
clients = {}
# define connection info
HOST = "0.0.0.0"
PORT = 12345

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
s.settimeout(30)
while True:
    try:
        conn, addr = s.accept()
    except socket.timeout:
        continue
    # logger.info(f"Connection from {str(addr)}")
