import numbers
from operator import truediv
import random
from statistics import mean



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
    
    def find_predecessor(self,id):
        if id == self.id:
            return self.predecessor
        n1 = self
        while not pos.atEND(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1
    
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
        self.wordlist[word] = meaning

    def get(self,word):
        return self.wordlist[word]

    # def stabilization()
        # 1. node x join and Id is between xp and xs
        # 2. x.suc  = xs
        # 3. xs.pre = x
        # 4. stabilization(xp)
        #     4.1 ?xs.pre->x
        #     4.2 xp.suc = x
        #     4.3 x.pre = xp



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