import numbers
from operator import truediv
import random
from statistics import mean
from unittest import result
import threading
import time



k = 6
# Assume the Number of the nodes are 9
MAX = 2**k
# Assume the longest steps need to take the 2^k step

# we need use the node's (IP + Node) change to the hash value
# result mod MAX

# find the closet numbers


import random
import hashlib



class pos:
    def decr(value,size):
        if size <= value:
            return value - size
        else:
            return MAX-(size-value)
            

    def between(value,init,end):
        if init == end:
            return True
        elif init > end :
            shift = MAX - init
            init = 0
            end = (end +shift)%MAX
            value = (value + shift)%MAX
        return init < value < end

    def atStart(value,init,end):
        if value == init:
            return True
        else:
            return pos.between(value,init,end)

    def atEND(value,init,end):
        if value == end:
            return True
        else:
            return pos.between(value,init,end)


class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        self.wordlist = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)

    def successor(self):
        return self.finger[0]
    
    def find_successor(self,id):  
        if pos.atEND(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()
    
    def find_successor(self,id):  
        if pos.betweenE(id,self.predecessor.id,self.id):
            print("I'm the finding node")
            return self
        print("Change to next node")
        print(self.id)
        n = self.find_predecessor(id)
        # tracking
        print(n.id)
        k = n.successor()
        print(k.id)                
        # tracking
        return n.successor()
    
    def closest_preceding_finger(self,id):
        for i in range(k-1,-1,-1):
            if pos.between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self
        
    
    def join(self,n1):
        if self == n1:
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else:
            self.init_finger_table(n1)
            self.update_others()  
           # Move keys !!! 
            
    def init_finger_table(self,n1):
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if pos.atStart(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])

    def update_others(self):
        for i in range(k):
            prev  = pos.decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
            
    def update_finger_table(self,s,i):
        if pos.atStart(s.id,self.id,self.finger[i].id) and self.id!=s.id:
                self.finger[i] = s
                p = self.predecessor
                p.update_finger_table(s,i)

    def update_others_leave(self):
        for i in range(k):
            prev  = pos.decr(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)
    # not checked 
    def leave(self):
        self.successor().predecessor = self.predecessor
        self.predecessor.setSuccessor(self.successor())
        self.update_others_leave()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ
    
    def put(self,word,meaning):
        wordID = HASHING.getHashId(word)
        print(wordID)
        findingnode = self.find_successor(wordID)
        findingnode.wordlist[word] = meaning


    def get(self,word):
        wordID = HASHING.getHashId(word)
        print(wordID)
        findingnode = self.find_successor(wordID)
        return findingnode.wordlist[word]
    

    # def stabilize():
    # def UpdateDHT():
        # Action == def update_others()


    # def stabilization()
        # 1. node x join and Id is between xp and xs
        # 2. x.suc  = xs
        # 3. xs.pre = x
        # 4. stabilization(xp)
        #     4.1 ?xs.pre->x
        #     4.2 xp.suc = x
        #     4.3 x.pre = xp

    def stabilize(self):
        '''
        The stabilize function is called in repetitively in regular intervals as it is responsible to make sure that each 
        node is pointing to its correct successor and predecessor nodes. By the help of the stabilize function each node
        is able to gather information of new nodes joining the ring.
        '''
        while True:
            if self.successor is None:
                time.sleep(10)
                continue
            data = "get_predecessor"

            if self.successor.ip == self.ip  and self.successor.port == self.port:
                time.sleep(10)
            result = self.request_handler.send_message(self.successor.ip , self.successor.port , data)
            if result == "None" or len(result) == 0:
                self.request_handler.send_message(self.successor.ip , self.successor.port, "notify|"+ str(self.id) + "|" + self.nodeinfo.__str__())
                continue

            # print("found predecessor of my sucessor", result, self.successor.id)
            ip , port = self.get_ip_port(result)
            result = int(self.request_handler.send_message(ip,port,"get_id"))
            if self.get_backward_distance(result) > self.get_backward_distance(self.successor.id):
                # print("changing my succ in stablaize", result)
                self.successor = Node(ip,port)
                self.finger_table.table[0][1] = self.successor
            self.request_handler.send_message(self.successor.ip , self.successor.port, "notify|"+ str(self.id) + "|" + self.nodeinfo.__str__())
            print("===============================================")
            print("STABILIZING")
            print("===============================================")
            print("ID: ", self.id)
            if self.successor is not None:
                print("Successor ID: " , self.successor.id)
            if self.predecessor is not None:
                print("predecessor ID: " , self.predecessor.id)
            print("===============================================")
            print("=============== FINGER TABLE ==================")
            self.finger_table.print()
            print("===============================================")
            print("DATA STORE")
            print("===============================================")
            print(str(self.data_store.data))
            print("===============================================")
            print("+++++++++++++++ END +++++++++++++++++++++++++++")
            print()
            print()
            print()
            time.sleep(10)

    def notify(self, node_id , node_ip , node_port):
        '''
        Recevies notification from stabilized function when there is change in successor
        '''
        if self.predecessor is not None:
            if self.get_backward_distance(node_id) < self.get_backward_distance(self.predecessor.id):
                # print("someone notified me")
                # print("changing my pred", node_id)
                self.predecessor = Node(node_ip,int(node_port))
                return
        if self.predecessor is None or self.predecessor == "None" or ( node_id > self.predecessor.id and node_id < self.id ) or ( self.id == self.predecessor.id and node_id != self.id) :
            # print("someone notified me")
            # print("changing my pred", node_id)
            self.predecessor = Node(node_ip,int(node_port))
            if self.id == self.successor.id:
                # print("changing my succ", node_id)
                self.successor = Node(node_ip,int(node_port))
                self.finger_table.table[0][1] = self.successor
        
    def fix_fingers(self):
        '''
        The fix_fingers function is used to correct the finger table at regular interval of time this function waits for
        10 seconds and then picks one random index of the table and corrects it so that if any new node has joined the 
        ring it can properly mark that node in its finger table.
        '''
        while True:

            random_index = random.randint(1,m-1)
            finger = self.finger_table.table[random_index][0]
            # print("in fix fingers , fixing index", random_index)
            data = self.find_successor(finger)
            if data == "None":
                time.sleep(10)
                continue
            ip,port = self.get_ip_port(data)
            self.finger_table.table[random_index][1] = Node(ip,port) 
            time.sleep(10)


