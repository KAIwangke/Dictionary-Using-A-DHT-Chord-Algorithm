## The node forms the DHT with help from thr SuperNode and are used by the client to perform "set" and "get"
## work information. Nodes need to store words and meanings locally.

import numbers
from operator import truediv
import random
from statistics import mean

import random
import sys
from sys import argv
import os
import glob
import time
import hashlib

import threading

sys.path.append('./gen-py/')
sys.path.insert(0, glob.glob('../lib/py/build/lib*')[0])

from PA2 import Node
from PA2 import SuperNode

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

threadLock = threading.Lock()

# the IP and port of current node
nodeIP = "localhost"
nodePort = 0

# the IP and port of the supernode
superNodeIP = "localhost"
superNodePort = 0

# default length and max_size of DHT
chordLen = 7
MAX_SIZE = 2**chordLen


## Below are helper functions for comparison of ids, [id, 2^i]
def decr(value, size):
  if size <= value:
    return value - size
  else:
    return MAX_SIZE-(size-value)
      
# check if a value is (start, end)
def between(id, start, end):
  if start == end:
    return True
  elif start > end :
    end = (end + MAX_SIZE - start) % MAX_SIZE
    id = (id + MAX_SIZE - start)% MAX_SIZE
    start = 0

  return start < id < end

# check if init belongs to [start, end)
def closeStart(id, start, end):
  return ( (id == start) or between(id, start, end) )

# check if init belongs to (start, end]
def closeEnd(id, start, end):
  return ( (id == end) or between(id, start, end) )


# helper function to hash the string of nodeInfo: "ip:port"
def hash(message):
  result = hashlib.sha256(message.encode()).hexdigest()
  result = int(result, 16) % MAX_SIZE
  return result


# class represents the actual Node which stores its ip and port
# class NodeInfo:
#   def __init__(self, id, ip, port):
#     self.id = id
#     self.ip = ip
#     self.port = port 
  
#   def __str__(self):
#     return self.ip + ":" + str(self.port)

# class represents the wordList each node stores
class WordList:
  def __init__(self):
    self.wordList = {}

  def insert(self, word, meaning):
    self.wordList[word] = meaning

  ## delete a word in the dictionary
  def delete(self, word):
    wordList.pop(word, None)

  def search(self, word):
    if word in self.wordList:
      return self.wordList[word]
    else:
      print("The word is not found in the dictionary.")
      return None



