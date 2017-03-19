#!/usr/bin/env python

import unittest
import graph

class TestNode(unittest.TestCase):

    def test_init(self):
        n = graph.Node('a')
        self.assertEqual('a', str(n))
        self.assertEqual('a', n.label)
        self.assertEqual('Node(a)', repr(n))
        
    def test_readonly(self):
        n = graph.Node('a')
        with self.assertRaises(AttributeError):
            n.label = 'b'

    def test_equals(self):

        m = graph.Node('aoeu')
        n = graph.Node('aoeu')

        self.assertEqual(n, n)
        self.assertEqual(m, n)
        
        q = graph.Node('ueoa')
        self.assertNotEqual(q, m)


class TestDGraph(unittest.TestCase):

    def test_basic(self):
        g = graph.DGraph()
        a = graph.Node('a')
        b = graph.Node('b')

        self.assertFalse(g.contains(a))

        # neither node is in the graph
        with self.assertRaises(Exception):
            g.addEdge(a, b)

        g.addNode(a)
        self.assertTrue(g.contains(a))

        # can't add a node twice
        with self.assertRaises(graph.GraphException):
            g.addNode(a)

        # still can't add the edge because b isn't there
        with self.assertRaises(Exception):
            g.addEdge(a, b)

        g.addNode(b)
        g.addEdge(a, b)

        # adding an edge twice is ok
        g.addEdge(a, b)

        g.dump()


#class TestMultipleEdges(unittest.TestCase):
#    '''
#    rewrote graph class so that we can have multiple edges between nodes
#    '''
#    def test_basic(self):
#        g = graph.UGraph()
#        n1 = graph.Node('a')
#        n2 = graph.Node('b')
#        g.addEdge(n1, n2)
#        g.addEdge(n1, n2)

class TestUGraph(unittest.TestCase):

    def test_basic(self):
        g = graph.UGraph()
        self.assertEqual(0, len(g.adj_list))
        self.assertEqual(0, len(g.nodes()))

    def test_addNode(self):
        g = graph.UGraph()
        n1 = graph.Node('a')
        
        g.addNode(n1)
        self.assertEqual(1, len(g.nodes()))
        
        g.addNode(n1)
        self.assertEqual(1, len(g.nodes()))

        n2 = graph.Node('a')

        g.addNode(n2)
        self.assertEqual(1, len(g.nodes()))

        n3 = graph.Node('b')
        g.addNode(n3)
        self.assertEqual(2, len(g.nodes()))

        self.assertTrue(g.contains(n1))
        self.assertTrue(g.contains(n2))
        self.assertTrue(g.contains(n3))

        n4 = graph.Node('notMe')
        self.assertFalse(g.contains(n4))
        
    def test_addEdge(self):

        g = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        with self.assertRaises(Exception):
            g.addEdge(a, b)

        g.addNode(a)
        with self.assertRaises(Exception):
            g.addEdge(a, b)

        g.addNode(b)
        g.addEdge(a, b)

    def test_sorting(self):
        # make sure that a node's neighbors are
        # presented in sorted order.

        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')

        gr.addNode(a)
        gr.addNode(b)
        gr.addNode(c)
        gr.addNode(d)
        gr.addNode(e)
        gr.addNode(f)
        gr.addNode(g)
        gr.addNode(h)
        
        gr.addEdge(a, h)
        gr.addEdge(a, g)
        gr.addEdge(a, f)
        gr.addEdge(a, e)
        gr.addEdge(a, d)
        gr.addEdge(a, c)
        gr.addEdge(a, b)

        k = ""
        for n in gr.neighbors(a):
            k += str(n)

        self.assertEqual('bcdefgh', k)

    def test_dfs(self):

        # cf. https://www.youtube.com/watch?v=zLZhSSXAwxI

        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')

        gr.addNode(a)
        gr.addNode(b)
        gr.addNode(c)
        gr.addNode(d)
        gr.addNode(e)
        gr.addNode(f)
        gr.addNode(g)
        gr.addNode(h)
        
        gr.addEdge(a, b)
        gr.addEdge(a, g)
        gr.addEdge(a, d)

        gr.addEdge(b, e)
        gr.addEdge(b, f)

        gr.addEdge(c, f)
        gr.addEdge(c, h)

        gr.addEdge(d, f)
        gr.addEdge(e, g)

        outsider = graph.Node('mr_lonely')
        
        with self.assertRaises(graph.GraphException):
            graph.dfs(gr, outsider)

        r = graph.dfs(gr, a)
        self.assertEqual('abegfchd', r)

    def test_bfs_simple(self):

        # graph with one vertex and no edges
        # graph with one vertex and one (loop) edge

        gr = graph.UGraph()
        a = graph.Node('a')
        
        outsider = graph.Node('mr_lonely')
        
        with self.assertRaises(graph.GraphException):
            graph.bfs(gr, outsider)

        gr.addNode(a)
        gr.addEdge(a, a)

        graph.bfs(gr, a)
        

    def test_bfs(self):

        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')

        gr.addNode(a)
        gr.addNode(b)
        gr.addNode(c)
        gr.addNode(d)
        gr.addNode(e)
        gr.addNode(f)
        gr.addNode(g)
        gr.addNode(h)
        
        gr.addEdge(a, b)
        gr.addEdge(a, g)
        gr.addEdge(a, d)

        gr.addEdge(b, e)
        gr.addEdge(b, f)

        gr.addEdge(c, f)
        gr.addEdge(c, h)

        gr.addEdge(d, f)
        gr.addEdge(e, g)

        r = graph.bfs(gr, a)
        self.assertEqual('abdgefch', r)

    def test_zigzag(self):
        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')
        i = graph.Node('i')
        j = graph.Node('j')

        gr.addNode(a)
        gr.addNode(b)
        gr.addNode(c)
        gr.addNode(d)
        gr.addNode(e)
        gr.addNode(f)
        gr.addNode(g)
        gr.addNode(h)
        gr.addNode(i)
        gr.addNode(j)

        gr.addEdge(a, b)
        gr.addEdge(a, c)

        gr.addEdge(b, d)
        gr.addEdge(b, e)

        gr.addEdge(c, f)

        gr.addEdge(d, g)
        gr.addEdge(d, h)

        gr.addEdge(f, i)
        gr.addEdge(f, j)

        r = graph.bfs_zigzag(gr, a)
        self.assertEqual('abcdefghij', r)
