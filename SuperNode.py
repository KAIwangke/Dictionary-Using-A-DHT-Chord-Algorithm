from cgitb import lookup
from html.entities import name2codepoint
from http.client import NOT_MODIFIED
from os import setgid
from telnetlib import IP


class SuperNode{

	def getRandomNode(){

    }

	def getNodeList(){

    }

	def finishJoining(int id){
        


    }

	def getNodeInfo(String ipAddr, String port){



    }


}

class Node{
    # need to specify the ID IP and port using thrift 
    # in order to get each node
    NodeId
    NodeIp
    NodePort


}

class NodeHDT{
    def makeConnection{
        # thrift.....
        #############
        
    }
    def run{

    }
    def considerInput{

    }
    def getWord{

    }
    def lookupkey{

    }
    def Insert{
        # 1. try inserting key
        # 2. inserting key

    }
    def init_finger_table{

    }
    def update_finger_table{

    }
    def setPredecessor(Node n){
        # get the predecessor node
        # set a global pred n
    }
    def update_others{

    }
    def find_predecessor(id){

    }
    def find_successor(id){
        
    }
    def get_successor(){

    }
    def closet_preceding_finger(int id){

    }

}






if __name__ == '__main__':

