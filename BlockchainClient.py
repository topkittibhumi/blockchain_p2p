from _thread import *
import threading
import time
import socket
import _thread
import sys
import json
import pickle
import datetime
import pprint
from Transaction import Transaction

cc = None

class BlockchainClient(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.args = args    
        self.HOST = "127.0.0.1"
        self.PORT_Server = self.args[0]
        self.neighbours = self.args[1]
        self.blockchain = self.args[2]
        self.lock = self.args[3]
        self.endlock = self.args[4]
        self.endlock.acquire()
    
    def run_myself(self, *args):
        global cc
        tmp = ""
        for a in args:
           tmp += a
        PORT_Server = int(tmp)
        while True:
            time.sleep(0.5)
            try:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a socket object
                    s.connect((self.HOST, PORT_Server))

                    while(1):
                    
                        # Parser for input command
                        commandContent = input("Please enter your command: ")
                        content = commandContent.split(" ")
                        commandType = content[0]

                        # Process command
                        
                        if commandType == 'tx':
                            requestContent = "tx"
                            
                            for i in range(len(content)):
                                if i >0:
                                    requestContent +=  "|" +str(content[i])

                            #if len()
                            #requestContent = f"tx|{str(content[1])}|{str(content[2])}"
                            """
                            trans = Transaction()
                            
                            if trans.validateTransaction(requestContent):
                                print(requestContent)
                            
                            else:
                                
                                print("Invalid transaction!")
                                continue
                                # sent to server?
                            """


                        elif commandType == 'pb':
                            if len(content) != 1:
                                print("Invalid arguments for pb request!")
                                continue
                            else:
                                requestContent = "pb"
                        elif commandType == 'cc':
                            if len(content) != 1:
                                print("Invalid arguments for cc request!")
                                continue
                            else:
                
                                requestContent = "cc"
                
        
                        else:
                            print("Please enter the supported request: ")
                            print("tx sender content -- [tx: command type of transaction] [sender of transaction] [content of transaction]")
                            print("pb -- [pb: command type of Print Blockchain]")
                            print("cc -- [cc: command type of Close Connection]")
                            continue
                        
                        # Create message for sending to Blockchain server
                        #mess_data = bytes(requestContent, encoding= 'utf-8')
                        mess_data = pickle.dumps(requestContent)
                        s.sendall(mess_data)

                        # Parse response from blockchain server
                        data_rev = s.recv(10000)
                        dataString = pickle.loads(data_rev)
                        if not data_rev:
                            pass
                        if commandType == 'pb':
                            pprint.pprint(dataString)
                        elif commandType == 'cc':
                            print(dataString)
                            self.endlock.release()

                            break
                        elif commandType =='tx':
                            print(dataString)

                        else:
                            pass

                    s.close()   
            except OSError as err:
                pass



    def run_others(self, *args):
        global cc
        tmp = ""
        for a in args:
           tmp += a
        PORT_Server = int(tmp)

        while True:
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
                    s.connect((self.HOST, PORT_Server))

                    while(1):
                        requestContent = "hb"
                        mess_data = pickle.dumps(requestContent)
                        s.sendall(mess_data)

                        data_rev = s.recv(10000)
                        try:
                            dataString = pickle.loads(data_rev)
                        except:
                            pass
                        if not data_rev:

                            pass
                        else:
                            blockchain_list = dataString[1] 
                            blockchain_pool = dataString[0]
                            flag = dataString[2]
                            self.lock.acquire()
                            if blockchain_list != None:

                                if len(blockchain_pool) > len(self.blockchain.blockchain):

                                    if flag == True:
                                        self.blockchain.pool = []

                                    elif len(blockchain_pool) > len(self.blockchain.pool):
                                        self.blockchain.pool = blockchain_pool.copy()
 
                                if len(blockchain_list) > len(self.blockchain.blockchain):
                                    self.blockchain.blockchain = blockchain_list.copy()
                                elif blockchain_list[-1]["index"] == self.blockchain.lastBlock()["index"]:
                                    if datetime.datetime.strptime(blockchain_list[-1]["timestamp"],"%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.strptime(self.blockchain.lastBlock()["timestamp"],"%Y-%m-%d %H:%M:%S.%f"):
                                        self.blockchain.blockchain = blockchain_list.copy()
                                
                                

                            else:

                                if flag == True:
                                    self.blockchain.pool = []

                                elif len(blockchain_pool) > len(self.blockchain.pool):
                                    self.blockchain.pool = blockchain_pool.copy()


                            tm_stmp = datetime.datetime.strptime(self.blockchain.lastBlock()["timestamp"],"%Y-%m-%d %H:%M:%S.%f")
                            for tx in self.blockchain.pool:
                                if datetime.datetime.strptime(tx[1],"%Y-%m-%d %H:%M:%S.%f") < tm_stmp:
                                    self.blockchain.pool.remove(tx)
                            self.lock.release()
                        time.sleep(0.5)
                
            except OSError as err:

                pass
    
    def run(self):
        ## start own client
        own_client_thread = threading.Thread(target = self.run_myself, args = (self.PORT_Server))
        own_client_thread.start()
    
        for server in self.neighbours:
            PORT_Server = server[1] 
            name = server[0]
            other_client_thread = threading.Thread(target = self.run_others, args = (PORT_Server))
            other_client_thread.start()
        
