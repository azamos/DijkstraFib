from DoublyLinkedList import *
class TreeNode:
    def __init__(self,key,value) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
        self.children = None
        self.parent = None
        self.marked = False

class FibonacciHeap:
    def __init__(self) -> None:
        self.roots = DLL()
        self.Min = None
        self.table = {}

    def insert(self,key,value):
        newNode = TreeNode(key=key,value=value)
        self.roots.addNode(newNode)
        self.table[key] = newNode
        if self.Min is None or self.Min.key > key:
            self.Min = newNode
    
    def GetMin(self):
        return self.Min
    
    def DecreaseKey(self,key,newKey):
        if newKey > key:
            raise ValueError("New key > old key")
        node = self.table[key]
        if node.parent is not None:
            if node.parent.marked is True:
                self.cut(node)
                self.cascading_cut(node.parent)
            else:
                node.parent.marked = True
        node.key = newKey
        self.table[newKey] = node
        del self.table[key]
        if node.key < self.Min.key:
            self.Min = node