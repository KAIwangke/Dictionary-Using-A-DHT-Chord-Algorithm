# Dictionary-Using-A-DHT-Chord-Algorithm

### Basic query

The core usage of the Chord protocol is to query a key from a client (generally a node as well), i.e. to find ![successor(k)](https://wikimedia.org/api/rest_v1/media/math/render/svg/0d7151defafe837a78ed2433cb004c3bd2411db9). The basic approach is to pass the query to a node's successor, if it cannot find the key locally. This will lead to a ![O(N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/78484c5c26cfc97bb3b915418caa09454421e80b)query time where ![N](https://wikimedia.org/api/rest_v1/media/math/render/svg/f5e3890c981ae85503089652feb48b191b57aae3) is the number of machines in the ring.

### Finger table

To avoid the linear search above, Chord implements a faster search method by requiring each node to keep a *finger table* containing up to ![m](https://wikimedia.org/api/rest_v1/media/math/render/svg/0a07d98bb302f3856cbabc47b2b9016692e3f7bc) entries, recall that ![m](https://wikimedia.org/api/rest_v1/media/math/render/svg/0a07d98bb302f3856cbabc47b2b9016692e3f7bc) is the number of bits in the hash key.

The ![i^{th}](https://wikimedia.org/api/rest_v1/media/math/render/svg/9c454bb35f050556d361ee85e06ca923b16a3bf4) entry of node ![n](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b) will contain ![successor((n+2^{i-1})\,\bmod\,2^m)](https://wikimedia.org/api/rest_v1/media/math/render/svg/6963c86821215f9a50af32995240d47c986949d0). The first entry of finger table is actually the node's immediate successor (and therefore an extra successor field is not needed). 

Every time a node wants to look up a key ![k](https://wikimedia.org/api/rest_v1/media/math/render/svg/c3c9a2c7b599b37105512c5d570edc034056dd40), it will pass the query to the closest successor or predecessor (depending on the finger table) of ![k](https://wikimedia.org/api/rest_v1/media/math/render/svg/c3c9a2c7b599b37105512c5d570edc034056dd40) in its finger table (the "largest" one on the circle whose ID is smaller than ![k](https://wikimedia.org/api/rest_v1/media/math/render/svg/c3c9a2c7b599b37105512c5d570edc034056dd40)), until a node finds out the key is stored in its immediate successor.

With such a finger table, the number of nodes that must be contacted to find a successor in an *N*-node network is ![O(\log N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/14eea297b4387decf341763c39dc038e05744272). 

[![If two nodes are at a distance 11 apart along the ring (i.e., there are 10 nodes between them), it takes three hops to send a message from one to the other. The first hop covers a distance of 8 units, the second 2 units, and the final hop 1 unit.](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Chord_route.png/250px-Chord_route.png)](https://en.wikipedia.org/wiki/File:Chord_route.png)

The routing path between nodes A and B. Each hop cuts the remaining distance in half (or better).

1. Node N wishes to find the successor of key **K**
2. Wish to find the **upper bond** of the number of steps it takes for finding the key
3. The node store the key called `f` and f is at most have 2^i-1^ distance from the previous node called `p`
4. After `t`'s loop the remaining distance is 2^m^/2^t^ (E.g. assume the t is 0 applied to the longest distacne 2^i-1^)
5. After ![\log N](https://wikimedia.org/api/rest_v1/media/math/render/svg/54e31347d160d1e54a70f79b23038030f33b6bf0) steps, the remaining distance is at most ![2^m / N](https://wikimedia.org/api/rest_v1/media/math/render/svg/77316633a5a77df5c4f3eff98d5d6d3f8925a426). 
6. Because nodes are distributed uniformly at random along the identifier circle, the expected number of nodes falling within an interval of this length is 1, and with high probability, there are fewer than ![\log N](https://wikimedia.org/api/rest_v1/media/math/render/svg/54e31347d160d1e54a70f79b23038030f33b6bf0) such nodes. Because the message always advances by at least one node, it takes at most ![\log  N](https://wikimedia.org/api/rest_v1/media/math/render/svg/54e31347d160d1e54a70f79b23038030f33b6bf0) steps for a message to traverse this remaining distance. The total expected routing time is thus ![O(\log N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/14eea297b4387decf341763c39dc038e05744272).

### Node join

Whenever a new node joins, three invariants should be maintained (the first two ensure correctness and the last one keeps querying fast):

1. Each node's successor points to its immediate successor correctly.
2. Each key is stored in ![successor(k)](https://wikimedia.org/api/rest_v1/media/math/render/svg/0d7151defafe837a78ed2433cb004c3bd2411db9).
3. Each node's finger table should be correct.

To satisfy these invariants, a *predecessor* field is maintained for each node. As the successor is the first entry of the finger table, we do not need to maintain this field separately any more. The following tasks should be done for a newly joined node ![n](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b):

1. Initialize node ![n](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b) (the predecessor and the finger table).
2. Notify other nodes to update their predecessors and finger tables.
3. The new node takes over its responsible keys from its successor.

The predecessor of ![n](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b) can be easily obtained from the predecessor of ![successor(n)](https://wikimedia.org/api/rest_v1/media/math/render/svg/e899d0a441b4194e39e7c6c35e6b39d8aa028bb7) (in the previous circle). As for its finger table, there are various initialization methods. The simplest one is to execute find successor queries for all ![m](https://wikimedia.org/api/rest_v1/media/math/render/svg/0a07d98bb302f3856cbabc47b2b9016692e3f7bc)entries, resulting in ![O(M\log N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/09eb5b9fbaa0b8b1e1ddafe192642825cef83142) initialization time. A better method is to check whether ![i^{th}](https://wikimedia.org/api/rest_v1/media/math/render/svg/9c454bb35f050556d361ee85e06ca923b16a3bf4) entry in the finger table is still correct for the ![(i+1)^{th}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2d5b302c449ca77ccfdeffd6d15a4fcf7a7346e8) entry. This will lead to ![O(\log^2 N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/9e31a0855c7eda8b8434c6ea152bee92bd19f50c). The best method is to initialize the finger table from its immediate neighbours and make some updates, which is ![O(\log N)](https://wikimedia.org/api/rest_v1/media/math/render/svg/14eea297b4387decf341763c39dc038e05744272).



### Stabilization

To ensure correct lookups, all successor pointers must be up to date. Therefore, a stabilization protocol is running periodically in the background which updates finger tables and successor pointers.

The stabilization protocol works as follows:

- Stabilize(): n asks its successor for its predecessor p and decides whether p should be n‘s successor instead (this is the case if p recently joined the system).
- Notify(): notifies n‘s successor of its existence, so it can change its predecessor to n
- Fix_fingers(): updates finger tables
