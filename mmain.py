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

if __name__ == __name__:
    win = False
    app = QApplication(sys.argv)
    undo_stack, deck = setup(size=4)
    ex = APP(deck, undo_stack)
    
    ex.showDeck()
    ex.show()
    app.exec_()