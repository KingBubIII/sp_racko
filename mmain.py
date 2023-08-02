from ds_classes import *
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

def setup(size):
    # initilize LinkedLists
    deck = LINKEDLIST()
    undo_stack = LINKEDLIST()

    # add all in randomized positions
    for i in range(1, size+1):
        # choses random position
        pos = random.randint(0,deck.length)
        # uses appropriate function to add node
        if i==1 or pos == 0:
            deck.prepend(i)
        elif pos == deck.length:
            deck.append(i)
        elif pos < deck.length:
            deck.insert(pos, i)
    return undo_stack, deck

if __name__ == __name__:
    # initilize qt5 application
    app = QApplication(sys.argv)
    # initilize linked lists
    undo_stack, deck = setup(size=6)
    # create main game window
    game_window = APP(deck, undo_stack)
    
    # start game window with deck show
    game_window.showDeck()
    game_window.show()

    # start app
    app.exec_()