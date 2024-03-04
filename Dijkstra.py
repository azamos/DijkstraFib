from Graph import *
from FibonacciHeap import *
#Reminder: in this graph implementation, the vertices are numbers in {1,2,..,n}
#and to access vertex 3 for example, G.vertices[3-1]
def intialise_single_source(G,s):
    for v in G.vertices:
        v.key = float("inf")
        v.PI = None
    s.key = 0

def relax(u,v,edge_weight):
    if v.key > u.key + edge_weight:
        v.key = u.key + edge_weight
        v.PI = u

def Dijkstra(G,s):
    intialise_single_source(G=G,s=1)
    queue = FibonacciHeap()
    for v in G.vertices:
        queue.insert(key = v)
    while queue.N:
        u = queue.ExtractMin()
        for v in u.neighbours:
            relax(u,v,G.edges[(u,v)])