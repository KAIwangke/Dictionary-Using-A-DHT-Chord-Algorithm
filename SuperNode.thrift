namespace py PA2

service SuperNode {

  string GetNodeForJoin(1: string IP, 2: i32 Port),

  void PostJoin(1: string IP, 2: string Port, 3: i32 id),

  string GetNodeForClient(),

  i32 getPossibleID(),

}