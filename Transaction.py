import re

class Transaction():
    def __init__(self, *args):
        self.args = args

    def validateTransaction(self, transaction):
        senderValidation = False 
        contentValidation = False
        pipeCounter = 0
        for c in transaction:
            if c == "|":
                pipeCounter += 1

        if pipeCounter > 2:
            return None
        
        transaction_split = str(transaction).split("|")
        sender = transaction_split[1]
        content = transaction_split[2]
        

        # Match sender Regex
        pattern = re.compile("[a-z]{4}[0-9]{4}")
        if pattern.fullmatch(sender) is not None:
            senderValidation = True

        # Content Validation
        
        if not (len(content) > 70):
            contentValidation = True
        
        # Validation of transaction
        if senderValidation == True and contentValidation == True:
            #print("Valid Transaction")
            return transaction
        else:
            #print("Invalid Transaction")
            return None