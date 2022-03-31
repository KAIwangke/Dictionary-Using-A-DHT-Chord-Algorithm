# Dictionary-Using-A-DHT-Chord-Algorithm



# System Design and Operation

For this project we build a Dictionary using a distributed hash table (DHT) based on the Chord protocol. Using this system, the client can lookup the meaning of a word using the DHT. The client can also insert a new word and its meaning into the dictionary. The system is completely decentralized with the use of the Apache Thrift.

## 1. Basic Ideas about the Chord Algorithm

#### 1.1 Basic query

The core usage of the Chord protocol is to query a key from a client (generally a node as well), i.e. to find successor(k). The basic approach is to pass the query to a node's successor, if it cannot find the key locally. This will lead to a [O(N)]query time where [N] is the number of machines in the ring.

#### 1.2 Finger table

To avoid the linear search above, Chord implements a faster search method by requiring each node to keep a *finger table* containing up to [m] entries, recall that [m] is the number of bits in the hash key.

The [i^{th}] entry of node [n] will contain Successor((n+2^(i-1)) mod 2^m)

The first entry of finger table is actually the node's immediate successor (and therefore an extra successor field is not needed). 

Every time a node wants to look up a key [k], it will pass the query to the closest successor or predecessor (depending on the finger table) of [k] in its finger table (the "largest" one on the circle whose ID is smaller than [k], until a node finds out the key is stored in its immediate successor.

With such a finger table, the number of nodes that must be contacted to find a successor in an *N*-node network is  [O(\log N)]. 

If two nodes are at a distance 11 apart along the ring (i.e., there are 10 nodes between them), it takes three hops to send a message from one to the other. The first hop covers a distance of 8 units, the second 2 units, and the final hop 1 unit.

<img width="210" alt="image" src="https://user-images.githubusercontent.com/46043861/160290600-7ea6c617-f6d1-4291-8148-8abf059bd3d3.png">


The routing path between nodes A and B. Each hop cuts the remaining distance in half (or better).

1. Node N wishes to find the successor of key **K**
2. Wish to find the **upper bond** of the number of steps it takes for finding the key
3. The node store the key called `f` and f is at most have 2^i-1^ distance from the previous node called `p`
4. After `t`'s loop the remaining distance is 2^m^/2^t^ (E.g. assume the t is 0 applied to the longest distacne 2^i-1^)
5. After  [log N] steps, the remaining distance is at most  [2^m / N]. 
6. Because nodes are distributed uniformly at random along the identifier circle, the expected number of nodes falling within an interval of this length is 1, and with high probability, there are fewer than  [log N] such nodes. Because the message always advances by at least one node, it takes at most  [log  N] steps for a message to traverse this remaining distance. The total expected routing time is thus  [O(log N)].

#### 1.3 Node join

Whenever a new node joins, three invariants should be maintained (the first two ensure correctness and the last one keeps querying fast):

1. Each node's successor points to its immediate successor correctly.
2. Each key is stored in  [successor(k)].
3. Each node's finger table should be correct.

To satisfy these invariants, a *predecessor* field is maintained for each node. As the successor is the first entry of the finger table, we do not need to maintain this field separately any more. The following tasks should be done for a newly joined node  [n]:

1. Initialize node  [n] (the predecessor and the finger table).
2. Notify other nodes to update their predecessors and finger tables.
3. The new node takes over its responsible keys from its successor.

The predecessor of  [n] can be easily obtained from the predecessor of  [successor(n)] (in the previous circle). As for its finger table, there are various initialization methods. The simplest one is to execute find successor queries for all  [m]entries, resulting in  [O(M\log N)] initialization time. A better method is to check whether  [i^{th}] entry in the finger table is still correct for the  [(i+1)^{th}] entry. This will lead to  [O(\log^2 N)]. The best method is to initialize the finger table from its immediate neighbours and make some updates, which is  [O(\log N)].



#### 1.4 Stabilization

To ensure correct lookups, all successor pointers must be up to date. Therefore, a stabilization protocol is running periodically in the background which updates finger tables and successor pointers.

The stabilization protocol works as follows:

- Stabilize(): n asks its successor for its predecessor p and decides whether p should be n‘s successor instead (this is the case if p recently joined the system).
- Notify(): notifies n‘s successor of its existence, so it can change its predecessor to n
- Fix_fingers(): updates finger tables





## 2. Function Implementation

#### 2.1 Client

Client is used to provide user interfaces to talk to the system. Client knows the super node information and will use a random node of the system as an enter point to get access to the whole system. 

There are 4 options a user can do:

1) To set a single `Word-Meaning` pair into the system:  Call `setSingleWord()` 
2) To set book title and genre with an input file. Get each line of pairs and store them into the system. 
3) To get book title, call getPair(). 
4) Exit the system For each operation here, user can choose whether or not to print the tracking information

