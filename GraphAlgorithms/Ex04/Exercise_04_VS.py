# Vid Sustar,
# student nr: 1901627,
# Graph algorithms, 2019,
# 4th homework



#TASK:
"""
Find a proper edge and vertex coloring for an undirected graph; colors could be
represented as integers.
• Bonus points: 5
• INPUT: list of undirected non-negative weighted edges in CSV table.
• OUTPUT: 2 CSV tables:
1. vertex-coloring (columns: vertex-id,vertex-color);
2. edge-coloring (columns: edge-id, edge-color)
• The benchmark graph is available on Moodle as CSV and PDF files. One possible output
for vertex coloring, pairs (i,j) represent (node,color): (1,0), (2,1), (3,0), (4,2), (5,1 ), (6,0 ),
(7,1 ), (8,2), (9,2), (10,0); And for edge-coloring, (edge, color): (e12,0), (e15,2), (e17,1),
(e23,2), (e28,1), (e34,1), (e39,0), (e45,0), (e410,2), (e56,1), (e68,2), (e69,3), (e79,2),
(e710,0), (e810,3). 
send to victor-bogdan.popescu@abo.fi
"""
#######################importing needed libraries
import os
import csv
import numpy as np
from collections import defaultdict

numnodes=0
path = os.getcwd()
print(path)

nonDirected = 0

#creating list of edges as a list of tuples, with starting, ending node, weight, edge id
edges=[]
nodeslist=[]
with open(path+'\\benchmark4.csv') as f:
    next(f) # Skip header
    for row in csv.reader(f, delimiter='\t'):
        #print ("row[2][1:-1]",row[2])
        tupletoadd=((row[0]),(row[1]),(row[2]))
        nodeslist.append(row[0])
        nodeslist.append(row[1])
        edges.append(tupletoadd)
        if nonDirected:
            tupletoadd = ((row[1]),(row[0]), (row[2]))#reversed order of nodes for nondirected graph
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
print("nodesInd: ",nodesInd)
print("nodesListSimp: ",nodesListSimp)  #nodeslist!!!!


def NInd(node): #function to return key by value (node index from node name)#####################
    return list(nodesInd.keys())[list(nodesInd.values()).index(node)]
def IndN(key): #function to return value by key (node name from node index)######################
    return nodesInd.get(key)

####################################################################################################################
###################################################################################################################
#making indices dictionary for edges


edgesInd={}
edgesListSimp=[]
for n in range(len(edges)):
    edgesInd.update({n:edges[n][2]})
    edgesListSimp.append(n)
print("edgesIndInd: ",edgesInd)
print("edgesListSimp: ",edgesListSimp)  #nodeslist!!!!


def eInd(edge): #function to return key by value (node index from node name)#####################
    return list(edgesInd.keys())[list(edgesInd.values()).index(edge)]
def Inde(key): #function to return value by key (node name from node index)######################
    return edgesInd.get(key)
print(eInd("e12"))
print(Inde(0))



#reading converting nodes to new indices
indedges=[]
for element in edges:
    tupletoadd = (NInd(element[0]), NInd(element[1]), eInd(element[2]))
    indedges.append(tupletoadd)
print("indedges: ",indedges)


#MAKING LIST OF VERTEX NEIGHBOURS, FROM WHICH WE WILL LATER CHECK THE COLORS USED
def nodeneighbours(v, insindedges):
    nneighblist=[]
    for x in range(len(insindedges)):
        if (insindedges[x][0]==v):
            nneighblist.append(insindedges[x][1])
        if (insindedges[x][1] == v):
            nneighblist.append(insindedges[x][0])
    return(nneighblist)

print("nodeneighbours: ",nodeneighbours(2, indedges))

#MAKING LIST OF EDGES NEIGHBOURS, FROM WHICH WE WILL LATER CHECK THE COLORS USED
#FUNCTION TO SEARCH FOR ALL EDGES CONNECTED TO A NODE OF AN EDGE
def edgnodeneighbours(ev, insindedges):
    eneighblist=[]
    for x in range(len(insindedges)):
        if (insindedges[x][0]==ev):
            eneighblist.append(insindedges[x][2]) ####ADDING EDGE!!!
        if (insindedges[x][1] == ev):
            eneighblist.append(insindedges[x][2])
    return(eneighblist)
