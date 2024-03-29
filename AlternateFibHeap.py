from math import log2,ceil
class TreeNode:
    def __init__(self,id,key,value) -> None:
        self.id = id#Unique, an identifier. Must never change.
        self.key = key#Not-unique,but integral to the way the heap is structured.Probably will change.
        self.children = {}
        self.parent = None
        self.marked = False
        self.value = value#Can be whatever. I will use it as a pointer to a graph vertex
    
    def print_node(self,depth):
        if depth == 0:
            print("ROOT")
            print(f"depth = {depth}, key = {self.key}")
        else:
            if self.parent is None:
                raise ValueError(f"parent is None but depth is NOT zero. id = {self.id}")
            print(f"depth = {depth}, key = {self.key}, parent.key = {self.parent.key}")
            # print(f"my id = {self.id}, parent id = {self.parent.id}, and i am marked = {self.marked}")
            # print(f"my degree is {len(self.children)}")
        for childNode in self.children.values():
            childNode.print_node(depth+1)

class AlteredFibonacciHeap:#instead of DLL's, uses hashtables/dictionaries
    def __init__(self) -> None:
        self.root_nodes = {}
        self.nodes = {}
        self.Min = None
        self.MaxNodes = 0

    def GetMin(self):
        return self.Min

    def Insert(self,new_id,new_key,value):
        newNode = TreeNode(id=new_id,key=new_key,value=value)
        self.root_nodes[new_id] = self.nodes[new_id] = newNode
        if self.Min is None or new_key < self.Min.key:
            self.Min = newNode
        if len(self.nodes) > self.MaxNodes:
            self.MaxNodes = len(self.nodes)
    
    def isEmpty(self):
        return len(self.nodes) == 0

    def ExtractMin(self):
        if self.isEmpty():
            return None
        #1.First, I will remove all of Min's children and add them as roots of trees.
        #2.Then, I will consolidate trees of the same degree.
        #3.Lastly, I will go over all roots to find the new Minimum, if there ARE more roots.
        for child in self.Min.children.values():
            child.parent = None
            child.marked = False
            self.root_nodes[child.id] = child
        # if self.Min.id in self.root_nodes:
        del self.root_nodes[self.Min.id]
        # else:
            # print("How could this be1?")
        if self.isEmpty():
            return self.Min
        #2.
        self._consolidate_()
        #3.Now, all of Min's children, if there were, are either in the roots, or a children of a root node
        newMin = None#Will temporarily hold keys until a minimum is found
        for rootNode in self.root_nodes.values():
            if newMin is None or (rootNode.key < newMin.key and rootNode.id!=self.Min.id):
                newMin = rootNode
        ret_val = self.Min
        self.Min = newMin#Could be None, indicating the heap is now empty
        # if ret_val.id in self.nodes:
        del self.nodes[ret_val.id]#IMPORTANT: otherwise, can't reinsert nodes with same id's
                                   #after their supposed removal
        # else:#THIS SOMETIMES CAUSE INFINITE LOOP. WHY?!?!?!?!?!
            # print(f"\nThe Min {ret_val.id} was prematurely deleted from the hashtable!\nThis can cause an infinie loop!")
        return ret_val
    
    def _consolidate_(self):#Goes over ALL roots and merges trees
        #assert that all TreeNodes in self.root_nodes parent is None
        nodesNoLongerRoots = {}
        N = max(len(self.nodes),self.MaxNodes)
        max_deg = (ceil(log2(N))+2)
        deg_trees = [None]*(max_deg+3)
        for treeRoot in self.root_nodes.values():#could be source of issue, since 
            #I am not removing a tree root immediately after merge due to still iterating over root list.
            merged_tree = treeRoot
            deg = len(merged_tree.children)
            if deg_trees[deg] is None:
                deg_trees[deg] = merged_tree
            else:
                while deg < len(deg_trees) and deg_trees[deg] is not None:
                    other_tree = deg_trees[deg]
                    if merged_tree.key < other_tree.key:
                        merged_tree.children[other_tree.id] = other_tree
                        other_tree.parent = merged_tree
                        nodesNoLongerRoots[other_tree.id] = other_tree.id#No longer a root
                        #merged_tree = treeRoot
                    else:
                        other_tree.children[merged_tree.id] = merged_tree
                        merged_tree.parent = other_tree
                        nodesNoLongerRoots[merged_tree.id] = merged_tree.id#No longer a root
                        merged_tree = other_tree
                    deg_trees[deg] = None
                    deg = len(merged_tree.children)#TODO: check if works with simply deg+=1
                deg_trees[deg] = merged_tree
        for noLongerRoot_id in nodesNoLongerRoots:
            del self.root_nodes[noLongerRoot_id]#could be source of bug, if new Min is here
        
    def print_heap(self):
        for root in self.root_nodes.values():
            root.print_node(0)
    
    def DecreaseKey(self,id,newKey):
        # if id not in self.nodes:
        #     print(id)
        #     print("ODD")
        treeNode = self.nodes[id]
        treeNode.key = newKey
        if self.Min is None or self.Min.key > newKey:
            self.Min = treeNode
            self.root_nodes[treeNode.id] = treeNode
        if treeNode.parent and treeNode.key < treeNode.parent.key:
            p = treeNode.parent
            self.cut(treeNode)
            self.cascading_cut(p)
 

    def cut(self,tree_node):
        del tree_node.parent.children[tree_node.id]
        tree_node.parent = None
        self.root_nodes[tree_node.id] = tree_node
        tree_node.marked = False

    def cascading_cut(self,tree_node):
        if tree_node.marked == False:
            tree_node.marked = True
            return
        while tree_node.parent and tree_node.marked:
            p = tree_node.parent
            self.cut(tree_node)
            tree_node = p

# Q = AlteredFibonacciHeap()
# N = 1001
# for i in range(1,N):
#     Q.Insert(i,i)
# for i in range(1,N):
#     if Q.ExtractMin().key != i:
#         print("ERROR")
# print("GOOD")
# if Q.isEmpty()==False:
#     print("BAD")

# for i in range(1,N):
#     Q.Insert(i,i)
# Q.ExtractMin()#To consolidate trees
# if len(Q.root_nodes) > log2(N)+1:
#     print("ERROR: Too many roots AFTER ExtractMin, which should consolidate trees")
# for treeRoot in Q.root_nodes.values():
#     deg = len(treeRoot.children)
#     print(f"{(treeRoot.id,treeRoot.key)} degree: {deg}")
#     if deg > log2(N)+1:
#         print("Problem: Tree of degree wayyy too big")
#         print(len(treeRoot.children),log2(N)+1)

#NEED TO TEST DECREASE KEY. Best solution: try implementening Dijkstra's and seeing if the result fits.