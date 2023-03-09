from Blockchain import Blockchain
from Transaction import Transaction
from BlockchainServer import BlockchainServer
from BlockchainClient import BlockchainClient
from BlockchainMiner import BlockchainMiner
import sys
import time
import threading
import os

class BlockchainPeer():
    def __init__(self, args):
        self.PORT_Server = args[0]
        self.neighbours = []
        self.config_txt = args[1]
        self.readfile()
        self.blockchain = Blockchain()
        self.lock = threading.Lock()

    def readfile(self):
        f = open(self.config_txt, 'r')
        f.readline()
        for line in f.readlines():
            line = line.split(" ")
            self.neighbours.append((line[0], line[1]))

        f.close()
        
    def createThread(self):
        endlock = threading.Lock()

        server_thread = BlockchainServer(self.PORT_Server, self.blockchain, self.lock)
        server_thread.start()
        client_thread = BlockchainClient(self.PORT_Server, self.neighbours, self.blockchain, self.lock, endlock)
        client_thread.start()
        miner_thread = BlockchainMiner(self.PORT_Server ,self.blockchain, self.lock)
        miner_thread.start()
        time.sleep(1)
        endlock.acquire()
        endlock.release()

        os.kill(os.getpid(), 9)


    def run(self):
        self.createThread()


b = BlockchainPeer([sys.argv[2], sys.argv[3]])
b.run()