##### 2.1.1 `def connectSuperNode()`

The function will connect to the supernode using the thrift frame work. Client will connect to the supernode and sends a request to the server via a RPC call using `superNodeAddress`.  The `nodeInfo` will get from the supernode in order to contact to the specific node itself.

##### 2.1.2 `def setFile(fileName, nodeAddress, port)`

Extract first two items, word and meaning, the function will contact the node using the thrift for the client and then use the information to request the `put(word,meaning)` action. Under this action we assume the file include all the information that is given for put action and well documented as `word` & `meaning` in above and after lines

In the interface for the clint this action according to the `add`



##### 2.1.3 `def setSingleWord(word, meaning, nodeAddress, port)`

Connect with Node using thrift for setting words, this function implement for the user to put single word and meaning adding into the DHT.  The function will contact the node using the thrift for the client and then use the information to request the `put(word,meaning)` action. 

In the interface for the clint this action according to the `set`



##### 2.1.4 `def getWord(word, nodeAddress, port)`

 The function will contact the node using the thrift for the client and then use the information to request the `get(word)` action. If the get meaning is `NA` that means the DHT didn’t include the meaning of the word. Otherwise it will get back the meaning for the user/client.

In the interface for the clint this action according to the `get`

==todo==

##### 2.1.5 `def ExitPrint`

In the interface for the clint this action according to the `exit and print`







#### 2.2 SuperNode

SuperNode will maintain the node list of the system knowing all the information of the nodes in the system.

The address of super node is well known for all the clients and new nodes. Each new node needs to contact the super node first to get a random node information of the system. Each client will also talk to the super node first to a random node information and do the following information. Super node will guarantee that there will be no concurrent node join and only return node information to clients when the system is ready.

##### 2.2.1 `def getPossibleID()`

Generate the random number for the ID for the new node to join.



 ##### 2.2.2 `def GetNodeForJoin(self, IP, Port)`

This function maintain the connection with the client, which will return a node information that is randomly chosen and also return the formatted ip and port for the client to contact with.



##### 2.2.3 `def PostJoin(self, IP, Port, id)`

This function maintain the connection between the supernode itself and the node. Suppose we have the nodeInfo that is `5, 127.0.0.1:54454:12` according to the nodeID, IP and port. After the node finished the joining the DHT, it will send the “DONE”, message to the supernode.



#### 2.3 Node

Each node will maintain a part of the DHT and maintains a finger table storing partial information of the other nodes in the system to provide “shortcut” to other nodes. We use [ip]:[port] as the string to generate hash code. When a node first joins the system, it will talk to the super node first to get a random node existing in the system. Then the new node will use the existing information to build its own finger table and join the system. Updating the finger tables of other nodes is also the job of the new node. Each node provides multiple services for other nodes and clients to get its own information (finger entries and real data pairs).



Assume MAX = 2^bits



##### 2.3.1 `Helper Functions for the Position`



