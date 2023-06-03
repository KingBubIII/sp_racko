class NODE:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None

class LINKEDLIST:
    def __init__(self, init_value) -> None:
        self.head = NODE(init_value)
        self.tail = self.head
        self.length = 1

    def __str__(self):
        curr_node = self.head
        myArr = ""
        while not curr_node is None:
            if self.head == curr_node:
                myArr+="->"
            else:
                myArr+="  "
            myArr += str(curr_node.value) + "\n"
            curr_node = curr_node.next
        return str(myArr)

    def Traverse(self, target):
        index = 0
        curr_node = self.head

        while not index == target:
            curr_node = curr_node.next
            index += 1

        return curr_node
    
    def append(self, new_value):
        new_node = NODE(new_value)
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1
    
    def prepend(self, new_value):
        new_node = NODE(new_value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

    def insert(self, targetI, new_value):        
        new_node = NODE(new_value)
        pre = self.Traverse(targetI-1)

        new_node.next = pre.next
        pre.next = new_node
        
        self.length += 1
        return

    def remove(self, index):
        pre = self.Traverse(index-1)
        if pre.next.next == None:
            self.tail = pre
        pre.next = pre.next.next

        self.length -= 1
        return
    
    def reverse(self):
        currNode = self.head
        prevNode = None
        while self.tail.next == None:
            temp_node = curr_node.next
            curr_node.next = prevNode

            prevNode = curr_node
            curr_node = temp_node
        temp_node = self.head
        self.head = self.tail
        self.tail = temp_node