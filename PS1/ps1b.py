global count
count=0

def calculateCost(L):
 cost=len(L)
 value=0
 for e in L:
  value+=e
 return (cost,value)


def dp_make_weight(egg_weights, target_weight,memo={}):
 toConsider=[]
 def backpack(toConsider,avail,limit):
  global count
  count+=1
  if(tuple(toConsider) in memo): return memo[tuple(toConsider)] 
  if(len(avail)==0):
   cost,value=calculateCost(toConsider)
   maxItem=(cost,value,toConsider)
   return maxItem
  else:
   next=toConsider+[avail[0]]
   remaining=avail[1:]
   withVal=backpack(next,remaining,limit)
   withoutVal=backpack(toConsider,remaining,limit)
   if(withVal[1]>withoutVal[1] and withVal[1]<=limit): 
    t=tuple(withVal[2])
    memo[t]=withVal
    return withVal
   elif(withVal[1]<withoutVal[1] and withoutVal[1]<=limit): 
    t=tuple(withoutVal[2])
    memo[t]=withoutVal
    return withoutVal
   else: 
    if(withVal[1]<=limit): return withVal
    else: return withoutVal
   
 return backpack(toConsider,egg_weights,target_weight)


def build_list(L,n):
 L2=L
 F=[]
 m=max(L)
 N=n//m
 Lp=[m]*N
 F.extend(Lp)
 for i in range(1,len(L)):
  m=max(L[i:])
  if(i<=2): Lp=[m]*1*N
  else: Lp=[m]*2*N
  F.extend(Lp)
 return F

egg_weights=[20,10,5,1]
n=99
L=build_list(egg_weights,n)

result=dp_make_weight(L,n)
print "best combination:", result[2]
print "number of callings using DP:", count














