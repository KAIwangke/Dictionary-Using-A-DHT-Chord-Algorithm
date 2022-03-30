namespace py PA2

struct NodeInfo {
  1: i32 id
  2: string ip
  3: i32 port
}

service Node {

  NodeInfo findSuccessor(1: i32 id),

  NodeInfo findPredecessor(1: i32 id),

  string Put(1: string word, 2: string meaning),
  
  string Get(1: string word),

  NodeInfo successor(),

  NodeInfo predecessor(),

  void setPredecessor(1: NodeInfo pred),

  NodeInfo closest_preceding_finger(1: i32 id),

  void init_finger_table(1: NodeInfo newNodeInfo),

  void update_finger_table(1: NodeInfo s, 2: i32 i),

  void update_others(),

  void setWord(1: string word, 2: string meaning),

  string getWord(1: string word),

}