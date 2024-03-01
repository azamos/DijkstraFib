class DLLNode:#is a DLL Node.
    def __init__(self,value,key,next = None) -> None:
        self.value = value
        self.key = key
        self.next = None
        self.prev = None
class DLL:
    def __init__(self) -> None:
        self.start = None
        self.end = None
        self.nodes = {}
    def addNode(self,value,key):
        if key in self.nodes:
            raise ValueError("DLL node with such key already exist.")
        newNode = DLLNode(value=value,key=key)
        if self.start is None:
            self.start = self.end = newNode
        else:
            self.end.next = newNode
            newNode.prev = self.end
            self.end = newNode
        self.nodes[key] = newNode
    def _find_node_(self,id):
        if id not in self.nodes:
            return None
        return self.nodes[id]
    
    def delete_node(self,id)->DLLNode:
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
        del self.nodes[node.id]
        return node
    
    def print_list(self):
        p = self.start
        while p is not None:
            print(f"{p.key}, ")
            p = p.next