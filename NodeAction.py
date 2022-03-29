from Node import *


def main():


    IPNode1 = "localhost"
    IPNode2 = "localhost"
    IPNode3 = "localhost"
    IPNode4 = "localhost"
    IPNode5 = "localhost"

    PortNode1 = 4041
    PortNode2 = 4042
    PortNode3 = 4043
    PortNode4 = 4044
    PortNode5 = 4045

    H_value1 = HASHING.hash(IPNode1,PortNode1)
    ID1 = HASHING.HashtoID(H_value1)

    H_value2 = HASHING.hash(IPNode2,PortNode2)
    ID2 = HASHING.HashtoID(H_value2)

    H_value3 = HASHING.hash(IPNode3,PortNode3)
    ID3 = HASHING.HashtoID(H_value3)

    H_value4 = HASHING.hash(IPNode4,PortNode4)
    ID4 = HASHING.HashtoID(H_value4)
    
    H_value5 = HASHING.hash(IPNode5,PortNode5)
    ID5 = HASHING.HashtoID(H_value5)

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
    



if __name__ == "__main__":

    main()