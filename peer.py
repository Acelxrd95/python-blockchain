import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from json import loads, dumps
from typing import Any


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
    "new-block": Protocol(type="new-block", data=None),
    "new-transaction": Protocol(type="new-transaction", data=None),
    "chain-info": Protocol(type="chain-info", data=None),
    "get-chain": Protocol(type="get-chain", data=None),
    "get-peers": Protocol(type="get-peers", data=()),
    "get-transactions": Protocol(type="get-transactions", data=None),
    "ack": Protocol(type="ack", data=None),
}


class Peer:
    def __init__(self, blockchain, port: int = 5000, buffer_size: int = 1024) -> None:
        self.host: str = socket.gethostbyname(socket.gethostname())
        self.port: int = port
        self.buffer_size: int = buffer_size
        self.thread_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=10)
        self.peers: list[tuple[str, int]] = []
        self.tracker_addr = (self.host, 12345)  # DEV: add real host address
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.blockchain = blockchain

    def start(self) -> None:
        with self.thread_executor as executor:
            executor.submit(self.get_alive)
            executor.submit(self.listen)

    def listen(self) -> None:
        """Listen for incoming connections"""
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
            self.process_protocol(conn, addr, data)

    def process_protocol(self, conn, addr, data: bytes) -> Any:
        prot = Protocol.from_bytes(data)
        if prot.type == "ping":
            conn.send(bytes(preset_protocols["ack"]))
        elif prot.type == "new-block":
            self.blockchain.add_block(prot.data)
            conn.send(bytes(preset_protocols["ack"]))
        elif prot.type == "new-transaction":
            self.blockchain.add_transaction(prot.data)
            conn.send(bytes(preset_protocols["ack"]))
        elif prot.type == "chain-info":
            if prot.data:
                return prot.data, addr
            else:
                prot = preset_protocols["chain-info"]
                prot.data = self.blockchain.get_chaininfo()
                conn.send(bytes(prot))
        elif prot.type == "get-chain":
            prot = preset_protocols["get-chain"]
            prot.data = self.blockchain.to_dict()
            conn.send(bytes(prot))
        elif prot.type == "get-peers":
            self.peers = prot.data
        elif prot.type == "get-transactions":
            prot = preset_protocols["get-trans"]
            prot.data = self.blockchain.ether
            conn.send(bytes(prot))

    def broadcast(self, message: Protocol) -> Any:
        """
        Broadcast a message to all peers

        Parameters
        ----------
        message : Protocol
            Message to broadcast
        """
        data = []
        futures = []
        with self.thread_executor as executor:
            for peer in self.peers:
                if self.check_alive(peer[0], peer[1]):
                    # connect to a peer on a new thread
                    futures.append(executor.submit(self.sendmsg, peer[0], peer[1], message))
        for future in futures:
            data.append(future.result())
        return data

    def sendmsg(self, host: str, port: int, message: Protocol) -> Any:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(30)
            try:
                addr = (host, port)
                sock.connect(addr)
                # send message
                sock.send(bytes(message))
                response = sock.recv(self.buffer_size)
            except ConnectionRefusedError:
                pass
            except socket.timeout:
                pass
            else:
                return self.process_protocol(sock, addr, response)

    def get_alive(self) -> None:
        """Send a "get-peers" message to the tracker"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to tracker server
        sock.connect(self.tracker_addr)
        # send get-peers message
        prot = preset_protocols["get-peers"]
        prot.data = (self.host, self.port)
        # send self server data to tracker server
        sock.send(bytes(prot))
        # receive peer data from tracker server
        data = sock.recv(1024)
        self.process_protocol(sock, self.tracker_addr, data)
        # close socket
        sock.close()
        self.peers = loads(data.decode())

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

    def get_longest_chain(self, chain_info) -> list:
        """
        Get the latest chain from all peers

        Returns
        -------
        list
            List of blocks
        """
        data = self.broadcast(preset_protocols["chain-info"])
        longest_chain = []
        if data:
            for info, address in data:
                if info["height"] > chain_info["height"]:
                    longest_chain = info, address
        if longest_chain:
            chain = self.sendmsg(longest_chain[1][0], longest_chain[1][1], preset_protocols["chain"])
            return chain