# class which include all node information and its fingertable, id, ip, port, successor, presecessor, wordList, etc
class Node:
  def __init__(self, id, ip, port):
    self.id = id
    self.ip = ip
    self.port = port
    self.nodeInfo = NodeInfo(ip, port)
    self.finger = {}  # dictionary of {id: NodeInfo}
    self.start = {}  # finger[k].start - {int:int}
    self.wordlist = WordList()
    self.predecessor = None
    self.successor = None
    self.traceInfo = ""
    for i in range(chordLen):
      self.start[i] = (self.id+(2**i)) % (MAX_SIZE)

  # get the successor of the node, return type: NodeInfo
  def successor(self):
    self.successor = self.finger[0]
    return NodeInfo(self.finger[0].id, self.finger[0].ip, self.finger[0].port)


  # get the successor of the node, return type: NodeInfo
  def predecessor(self):
    return predecessor

  # set the predecessot of self to be pred NodeInfo
  def setPredecessor(self, pred):
    self.predecessor.id = pre.id
    self.predecessor.ip = pre.ip
    self.predecessor.port = pre.port

  # ask node self to find id's successor, return type: NodeInfo
  def findSuccessor(self, id):
    self.traceInfo = "[" + str(self.id)
    # if the id is between [self.pred.id, self.id], then current node is the one
    if between(id, self.predecessor.id, self.id):
      print("Current node is responsible for the word.")
      self.traceInfo += "]"
      return self

    # return pred NodeInfo 
    pred = self.findPredecessor(id)
    print(pred.id)
    self.traceInfo += ", "
    self.traceInfo += str(pred.id)

    # connect to the pred via thrift to get its successor
    transport = TSocket.TSocket(pred.ip, pred.port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Node.Client(protocol)
    transport.open()
    succ = client.successor()
    transport.close()

    # get the successor of the pred of id

    print(succ.id)     
    self.traceInfo += ", "
    self.traceInfo += str(succ.id)           
    self.traceInfo += "]"
    
    return succ


  # ask node self to find id's predecessor
  def findPredecessor(self, id):
    ## if the node is itself
    if id == self.id:
      return NodeInfo(self.predecessor.id, self.predecessor.ip, self.predecessor.port)

    current = NodeInfo(self.id, self.ip, self.port)
    succ = current.successor() # NodeInfo type
    ## while (id is not belong to (current, current.successor])), then update current
    while not closeEnd(id, current.id, succ.id):
      # connect to current via thrift
      transport = TSocket.TSocket(current.ip, current.port)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      client = Node.Client(protocol)
      transport.open()
      current = client.closest_preceding_finger(id)
      transport.close()

      # get the current node's successor
      # connect to the pred via thrift to get its successor
      transport = TSocket.TSocket(current.ip, current.port)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      client = Node.Client(protocol)
      transport.open()
      succ = client.successor() # get the updated succ
      transport.close()
    
    return current
  

  # return closest finger preceding id, return type: NodeInfo
  def closest_preceding_finger(self, id):
    for i in range(chordLen)[::-1]: # i is [m-1,0], i+1 -> [m,1]
      if between(self.finger[i+1].id, self.id, id):
        return NodeInfo(self.finger[i+1].id, self.finger[i+!].ip, self.finger[i+1].port)
    
    result = NodeInfo(self.id, self.ip, self.port)
    return result
     
  # join from another arbitrary node in the network
  def join(self):
    if self == n1:
      for i in range(chordLen):
        self.finger[i] = self
      self.predecessor = self
    else:
      self.init_finger_table(n1)
      self.update_others()  

  # initialize finger table of local node
  def init_finger_table(self, newNodeInfo):
    # connect with new Node to find its successor
    # connect to the pred via thrift to get its successor
    suctransport = TSocket.TSocket(newNodeInfo.ip, newNodeInfo.port)
    suctransport = TTransport.TBufferedTransport(suctransport)
    sucprotocol = TBinaryProtocol.TBinaryProtocol(suctransport)
    succlient = Node.Client(sucprotocol)
    suctransport.open()
    suc = succlient.findSuccessor(self.start[0])
    
    # update the finger table [0] {id: NodeInfo}
    self.finger[0] = suc
    # self.successor = finger[0] - NodeInfo = suc

    # connect to self.successor to get the pred via thrift
    transport = TSocket.TSocket(suc.ip, suc.port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Node.Client(protocol)
    transport.open()
    t = client.predecessor()
    
    # update predecessor
    self.predecessor = NodeInfo(t.id, t.ip. t.port)
    selfNodeInfo = NodeInfo(self.id, self.ip, self.port)

    # change the successot's pred to the current node self
    client.setPredecessor(selfNodeInfo)
    
    transport.close()

    for i in range(chordLen - 1): # i+2 => 1 to m-1
      if closeStart(self.start[i+1], self.id, self.finger[i].id):
        self.finger[i+1] = self.finger[i]
      else :
        self.finger[i+1] = succlient.findSuccessor(self.start[i+1])

    suctransport.close()
    
  ## update all nodes whose finger tables should be refer to n
  def update_others(self):
    for i in range(chordLen): # i+1 -> [1,m]
      prev  = decr(self.id, 2**i)
      p = self.findPredecessor(prev)
      # connect to the p via thrift to get its successor
      transport = TSocket.TSocket(p.ip, p.port)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      client = Node.Client(protocol)
      transport.open()
      client.update_finger_table(self, i+1) # update finger table of pred
      transport.close()

      # if prev == p.successor().id:
      #     p = p.successor()
      # p.update_finger_table(self, (i+1))

  # if s(NodeInfo) is ith finger of n, update n's finger table with s
  def update_finger_table(self, s, i):
    if closeStart(s.id, self.id, self.finger[i].id) and self.id != s.id:
      self.finger[i] = s # update ith entry of finger table

      p = self.predecessor # NodeInfo type

      # update prec's finger table
      # connect to the pred via thrift to get its successor
      transport = TSocket.TSocket(p.ip, p.port)
      transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      client = Node.Client(protocol)
      transport.open()
      client.update_finger_table(s, i) # update finger table of pred
      transport.close()

      
  # set the successor of self
  def setSuccessor(self, succ):
    self.finger[0] = succ  

  ## add the pair in the node's wordlist
  def setWord(self, word, meaning):
    threadLock.acquire()
    wordlist.insert(word, meaning)
    threadLock.release()

  ## insert the pair [word, meaning] in the DHT
  # return format: [word:meaning] is successfully set on Node ID with hash value wordID
  # The trace is [...]
  def Put(self, word, meaning):
    wordID = hash(word) # hash the word
    print("The hashing ID of the word is: " + wordID)
    # find the successor of the target ID
    findingNode = self.findSuccessor(wordID)

    # building connection to the findingNode 
    # connect to the pred via thrift to get its successor
    transport = TSocket.TSocket(findingNode.ip, findingNode.port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Node.Client(protocol)
    transport.open()
    client.setWord(word, meaning) # store (word, meaning) in wordlist
    transport.close()

    message = "[" + word + " : " + meaning + "] is inserted on Node " + str(findingNode.id) + " with hash value " + str(wordID)
    message = message + " TraceInfo is: " + self.traceInfo
    # set the traceInfo to be empty for next Put request
    self.traceInfo = ""
    return message


  ## get the meaning of the word in the node's wordlist
  def getWord(self, word):
    threadLock.acquire()
    result = wordlist.search(word)
    threadLock.release()
    if (result == None):
      print("Not existed. Try another word.")
      return "NOT EXISTED"

    return wordlist.search(word)

  ## get the meaning of the word in the DHT
  # return format: 
  def Get(self, word):
    wordID = hash(word) # hash the word
    print("The hashing ID of the word is: " + wordID)
    # find the successor of the target ID
    findingNode = self.findSuccessor(wordID)

    # building connection to the findingNode 
    # connect to the pred via thrift to get its successor
    transport = TSocket.TSocket(findingNode.ip, findingNode.port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Node.Client(protocol)
    transport.open()
    result = client.getWord(word) # get (word, meaning) in wordlist
    transport.close()

    message = ""
    if (result != "NOT EXISTED"):
      message = "[" + word + " : " + result + "] is get on Node " + str(findingNode.id) + " with hash value " + str(wordID)
    else:
      message = "Fail to find: " + word + " on Node " + str(findingNode.id) + " with hash value " + str(wordID)
    
    message = message + " TraceInfo is: " + self.traceInfo
    # set the traceInfo to be empty for next Put request
    self.traceInfo = ""
    return message


  def UpdateDHT(self):


# The new node contacts the Supernode when it wants to join the DHT
def ConnectSuperNode(IP, port):

  transport = TSocket.TSocket(superNodeIP, superNodePort)

  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  client = SuperNode.Client(protocol)

  # Connect!
  transport.open()

  # pass the node IP and port to the supernode to get the node info back 
  info = client.GetNodeForJoin(IP, port) 

  # Close!
  transport.close()

  return info

# helper function which will start the node server
def startNodeServer(id, ip, port):
  handler = NodeHandler()
  processor = Node.Processor(handler)

  transport = TSocket.TServerSocket(host=ip, port=port)
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  # multithreaded server for Node
  server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

  server.serve()

  # send join request to the supernode

## server should be multi-threaded as there can be multiple clients in the system at the same time
## python3 Node.py port superNodeip superNodeport chordLen: [0,1,2,3,4]
if __name__ == '__main__':

  print("Starting Node ...")

  # set the chord length if user input 
  if (len(sys.argv) == 5):
    chordLen = int(argv[4])
    nodePort = int(argv[1])
    superNodeIP = argv[2]
    superNodePort = int(argv[3])
  else:
    print("Please specify the node port, superNode ip, superNode port and chordLen.")

  # TODO: DELETE 
  nodeIP = "localhost"
  nodePort = 9091

  # get the node ID using hash
  id = hash(nodeIP + ":" + str(nodePort))
  print("This node has id: " + str(id))

  ## connect to the supernode to start the node join process
  info = ConnectSuperNode(nodeIP, nodePort)
  print("Get response from the SuperNode: " + info)

  ## start the node join process
  currNode = Node(id, nodeIP, nodePort)
  # 1. the node is the first one to join 
  if (info == "NACK"):
    print("SuperNode is busy right now. Please try again later.")
  elif (info == "EXISTED"):
    print("The node has already joined. Please join a new node.")
  elif (info == "FULL"):
    print("The DHT system has already reached the maximum node size. Sorry.")
  elif (info == "EMPTY"): # add itself into the system
    currNode.join(currNode)
  else: ## success case - parse the info "5,127.0.0.1,54454,12"
    ## TODO: put the following into updateDHT()
    comp = info.split(",")
    randomNode = NodeInfo(int(comp[3]), comp[1], int(comp[2]))
    currNode.init_finger_table(randomNode)
    startNodeServer(id, nodeIP, nodePort)
    time.sleep(60)

    # update finger table in other nodes
    currNode.update_others()
    print("Finishing updating other nodes.")
  

  # tell supernode it's done
  transport = TSocket.TSocket(superNodeIP, superNodePort)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  superNodeclient = SuperNode.Client(protocol)
  # Connect!
  transport.open()
  
  info = superNodeclient.PostJoin(nodeIP, nodePort, id) 
  # Close!
  transport.close()



  


 



  




