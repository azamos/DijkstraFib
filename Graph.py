class DLLNode:#is a DLL Node.
    def __init__(self,value,next = None) -> None:
        self.value = value#maybe value should be a pointer to a Vertex()
        self.next = None
        self.prev = None
class DLL:
    def __init__(self,first = None) -> None:
        self.head = first
    def addNode(self,newNode):
        if self.head is None:
            self.head = newNode
        else:
            self.head.next = newNode
            newNode.prev = self.head
            self.head = newNode
    def _find_node_(self,id):
        p = self.head
        while p is not None:
            if p.value.id == id:
                return p
            p = p.prev
        return None
    
    def _delete_node_(self,id)->DLLNode:
        node = self._find_node_(id)
        if node is None:
            return None
        #there are 4 cases possible:
        #   1.node is in the middle of 2 nodes
        #   2.node has no prev and no next(list of size 1)
        #   3.node has prev but no next(head in a size 2 DLL)
        #   4.node has next but no prev(oldest element of a DLL)

        #case1: connect prev to next, and next to prev
        if node.prev and node.next:
            prev_node = node.prev
            next_node = node.next
            #first, I remove pointers from node to its neighbours
            node.prev = None
            node.next = None
            #Now, I connect prev and next in a bidirectional connection
            prev_node.next = next_node
            next_node.prev = prev_node
        #case2:
        elif node.prev is None and node.next is None:
            self.head = None
        #case3:
        elif node.prev is not None and node.next is None:
            #need to make the node not point to its prev anymore,
            #and to make the prev_node the head, and make its next point to None
            prev_node = node.prev
            node.prev = None
            prev_node.next = None
            self.head = prev_node
        #case 4, final case:
        elif node.prev is None and node.next is not None:
            #here, I just need to disconnect the first node from the second node 
            next_node = node.next
            node.next = None
            next_node.prev = None
        return node
class Graph:
    def __init__(self,n,directed = True) -> None:
        self.n = n
        self.m = 0
        self.directed = directed
        self.vertices = [ Vertex(i) for i in range(1,n+1)]
        self.edges = {}#todo: swich to dict implementation of edges. say {(1,2):w(1,2),(1,5):w:(1,5)} and so forth
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