from ds_classes import *
import random

def setup(size):
    deck = LINKEDLIST(1)
    for i in range(2, size+1):
        pos = random.randint(0,deck.length)
        
        if pos == 0:
            deck.prepend(i)
        elif pos == deck.length:
            deck.append(i)
        elif pos < deck.length:
            deck.insert(pos, i)
    return deck

def topToBottom(deck):
    temp = deck.head
    deck.head = temp.next
    temp.next = deck.tail.next
    deck.tail.next = temp
    deck.tail = temp
    
    return deck

def topToNPlusOne(deck):
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
    
    return deck

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
    deck = setup(4)

    while not win:
        print("\n"*(deck.length + 4))
        print(deck)
        action = input("1) Bottom\n2) Position = n+1\nWhat would you like to do? ")

        if not action.isnumeric():
            print("You did not enter a number. Try again")
        elif int(action) == 1:
            deck = topToBottom(deck)
        elif int(action) == 2:
            deck = topToNPlusOne(deck)
        else:
            print("You did not chose an acceptable choice. Try again")
        
        if winCheck(deck):
            print(deck)
            print("You win!")
            break