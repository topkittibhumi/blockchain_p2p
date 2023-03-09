from _thread import *
import threading
import time
import datetime
import socket
import _thread
import json 
import hashlib
from Blockchain import Blockchain
from Transaction import Transaction
import pickle

IP = "127.0.0.1" # '' -> localhost

cc = None

class BlockchainServer(threading.Thread):
    
    def __init__(self, *args):
        threading.Thread.__init__(self)
        #print("hello from server")
        self.args = args
        self.proof = 0
        self.PORT_Server = int(self.args[0])
        self.blockchain = self.args[1]
        self.lock = self.args[2]
        self.hb_counter = 0
    #     self._stop_event = threading.Event()
        
    # def stop(self):
    #     self._stop_event.set()
    def run(self):
        global cc
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                s.bind((IP, self.PORT_Server)) # Bind to the port
                s.listen(5)
                while True:
                    # to avoid deadlock, counter can be used here: if counter == 6 or cc = 'cc':
    
                    c, addr = s.accept()
                    _thread.start_new_thread(self.serverHandler,(c, addr))
                    if cc == 'cc':
                        
                        break
                s.close()
                return
        except:
            pass

   


    def serverHandler(self, c , addr):
        while(True):

            global cc


            # Parsing and processing data from client
            try:
                data_rev = c.recv(10000)
            except:
                pass
            try:
                dataString = pickle.loads(data_rev)
            except:
                pass
            typeRequest = dataString[:2]
            clientData = ""
            # Handle tx request
            if typeRequest == 'tx':
                transaction = Transaction()
                transactionContent = transaction.validateTransaction(dataString)
                if transactionContent != None:
                    self.blockchain.addTransaction((transactionContent, str(datetime.datetime.now())))
                    clientData = "Accepted"
                else:
                    clientData = "Rejected"

            # Handle pb request
            elif typeRequest == 'pb':
                clientData = str(self.blockchain.blockchain)

            # Handle cc request
            elif typeRequest == 'cc':
                cc = 'cc'
                clientData = "Connection closed!"
            
            elif typeRequest == 'gp':

                    

                clientData = 100


            elif typeRequest == 'up':
                #TODO
                proof_to_check = dataString.split("|")[1]
               
                if self.blockchain.calculateHash(int(proof_to_check)**2 - int(self.blockchain.lastBlock()["proof"])**2)[:2] == "00":
                    clientData = "Reward"
                    #print("reward to miner")
                    self.lock.acquire()
                    if len(self.blockchain.pool) == 5:
                        self.blockchain.newBlock(int(proof_to_check), self.blockchain.lastBlock()["currentHash"])
                        self.blockchain.pool = []
                        # notify all other client except our client
                        #clientData.append(self.blockchain.blockchain)
                    self.lock.release()    
                    time.sleep(0.1)
                else:
                    clientData = "No Reward"
                
            elif typeRequest == 'hb':

                self.hb_counter += 1
                self.lock.acquire()
                if self.hb_counter % 10 == 0:
                    clientData = (self.blockchain.pool, self.blockchain.blockchain, self.blockchain.flag)
                else:
                    clientData = (self.blockchain.pool, None, self.blockchain.flag)
                
                if self.blockchain.flag == True:
                    self.blockchain.pool = []
                    self.blockchain.flag = False
                

                self.lock.release()
                time.sleep(0.1)
                


            clientData = pickle.dumps(clientData)
            try:
                c.sendall(clientData)
            except:
                pass


            if typeRequest == 'cc':
                break
        c.close()
        return
    
