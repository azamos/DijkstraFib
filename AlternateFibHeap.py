from math import log2,ceil
class TreeNode:
    def __init__(self,id,key) -> None:
        self.id = id#Unique, an identifier
        self.key = key#Not-unique,but integral to the way the heap is structured
        self.children = {}
        self.parent = None
        self.marked = False
    
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

class AlteredFibonacciHeap:
    def __init__(self) -> None:
        self.root_nodes = {}
        self.nodes = {}
        self.Min = None

    def GetMin(self):
        return self.Min

    def Insert(self,new_id,new_key):
        if new_id in self.nodes:
            print("use another id.")
            return
        newNode = TreeNode(id=new_id,key=new_key)
        self.root_nodes[new_id] = self.nodes[new_id] = newNode
        if self.Min is None or new_key < self.Min.key:
            self.Min = newNode
    
    def isEmpty(self):
        return self.Min is None

    def ExtractMin(self):
        if self.isEmpty():
            return None
        #1.First, I will remove all of Min's children and add them as roots of trees.
        #2.Then, I will go over all roots to find the new Minimum
        #3.Lastly, I will consolidate trees of the same degree
        for child in self.Min.children.values():
            child.parent = None
            child.marked = False
            self.root_nodes[child.id] = child
        Minimal = self.Min
        newMin = None
        del self.root_nodes[Minimal.id]
        self._consolidate_()
        for rootNode in self.root_nodes.values():
            if newMin is None or rootNode.key < newMin.key:
                newMin = rootNode
        self.Min = newMin
        return Minimal 
    
    def _consolidate_(self):#Goes over ALL roots and merges trees
        #assert that all TreeNodes in self.root_nodes parent is None
        nodesNoLongerRoots = {}
        N = len(self.nodes)
        max_deg = (ceil(log2(N))+2)
        deg_trees = [None]*(max_deg+1)
        for treeRoot in self.root_nodes.values():
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
                    # if deg > len(deg_trees):
                    #     print(f"deg is {deg}")
                deg_trees[deg] = merged_tree
        for noLongerRoot_id in nodesNoLongerRoots:
            del self.root_nodes[noLongerRoot_id]
        
    def print_heap(self):
        for root in self.root_nodes.values():
            root.print_node(0)
    
    def DecreaseKey(self,id,newKey):
        treeNode = self.nodes[id]
        treeNode.key = newKey
        if treeNode.parent and treeNode.key < treeNode.parent.key:
            p = treeNode.parent
            self.cut(treeNode)
            self.cascading_cut(p)
        if self.Min and self.Min.key > newKey:
            self.Min = treeNode

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

Q = AlteredFibonacciHeap()
for i in range(1,17):
    Q.Insert(i,i)
print(f"min key is : {Q.ExtractMin().key}")
# print(f"min key is : {Q.ExtractMin().key}")
# print(f"min key is : {Q.ExtractMin().key}")
# Q.DecreaseKey(6,3)
Q.DecreaseKey(6,1)
Q.print_heap()
print("\n\n\n")
print(f"min key is : {Q.ExtractMin().key}")
Q.print_heap()