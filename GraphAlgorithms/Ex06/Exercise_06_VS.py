
#Vid Sustar,
# student nr: 1901627,
# Graph algorithms, 2019,
# 6th homework




#TASK:
"""
Find a maximum flow in a given network. Use the Ford–Fulkerson algorithm.
• Bonus points: 5
• INPUT: list of directed edges and their capacities in CSV table, the source and the sink
vertex. The format of CSV table: Vertex1, Vertex2, capacity, id.
• OUTPUT: CSV table with flow value assigned to each edge and the max-flow value. The
format of the CSV table: edge_id, flow_value
• The benchmark graph is available on Moodle as CSV and PDF files. The maxflow for the
graph is: 12; SRC:n45, SINK:n52
"""
#######################importing needed libraries

import csv
import numpy as np
from collections import defaultdict
import copy
import os

path = os.getcwd()################################################# PLEASE SET THE RIGHT PATH  (or put input file to same folder where this script is) ####################################################################
print(path)
numnodes=0

nonDirected = 0

#####################reading the file

source="source"#input("Please type name of the source: "))
sink="sink"#input("Please type name of the sink: "))

#creating list of edges as a list of tuples, with starting, ending node, weight, edge id
edges=[]
nodeslist=[]
with open(path+'\\benchmark6.csv') as f:
    next(f) # Skip header
    for row in csv.reader(f, delimiter='\t'):
        tupletoadd=((row[0]),(row[1]),(row[2]),(row[3]))
        nodeslist.append(row[0])
        nodeslist.append(row[1])
        edges.append(tupletoadd)
        if nonDirected:
            tupletoadd = ((row[1]),(row[0]), (row[2]),(row[3]))#reversed order of nodes for nondirected graph
            edges.append(tupletoadd)

print ("EDGES: ",edges)
print("number of edges: ",len(edges))
print("NODESLIST: ", nodeslist)
nodestemp=[]
nodes=[]
for node in nodeslist:
    if node not in nodestemp:
        nodestemp.append(node)

nodes = sorted(set(nodeslist))#, key=len)
nodes.remove(source)
nodes.remove(sink)
nodes.insert(0, source)
nodes.append(sink)
print("sorted nodes", nodes)
print("number of nodes: ",len(nodes))
nNodes=len(nodes)

###################################################################################################################
#making indices dictionary for nodes
nodesInd={}
nodesListSimp=[]
for n in range(len(nodes)):
    nodesInd.update({n:nodes[n]})
    nodesListSimp.append(n)
print("nodesInd: ",nodesInd)
print("nodesListSimp: ",nodesListSimp)  #nodeslist!!!!


def NInd(node): #function to return key by value (node index from node name)#####################
    return list(nodesInd.keys())[list(nodesInd.values()).index(node)]
def IndN(key): #function to return value by key (node name from node index)######################
    return nodesInd.get(key)

##############################################################################################
graphAdjMtrx=[]
graphEdgList=[]
for z in range(nNodes):
    sublist=[]
    for x in range(nNodes):
        sublist.append(0)
    graphAdjMtrx.append(sublist)

for z in range(nNodes):
    sublist = []
    for x in range(nNodes):
        sublist.append(0)
        # print(sublist)
    graphEdgList.append(sublist)
edgesFlowCap={}
#populating two matrices from EDGES list
for m in range(len(edges)):
    graphAdjMtrx[NInd(edges[m][0])][NInd(edges[m][1])]=int(edges[m][2])
for m in range(len(edges)):
    graphEdgList[NInd(edges[m][0])][NInd(edges[m][1])]=edges[m][3]
    graphEdgList[NInd(edges[m][1])][NInd(edges[m][0])] = edges[m][3]
for m in range(len(edges)):
    edgesFlowCap.update({edges[m][3]:int(edges[m][2])})

origgraph=copy.deepcopy(graphAdjMtrx)
final=copy.deepcopy(graphAdjMtrx)
##########################################################################################

prtTrck=[]
Inf=99999999999 #max element checker

def BrFrSc(resGr,source,sink,prtTrck):
    que=[] #que array
    vstd=[] #vstd array
    #initialization
    for x in range(0,nNodes): #parent array
        vstd.append(0)
    que.append(source)#append the source to the que, initialy source
    vstd[source]=True #setting the vstd to true
    prtTrck[source]=-1 #initial parent
    while (len(que)!=0): #while que not empty
        u=que.pop(0) #first in first out, pop of the u element
        for v in range(0,nNodes): #for all the u-v
            if ((vstd[v]==False) and (resGr[u][v]>0)):#if there is a path between u and v, v is not vstd and auxil graph not 0
                que.append(v) #add them to the que
                vstd[v]=True#vstd becomes true
                prtTrck[v]=u #we put u into parent value of v node
    if (vstd[sink]):
        return True
    else:
        return False #if sink can not be accesed then the whole thing stops, all the capacity was used

def FFAl(graph, source, sink):
    u,v=0,0 #pointers to elements, nodes in the graph
    resGr=copy.copy(graph) #auxiliary graph to make changes to
    maxFlow=0 #keep track of the max flow..

    while (BrFrSc(resGr,source,sink,prtTrck)): #true or false
        pthFl=Inf
        v=sink

        while (v!=source): #tracking through parents through path

            u=prtTrck[v]
            pthFl=min(pthFl, resGr[u][v]) #looks for the new pthFl, always smaller than Inf
            v=prtTrck[v]
        v = sink
        while (v != source):
            u=prtTrck[v]
            resGr[u][v]=resGr[u][v]-pthFl  #updating new flow through elements of the path
            resGr[v][u] =resGr[v][u] + pthFl #adding pthFl to elements of oposite direction
            v = prtTrck[v]

        maxFlow = maxFlow+pthFl #updating maxflow'
    for z in range(nNodes):
        for zz in range(nNodes):
            if (final[z][zz]!=0):
                final[z][zz]=origgraph[z][zz]-resGr[z][zz]
                edgesFlowCap.update({graphEdgList[z][zz]: final[z][zz]})
    return maxFlow

def main():
    for x in range(0,nNodes):
        prtTrck.append(0) #appending the number of elements equal to number of vertices to prtTrck
        #print("1 len(prtTrck): ",len(prtTrck))
    print("\nMAX FLOW IS: ", FFAl(graphAdjMtrx,0,nNodes-1)) #0-source, n-1 sink

main()
print("EDGES FLOW: ",edgesFlowCap)

###########################################################################################################

with open('edge-flow-value.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for key, value in edgesFlowCap.items():
       writer.writerow([key, value])

