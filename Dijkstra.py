import random
from hashGraph import *
from AlternateFibHeap import *
#Reminder: in this graph implementation, the vertices are numbers in {1,2,..,n}
#and to access vertex 3 for example, G.vertices[3-1]
def intialise_single_source(G,s):
    for v in G.vertices.values():
        v.key = float("inf")
        v.PI = None
    s.key = 0

def relax(u,v,edge_weight,Q):
    if v.key > u.key + edge_weight:
        Q.DecreaseKey(v.id,u.key + edge_weight)
        v.PI = u

def Dijkstra(G,s):
    intialise_single_source(G=G,s=s)
    queue = AlteredFibonacciHeap()
    S = set()
    for v in G.vertices.values():
        queue.Insert(new_id = v.id,new_key=v.key,value=v)
    while not queue.isEmpty():
        u = queue.ExtractMin()
        u.value.key = u.key
        u = u.value
        for v_id in u.neighbours:
            if v_id not in S:
                relax(u,G.vertices[v_id],G.edges[(u.id,v_id)].weight,queue)
        S.add(u.id)

N = 50
G = HashedAdjListGraph()
for i in range(1,N+1):
    G.add_vertex(u_id = i )
#G.print_graph()
for u in range(1,N+1):
    for v in range(1,N+1):
        if u!=v and (u,v) not in G.edges:
            G.add_edge(u_id=u,v_id=v,weight=random.randint(1,101))
#G.print_graph()
s=G.vertices[1]
Dijkstra(G,s=s)
for vertex in G.vertices.values():
    print(f"vertex {vertex.id} lightest distance from s = {s.id} is: {vertex.key}")
