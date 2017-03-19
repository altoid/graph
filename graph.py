import pprint
import collections

class GraphException(Exception):
    pass

class Node(object):

    def __init__(self, label):
        self._label = label

    def __str__(self):
        return '%s' % self._label

    def __repr__(self):
        return 'Node(%s)' % (self._label)

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented

        if self._label != other._label:
            return False

        return True

    def __hash__(self):
        return hash(self._label)
    
    def show_ids(self, tag):
        print '=' * 11, tag, '=' * 11
        print repr(self)
        print id(self)
        print id(self._label)
        
    @property
    def label(self):
        return self._label
    
class UGraph(object):
    '''
    implements an undirected graph.  there can be at most one # edge
    directly connecting two nodes.
    '''
    # implemented as a dictionary that maps nodes to sets
    # of nodes.  the sets represent adjacent nodes.
    # this is an undirected graph, so for an edge between two
    # nodes, each appears as a key and is in the other's adjacency
    # set.  because we are using a set, there can be at most one
    # edge directly connecting two nodes.

    def __init__(self):
        self.adj_list = {}

    def addNode(self, n):
        if n not in self.adj_list:
            self.adj_list[n] = set()

    def contains(self, n):
        return n in self.adj_list

    def dump(self):
        pp = pprint.PrettyPrinter()
        
        pp.pprint(self.adj_list)

    def addEdge(self, a, b):
        if not self.contains(a):
            raise GraphException("node %s not in graph" % a)

        if not self.contains(b):
            raise GraphException("node %s not in graph" % b)

        s = self.adj_list[a]
        s.add(b)

        s = self.adj_list[b]
        s.add(a)
        
    '''
    return the nodes in the graph, as a list
    '''
    def nodes(self):
        return self.adj_list.keys()


    def neighbors(self, n):
        if not self.contains(n):
            raise GraphException("node %s not in graph" % n)

        sorted_neighbors = sorted(self.adj_list[n], key=lambda n: n._label)
        for k in sorted_neighbors:
            yield k

##########    ##########    ##########    ##########    ##########

def _next_unvisited_neighbor(g, n, visited):

    adj_list = sorted(g.adj_list[n], key=lambda n: n._label)
    for k in adj_list:
        if k not in visited:
            return k
    return None

def dfs(g, n):
    # non-recursive implementation
    
    if not g.contains(n):
        raise GraphException("node %s not in graph" % n)
    
    stack = []
    visited = set()
    
    stack.append(n)
    visited.add(n)
    result = str(n)
    
    # look at node on top of stack
    # if it has an unvisited neighbor,
    # mark it visited and put it at top of stack
    # otherwise pull it off
    
    while len(stack) > 0:
        top = stack[-1]
        # get next unvisited neighbor
        k = _next_unvisited_neighbor(g, top, visited)
        if k is None:
            stack.pop()
        else:
            stack.append(k)
            visited.add(k)
            result += str(k)

    return result
            
def bfs(g, n):
    # non-recursive implementation

    if not g.contains(n):
        raise GraphException("node %s not in graph" % n)
    
    q = collections.deque()
    visited = set()

    # look at front of queue
    # put all unvisited adj_list on queue, mark visited
    # dequeue

    q.append(n)
    visited.add(n)
    result = ""

    while len(q) > 0:

        front = q.popleft()
        result += str(front)
        
        # enqueue all unvisited adj_list
        adj_list = g.neighbors(front)
        for k in adj_list:
            if k not in visited:
                q.append(k)
                visited.add(k)
                
    return result

            
def bfs_zigzag(g, n):
    # non-recursive implementation

    if not g.contains(n):
        raise GraphException("node %s not in graph" % n)
    
    q = collections.deque()
    visited = set()

    q.append(n)
    visited.add(n)
    result = str(n)

    while len(q) > 0:

        front = q.popleft()
        
        # enqueue all unvisited adj_list
        adj_list = g.neighbors(front)
        for k in adj_list:
            if k not in visited:
                q.append(k)
                visited.add(k)
                result += str(k)

    return result

            
