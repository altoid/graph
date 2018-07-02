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

    def test_cmp(self):
        a = graph.Node('aaa')
        b = graph.Node('bbb')
        c = graph.Node('ccc')
        self.assertTrue(b == b)
        self.assertTrue(a < b)
        self.assertTrue(b < c)
        self.assertTrue(c > a)


class TestDGraph(unittest.TestCase):

    def test_bool(self):
        g = graph.UGraph()
        self.assertFalse(g)
        self.assertEqual(0, len(g))
        n = graph.Node('hello')
        g.addnode(n)
        self.assertTrue(g)
        self.assertEqual(1, len(g))

    def test_basic(self):
        g = graph.DGraph()
        a = graph.Node('a')
        b = graph.Node('b')

        self.assertFalse(g.contains(a))

        # neither node is in the graph
        with self.assertRaises(Exception):
            g.addedge(a, b)

        g.addnode(a)
        self.assertTrue(g.contains(a))

        # can't add a node twice
        with self.assertRaises(graph.GraphException):
            g.addnode(a)

        # still can't add the edge because b isn't there
        with self.assertRaises(Exception):
            g.addedge(a, b)

        g.addnode(b)
        g.addedge(a, b)

        # adding an edge twice is ok
        g.addedge(a, b)


#class TestMultipleEdges(unittest.TestCase):
#    '''
#    rewrote graph class so that we can have multiple edges between nodes
#    '''
#    def test_basic(self):
#        g = graph.UGraph()
#        n1 = graph.Node('a')
#        n2 = graph.Node('b')
#        g.addedge(n1, n2)
#        g.addedge(n1, n2)

class TestUGraph(unittest.TestCase):

    def setUp(self):
        # sedgewick, p. 374

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
        k = graph.Node('k')
        l = graph.Node('l')
        m = graph.Node('m')

        gr.addnodes(a, b, c, d, e, f, g, h, i, j, k, l, m)

        gr.addedge(h, i)

        gr.addedge(j, k)
        gr.addedge(j, m)
        gr.addedge(j, l)
        gr.addedge(l, m)

        gr.addedge(a, b)
        gr.addedge(a, c)
        gr.addedge(a, f)
        gr.addedge(a, g)
        gr.addedge(d, f)
        gr.addedge(f, e)
        gr.addedge(e, g)

        self.sedgewick = gr

    def test_addNode(self):
        g = graph.UGraph()
        n1 = graph.Node('a')
        
        g.addnode(n1)
        self.assertEqual(1, len(g))

        with self.assertRaises(graph.GraphException):
            g.addnode(n1)

        n2 = graph.Node('a')

        with self.assertRaises(graph.GraphException):
            g.addnode(n2)

        self.assertEqual(1, len(g))

        n3 = graph.Node('b')
        g.addnode(n3)
        self.assertEqual(2, len(g))

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
            g.addedge(a, b)

        g.addnode(a)
        with self.assertRaises(Exception):
            g.addedge(a, b)

        g.addnode(b)
        g.addedge(a, b)

    def test_addNodes(self):
        # new convenience method
        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')
        gr.addnodes(a, b, c, d, e, f, g, h)
        self.assertEqual(8, len(gr))

    def test_nodes_generator(self):
        # new convenience method
        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')
        h = graph.Node('h')
        gr.addnodes(a, b, c, d, e, f, g, h)
        control = [a, b, c, d, e, f, g, h]
        nodes = sorted([n for n in gr.nodes()])
        self.assertEqual(control, nodes)

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

        gr.addnodes(a, b, c, d, e, f, g, h)

        gr.addedge(a, h)
        gr.addedge(a, g)
        gr.addedge(a, f)
        gr.addedge(a, e)
        gr.addedge(a, d)
        gr.addedge(a, c)
        gr.addedge(a, b)

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

        gr.addnodes(a, b, c, d, e, f, g, h)
        
        gr.addedge(a, b)
        gr.addedge(a, g)
        gr.addedge(a, d)

        gr.addedge(b, e)
        gr.addedge(b, f)

        gr.addedge(c, f)
        gr.addedge(c, h)

        gr.addedge(d, f)
        gr.addedge(e, g)

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

        gr.addnode(a)
        gr.addedge(a, a)

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

        gr.addnodes(a, b, c, d, e, f, g, h)
        
        gr.addedge(a, b)
        gr.addedge(a, g)
        gr.addedge(a, d)

        gr.addedge(b, e)
        gr.addedge(b, f)

        gr.addedge(c, f)
        gr.addedge(c, h)

        gr.addedge(d, f)
        gr.addedge(e, g)

        r = graph.bfs(gr, a)
        self.assertEqual('abdgefch', r)

    def test_getpartitions(self):
        # sedgewick, p. 374

        subgraphs = graph.getpartitions(self.sedgewick)
        self.assertEqual(3, len(subgraphs))
        results = []
        for sgr in subgraphs:
            # gimme a node from the graph, i don't care which
            nd = next(iter(sgr.nodes()))
            r = ''.join(sorted(list(graph.dfs(sgr, nd))))
            results.append(r)
        self.assertEqual(['abcdefg', 'hi', 'jklm'], sorted(results))

    def test_edges(self):
        for e in self.sedgewick.edges():
            print e

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

        gr.addnodes(a, b, c, d, e, f, g, h, i, j)

        gr.addedge(a, b)
        gr.addedge(a, c)

        gr.addedge(b, d)
        gr.addedge(b, e)

        gr.addedge(c, f)

        gr.addedge(d, g)
        gr.addedge(d, h)

        gr.addedge(f, i)
        gr.addedge(f, j)

        r = graph.bfs_zigzag(gr, a)
        self.assertEqual('abcdefghij', r)

    def test_kruskal(self):
        # https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
        gr = graph.UGraph()
        a = graph.Node('a')
        b = graph.Node('b')
        c = graph.Node('c')
        d = graph.Node('d')
        e = graph.Node('e')
        f = graph.Node('f')
        g = graph.Node('g')

        gr.addnodes(a, b, c, d, e, f, g)

        gr.addedge(a, d, 5)
        gr.addedge(a, b, 7)
        gr.addedge(b, c, 8)
        gr.addedge(b, d, 9)
        gr.addedge(b, e, 7)
        gr.addedge(c, e, 5)
        gr.addedge(d, e, 15)
        gr.addedge(d, f, 6)
        gr.addedge(f, e, 8)
        gr.addedge(e, g, 9)
        gr.addedge(f, g, 11)

        mst = graph.kruskal(gr)
        for ex in mst.edges():
            print ex