​	`def decr()` In order to find the distance between the target node and the currrent node. if the value is bigger than the max size for the chord, then there should be the modular operation in order to find the correspingding position for the node. `(size<=value)? return value-size :return MAX-(size-value)`

​	`def between()`	to check if the id is in the interval [start, end]. Edge case is if the node is the first node hence the start should be the end and return true. Else check the relation for the `start < id < end` , brefore heading to the comparison, we need to make sure all the index is inside the interval of the 0 and max.

​	`def closeStart()` to check the init belongs to the interval of [start,end)

​	`def closeEnd()` to check the init belongs to the interval of (start,end]

​	

##### 2.3.2 `class WordList` 

` def insert(self, word, meaning)` The insert functon will insert the meaning into the wordlist

` def delete(self, word) ` The delet function will pop out the word in the dictionary

` def search(self, word)` The search function will search for the word in the list



##### 2.3.4`class Node:`

Assume the Node class has init the attribute for the self {id,ip,port,nodeInfo(ip,port),finger, start,wordlist,predecessor,successor,traceInfo}



 	`def successor(self)` set the successor for the node as the attribute

​	 ` 	def predecessor(self)` set the predecessor for the node as attribute

 	`def findSuccessor(self, id)` Ask the node self to find id’s successor and return NodeInfo,  if the id is in the between [self.pred.id, self.id]. if current one is not in the interval of the id then it should return th predecessor’s nodeInfo. All the process assume the ip and the port can be access by the node and contactable for the current node while connecting using the thrift.

 	`def findPredecessor(self, id)` Ask the node self to find the id’s predecessor and return NodeInfo, while Id is not belong to the (current, current.successor) then it should update the current node and keep finding. All the process assume the ip and the port can be access by the node and contactable for the current node while connecting using the thrift.

 	`def closest_preceding_finger(self, id)` The function will return the closest finger preceding id and return the nodeInfo using the chord algorithm.

 	`def join(self)` Join into the network for the arbitrary node and initial the finger table also updates all the other one’s fingertable.

 	`def init_finger_table(self, newNodeInfo)`: initialize finger table of local node, connect with new Node to find its successor, connect to the pred via thrift to get its successor. 

 	`def update_others(self)`

 	`def update_finger_table(self, s, i)`

 	`def update_others_leave(self)`

 	`def leave(self)`

 	`def setSuccessor(self, succ)`

 	`def setWord(self, word, meaning)`

 	`def Put(self, word, meaning)`

 	`def getWord(self, word)`

​	`def ConnectSuperNode(IP, port)`

​	`def startNodeServer(id, ip, port)`









## 3. User Document: how to run the service

#### 3.1 Compile

```
cd Dictionary-Using-A-DHT-Chord-Algorithm

thrift -gen py Node.thrift
thrift -gen py SuperNode.thrift
```

#### 3.2 Run

```python
python3 client.py
python3 SuperNode.py

python3 Nodes.py <Port1> <IP> <number of bits>
python3 Nodes.py <Port2> <IP> <number of bits>
python3 Nodes.py <Port3> <IP> <number of bits>
python3 Nodes.py <Port4> <IP> <number of bits>
python3 Nodes.py <Port5> <IP> <number of bits>
```

Assume we have 5 nodes for the supernode in the chord.



## Reference:

a. Stoica, R. Morris, D. Karger, M. F. Kaashoek, and H. Balakrishnan. Chord: A scalable peer-to-peer lookup service for Internet applications. In Proc. ACM SIGCOMM’01, San Diego, CA, Aug. 2001. [LINK](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf)
b. Thrift White paper
\- https://thrift.apache.org/static/files/thrift-20070401.pdf
c. How to setup Thrift in your own machine (Ubuntu)

- Packages for compiling Thrift
  https://thrift.apache.org/docs/install/debian

- Building Thrift from source codes

  https://thrift.apache.org/docs/BuildingFromSource 

  Tutorial by Examples

  Python
  https://thrift.apache.org/tutorial/py
