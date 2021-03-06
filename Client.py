#!/usr/bin/env python

import sys
import glob
import time
sys.path.append('./gen-py/')
sys.path.insert(0, glob.glob('../lib/py/build/lib*')[0])

from PA2 import Node
from PA2 import SuperNode

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
# from thrift.server import TServer

# connect with the supernode to get the node information
def connectSuperNode():
  superNodeAddress = 'localhost'
  port = 9091
  transport = TSocket.TSocket(superNodeAddress, port)

  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  client = SuperNode.Client(protocol)

  # Connect!
  transport.open()

  # return the randomly chosen node with its ip and port
  # nodeInfo = "ip port"
  nodeInfo = client.GetNodeForClient()

  # Close!
  transport.close()
  if (nodeInfo == "Empty"):
    return "Empty"

  return nodeInfo

# TODO: need to track the nodes visited to handle the request
# connect with Node using thrift for setting words in the file
def setFile(fileName, nodeAddress, port):

  transport = TSocket.TSocket(nodeAddress, port)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = Node.Client(protocol)
  # Connect!
  transport.open()

  file = open(fileName, "r")
  Lines = file.readlines()
  for line in lines:
    comp = line.split(":") # extract first two items, word, meaning
    word = comp[0]
    meaning = comp[1].rstrip()
    result = client.Put(word, meaning) # client contact the node using thrift
    print(result)
    print("Succeed to set: " + word + " " + meaning)

  # Close!
  transport.close()

# connect with Node using thrift for setting words
def setSingleWord(word, meaning, nodeAddress, port):

  transport = TSocket.TSocket(nodeAddress, port)

  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  client = Node.Client(protocol)

  # Connect!
  transport.open()

  result = client.Put(word, meaning) # client contact the node using thrift
  print(result)
  print("Succeed to set: " + word + " " + meaning)

  # Close!
  transport.close()

# connect with Node using thrift for getting word meaning
def getWord(word, nodeAddress, port):
  transport = TSocket.TSocket(nodeAddress, port)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = Node.Client(protocol)

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
    nodeInfo = connectSuperNode()
    if (nodeInfo == "Empty"):
      print("There is no node ready to be used.") 

    # parse the nodeInfo
    temp = nodeInfo.split()
    nodeAddress = temp[0]
    port = temp[1]

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
      print("Your input syntax is wrong. Please check User Document.")
  except Thrift.TException as tx:
    print('%s' % tx.message)

## The client is responsible for setting word and meanings to the system as well as 
## getting a meaning from the system with a word