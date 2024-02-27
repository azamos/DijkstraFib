from DoublyLinkedList import *
from math import ceil,log,e
class TreeNode:
    def __init__(self,key,value) -> None:
        self.key = key
        self.next = None
        self.prev = None
        self.children = DLL()#instead of keeping track of degree(num of children),
                             #it can be simply retrieved by len(self.children)
        self.parent = None
        self.marked = False

class FibonacciHeap:
    def __init__(self) -> None:
        self.roots = DLL()
        self.Min = None
        self.table = {}
        self.N = 0

    def insert(self,key,value):
        newNode = TreeNode(key=key,value=value)
        self.roots.addNode(newNode)
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

    def merge_trees(self,treeRoot1,treeRoot2):
        if treeRoot1.key <= treeRoot2.key: #make tree2 child of tree1
            treeRoot2.parent = treeRoot1
            treeRoot1.children.addNode(value = treeRoot2)
            return (treeRoot1,treeRoot2)
        else:
            treeRoot1.parent = treeRoot2
            treeRoot2.children.addNode(value = treeRoot1)
            return (treeRoot2,treeRoot1)
    
    def consolidate(self,N):
        degree_array = [None for _ in range(log(N,2))]
        p = self.roots.head
        while p is not None:
            treeNode = p.value
            degree = len(treeNode.children)
            if degree_array[degree-1] is None:
                degree_array[degree-1] = treeNode
            else:#merge trees, add merged result to the end of the list, and remove the 2 original ones
                other_tree = degree_array[degree-1]
                merged_tree,other_tree = self.merge_trees(treeNode,other_tree)
                self.roots.delete_node(treeNode.key)
                self.roots.delete_node(other_tree.key)
                del self.table[treeNode.key]
                del self.table[other_tree.key]
                self.roots.addNode(value=merged_tree)
                self.table[merged_tree.key] = merged_tree
                
            p = p.next