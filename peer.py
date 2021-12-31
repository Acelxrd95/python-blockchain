import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from json import loads, dumps
from typing import Any, Optional


@dataclass
class Protocol:
    type: str
    data: Any

    def __str__(self):
        return dumps(self.__dict__)

    def __bytes__(self):
        return dumps(self.__dict__).encode()

    @staticmethod
    def from_str(s):
        return Protocol(**loads(s))

    @staticmethod
    def from_bytes(b):
        return Protocol.from_str(b.decode())


preset_protocols = {
    "ping": Protocol(type="ping", data=None),
    "pong": Protocol(type="pong", data=None),
    "message": Protocol(type="message", data=None),
    "get_chain": Protocol(type="get_chain", data=None),
    "chain": Protocol(type="chain", data=None),
    "get_peers": Protocol(type="get_peers", data=None),
}


class Peer:
    def __init__(self, port: int = 5000, buffer_size: int = 1024) -> None:
        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = port
        self.buffer_size: int = buffer_size
        self.threads: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=10)
        self.peers: list[tuple[str, int]] = []
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self) -> None:
        with self.threads as executor:
            executor.submit(self.listen)
            executor.submit(self.get_alive)

    def listen(self) -> None:
        """
        Listen for incoming connections

        TODO
        ----
        - Manage protocols sent by other peers
        """
        self.node.bind((self.host, self.port))
        self.node.listen()
        self.node.settimeout(30)
        while True:
            try:
                conn, addr = self.node.accept()
            except socket.timeout:
                continue
            print("Connected by", addr)
            data = conn.recv(1024)
            # if first part of data is 'testalive'
            if Protocol.from_bytes(data).type == preset_protocols["ping"].type:
                print("Received print from", addr)
                conn.send(bytes(preset_protocols["pong"]))
            else:
                pass

    def get_alive(self) -> None:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to tracker server
        sock.connect((socket.gethostbyname(socket.gethostname()), 12345))
        # receive peer data from tracker server
        data = sock.recv(1024)
        # send self server data to tracker server
        sock.send(dumps((self.host, self.port)).encode())
        # close socket
        sock.close()
        self.peers = loads(data.decode())

    def broadcast(self, message: Protocol) -> None:
        """
        Broadcast a message to all peers

        Parameters
        ----------
        message : str
            Message to broadcast
        """
        for peer in self.peers:
            if self.check_alive(peer[0], peer[1]):
                # connect to a peer on a new thread
                with self.threads as executor:
                    pass
        for peer in self.peer_threads:
            peer.join()

    @staticmethod
    def check_alive(host: str, port: int) -> bool:
        """
        Check if a node is alive.

        Parameters
        ----------
        host : str
            Hostname of the node
        port : int
            Port of the node

        Returns
        -------
        bool
            True if node is alive, False otherwise
        """
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to peer
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            return False
        # send testalive message
        sock.send(bytes(preset_protocols["ping"]))
        # receive response
        data = sock.recv(1024)
        # close socket
        sock.close()
        # if response is 'alive' return True else False
        return data.decode("utf-8") == "alive"

    def get_latest_chain(self) -> None:
        """
        Get the latest chain from all peers

        Returns
        -------
        list
            List of blocks
        """
        for peer in self.peers:
            if self.check_alive(peer[0], peer[1]):
                pass
            pass

    def get_chain(self, host: str, port: int) -> Optional[list]:
        """
        Get the latest chain from a peer

        Parameters
        ----------
        host : str
            Hostname of the peer
        port : int
            Port of the peer

        Returns
        -------
        list
            List of blocks
        """
        # connect to peer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            # send getchain protocol
            prtcl = preset_protocols["get_chain"]
            sock.send(bytes(prtcl))
            # receive chain
            data = Protocol.from_bytes(sock.recv(1024))
        if data.type == "chain":
            return data.data
        return None
