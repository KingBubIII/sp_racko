from ds_classes import *
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

def setup(size):
    deck = LINKEDLIST()
    undo_stack = LINKEDLIST()

    for i in range(1, size+1):
        pos = random.randint(0,deck.length)
        
        if i==1 or pos == 0:
            deck.prepend(i)
        elif pos == deck.length:
            deck.append(i)
        elif pos < deck.length:
            deck.insert(pos, i)
    return undo_stack, deck

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

if __name__ == __name__:
    win = False
    app = QApplication(sys.argv)
    undo_stack, deck = setup(size=4)
    ex = APP(deck)
    
    ex.showDeck()
    ex.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("closing window")