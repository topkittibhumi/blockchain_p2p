import hashlib
import json
from time import time
import datetime

class Blockchain():
    def  __init__(self):
        self.blockchain = []
        self.pool = []
        self.pool_limit = 5 

        self.newBlock(previousHash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)
        self.flag = False
        self.sentflag = False
        self.flushFlag = 0

    def newBlock(self, proof, previousHash = None):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transaction': self.pool.copy(),
            'proof': proof,
            'previousHash': previousHash or self.calculateHash(self.blockchain[-1]),

            'currentHash': None
        }
        block['currentHash'] = self.currentHash(block)
        self.pool = []
        self.flag = True
        self.blockchain.append(block)


    def lastBlock(self):
        return self.blockchain[-1]

    def calculateHash(self, data):
        dataObject = json.dumps(data, sort_keys=True)
        dataString = dataObject.encode()
        rawHash = hashlib.sha256(dataString)
        hexHash = rawHash.hexdigest()
        return hexHash

    def currentHash(self, block):
        data = str(self.previousHash(block))

        for transaction in block["transaction"]:
            data += str(transaction)
        
        data += str(block["proof"])

        hash = self.calculateHash(data)
        return hash

    def previousHash(self, block):
        return block["previousHash"]
    
    def addTransaction(self, transaction):
        if len(self.pool) < self.pool_limit:
            self.pool.append(transaction)

