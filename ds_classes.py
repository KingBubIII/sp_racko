import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class NODE:
    def __init__(self, value:int, qt_class) -> None:
        self.value = value
        self.next = None
        self.qt5_widget = self.initWidget(qt_class)

    def initWidget(self, qt_class) -> None:
        label = QLabel(qt_class)
        pixmap = QPixmap('pictures\\{0}_card.png'.format(self.value))
        label.setPixmap(pixmap)
        return label

class LINKEDLIST:
    def __init__(self) -> None:
        self.head = None
        self.tail = self.head
        self.length = 0

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
    
    def append(self, new_value, qt_class):
        new_node = NODE(new_value, qt_class)
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1
    
    def prepend(self, new_value, qt_class=None):
        new_node = NODE(new_value, qt_class)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

        if self.length == 1:
            self.tail = self.head

    def insert(self, targetI, new_value, qt_class):        
        new_node = NODE(new_value, qt_class)
        pre = self.Traverse(targetI-1)

        new_node.next = pre.next
        pre.next = new_node
        
        self.length += 1
        return

    def remove(self, index):
        self.length -= 1
        if index > 0:
            pre = self.Traverse(index-1)
            temp = pre.next.value
            if pre.next.next == None:
                self.tail = pre
            pre.next = pre.next.next
        else:
            temp = self.head.value
            self.head = self.head.next
        
        return temp
    
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

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Single Player Racko'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 750

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.show()