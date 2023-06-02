from ds_classes import *
import random

def setup(size):
    deck = LinkedList(1)
    for i in range(2, size+1):
        pos = random.randint(0,deck.length)
        
        if pos == 0:
            deck.prepend(i)
        elif pos == deck.length:
            deck.append(i)
        elif pos < deck.length:
            deck.insert(pos, i)
    print(deck)