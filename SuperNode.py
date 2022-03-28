import random
import sys
import glob
import time
import threading

sys.path.append('./gen-py/')
sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from PA2 import Node
from PA2 import SuperNode

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Node:
  fingerTable = {} # dictionary for fingertable
  wordsList = {} # dictionary for wordsList
  numWords = 0 # number of words stored

  # successor and predecessor information ip, port , id
  successor = ""
  predecessor = "" 
  def __init__(self, nodeID, IP, port):
    self.nodeID = nodeID
    self.IP = IP
    self.port = port


class SuperNodeHandler:
  
  nodesList = [] # a list of node 
  nodesNum = 0 # total number of nodes
  def __init__(self):

  # return a possible id for the new node
  def getPossibleID():


  def Check():
    # thrift with node
    done = client.PostJoin() # if done = "Done", allow other nodes to join the DHT


  ###### function for client/supernode ######
  # return node information randomly chosen 
  # return in format "ip port"
  def GetNodeForClient(self):
    idx = random.randint(0, nodesNum-1) # get index randomly
    chosenNode = nodesList[idx]
    return str(chosenNode.IP) + str(chosenNode.port)


  ###### function for node/supernode ######
  # for example: 5, 127.0.0.1:54454:12
  # node wants to join DHT, contact supernode which will assign a node ID and provide info about
  # an existing DHT node(including IP and Port)
  # node need to contact super node via thrift to join the DHT
  def GetNodeForJoin(self, IP, Port):
    # if the new node is the first node
    if (nodesNum == 0):
      return "EMPTY"
    else: # return the latest node in the nodesList
      latestNode = nodesList[-1]
      newID = getPossibleID()
      ip = latestNode.IP
      port = latestNode.port
      id = latestNode.nodeID
      nodeInfo = str(newID) + "," + str(ip) + "," + str(port) + "," + str(id)
      return nodeInfo


  # send "DONE" message to super node when the node is donw joining the DHT
  def PostJoin(self, IP, Port):
    # lock when a node is joining
    threadLock.acquire()
    GetNodeForJoin(IP, Port)
    threadLock.release()




if __name__ == '__main__':
  print("Starting SuperNode ...")

  superNodeAddress = "localhost" ## TODO
  port = 9091

  handler = SuperNodeHandler()
  processor = SuperNode.Processor(handler)

  transport = TSocket.TServerSocket(host="0.0.0.0", port=nodePort)
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  # multithreaded server for superNode?? probably not
  server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

  server.serve()
  print('done.')


  


