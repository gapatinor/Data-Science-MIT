# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

import unittest

#
# A set of data structures to represent graphs
#

class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # This function is necessary so that Nodes can be used as
        # keys in a dictionary, even though Nodes are mutable
        return self.name.__hash__()


class Edge(object):
    """Represents an edge in the dictionary. Includes a source and
    a destination."""
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest

    def __str__(self):
        return '{}->{}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, total_distance, outdoor_distance):
        self.src=src
        self.dest=dest
        self.total_distance=total_distance
        self.outdoor_distance=outdoor_distance

    def get_total_distance(self):
        return self.total_distance

    def get_outdoor_distance(self):
        return self.outdoor_distance

    def __str__(self):
        s=str(self.src)+"->"+str(self.dest)+\
        " ("+str(self.total_distance)+", "+str(self.outdoor_distance)+")"
        return s

class Digraph(object):
    """Represents a directed graph of Node and Edge objects"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}  # must be a dict of Node -> list of edges

    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them

    def get_edges_for_node(self, node):
        return self.edges[node]

    def childrenOf(self,node):
      S=self.edges[node]
      children=[]
      for child in S:
        children.append(child)
      children.pop(0)
      return children

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        if(node in self.nodes): raise ValueError("existing node")
        self.nodes.add(node)
        self.edges[node]=[] 

    def add_edge(self, edge):
        src=edge.get_source()
        dest=edge.get_destination()
        if not(src in self.nodes and dest in self.nodes):\
        raise ValueError("Node not in graph")        
        self.edges[src].append(edge)

    def getDistance(self,node1, node2):
        if not(node1 in self.nodes and node2 in self.nodes):
         raise ValueError("Node not in graph") 
        S=self.edges[node1]
        for child in S:
         if(child.get_destination()==node2):
          return (float(child.get_total_distance()), float(child.get_outdoor_distance())) 

        raise ValueError("nodes not existing")

'''
def totalCost(g,path):
 totalD=0.0
 outdoors=0.0
 for i in range(len(path)-1):
  total=g.getDistance(path[i],path[i+1])
  totalD+=total[0]
  outdoors+=total[1]
 return (totalD, outdoors)

a=Node("a")
b=Node("b")
c=Node("c")
e=Node("e")
f=Node("f")

e1=WeightedEdge(a,b,15,10)
e2=WeightedEdge(a,c,14,6)
e3=WeightedEdge(b,e,7,4)
e4=WeightedEdge(e,f,23,20)

g=Digraph()
g.add_node(a)
g.add_node(b)
g.add_node(c)
g.add_node(e)
g.add_node(f)

g.add_edge(e1)
g.add_edge(e2)
g.add_edge(e3)
g.add_edge(e4)
print g

path=[a,b,e,f]
print totalCost(g,path)'''









