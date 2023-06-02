class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, value) -> None:
        self.head = {"value" : value, "next" : None}
        self.tail = self.head
        self.length = 1

    def printList(self):
        currNode = self.head
        myArr = []
        while not currNode is None:
            myArr.append(currNode["value"])
            currNode = currNode["next"]
        print(myArr)

    def Traverse(self, target):
        index = 0
        currNode = self.head

        while not index == target:
            currNode = currNode["next"]
            index += 1

        return currNode
    
    def append(self, value):
        newNode = {"value" : value, "next" : None}
        self.tail["next"] = newNode
        self.tail = newNode
        self.length += 1
    
    def prepend(self, value):
        newNode = {"value" : value, "next" : None}
        newNode["next"] = self.head
        self.head = newNode
        self.length += 1

    def insert(self, targetI, value):        
        newNode = {"value" : value, "next" : None}
        pre = self.Traverse(targetI-1)

        newNode["next"] = pre["next"]
        pre["next"] = newNode
        
        self.length += 1
        return

    def remove(self, index):
        pre = self.Traverse(index-1)
        pre["next"] = pre["next"]["next"]
        self.length -= 1
        return
    
    def reverse(self):
        currNode = self.head
        prevNode = None
        while self.tail["next"] == None:
            tempNode = currNode["next"]
            currNode["next"] = prevNode

            prevNode = currNode
            currNode = tempNode
        tempNode = self.head
        self.head = self.tail
        self.tail = tempNode