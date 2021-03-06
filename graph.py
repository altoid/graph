from pprint import pprint, pformat
import collections
import random

class GraphException(Exception):
    pass


class Node(object):

    def __init__(self, label):
        self._label = label

    def __str__(self):
        return '%s' % self._label

    def __repr__(self):
        return "Node('%s')" % (self._label)

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented

        return self._label == other._label

    def __hash__(self):
        return hash(self._label)

    def __cmp__(self, other):
        if not isinstance(other, Node):
            raise NotImplemented

        return cmp(self._label, other._label)

    def show_ids(self, tag):
        print '=' * 11, tag, '=' * 11
        print repr(self)
        print id(self)
        print id(self._label)
        
    @property
    def label(self):
        return self._label


class Edge(object):
    def __init__(self, origin, terminus, cost):
        self._origin = origin
        self._terminus = terminus
        self._cost = cost

    def __str__(self):
        return "(%s - %s - %s)" % (self._origin, self._cost, self._terminus)

    def __hash__(self):
        return hash((self.origin, self.terminus, self.cost))

    def __eq__(self, other):
        if not isinstance(other, Edge):
            raise NotImplemented

        return self.origin == other.origin and self.terminus == other.terminus and self.cost == other.cost

    @property
    def origin(self):
        return self._origin

    @property
    def terminus(self):
        return self._terminus

    @property
    def cost(self):
        return self._cost


class DGraph(object):
    '''
    directed graph.
    '''
    # implemented as a dictionary that maps nodes to lists of
    # tuples:  (Node, cost) which indicate the cost of the path.

    def __init__(self):
        self.adj_list = {}

    def __nonzero__(self):
        # returns true if the graph has > 0 nodes
        return len(self.adj_list) > 0

    def __len__(self):
        # returns the number of nodes in the graph.
        return len(self.adj_list)

    def addnode(self, n):
        if n in self.adj_list:
            raise GraphException("node %s is already in the graph" % n)
        self.adj_list[n] = list()

    def addnodes(self, *nodes):
        for n in nodes:
            self.addnode(n)

    def contains(self, n):
        return n in self.adj_list

    def addedge(self, a, b, cost=1):
        '''
        add an edge from a to be with default cost 1
        '''
        if a not in self.adj_list:
            raise GraphException("origin %s not in graph" % a)

        if b not in self.adj_list:
            raise GraphException("terminus %s not in graph" % b)

        edge = (b, cost)
        self.adj_list[a].append(edge)

    def dump(self):
        pprint(self.adj_list)

    '''
    return the nodes in the graph, as a list
    '''
    def nodes(self):
        for k in self.adj_list.keys():
            yield k

    def neighbors(self, n):
        if not self.contains(n):
            raise GraphException("node %s not in graph" % n)

        sorted_neighbors = sorted(self.adj_list[n], key=lambda n: n[0]._label)
        for k in sorted_neighbors:
            yield k[0]

    def edges(self):
        for n in self.nodes():
            for arc in self.adj_list[n]:
                yield Edge(n, arc[0], arc[1])

    def dijkstra(self, n):
        # single-source shortest pair problem
        if n not in self.adj_list:
            raise GraphException("node %s not in graph" % n)

        bigs = set([n])
        #print "S: %s" % bigs
        bigv = {k for k in self.adj_list.keys()}
        diff = bigv - bigs

        # construct dict mapping (origin, terminus) to cost
        bigc = {}
        for e in self.edges():
            bigc[(e.origin, e.terminus)] = e.cost
        #print "bigc:  %s" % pformat(bigc)
        bigd = {x: None for x in diff}
        for x in self.adj_list[n]:
            if (n, x[0]) in bigc:
                bigd[x[0]] = bigc[(n, x[0])]

        while len(bigs) < len(self):
            # find the node in diff where v (cost) is minimum

            x = filter(lambda x: bigd[x] is not None, diff)
            x = [(i, bigd[i]) for i in x]
            #print pformat(x)
            w, mincost = min(x, key=lambda x: x[1])
            #print w, mincost
            diff.remove(w)
            bigs.add(w)
            #print "S: %s" % bigs
            for v in diff:
                if (w, v) not in bigc:
                    continue

                if not bigd[v]:
                    bigd[v] = bigd[w] + bigc[(w, v)]
                    continue

                bigd[v] = min(bigd[v], bigd[w] + bigc[(w, v)])

        print "d: %s" % pformat(bigd)


class UGraph(DGraph):
    '''
    implements an undirected graph.
    '''

    def __init__(self):
        super(UGraph, self).__init__()

    def addedge(self, a, b, cost=1):
        super(UGraph, self).addedge(a, b, cost)
        super(UGraph, self).addedge(b, a, cost)

    def edges(self):
        # since this is an undirected graph, we have to be careful about not putting back-and-forth edges into the
        # result set.  we'll put edges in where the origin is lexicographically less than the terminus

        for n in self.nodes():
            for arc in self.adj_list[n]:
                a1 = n
                a2 = arc[0]
                if a1 < a2:
                    yield Edge(a1, a2, arc[1])

##########    ##########    ##########    ##########    ##########


def _next_unvisited_neighbor(g, n, visited):
    adj_list = sorted([x[0] for x in g.adj_list[n]], key=lambda n: n._label)
    for k in adj_list:
        if k not in visited:
            return k


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


def getpartitions(g):
    # for the given graph, return its disjoint subgraphs.  if the graph isn't partitioned, just return the the
    # graph.  if it is, return one node from each subgraph.
    #
    # todo - this will only work for undirected graphs.  if the graph is directed, we can't traverse the subgraphs
    # todo - whose member nodes we are returning.

    result = []

    # idea:  pick a node and do DFS on the graph.  if there are any nodes we still haven't visited, do it again.
    unvisited = set([n for n in g.nodes()])
    while len(unvisited) > 0:
        stack = []
        visited = set()

        n = unvisited.pop()
        stack.append(n)
        visited.add(n)

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
                unvisited.remove(k)

        # visited now has all the nodes in the subgraph.  make a new graph out of them.
        subgraph = UGraph()
        for n in visited:
            subgraph.addnode(n)
            subgraph.adj_list[n] = list(g.adj_list[n])
        result.append(subgraph)

    return result


def kruskal(g):
    # return a MST for this graph using kruskal's algorithm.

    # make a dict mapping each node to a set containing that node.
    lookup = {}
    for n in g.nodes():
        lookup[n] = set([n])

    mstedges = set()
    allnodes = set([n for n in g.nodes()])
    edges = sorted([e for e in g.edges()], key=lambda x: x.cost)
    for ex in edges:
        sorigin = lookup[ex.origin]
        sterminus = lookup[ex.terminus]

        # if the nodes of this edge are already in some set, skip it, because we'd introduce a cycle.
        if ex.origin in sorigin and ex.terminus in sorigin:
            continue

        if ex.origin in sterminus and ex.terminus in sterminus:
            continue

        tmpset = sorigin | sterminus
        for n in tmpset:
            lookup[n] = tmpset
        mstedges.add(ex)

        if tmpset == allnodes:
            break

    returnme = UGraph()
    for n in allnodes:
        returnme.addnode(n)

    for ex in mstedges:
        returnme.addedge(ex.origin, ex.terminus, ex.cost)
    return returnme
