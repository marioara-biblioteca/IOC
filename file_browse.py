from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class FileBrowser(QtWidgets.QWidget):
  
    OpenFile = 0
    
    def __init__(self, title):
        QtWidgets.QWidget.__init__(self)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
    
        self.filter_name = 'All files (*.*)'
        self.dirpath = QtCore.QDir.currentPath()
        
        label = QtWidgets.QLabel()
        label.setText(title)
        label.setFixedWidth(265)
        label.setFont(QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(label)
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        
        self.layout.addWidget(self.lineEdit)
        
        self.buttonSearch = QtWidgets.QPushButton('Search')
        self.buttonSearch.clicked.connect(self.get_file)
        self.layout.addWidget(self.buttonSearch)

        self.layout.addStretch()
    
        return
    def get_file(self):
        self.filepaths = []
        self.filepaths.append(QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose File',
                                                directory=self.dirpath,
                                                filter=self.filter_name)[0])            
            
        if len(self.filepaths) == 0:
            return
        elif len(self.filepaths) == 1:
            self.lineEdit.setText(self.filepaths[0])
        else:
            self.lineEdit.setText(",".join(self.filepaths))    
    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)    
 
    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    def getPaths(self):
        return self.filepaths