#FUNCTION TO COMBINE (NEIGHBOURING) EDGES FOR ALL NODES OF AN EDGE OF INTEREST
def combnedges(e, insindedges):
    edneighblist=[]
    nedneighblist=[]
    for x in range(len(insindedges)):
        if (insindedges[x][2]==e):
            edneighblist=edneighblist+edgnodeneighbours(insindedges[x][0], indedges) #combining lists
            edneighblist=edneighblist+edgnodeneighbours(insindedges[x][1], indedges)
    edneighblist=list(set(edneighblist)) #removal of duplicates from list by set conversions
    for elem in edneighblist: #removal of edge of interest from the list of its neighbours, REMOVE DID NOT WORK!!
        if (elem!=e):
            nedneighblist.append(elem)
    return(nedneighblist)

#########################################################    NODES       ##############################################################################
NodeNeighboursListOfLists=[]

for xnode in nodesListSimp:
    NodeNeighboursListOfLists.append(nodeneighbours(xnode, indedges))
print("NodeNeighboursListOfLists",NodeNeighboursListOfLists)

NodeColors={0: 0}#assigning lowest color to node 0 #Color first vertex with first color

globalowestColor=min(NodeColors.values())

for currentnode in range(len(NodeNeighboursListOfLists)):
    listOfColors = []
    listOfColorsinDict=[]
    unusedDictColor =[]
    for key in NodeColors:
        listOfColorsinDict.append(NodeColors[key])
    for neighbournode in NodeNeighboursListOfLists[currentnode]:
        if neighbournode in NodeColors:
            listOfColors.append(NodeColors[neighbournode])
    for dictCol in listOfColorsinDict:
        if dictCol not in listOfColors:
            unusedDictColor.append(dictCol)
    if len(unusedDictColor)!=0:
        NodeColors.update({currentnode: min(unusedDictColor)})
    else:
        NodeColors.update({currentnode: max(listOfColorsinDict)+1})
print ("FINALY:")

for key in NodeColors:
    print ("node:",IndN(key), "color: ",NodeColors[key])

print("REFERENCE: (1,0), (2,1), (3,0), (4,2), (5,1 ), (6,0 ), (7,1 ), (8,2), (9,2), (10,0)")#

with open('vertex-coloring.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for key, value in NodeColors.items():
       writer.writerow([IndN(key), value])

################################################     EDGES          ########################################################################################
EdgeNeighboursListOfLists=[]
for xedge in edgesListSimp:
    EdgeNeighboursListOfLists.append(combnedges(xedge, indedges))
print("EdgeNeighboursListOfLists",EdgeNeighboursListOfLists)



#dictionary checking the colors of neighbours, updating dictionary
edgeColors={0: 0}#assigning lowest color to edge 0 #Color first vertex with first color

globalowestColor=min(edgeColors.values())

for currentedge in range(len(EdgeNeighboursListOfLists)):
    listOfColors = []
    listOfColorsinDict=[]
    unusedDictColor =[]
    for key in edgeColors:
        listOfColorsinDict.append(edgeColors[key])
    for neighbouredge in EdgeNeighboursListOfLists[currentedge]:
        if neighbouredge in edgeColors:
            listOfColors.append(edgeColors[neighbouredge])
    for dictCol in listOfColorsinDict:
        if dictCol not in listOfColors:
            unusedDictColor.append(dictCol)
    if len(unusedDictColor)!=0:
        edgeColors.update({currentedge: min(unusedDictColor)})
    else:
        edgeColors.update({currentedge: max(listOfColorsinDict)+1})
print ("FINALY:")
for key in edgeColors:
    print ("edge:",Inde(key), "color: ",edgeColors[key])


print("REFERENCE: (e12,0), (e15,2), (e17,1), (e23,2), (e28,1), (e34,1), (e39,0), (e45,0), (e410,2), (e56,1), (e68,2), (e69,3), (e79,2), (e710,0), (e810,3))")#

with open('edge-coloring.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for key, value in edgeColors.items():
       writer.writerow([Inde(key), value])

