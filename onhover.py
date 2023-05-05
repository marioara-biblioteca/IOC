import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton,QToolTip
from PyQt5.QtCore import QSize    
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 100))    
        self.setWindowTitle("PyQt tooltip example - pythonprogramminglanguage.com") 
       
        pybutton = QPushButton('Pyqt', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 20)        
        pybutton.setToolTip('This is a tooltip message.')  
        QToolTip.setFont(QFont('Arial', 16))
    def clickMethod(self):
        print('PyQt')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
