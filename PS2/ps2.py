import unittest
from graph import Digraph, Node, WeightedEdge
import time

def load_map(map_filename):
 g=Digraph()
 infile=open(map_filename,"r") 
 
 for line in infile:
  coord=line.split()
  n1=Node(coord[0])
  n2=Node(coord[1])
  e=WeightedEdge(n1,n2,coord[2],coord[3])
  if(not g.has_node(n1)): g.add_node(n1)
  if(not g.has_node(n2)): g.add_node(n2)
  g.add_edge(e)
 return g

def totalCost(g,path):
 totalD=0.0
 outdoors=0.0
 for i in range(len(path)-1):
  total=g.getDistance(path[i],path[i+1])
  totalD+=total[0]
  outdoors+=total[1]
 return (totalD, outdoors)

def DFSW(graph, start, end, path=[],shortest=None):
 path=path+[start]
 if shortest!=None:
  if(totalCost(g,path)[0]>totalCost(g,shortest)[0]): return shortest
 if(start==end):  
  return path
 for node in g.get_edges_for_node(start):
  node=node.get_destination()
  if(node not in path):
    newPath=DFSW(graph,node, end, path,shortest)  
    if(newPath!=None):
     if(shortest==None): shortest=newPath
     else:
       if(totalCost(graph,shortest)[0]>totalCost(graph,newPath)[0]): shortest=newPath
 return shortest
  
def get_best_path(digraph,start,end):
  start=Node(start)
  end=Node(end)
  if(not digraph.has_node(start) or not digraph.has_node(end)):
   raise ValueError("Node not in graph")
  init=time.time() 
  best=DFSW(digraph, start, end)
  final=time.time()
  print "best path:", best, "total distance:", totalCost(g,best)[0], "outdoors:", totalCost(g,best)[1] 
  print "time using brute force:", final-init

g=load_map("mit_map.txt")
#print g
n1="32"
n2="13"
get_best_path(g,n1,n2)







