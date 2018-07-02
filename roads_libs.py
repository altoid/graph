#!/usr/bin/env python

import graph


def evaluate(mst, libcost, roadcost):
    nnodes = len(mst)
    nroads = nnodes - 1

    # rule of thumb:
    # if cost of lib <= cost of road, rebuild all libs and no roads
    # if cost of lib > cost of road, rebuild 1 lib & all roads

    if libcost > roadcost:
        return libcost + nroads * roadcost
    return nnodes * libcost


def solution(ncities, libcost, roadcost, edges):
    # construct the graph
    gr = graph.UGraph()
    node_dict = {}
    for i in xrange(1, ncities + 1):
        node_dict[i] = graph.Node("%s" % i)
        gr.addnode(node_dict[i])
    for e in edges:
        gr.addedge(node_dict[e[0]], node_dict[e[1]], roadcost)

    subgraphs = graph.getpartitions(gr)
    msts = map(lambda x: graph.kruskal(x), subgraphs)
    total = 0
    for mst in msts:
        cost = evaluate(mst, libcost, roadcost)
        total += cost
    return total


if __name__ == '__main__':
    edges = [[1, 2], [3, 1], [2, 3]]
    total = solution(3, 2, 1, edges)
    print total

    total = solution(6, 2, 5,
                     [[1,3], [3,4], [2,4], [1,2], [2,3], [5,6]])
    print total
