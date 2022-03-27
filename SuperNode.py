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


# needed calls to the suppernode ==============================
    def GetNodeForJoin_actual(IP,Port){
        # getNodeInfo(String ipAddr, String port)


    }

    def PostJoin_actual(){
        # def finishJoining(int id)
    }


    def GetNodeForClient_actual(){

    }

}

class Node{
    # need to specify the ID IP and port using thrift 
    # in order to get each node
    NodeId
    NodeIp
    NodePort


}


if __name__ == '__main__':
    # connection between the supernode and the client interface


