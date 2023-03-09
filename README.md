# Blockchain

How to run Programe:

1. open 3 terminals
2. run python3 BlockchainPeer.py 1 6000 config_A.txt on terminal 1
3. run python3 BlockchainPeer.py 2 6001 config_B.txt on terminal 2
4. run python3 BlockchainPeer.py 3 6002 config_C.txt on terminal 3

How to test:

1. do "pb" in every terminal, each terminal should print 1 block.
1. do "tx abcd1234 abc" 5 times in any terminal
2. wait 5 seconds
3. do "pb" in every terminal, each terminal should print 2 blocks. 
4. do "cc" in any terminal, that peer should terminate.


If the length of the blockchain is not synchronous, please allow some time for the hb message to be broadcasted. Sometimes mutexes can be held up and the hb mutex might be clogged thus not updating the network of a longer blockchain.