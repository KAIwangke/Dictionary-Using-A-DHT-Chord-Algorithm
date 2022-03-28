#!/usr/bin/env python

import sys
import glob
import time
sys.path.append('./gen-py/')
sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from PA2 import DictionaryDHT

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# connect with the supernode to get the node information
def connectSuperNode():
  superNodeAddress = 'kh4250-05.cselabs.umn.edu'
  port = 9091
  transport = TSocket.TSocket(superNodeAddress, port)

  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  client = DictionaryDHT.Client(protocol)

  # Connect!
  transport.open()

  # return the randomly chosen node with its ip and port
  # nodeInfo = "ip port"
  nodeInfo = client.GetNodeForClient()

  # Close!
  transport.close()

  # parse the nodeInfo
  temp = nodeInfo.split()
  ip = temp[0]
  port = temp[1]
  return ip, port

# TODO: need to track the nodes visited to handle the request
# connect with Node using thrift for setting words in the file
def setFile(fileName, nodeAddress, port):

  transport = TSocket.TSocket(nodeAddress, port)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DictionaryDHT.Client(protocol)
  # Connect!
  transport.open()

  file = open(fileName, "r")
  Lines = file.readlines()
  for line in lines:
    comp = line.split(":") # extract first two items, word, meaning
    word = comp[0]
    meaning = comp[1].rstrip()
    nodeID = client.Put(word, meaning) # client contact the node using thrift
    print("[ " + word + " is set on node with ID " + nodeID + " ]")
    print("Succeed to set: " + word + " " + meaning)

  # Close!
  transport.close()

# connect with Node using thrift for setting words
def setSingleWord(word, meaning, nodeAddress, port):

  transport = TSocket.TSocket(nodeAddress, port)

  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  client = DictionaryDHT.Client(protocol)

  # Connect!
  transport.open()

  nodeID = client.Put(word, meaning) # client contact the node using thrift
  print("[ " + word + " is set on node with ID " + nodeID + " ]")
  print("Succeed to set: " + word + " " + meaning)

  # Close!
  transport.close()

# connect with Node using thrift for getting word meaning
def getWord(word, nodeAddress, port):
  transport = TSocket.TSocket(nodeAddress, port)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DictionaryDHT.Client(protocol)

  # Connect!
  transport.open()

  meaning = client.Get(word) # client contact the node using thrift
  if (meaning != "NA"):
    print("Succeed to get the meaning of word: " + word)
    print("[ " + word + " : " + meaning + " ]")
  else:
    print("The word " + word + " doesn't exist in DHT.")

  # Close!
  transport.close()


# python3 Client.py set word meaning [0,1,2,3]
# python3 Client.py get word [0,1,2]
# python3 Client.py add filename [0,1,2]
if __name__ == '__main__':
    try:
      print("Starting client ...")
      # The client contact SuperNode only once when the client is running
      nodeAddress, port = connectSuperNode()
      operation = argv[1]
      if (operation == "add"):
        filename = sys.argv[2]
        setFile(filename, nodeAddress, port)
      elif (operation == "set"): 
          word = sys.argv[2]
          meaning = sys.argv[3]
          setSingleWord(word, meaning, nodeAddress, port)
      elif (operation == "get"): 
        word = sys.argv[2]
        getWord(word, nodeAddress, port)
      else:
        print("You input syntax is wrong. Please check User Document.")
    except Thrift.TException as tx:
      print('%s' % tx.message)

## The client is responsible for setting word and meanings to the system as well as 
## getting a meaning from the system with a word