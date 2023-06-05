from ds_classes import *
import random

def setup(size):
    deck = LINKEDLIST(1)
    undo_stack = LINKEDLIST()
    for i in range(2, size+1):
        pos = random.randint(0,deck.length)
        
        if pos == 0:
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

def topToBottom(deck, undo_stack):
    temp = deck.head
    deck.head = temp.next
    temp.next = deck.tail.next
    deck.tail.next = temp
    deck.tail = temp
    
    undo_stack = addToUndoStack(undo_stack, deck.length)

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

    undo_stack = addToUndoStack(undo_stack, index+1)
    
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
    undo_stack, deck = setup(8)

    while not win:
        print("\n"*(deck.length + 4))
        print(deck)
        action = input("1) Bottom\n2) Position = n+1\nWhat would you like to do? ")

        if not action.isnumeric():
            print("You did not enter a number. Try again")
        elif int(action) == 1:
            undo_stack, deck = topToBottom(deck, undo_stack)
        elif int(action) == 2:
            undo_stack, deck = topToNPlusOne(deck, undo_stack)
        else:
            print("You did not chose an acceptable choice. Try again")
        
        win = winCheck(deck)
    
    print(deck)
    print("You win!")