from ds_classes import *
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

def setup(size):
    # initilize LinkedLists
    supply_deck = LINKEDLIST()
    end_deck = LINKEDLIST()

    # add all in randomized positions
    for i in range(1, size+1):
        # choses random position
        pos = random.randint(0,supply_deck.length)
        # uses appropriate function to add node
        if i==1 or pos == 0:
            supply_deck.prepend(i)
        elif pos == supply_deck.length:
            supply_deck.append(i)
        elif pos < supply_deck.length:
            supply_deck.insert(pos, i)
    end_deck.append(supply_deck.remove(0))
    return end_deck, supply_deck

if __name__ == __name__:
    # initilize qt5 application
    app = QApplication(sys.argv)
    # initilize linked lists
    deck, supply_deck = setup(size=6)
    # create main game window
    game_window = APP(deck, supply_deck)
    
    # start game window with deck show
    game_window.showDecks()
    game_window.show()

    # start app
    app.exec_()