import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal

# this class makes up the elements in the linked list class
class NODE:
    def __init__(self, value:int) -> None:
        self.value = value
        self.next = None
        self.image_path = 'pictures\\{0}_card.png'.format(self.value)

# this class is for logic that manipulates the order of the nodes
class LINKEDLIST:
    def __init__(self) -> None:
        self.head = None
        self.tail = self.head
        self.length = 0

    # prints out list in a easily readable format for debugging
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

    # retieves node element at index
    def Traverse(self, target):
        index = 0
        curr_node = self.head

        while not index == target:
            curr_node = curr_node.next
            index += 1

        return curr_node
    
    # adds new node with a value at end of list
    def append(self, new_value):
        new_node = NODE(new_value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
    
    # adds new node with a value at beginning of list
    def prepend(self, new_value):
        new_node = NODE(new_value)
        new_node.next = self.head
        self.head = new_node
        self.length += 1

        if self.length == 1:
            self.tail = self.head

    # adds new node with a value at index in list
    def insert(self, targetI, new_value):        
        new_node = NODE(new_value)
        pre = self.Traverse(targetI-1)

        new_node.next = pre.next
        pre.next = new_node
        
        self.length += 1
        return

    # removes node at index in list
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

    # moves list head element to an index of it's value plus one
    #               before                  after
    # example: list = [2, 4, 1, 3] --> list = [4, 1, 2, 3]
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
    
    #  moves list head node to bottom of list
    def topToBottom(self):
        temp = self.head
        self.head = temp.next
        temp.next = self.tail.next
        self.tail.next = temp
        self.tail = temp

        return self.length-1
    
    # checks to see if all nodes are in order
    # either ascending or descending
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

    # undos last move by removing node at index
    # then adding the value of removed node back on top of list
    def undo(self, index):
        temp_val = self.remove(index)
        self.prepend(temp_val)

# creates custom qt5 button class 
# add functionality for hovering mouse on button in GUI 
class BUTTON(QPushButton):
    entered = pyqtSignal()
    leaved = pyqtSignal()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.entered.emit()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.leaved.emit()

# creates custom qt5 class
class APP(QWidget):
    def __init__(self, deck, undo_stack):
        super().__init__()
        self.title = 'Single Player Racko'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 750
        self.deck_pos_start_x = 700
        self.deck_pos_start_y = 75
        self.card_offset = 50
        self.initButtons()
        self.refenceDeck = deck
        self.undo_stack = undo_stack
        self.pictureWidgets = self.initNodePictures(self.refenceDeck.length)
        self.hover_arrow = self.initHoverIndicator()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    # handles all event calling for clicking N+1 button
    @pyqtSlot()
    def nPlusOne_on_click(self):
        # gets new index of moved node
        index = self.refenceDeck.topToNPlusOne()
        # adds index as value to undo stack
        self.addToUndoStack(index)
        # update deck visuals
        self.showDeck()
        # checks for win/if all nodes are in order
        if self.refenceDeck.winCheck():
            self.close()
        # redo hover event
        self.buttonStopHovering()
        self.nPlusOneButtonHover()

    # handles all event calling for clicking bottom button
    @pyqtSlot()
    def bottom_on_click(self):
        # gets new index of moved node
        index = self.refenceDeck.topToBottom()
        # adds index as value to undo stack
        self.addToUndoStack(index)
        # update deck visuals
        self.showDeck()
        # checks for win/if all nodes are in order
        if self.refenceDeck.winCheck():
            self.close()
        # redo hover event
        self.buttonStopHovering()
        self.bottomButtonHover()

    # handles all event calling for undo button click
    @pyqtSlot()
    def undo_on_click(self):
        # checks that there is an event to undo
        if self.undo_stack.length > 0:
            # passes index value from removed undo stack node to undo meathod
            self.refenceDeck.undo(self.undo_stack.remove(0))
        else:
            print("You have nothing left to undo. Remember the max you can undo at one time is 3.")
        # update deck visuals
        self.showDeck()
        self.buttonStopHovering()
        self.undoButtonHover()

    # calculates position of next position indicator image to be at the bottom of the stack
    def bottomButtonHover(self):
        self.pictureWidgets[0].setStyleSheet("border: 3px solid red;")
        # calculates x position
        x = self.deck_pos_start_x-(self.card_offset*(self.refenceDeck.length-1))
        # calcuates y position
        y = (self.deck_pos_start_y+(self.card_offset*(self.refenceDeck.length-1)))-self.card_offset
        # moves indicator image to position
        self.hover_arrow.move(x, y)
        # shows image
        self.hover_arrow.setVisible(True)

    # calculates position of next position indicator image to be at n+1 the value of the stack head
    def nPlusOneButtonHover(self):
        self.pictureWidgets[0].setStyleSheet("border: 3px solid red;")
        # calculates x position
        x = self.deck_pos_start_x-(self.card_offset*(self.refenceDeck.head.value % self.refenceDeck.length))
        # calcuates y position
        y = (self.deck_pos_start_y+(self.card_offset*(self.refenceDeck.head.value % self.refenceDeck.length)))-self.card_offset
        # moves indicator image to position
        self.hover_arrow.move(x, y)
        # shows image
        self.hover_arrow.setVisible(True)

    def undoButtonHover(self):
        if not self.undo_stack.head is None:
            self.pictureWidgets[self.undo_stack.head.value].setStyleSheet("border: 3px solid red;")
            self.hover_arrow.move(self.deck_pos_start_x, self.deck_pos_start_y-self.card_offset)
            self.hover_arrow.setVisible(True)

    # when leaving button turn off indicator image visabllity 
    def buttonStopHovering(self):
        self.hover_arrow.setVisible(False)
        for image in self.pictureWidgets:
            image.setStyleSheet("border: 0px solid red;")

    # creates three buttons to manipulate the deck and attach event handlers to meathods
    def initButtons(self):
        # top to bottom button
        bottom_btn = BUTTON(self)
        bottom_btn.setText('Node to Bottom')
        bottom_btn.setToolTip('Moves current node to bottom of deck')
        bottom_btn.move(100,70)
        # attaches meathod to click event
        bottom_btn.clicked.connect(self.bottom_on_click)
        # attaches meathod to enter hover event
        bottom_btn.entered.connect(self.bottomButtonHover)
        # attaches meathod to stop hover event
        bottom_btn.leaved.connect(self.buttonStopHovering)

        # top to n+1 button
        nPlusOne_btn = BUTTON(self)
        nPlusOne_btn.setText('Node to N+1')
        nPlusOne_btn.setToolTip('Put current node on bottom of stack')
        nPlusOne_btn.move(100,140)
        # attaches meathod to click event
        nPlusOne_btn.clicked.connect(self.nPlusOne_on_click)
        # attaches meathod to enter hover event
        nPlusOne_btn.entered.connect(self.nPlusOneButtonHover)
        # attaches meathod to stop hover event
        nPlusOne_btn.leaved.connect(self.buttonStopHovering)

        # undo button
        undo_btn = BUTTON(self)
        undo_btn.setText('Undo')
        undo_btn.setToolTip('Put last node moved back ontop of deck')
        undo_btn.move(100,210)
        # attaches meathod to click event
        undo_btn.clicked.connect(self.undo_on_click)
        undo_btn.entered.connect(self.undoButtonHover)
        undo_btn.leaved.connect(self.buttonStopHovering)

    # This is where the card images will be attached to
    def initNodePictures(self, amount = 1):
        # the list of widgets to be returned
        image_widgets = []
        # the starting position on the qt5 canvas
        # creates an object for however long the list is
        for count in range(amount):
            # initialize the object
            label = QLabel(self)
            # sets image path
            pixmap = QPixmap()
            # attaches image to object via path
            label.setPixmap(pixmap)
            # moves each image so that corner where card value is displayed
            label.move(self.deck_pos_start_x-(self.card_offset*count), self.deck_pos_start_y+(self.card_offset*count))
            # lowers the objects view priority so the stack of images is decending
            label.lower()
            # adds item to list
            image_widgets.append(label)
        return image_widgets
    
    # creates picture object for indicating where next node will go 
    def initHoverIndicator(self):
        arrow_size = self.card_offset
        # initialize the object
        arrow = QLabel(self)
        # sets image path
        pixmap = QPixmap('pictures\\arrow.png')
        # resize image object to fit inbetween cards
        pixmap = pixmap.scaled(arrow_size, arrow_size)
        # attach picture to object 
        arrow.setPixmap(pixmap)
        # move object to default position
        arrow.move(self.deck_pos_start_x,self.deck_pos_start_y-arrow_size)
        # turn off visabilty
        arrow.setVisible(False)

        return arrow
    
    # sets image objects equal to corisponding node value images
    def showDeck(self):
        curr = self.refenceDeck.head
        for object in self.pictureWidgets:
            pixmap = QPixmap(curr.image_path)
            object.setPixmap(pixmap)
            curr = curr.next
        
        return
    
    # logic to keep the undo stack 'memory' to a defined maximum
    # default is 3
    def addToUndoStack(self, index):
        # checks if there are already 3 nodes
        if self.undo_stack.length >= 3:
            # removes last node 
            self.undo_stack.remove(2)

        # add new value node
        self.undo_stack.prepend(index)