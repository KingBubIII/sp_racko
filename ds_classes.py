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
    def inOrder(self):
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
    def __init__(self, end_deck, supply_deck):
        super().__init__()
        self.title = 'Single Player Racko'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 750
        self.deck_pos_start_x = 300
        self.deck_pos_start_y = 100
        self.supply_pos_x = 700
        self.supply_pos_y = 50
        self.card_offset = 50
        self.initButtons()
        self.refence_deck = end_deck
        self.supply_deck = supply_deck
        self.sorted_deck_images = self.initSortedDeckWidgets(self.supply_deck.length + self.refence_deck.length)
        self.supply_card_widget = self.initSupplyCardWidget()
        self.hover_arrow = self.initHoverIndicator()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    @pyqtSlot()
    def stackFromSupply(self):
        if self.supply_deck.head == None:
            print('There are no more cards left in supply pile')
        else:
            self.refence_deck.prepend(self.supply_deck.remove(0))
            self.showDecks()
            self.winCheck()
            self.stackFromSupplyHover()

    @pyqtSlot()
    def queueFromSupply(self):
        if self.supply_deck.head == None:
            print('There are no more cards left in supply pile')
        else:
            self.refence_deck.append(self.supply_deck.remove(0))
            self.showDecks()
            self.winCheck()
            self.queueFromSupplyHover()

    @pyqtSlot()
    def popFromUserSorted(self):
        if self.refence_deck.head == None:
            print('There are no more cards left in sorted pile')
        else:
            self.supply_deck.append(self.refence_deck.remove(0))
            self.showDecks()
            self.popFromUserSortedHover()
        
    @pyqtSlot()
    def stackFromSupplyHover(self):
        if not self.supply_deck.head == None:
            self.supply_card_widget.setStyleSheet("border: 3px solid red;")
            self.hover_arrow.move(self.deck_pos_start_x, self.deck_pos_start_y-self.card_offset)
            self.hover_arrow.show()
        else:
            self.buttonStopHovering()

    @pyqtSlot()
    def popFromUserSortedHover(self):
        if not self.refence_deck.head == None:
            self.sorted_deck_images[0].setStyleSheet("border: 3px solid red;")
            self.hover_arrow.move(self.supply_pos_x, self.supply_pos_y-self.card_offset)
            self.hover_arrow.show()
        else:
            self.buttonStopHovering()

    @pyqtSlot()
    def queueFromSupplyHover(self):
        if not self.supply_deck.head == None:
            self.supply_card_widget.setStyleSheet("border: 3px solid red;")
            self.hover_arrow.move( (self.deck_pos_start_x - (self.card_offset*self.refence_deck.length)) , (self.deck_pos_start_y+(self.card_offset*(self.refence_deck.length-1))) )
            self.hover_arrow.show()
        else:
            self.buttonStopHovering()

    # when leaving button turn off indicator image visabllity 
    def buttonStopHovering(self):
        self.supply_card_widget.setStyleSheet("")
        self.sorted_deck_images[0].setStyleSheet("")
        self.hover_arrow.setVisible(False)

    # creates three buttons to manipulate the deck and attach event handlers to meathods
    def initButtons(self):
        # top to bottom button
        queue_btn = BUTTON(self)
        queue_btn.setText('Queue')
        queue_btn.setToolTip('Moves top supply card to bottom of deck')
        queue_btn.move(100,70)
        # attaches meathod to click event
        queue_btn.clicked.connect(self.queueFromSupply)
        # attaches meathod to enter hover event
        queue_btn.entered.connect(self.queueFromSupplyHover)
        # attaches meathod to stop hover event
        queue_btn.leaved.connect(self.buttonStopHovering)

        # top to n+1 button
        stack_btn = BUTTON(self)
        stack_btn.setText('Stack')
        stack_btn.setToolTip('Moves top supply card to top of deck')
        stack_btn.move(100,140)
        # attaches meathod to click event
        stack_btn.clicked.connect(self.stackFromSupply)
        # attaches meathod to enter hover event
        stack_btn.entered.connect(self.stackFromSupplyHover)
        # attaches meathod to stop hover event
        stack_btn.leaved.connect(self.buttonStopHovering)

        pop_btn = BUTTON(self)
        pop_btn.setText('Pop')
        pop_btn.setToolTip('removes top most card of the user sorted pile and adds it to bottom of supply pile')
        pop_btn.move(self.supply_pos_x, self.supply_pos_y+600)
        # attaches meathod to click event
        pop_btn.clicked.connect(self.popFromUserSorted)
        # attaches meathod to enter hover event
        pop_btn.entered.connect(self.popFromUserSortedHover)
        # attaches meathod to stop hover event
        pop_btn.leaved.connect(self.buttonStopHovering)

    def initPictureWidget(self, x, y, value = None):
        # initialize the object
        label = QLabel(self)
        # sets image path
        pixmap = QPixmap("pictures\\{0}_card.png".format(value))
        # attaches image to object via path
        label.setPixmap(pixmap)
        # moves each image so that corner where card value is displayed
        label.move(x, y)

        return label

    # This is where the card images will be attached to
    def initSortedDeckWidgets(self, amount = 1):
        # the list of widgets to be returned
        image_widgets = []
        # the starting position on the qt5 canvas
        # creates an object for however long the list is
        for count in range(amount):
            picture_widget = self.initPictureWidget(self.deck_pos_start_x-(self.card_offset*count), self.deck_pos_start_y+(self.card_offset*count))
            # lowers the objects view priority so the stack of images is decending
            picture_widget.lower()
            # adds item to list
            image_widgets.append(picture_widget)
        return image_widgets
    
    def initSupplyCardWidget(self):
        picture_widget = self.initPictureWidget(self.supply_pos_x, self.supply_pos_y)
        return picture_widget
    
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
    def showDecks(self):
        curr = self.refence_deck.head
        for image in self.sorted_deck_images:
            if curr == None:
                temp_image_path = "pictures\\None_card.png"
            else:
                temp_image_path= curr.image_path
            pixmap = QPixmap(temp_image_path)
            image.setPixmap(pixmap)
            if not curr == None:
                curr = curr.next
        if self.supply_deck.head == None:
            self.supply_card_widget.setPixmap(QPixmap("pictures\\None_card.png"))
        else:
            self.supply_card_widget.setPixmap(QPixmap(self.supply_deck.head.image_path))
        
        return
    
    def winCheck(self):
        if self.refence_deck.inOrder() and self.refence_deck.length == len(self.sorted_deck_images):
            self.close()