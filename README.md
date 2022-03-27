# Dictionary-Using-A-DHT-Chord-Algorithm

### Basic query

The core usage of the Chord protocol is to query a key from a client (generally a node as well), i.e. to find successor(k). The basic approach is to pass the query to a node's successor, if it cannot find the key locally. This will lead to a [O(N)]query time where [N] is the number of machines in the ring.

### Finger table

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

### Node join

Whenever a new node joins, three invariants should be maintained (the first two ensure correctness and the last one keeps querying fast):

1. Each node's successor points to its immediate successor correctly.
2. Each key is stored in  [successor(k)].
3. Each node's finger table should be correct.

To satisfy these invariants, a *predecessor* field is maintained for each node. As the successor is the first entry of the finger table, we do not need to maintain this field separately any more. The following tasks should be done for a newly joined node  [n]:

1. Initialize node  [n] (the predecessor and the finger table).
2. Notify other nodes to update their predecessors and finger tables.
3. The new node takes over its responsible keys from its successor.

The predecessor of  [n] can be easily obtained from the predecessor of  [successor(n)] (in the previous circle). As for its finger table, there are various initialization methods. The simplest one is to execute find successor queries for all  [m]entries, resulting in  [O(M\log N)] initialization time. A better method is to check whether  [i^{th}] entry in the finger table is still correct for the  [(i+1)^{th}] entry. This will lead to  [O(\log^2 N)]. The best method is to initialize the finger table from its immediate neighbours and make some updates, which is  [O(\log N)].



### Stabilization

To ensure correct lookups, all successor pointers must be up to date. Therefore, a stabilization protocol is running periodically in the background which updates finger tables and successor pointers.

The stabilization protocol works as follows:

- Stabilize(): n asks its successor for its predecessor p and decides whether p should be n‘s successor instead (this is the case if p recently joined the system).
- Notify(): notifies n‘s successor of its existence, so it can change its predecessor to n
- Fix_fingers(): updates finger tables
