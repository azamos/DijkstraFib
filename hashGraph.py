class Vertex:#Generic. If someone whishes to add other paramaters,
    #such as PI, d, key and so on, they can override the class
    def __init__(self,id) -> None:
        self.id = id
        self.neighbours = {}
        self.in_degree = 0
        self.out_degree = 0

class Edge:#Generic. If someone whishes to add other paramaters,
    #such as Weight, Colour and so on they can override the class
    def __init__(self,src_id,target_id,weight = None) -> None:
        self.src_id = src_id
        self.target_id = target_id
        self.weight = weight

class HashedAdjListGraph:#Generic. If someone whishes to add other paramaters, he can override the class
    def __init__(self,directed = True) -> None:
        self.vertices = {}
        self.edges = {}
        self.directed = directed

    def add_vertex(self,u_id):
        new_vertex = Vertex(u_id)
        self.vertices[u_id] = new_vertex

    #Adds a new edge if not existing, otherwise alters
    def add_edge(self,u_id,v_id, weight = None):
        cond1 = u_id in self.vertices
        cond2 = v_id in self.vertices
        if cond1 == False:
            self.add_vertex(u_id=u_id)
        if cond2 == False:
            self.add_vertex(v_id=v_id)
        if (u_id,v_id) in self.edges or (self.directed == False and (v_id,u_id) in self.edges):
            #print("Edge already present.Did not add.")
            return
        newEdge = Edge(src_id=u_id,target_id=v_id,weight=weight)
        self.edges[(u_id,v_id)] = newEdge
        self.vertices[u_id].neighbours[v_id] = v_id
        self.vertices[v_id].neighbours[u_id] = u_id
        # if self.directed == False:
        #     self.edges[(v_id,u_id)] = newEdge
    
    def remove_edge(self,u_id,v_id):
        # if self.directed == False:
        #     if (v_id,u_id) in self.edges:
        #         del self.edges[(u_id,v_id)]#deleting only deletes the key
        #     else:
        #         raise ValueError("No such undirected edge")
            
        if (u_id,v_id) in self.edges:
            removedEdge = self.edges[(u_id,v_id)]
            del self.edges[(u_id,v_id)]
            return removedEdge
        else:
            pass
            #print("No such edge.")

    def remove_vertex(self,u_id):
        if u_id not in self.vertices:
            #print(f"No vertex with vertex_id = {u_id}. Did nothing.")
            return
        u = self.vertices[u_id]
        for v_id in u.neighbours:
            key = (u_id,v_id)
            if  key in u.neighbours:
                del u.neighbours[key]
            if key in self.edges:
                del self.edges[key]
            r_key = (v_id,u_id)
            if r_key in self.edges:
                del self.edges[r_key]
        del self.vertices[u_id]
        return u
    
    def get_dimensions(self):
        return {"|V|":len(self.vertices),"|E|":len(self.edges)}
    
    def print_graph(self):
        print(self.get_dimensions())
        for edge in self.edges.values():
            print((edge.src_id,edge.target_id),edge.weight)

# g = HashedAdjListGraph(directed=False)
# for i in range(10):
#     g.add_vertex(i+1)
# #g.print_graph()

# for u in g.vertices:
#     for v in g.vertices:
#         if u!=v and (u,v) not in g.edges:
#             g.add_edge(u,v,abs(u - v))
# # g.print_graph()
# g.remove_vertex(6)
# g.print_graph()
# edges = g.edges
# for i in range(11):
#     for j in range(11):
#         if (i,j) in g.edges:
#             g.remove_edge(i,j)
# g.print_graph()