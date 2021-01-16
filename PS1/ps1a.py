from ps1_partition import get_partitions
import time
import numpy as np

def load_cows(filename):
 inFile = open(filename, 'r')
 wordlist = {}
 for line in inFile:
   line=line.rstrip()
   tmp=line.split(",")
   wordlist[tmp[0]]=tmp[1]
 #print len(wordlist), "words loaded."
 return wordlist

def greedy_cow_transport(cows,limit=10):
 def maximum_weight(cows): 
    maxW=max(C.values())
    for key in C.keys():
     if(C[key]==maxW): 
      maxKey=key 
      break
    return (int(maxW), maxKey)

 #taking a trip
 C=cows.copy()
 C2=cows.copy()
 trip=[]
 while (len(C2)!=0):
  taken=[]
  actual_w=0
  while(True):
   if(actual_w>limit or len(C)==0): break
   maxW,maxKey=maximum_weight(C)
   if(actual_w+maxW<=10): 
    actual_w+=maxW
    taken.append(maxKey)
   del C[maxKey]
  for take in taken:
    del C2[take]
  trip.append(taken)
  C=C2.copy() 
 return trip 

def brute_force_cow_transport(cows,limit=10):
  l=[]
  #building a set using the keys
  S=[]
  for c in cows.keys():
   S.append(c)
  S=set(S)

  for partition in get_partitions(cows.keys()):
   #print(partition)
   l.append(partition)
 
  def weight_calculator(L):
   w=0
   for e in L:
     w+=int(cows[e])  
   return w
  
  def delete_elements(ll,S):
   for elem in ll:
    S2=set(elem)
    S=S.difference(S2) 
   return S

  trip=[]
  for elem in l:
   Flag=0
   for i in range(len(elem)):
    if(weight_calculator(elem[i])<=10): 
     Flag+=1
   if(Flag==len(elem)):
    trip.append(elem)
    S=delete_elements(elem,S)
   if(len(S)==0): break
     
  return trip[0]

def compare_cow_transport_algorithms():
  cows=load_cows("ps1_cow_data.txt")
  start=time.time()
  trip1=greedy_cow_transport(cows)
  end=time.time()
  print "time using greedy:", end-start
  print "trips:", trip1, "number of trips:", len(trip1),"\n"
  start=time.time()
  trip2=brute_force_cow_transport(cows)
  end=time.time()
  print "time using brute force:", end-start
  print "trips:", trip2, "number of trips:", len(trip2)
  

compare_cow_transport_algorithms()






