from DoublyLinkedList import *
from math import ceil,log,e
class TreeNode:
    def __init__(self,key) -> None:
        self.key = key
        self.next = None
        self.prev = None
        self.children = DLL()#instead of keeping track of degree(num of children),
                             #it can be simply retrieved by len(self.children)
        self.parent = None
        self.marked = False

    def print_subtree(self,depth):
        print(f"\n depth = {depth},key = {self.key}, {'ROOT' if not self.parent else f'son of {self.parent.key}'}")
        p = self.children.start
        while p is not None:
            p.value.print_subtree(depth+1)
            p = p.next

class FibonacciHeap:
    def __init__(self) -> None:
        self.roots = DLL()
        self.Min = None
        self.table = {}
        self.N = 0

    def insert(self,key):
        newNode = TreeNode(key=key)
        self.roots.addNode(value=newNode,key=key)
        self.table[key] = newNode
        if self.Min is None or self.Min.key > key:
            self.Min = newNode
        self.N+=1
    
    def GetMin(self):
        return self.Min
    
    def DecreaseKey(self,key,newKey):
        if newKey > key:
            raise ValueError("New key > old key. If you wish to decrease by newKey, simply pass key-newKey as the argument.")
        node = self.table[key]
        if node.parent is not None:
            if node.parent.marked is True:
                self.cut(node)
                self.cascading_cut(node.parent)
            else:
                node.parent.marked = True
        node.key = newKey
        del self.table[key]
        self.table[newKey] = node
        if node.key < self.Min.key:
            self.Min = node

    def cut(self,node):
        node.parent.children.delete_node(node.key)
        node.parent = None
        node.marked = False
        self.roots.addNode(node,node.key)
        self.table[node.key] = node

    def cascading_cut(self,node):
        if not node.marked:
            node.marked = True
            return
        
        while node.marked and node.parent is not None:
            p = node.parent
            self.cut(node=node)
            node = p
        
        

    def merge_trees(self,treeRoot1,treeRoot2):
        if treeRoot1.key <= treeRoot2.key: #make tree2 child of tree1
            treeRoot2.parent = treeRoot1
            treeRoot1.children.addNode(value = treeRoot2,key = treeRoot2.key)
            return treeRoot1
        else:
            treeRoot1.parent = treeRoot2
            treeRoot2.children.addNode(value = treeRoot1,key = treeRoot1.key)
            return treeRoot2
    
    def consolidate(self):
        degree_array = [None for _ in range(ceil(log(self.N,2)))]
        p = self.roots.start
        while p is not None:
            treeNode = p.value
            next = p.next
            degree = len(treeNode.children.nodes)
            if degree_array[degree] is None:
                degree_array[degree] = treeNode
            else:#merge trees, add merged result to the end of the list, and remove the 2 original ones
                other_tree = degree_array[degree]
                merged_tree = self.merge_trees(treeNode,other_tree)
                self.roots.delete_node(treeNode.key)
                self.roots.delete_node(other_tree.key)
                del self.table[treeNode.key]
                del self.table[other_tree.key]
                self.roots.addNode(value=merged_tree,key=merged_tree.key)
                self.table[merged_tree.key] = merged_tree

                degree_array[degree] = None
                #degree_array[len(merged_tree.children.nodes)] = merged_tree
            p = next
    
    def ExtractMin(self):
        result = self.Min
        temp = None#will point to the new Min

        #first, going over the current roots
        root_traverser = self.roots.start
        while root_traverser is not None:
            treeNode = root_traverser.value
            #The if bellow makes sure to update temp only if 
            #it temp is None and the current DLL node is not the Min.
            #If we do encounter the Min, then it must be removed. Idiotic.
            if temp is None:
                if treeNode is not self.Min:
                    temp = treeNode
            elif temp.key > treeNode.key:
                temp = treeNode
            root_traverser = root_traverser.next

        p = result.children.start
        while p is not None:
            treeNode = p.value
            treeNode.parent = None
            if temp is None or temp.key > treeNode.key:
                temp = treeNode
            next = p.next
            if treeNode.marked:
                treeNode.marked = False
            result.children.delete_node(p)
            self.roots.addNode(p)
            p = next
        self.roots.delete_node(result.key)
        del self.table[result.key]
        self.Min = temp#Updating the new minimu
        self.N-=1
        self.consolidate()
        return result.key
    
    def print_heap(self):
        for key in self.table:
            self.table[key].print_subtree(0)

dijkstra_queue = FibonacciHeap()
for i in range(10):
    dijkstra_queue.insert(key=i+1)
#dijkstra_queue.print_heap()
print(f"Extracted Min = {dijkstra_queue.ExtractMin()}")
print(f"New Min = {dijkstra_queue.GetMin().key}")
dijkstra_queue.print_heap()
