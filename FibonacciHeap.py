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
        self.roots_table = {}
        self.allnodes = {}
        self.N = 0

    def insert(self,key):
        newNode = TreeNode(key=key)
        self.roots.addNode(value=newNode,key=key)
        self.roots_table[key] = newNode
        self.allnodes[key] = newNode
        if self.Min is None or self.Min.key > key:
            self.Min = newNode
        self.N+=1
    
    def GetMin(self):
        return self.Min
    
    def DecreaseKey(self,oldKey,newKey):
        #error cases
        if newKey > oldKey:
            raise ValueError("New key > old key. If you wish to decrease by newKey, simply pass key-newKey as the argument.")
        if newKey in self.allnodes:
            raise ValueError("There's already a node with key = newKey. Pick another...")
        #accessing and updating node's key, and updating minimum
        node = self.allnodes[oldKey]
        node.key = newKey
        if newKey < self.Min.key:
            self.Min = node
        #deleting references to the node which rely on its old key, and updating them
        #to be according to the new key
        del self.allnodes[oldKey]
        self.allnodes[newKey] = node
        if oldKey in self.roots_table:#if it was a root, also need to update roots_table reference
            del self.roots_table[oldKey]
            self.roots_table[newKey] = node
        #Lastly, if the heap propery is broken, i.e. if the newKey is smaller than that of
        #the parent, then the subtree starting at the node must be removed from its parent
        #and then must be added as a new root,
        #and this may potentialy lead to a cascading cut, if the parent
        #has already lost another child.
        if node.parent and oldKey < node.parent.key:#TODO: consider changing it to <=
            self.cut(node)
            self.cascading_cut(node.parent)

    def cut(self,node):
        if self.node.parent is None:
            return
        node.parent.children.delete_node(node.key)
        node.parent = None
        node.marked = False
        link = self.roots.addNode(node,node.key)
        self.roots_table[node.key] = link

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
                del self.roots_table[treeNode.key]
                del self.roots_table[other_tree.key]
                self.roots.addNode(value=merged_tree,key=merged_tree.key)
                self.roots_table[merged_tree.key] = merged_tree

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
            elif temp.key > treeNode.key and treeNode is not result:
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
            result.children.delete_node(p.key)
            link = self.roots.addNode(value=p.value,key=p.key)
            #FORGOT to add to roots table?Attempted fix
            self.roots_table[p.key] = link
            p = next
        self.roots.delete_node(result.key)
        del self.roots_table[result.key]
        del self.allnodes[result.key]
        self.Min = temp#Updating the new minimu
        self.N-=1
        self.consolidate()
        return result.key
    
    def print_heap(self):
        for key in self.roots_table:
            self.roots_table[key].print_subtree(0)

dijkstra_queue = FibonacciHeap()
for i in range(16):
    dijkstra_queue.insert(key=i+1)
#dijkstra_queue.print_heap()
print(f"Extracted Min = {dijkstra_queue.ExtractMin()}")
print(f"New Min = {dijkstra_queue.GetMin().key}")
dijkstra_queue.print_heap()
print(f"Extracted Min = {dijkstra_queue.ExtractMin()}")
print(f"New Min = {dijkstra_queue.GetMin().key}")
dijkstra_queue.print_heap()
dijkstra_queue.DecreaseKey(oldKey=7,newKey=2)
dijkstra_queue.DecreaseKey(oldKey=8,newKey=1)
dijkstra_queue.DecreaseKey(oldKey=10,newKey=0)
print(f"after 3 DecreaseKey calls...")
dijkstra_queue.print_heap()
