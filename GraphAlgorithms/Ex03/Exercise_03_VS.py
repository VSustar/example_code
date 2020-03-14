# Vid Sustar,
# student nr: 1901627,
# Graph algorithms, 2019,
# 3rd homework

#TASK:
"""
Project Task 3
• Find a minimum spanning tree for every connected component from
the graph
• Bonus points: 5
• INPUT: list of undirected non-negative weighted edges in CSV table.
• OUTPUT: a comma-separated list of edge labels forming the spanning
tree
• The benchmark graph is available on Moodle as CSV and PDF files.
The resulting spanning tree is available (on Moodle, as TXT file) as a
list of edge ids in the alphabetical order. The total weight of the
minimal spanning tree is 395. Note that in general a graph may have
more than one minimal-weight spanning tree
send to victor-bogdan.popescu@abo.fi
"""
#######################importing needed libraries
import os
import csv
import numpy as np

from collections import defaultdict

path = os.getcwd()
numnodes=0
nonDirected = 0

#creating list of edges as a list of tuples, with starting, ending node, weight, edge id
edges=[]
nodeslist=[]
with open(path+'\\benchmark3.csv') as f:
    next(f) # Skip header
    for row in csv.reader(f, delimiter='\t'):
        #print ("row[2][1:-1]",row[2])
        tupletoadd=((row[0]),(row[1]),int(row[2]),(row[3]))
        nodeslist.append(row[0])
        nodeslist.append(row[1])
        edges.append(tupletoadd)
        if nonDirected:
            tupletoadd = ((row[1]),(row[0]), int(row[2]), (row[3]))#reversed order of nodes for nondirected graph
            edges.append(tupletoadd)

print ("EDGES: ",edges)
print("number of edges: ",len(edges))
nodes = sorted(set(nodeslist))#, key=len)
print("number of nodes: ",len(nodes))
nNodes=len(nodes)

###################################################################################################################
#making indices dictionary for nodes
nodesInd={}
nodesListSimp=[]
for n in range(len(nodes)):
    nodesInd.update({n:nodes[n]})
    nodesListSimp.append(n)

def NInd(node): #function to return key by value (node index from node name)#####################
    return list(nodesInd.keys())[list(nodesInd.values()).index(node)]
def IndN(key): #function to return value by key (node name from node index)######################
    return nodesInd.get(key)
####################################################################################################################

#reading converting nodes to new indices
indedges=[]
for element in edges:
    tupletoadd = (NInd(element[0]), NInd(element[1]), int(element[2]), (element[3]))
    indedges.append(tupletoadd)

#initialising new tree (edges list)
TreeEdges=[]
#initialising V' (vertex list)
VertexDump=[]
#initialising V-V' (vertex list)
VertexRemain=nodesListSimp
VertexDump.append (VertexRemain[0])
VertexRemain.remove (VertexRemain[0])
edgesTemp=[]
indedges2= indedges.copy()
for v in VertexRemain:
    for edge in indedges:
        if ((edge[0]==v)&(edge[1]==VertexDump[0]) or (edge[1]==v)&(edge[0]==VertexDump[0])):
            edgesTemp.append(edge)

while (len(VertexRemain)!=0):
    counter=0
    for z in range(len(edgesTemp)):
        if(edgesTemp[z][2]==min(i[2] for i in edgesTemp)): #finding minimum weight edge
            if(edgesTemp[z][0] not in VertexDump):
                VertexDump.append(edgesTemp[z][0])
                VertexRemain.remove(edgesTemp[z][0])
                w=edgesTemp[z][0]
            if(edgesTemp[z][1] not in VertexDump):
                VertexDump.append(edgesTemp[z][1])#appending the node of min w. edge to V'
                VertexRemain.remove(edgesTemp[z][1])#removing the node of min w. edge from V
                w = edgesTemp[z][1]
            TreeEdges.append(edgesTemp[z][3]) #appending minimum weight edge
            counter=counter+1

    edgesTemp = []
    for v in VertexRemain:
        for edge in indedges:
            for dumped in VertexDump:
                if ((edge[0] == v) & (edge[1] == dumped) or (edge[1] == v) & (edge[0] == dumped)):
                    edgesTemp.append(edge)

print("RESULTING LIST OF ALPHABETICALLY ORDERED MIN SPAN TREE EDGES: ")
sortedTreeEdges=sorted(TreeEdges, key=lambda x: int(x[1:]))
print ("TreeEdges: ",sortedTreeEdges)

import csv

with open(path+'\\edge_labels.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, delimiter=',')#quoting=csv.QUOTE_ALL)
    wr.writerow(sortedTreeEdges)