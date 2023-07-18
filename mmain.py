from ds_classes import *
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

def setup(size, qt_class):
    deck = LINKEDLIST()
    undo_stack = LINKEDLIST()
    image_widgets = initWidgets(qt_class, size)

    for i in range(1, size+1):
        pos = random.randint(0,deck.length)
        
        if i==1 or pos == 0:
            deck.prepend(i)
        elif pos == deck.length:
            deck.append(i)
        elif pos < deck.length:
            deck.insert(pos, i)
    return undo_stack, deck, image_widgets

# This is where the card images will be attached to
def initWidgets(qt_class, amount = 1):
    # the list of widgets to be returned
    image_widgets = []
    # the starting position on the qt5 canvas
    start_pos = [700,25]
    # creates an object for however long the list is
    for count in range(amount):
        # initialize the object
        label = QLabel(qt_class)
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

def addToUndoStack(undo_stack, index):
    if undo_stack.length >= 3:
        undo_stack.remove(2)

    undo_stack.prepend(index)
    return undo_stack

def undo(undo_stack, deck):
    if undo_stack.length > 0:
        pre = deck.Traverse(undo_stack.remove(0)-1)            
        temp = pre.next
        aft = temp.next

        pre.next = aft
        temp.next = deck.head
        deck.head = temp
    else:
        print("You have nothing left to undo. Remember the max you can undo at one time is 3.")
    
    return undo_stack, deck

def topToBottom(deck, undo_stack):
    temp = deck.head
    deck.head = temp.next
    temp.next = deck.tail.next
    deck.tail.next = temp
    deck.tail = temp
    
    undo_stack = addToUndoStack(undo_stack, deck.length-1)

    return undo_stack, deck

def topToNPlusOne(deck, undo_stack):
    index = (deck.head.value+1) % deck.length
    if index > 0:
        pre = deck.head
        for count in range(index):
            pre = pre.next
        
        aft = pre.next
        
        temp = deck.head
        deck.head = deck.head.next
        pre.next = temp
        temp.next = aft
        if aft == None:
            deck.tail = temp

        undo_stack = addToUndoStack(undo_stack, index)
    
    return undo_stack, deck

def winCheck(deck):
    win = True
    curr_node = deck.head
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

def showDeck(deck, image_widgets):
    curr = deck.head
    for object in image_widgets:
        pixmap = QPixmap(curr.image_path)
        object.setPixmap(pixmap)
        curr = curr.next
    
    return deck, image_widgets

if __name__ == __name__:
    win = False
    app = QApplication(sys.argv)
    ex = App()
    undo_stack, deck, image_widgets = setup(size=4, qt_class=ex)
    deck, image_widgets = showDeck(deck, image_widgets)
    ex.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("closing window")
    
    print(deck)
    print("You win!")