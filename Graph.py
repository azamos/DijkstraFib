from DoublyLinkedList import *
class Graph:
    def __init__(self,n,directed = True) -> None:
        self.n = n
        self.m = 0
        self.directed = directed
        self.vertices = [ Vertex(i) for i in range(1,n+1)]
        self.edges = {}
        
    def addEdge(self,u,v,weight = 0):
        self.vertices[u-1].neighbours.addNode(DLLNode(Vertex(v)))
        self.edges[(self.vertices[u-1].id,self.vertices[v-1].id)] = weight
        self.m+=1
        if self.directed is False:
            self.vertices[v-1].neighbours.addNode(DLLNode(Vertex(u)))
            self.edges[(self.vertices[v-1].id,self.vertices[u-1].id)] = weight
            m+=1
    
    def deleteEdge(self,u,v):
        del self.edges[(u,v)]#first, remove from dictionary
        self.vertices[u].neighbours._delete_node_(v)#remove from neighhbours adjacency list
        if not self.directed:
            del self.edges[(v,u)]#first, remove from dictionary
            self.vertices[v].neighbours._delete_node_(u)#remove from neighhbours adjacency list

    def printGraph(self):
        print(f"There are a total of {self.m} edges, and there are n = {self.n} vertices.")
        for edge in self.edges:
            w = self.edges[edge]
            if w<0:
                print(f"w({edge})=\033[91m{w}\033[0m")
            else:
                print(f"w({edge})={w}")

    def print_spanning_tree(self):
        for vertex in self.vertices:
            print(f"vertex.id = {vertex.id},vertex.key={vertex.key},vertex.PI={vertex.PI}")

class Vertex:
    def __init__(self,index) -> None:
        self.key = float("inf")#eventual minimum edge weight
        self.PI = None#from which other vertex the edge to this one came
        self.neighbours = DLL()#specifies the edges
        self.id =  index

def test_directed_graph():
    # Create a directed graph with 10 vertices
    directed_graph = Graph(10, directed=True)

    # Add all possible directed edges
    for u in range(1, 11):
        for v in range(1, 11):
            if u != v:
                directed_graph.addEdge(u, v, weight=1)  # Adding directed edges with weight 1

    return directed_graph

directed_graph = test_directed_graph()

# Print the directed graph
directed_graph.printGraph()

