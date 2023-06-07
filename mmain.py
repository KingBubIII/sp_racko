from ds_classes import *
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

def setup(size, qt_class):
    deck = LINKEDLIST()
    undo_stack = LINKEDLIST()

    for i in range(1, size+1):
        pos = random.randint(0,deck.length)
        
        if i==1 or pos == 0:
            deck.prepend(i, qt_class)
        elif pos == deck.length:
            deck.append(i, qt_class)
        elif pos < deck.length:
            deck.insert(pos, i, qt_class)
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

def showDeck():
    start_pos = [700,25]
    curr = deck.head
    shift_count = 0
    while not curr == None:
        curr.qt5_widget.move(start_pos[0]-(50*shift_count), start_pos[1]+(50*shift_count))
        curr.qt5_widget.lower()
        curr = curr.next
        shift_count+=1

if __name__ == __name__:
    win = False
    app = QApplication(sys.argv)
    ex = App()
    undo_stack, deck = setup(size=4, qt_class=ex)

    while not win:
        showDeck()
        ex.show()
        action = input("1) Bottom\n2) Position = n+1\n3) Undo\nWhat would you like to do? ")

        if not action.isnumeric():
            print("You did not enter a number. Try again")
        elif int(action) == 1:
            undo_stack, deck = topToBottom(deck, undo_stack)
        elif int(action) == 2:
            undo_stack, deck = topToNPlusOne(deck, undo_stack)
        elif int(action) == 3:
            undo_stack, deck = undo(undo_stack, deck)
        else:
            print("You did not chose an acceptable choice. Try again")
        
        win = winCheck(deck)
    
    print(deck)
    print("You win!")