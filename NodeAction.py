from Node import *
import hashlib


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

# def connection()



class Hashing:
    def hash(IP,port):
        message = IP + port
        message = message.encode()
        # then sending to md5()
        result = hashlib.md5(message)
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


def main():


    IPNode1 = "localhost"
    IPNode2 = "localhost"
    IPNode3 = "localhost"
    IPNode4 = "localhost"
    IPNode5 = "localhost"

    PortNode1 = "4041"
    PortNode2 = "4042"
    PortNode3 = "4043"
    PortNode4 = "4044"
    PortNode5 = "4045"

    H_value1 = Hashing.hash(IPNode1,PortNode1)
    ID1 = Hashing.HashtoID(H_value1)

    H_value2 = Hashing.hash(IPNode2,PortNode2)
    ID2 = Hashing.HashtoID(H_value2)

    H_value3 = Hashing.hash(IPNode3,PortNode3)
    ID3 = Hashing.HashtoID(H_value3)

    H_value4 = Hashing.hash(IPNode4,PortNode4)
    ID4 = Hashing.HashtoID(H_value4)
    
    H_value5 = Hashing.hash(IPNode5,PortNode5)
    ID5 = Hashing.HashtoID(H_value5)

    n1 = Node(ID1)
    n2 = Node(ID2)
    n3 = Node(ID3)
    n4 = Node(ID4)
    n5 = Node(ID5)

    
        
    n1.join(n1)
    n2.join(n1)
    n3.join(n1)
    n4.join(n1)
    n5.join(n1)

       
    
    showFinger(n1)
    showFinger(n2)
    showFinger(n3)
    printNodes(n1)

    print ("finish !!!")
    
    server = serve(chord_server, port)
    stabilize_thread = threading.Thread(target=stabilize)
    stabilize_thread

if __name__ == "__main__":

    main()