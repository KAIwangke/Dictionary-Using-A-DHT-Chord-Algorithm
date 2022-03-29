import random
import sys
import glob
import time
import hashlib

from threading

sys.path.append('./gen-py/')
sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from PA2 import Node
from PA2 import SuperNode

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# thread lock for the supernode
threadLock = threading.Lock()
chordLen = 7
MAX_SIZE = 2**chordLen

class NodeInfo:

  def __init__(self, nodeID, IP, port):
    self.nodeID = nodeID
    self.IP = IP
    self.port = port


class SuperNodeHandler:
  
  nodesList = [] # a list of node 
  nodesNum = 0 # total number of nodes
  possibleIDs = [] # list store all possible ids

  def __init__(self):
    ## insert [0, max_size-1] into possibleIDs
    for i in range(0, MAX_SIZE):
      possibleIDs.append(i)


  # return a possible id for the new node randomly
  def getPossibleID():
    return random.choice(possibleIDs)


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
  def GetNodeForJoin(self, IP, Port):
    ## check if the node is already in the system 
    for node in nodesList:
      if (node.IP == IP and node.port == Port):
        print("The node has already joined.")
        return "EXISTED"

    ## check if the DHT is full 
    if (nodesNum == MAX_SIZE):
      print("The DHT is full. Can't add more nodes.")
      return "FULL"

    # check if the thread is locking or not
    if(threadLock.locked()):
      print("The supernode is busy with adding another node. Please wait...")
      return "NACK"
    else:
      threadLock.acquire()
      # if there is no nodes in the nodeList
      if (nodesNum == 0):
        return "EMPTY"
      else: 
        # return the latest node in the nodesList
        latestNode = nodesList[-1]
        newID = getPossibleID(IP, Port)
        # remove the used ID from possibleIDs list
        possibleIDs.remove(newID)
        ip = latestNode.IP
        port = latestNode.port
        id = latestNode.nodeID
        nodeInfo = str(newID) + "," + str(ip) + "," + str(port) + "," + str(id)
        return nodeInfo


  # send "DONE" message to super node when the node is donw joining the DHT
  def PostJoin(self, IP, Port, id):
    # append the new node into the nodeList
    newNode = NodeInfo(id, IP, Port)
    nodesList.append(newNode)
    nodesNum += 1
    # release the lock after getting this call from the node
    threadLock.release()
    print("Current node finished join. Allowing for other nodes to join.")



## python3 SuperNode.py chordLen: [0,1]
if __name__ == '__main__':

  print("Starting SuperNode ...")

  # set the chord length if user input 
  if (len(sys.argv) == 2):
    global chordLen
    chordLen = int(argv[1])

  superNodeAddress = "localhost" ## TODO
  port = 9091

  handler = SuperNodeHandler()
  processor = SuperNode.Processor(handler)

  transport = TSocket.TServerSocket(host="0.0.0.0", port=nodePort)
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  # multithreaded server for superNode
  server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

  server.serve()
  print('done.')


  


