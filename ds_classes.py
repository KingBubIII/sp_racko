import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class NODE:
    def __init__(self, value:int) -> None:
        self.value = value
        self.next = None
        self.image_path = 'pictures\\{0}_card.png'.format(self.value)

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
    
    def append(self, new_value):
        new_node = NODE(new_value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
    
    def prepend(self, new_value):
        new_node = NODE(new_value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

        if self.length == 1:
            self.tail = self.head

    def insert(self, targetI, new_value):        
        new_node = NODE(new_value)
        pre = self.Traverse(targetI-1)

        new_node.next = pre.next
        pre.next = new_node
        
        self.length += 1
        return

    def remove(self, index):
        if index > 0:
            pre = self.Traverse(index-1)
            temp = pre.next.value
            if pre.next.next == None:
                self.tail = pre
            pre.next = pre.next.next
        else:
            temp = self.head.value
            self.head = self.head.next

        self.length -= 1
        if self.length == 1:
            self.tail = self.head
        elif self.length == 0:
            self.tail = None
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

    def topToNPlusOne(self):
        index = (self.head.value) % self.length
        if index > 0:
            pre = self.head
            for count in range(index):
                pre = pre.next
            
            aft = pre.next
            
            temp = self.head
            self.head = self.head.next
            pre.next = temp
            temp.next = aft
            if aft == None:
                self.tail = temp

        return index
    
    def topToBottom(self):
        temp = self.head
        self.head = temp.next
        temp.next = self.tail.next
        self.tail.next = temp
        self.tail = temp

        return self.length-1
    
    def winCheck(self):
        win = True
        curr_node = self.head
        if curr_node.next.value > curr_node.value:
            while not curr_node.next == None:
                if curr_node.next.value < curr_node.value:
                    win = False
                    break
                curr_node = curr_node.next
        elif curr_node.next.value < curr_node.value:
            while not curr_node.next == None:
                if curr_node.next.value > curr_node.value:
                    win = False
                    break
                curr_node = curr_node.next
        
        return win

    def undo(self, index):
        temp_val = self.remove(index)
        self.prepend(temp_val)

class BUTTON(QPushButton):
    entered = pyqtSignal()
    leaved = pyqtSignal()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.entered.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()

class APP(QWidget):
    def __init__(self, deck, undo_stack):
        super().__init__()
        self.title = 'Single Player Racko'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 750
        self.initUI()
        self.refenceDeck = deck
        self.undo_stack = undo_stack
        self.pictureWidgets = self.initPictureWidgets(self.refenceDeck.length)

    @pyqtSlot()
    def nPlusOne_on_click(self):
        index = self.refenceDeck.topToNPlusOne()
        self.addToUndoStack(index)
        self.showDeck()
        if self.refenceDeck.winCheck():
            self.close()

    @pyqtSlot()
    def bottom_on_click(self):
        index = self.refenceDeck.topToBottom()
        self.addToUndoStack(index)
        self.showDeck()
        if self.refenceDeck.winCheck():
            self.close()

    @pyqtSlot()
    def undo_on_click(self):
        # print(self.undo_stack.length)
        if self.undo_stack.length > 0:
            self.refenceDeck.undo(self.undo_stack.remove(0))
        else:
            print("You have nothing left to undo. Remember the max you can undo at one time is 3.")

        self.showDeck()

    def buttonHover(self):
        print('Entered')

    def buttonStopHovering(self):
        print('Left')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.show()

        bottom_btn = BUTTON(self)
        bottom_btn.setText('Node to Bottom')
        bottom_btn.setToolTip('This is an example button')
        bottom_btn.move(100,70)
        bottom_btn.clicked.connect(self.bottom_on_click)
        bottom_btn.entered.connect(self.buttonHover)
        bottom_btn.leaved.connect(self.buttonStopHovering)

        nPlusOne_btn = BUTTON(self)
        nPlusOne_btn.setText('Node to N+1')
        nPlusOne_btn.setToolTip('Put current node on bottom of stack')
        nPlusOne_btn.move(100,140)
        nPlusOne_btn.clicked.connect(self.nPlusOne_on_click)
        nPlusOne_btn.entered.connect(self.buttonHover)
        nPlusOne_btn.leaved.connect(self.buttonStopHovering)

        undo_btn = BUTTON(self)
        undo_btn.setText('Undo')
        undo_btn.setToolTip('Put last node moved back ontop of deck')
        undo_btn.move(100,210)
        undo_btn.clicked.connect(self.undo_on_click)
        undo_btn.entered.connect(self.buttonHover)
        undo_btn.leaved.connect(self.buttonStopHovering)

    # This is where the card images will be attached to
    def initPictureWidgets(self, amount = 1):
        # the list of widgets to be returned
        image_widgets = []
        # the starting position on the qt5 canvas
        start_pos = [700,25]
        # creates an object for however long the list is
        for count in range(amount):
            # initialize the object
            label = QLabel(self)
            # sets image path
            pixmap = QPixmap()
            # attaches image to object via path
            label.setPixmap(pixmap)
            # moves each image so that corner where card value is displayed
            label.move(start_pos[0]-(50*count), start_pos[1]+(50*count))
            # lowers the objects view priority so the stack of images is decending
            label.lower()
            # adds item to list
            image_widgets.append(label)
        return image_widgets
    
    def showDeck(self):
        curr = self.refenceDeck.head
        for object in self.pictureWidgets:
            pixmap = QPixmap(curr.image_path)
            object.setPixmap(pixmap)
            curr = curr.next
        
        return
    
    def addToUndoStack(self, index):
        if self.undo_stack.length >= 3:
            self.undo_stack.remove(2)

        self.undo_stack.prepend(index)