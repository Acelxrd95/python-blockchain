import socket
import threading
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor


class Peer:
    def __init__(self):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5000
        self.BUFFER_SIZE = 1024
        self.threads = []
        self.peer_threads = []
        self.node = None
        self.peers = []

    def start(self):
        with ThreadPoolExecutor as executor:
            self.threads.append(executor.submit(self.start_server))
            self.threads.append(executor.submit(self.get_alive_peers))

    def start_server(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node.bind((self.HOST, self.PORT))
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
            if data.decode("utf-8") == "testalive":
                print("Received testalive from", addr)
            else:
                print(data.decode("utf-8"))

    def get_alive_peers(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to tracker server
        sock.connect((socket.gethostbyname(socket.gethostname()), 12345))
        # receive peer data from tracker server
        data = sock.recv(1024)
        # send self server data to tracker server
        sock.send(dumps((self.HOST, self.PORT)).encode())
        # close socket
        sock.close()
        self.peers = loads(data.decode())

    def broadcast(self):
        for peer in self.peers:
            if self.check_alive(peer[0], peer[1]):
                # connect to a peer on a new thread
                self.peer_threads.append(threading.Thread(target=self.sendmsg, args=(peer[0], peer[1])))
                self.peer_threads[-1].start()
        for peer in self.peer_threads:
            peer.join()

    def sendmsg(host, port):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to peer server
        sock.connect((host, port))
        sock.send(b"hello")
        # # receive peer data from peer server
        # data = sock.recv(1024)
        # # send self server data to peer server
        # sock.send(dumps((HOST, PORT)).encode())
        # print peer data
        # print(data.decode())
        # close socket
        sock.close()

    @staticmethod
    def check_alive(host, port):
        """
        Check if a host is alive.
        """
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sckt.connect((host, port))
            sckt.send(b"testalive")
            sckt.shutdown(2)
            return True
        except:
            return False
