from _thread import *
import threading
import time
import socket
import _thread
import sys
import json
import hashlib
import time
import pickle

class BlockchainMiner(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args    
        self.HOST = "127.0.0.1"
        #print(self.args)
        self.PORT_Server = self.args[0]
        self.port = args[1]
        self.blockchain = args[1]
        self.lock = self.args[2]
        self.current_proof = None

   
    def run(self):
        #print("HELLO TOBY")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.HOST, int(self.PORT_Server)))

                while True:
                    time.sleep(3)

                    requestContent = "gp"
                    mess_data = pickle.dumps(requestContent)
                    s.sendall(mess_data)
                    #gets the last block proof
                    data_rev = s.recv(10000)
                    self.current_proof = pickle.loads(data_rev)

                    self.lock.acquire()
                    tmp = self.blockchain.pool
                    self.lock.release()
   
                    if len(tmp) == 5:
  
                        new_proof = self.proof_of_work()

                        requestContent = f"up|{new_proof}"
                        mess_data = pickle.dumps(requestContent)
                        s.sendall(mess_data)

                        data_rev = s.recv(10000)
    


        except OSError as err:
            pass

        pass
    def proof_of_work(self):
        
        new_proof = 0
        self.lock.acquire()
        tmp = self.blockchain.pool
        tmp_lastBlock = self.blockchain.lastBlock()
        self.lock.release()
        while len(tmp) == 5:

            if self.blockchain.calculateHash(int(new_proof)**2 - int(tmp_lastBlock["proof"])**2)[:2] == '00':
                return new_proof
            new_proof += 1
        
        return None
