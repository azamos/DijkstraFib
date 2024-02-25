class TreeNode:
    def __init__(self,key,value) -> None:
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
        self.children = None
        self.parent = None
        self.marked = False

class FibTree:
    def __init__(self,key,value) -> None:
        self.root = TreeNode(key=key,value=value)

class FibonacciHeap:
    def __init__(self) -> None:
        self.roots_head = None
        self.Min = None
        self.table = {}

    def insert(self,key,value):
        newTree = FibTree(key=key,value=value)
        if self.roots_head is None:
            self.roots_head = newTree
        else:
            self.roots_head.next = newTree
            newTree.prev = self.roots_head
            self.roots_head = newTree
        if self.Min is None or self.Min.key > key:
            self.Min = newTree
        self.table[key] = newTree
    
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