class HASHING:
    def hash(IP,port):
        message = IP + port
        message = message.encode()
        # then sending to md5()
        result = hashlib.md5(message.encode())
        print("this is the result for the md5")
        print(result)
        # printing the equivalent hexadecimal value.
        print("The hexadecimal equivalent of hash is : ", end ="")
        print(result.hexdigest())
        resulthex = result.hexdigest()
        return resulthex
    
    def wordhash_id(string):
        string = string.encode()
        result  = hashlib.md5(string.encode())
        wordresult = result.hexdigest()
        wordH_id = int(wordresult,16)
        id = wordH_id % MAX
        return id


    def HashtoID(resulthex):
        # string type for resulthex
        i = int(resulthex, 16)
        i = i%MAX
        return i


    def compareHASH(beforehash1,befrehash2):
        if beforehash1 == befrehash2:
            return True
        else:
            return False

def id():
    return long(random.uniform(0,2**k))


def printNodes(node):
    print (" Ring nodes:")
    end = node
    print (node.id)
    while end != node.successor():
        node = node.successor()
        print (node.id)
    print ('-----------')

def showFinger(node):
    print ('Finger table of node ' + str(node.id))
    print ('start:node')
    for i in range(k):
        print (str(node.start[i]) +' : ' +str(node.finger[i].id))  
    print ('-----------')
