class DLLNode:#is a DLL Node.
    def __init__(self,value,next = None) -> None:
        self.value = value
        self.next = None
        self.prev = None
class DLL:
    def __init__(self,first = None) -> None:
        self.head = first
        self.nodes = {}
    def addNode(self,newNode):
        if self.head is None:
            self.head = newNode
        else:
            self.head.next = newNode
            newNode.prev = self.head
            self.head = newNode
        self.nodes[newNode.value.id] = newNode
    def _find_node_(self,id):
        if id not in self.nodes.keys():
            return None
        return self.nodes[id]
    
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