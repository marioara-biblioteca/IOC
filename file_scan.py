import hashlib
import zlib
from PyQt5 import QtCore, QtGui, QtWidgets
from file_browse import *
import urllib.request
import sys

data=[
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:01','Rule':'Potential persitance via login hook','Severity':'medium','Risk Score':'50','Reason':'modify key-value pairs in plist files to influence system behaviors, such as hiding the execution of an application (i.e. Hidden Window) or running additional commands for persistence '},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:02','Rule':'Malware prevention alert','Severity':'high','Risk Score':'73','Reason':'malware, intrusion_detection file event with process AYHelperService'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'}
]
class Ui_FileScan(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vLayout1 = QtWidgets.QVBoxLayout()
        self.vLayout2=QtWidgets.QVBoxLayout()
        self.layout0 = QtWidgets.QHBoxLayout()
        self.layout = QtWidgets.QHBoxLayout()
        self.bigLayout=QtWidgets.QVBoxLayout()
        
        self.create_menu_bar(self.layout0)
        self.layout0.addStretch()
        self.bigLayout.addLayout(self.layout0)
        
        self.add_label("Sandbox",1.5,Qt.AlignCenter,20)


        self.add_file_browser_layer1()
        self.add_submit_url_layer2()

        

        self.buttonClose = QtWidgets.QPushButton('Back')
        self.buttonClose.clicked.connect(self.close)
        
        
        self.vLayout1.addStretch()
        self.vLayout2.addStretch()
       

        self.bigLayout.addLayout(self.layout)
        self.add_label("Drag your file into left field or click to select a file",0.5,Qt.AlignVCenter,10)

        self.bigLayout.addStretch()

        self.setLayout(self.bigLayout)

    def create_menu_bar(self,parent):

        image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('panda.png')
        pixmap = pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.setAlignment(QtCore.Qt.AlignCenter)
        parent.addWidget(image)

        menubar = QtWidgets.QMenuBar()

        actionFile = menubar.addMenu("&Actions")

        actionFile.addAction(QtGui.QIcon("./icons/bug.png"),"&Scan file")
        actionFile.addAction(QtGui.QIcon("./icons/file-open.svg"), "&Detailed Alerts")
        actionFile.addAction(QtGui.QIcon("./icons/expand.svg"),"Open State Charts")
        actionFile.addSeparator()
       
       
        helpMenu=menubar.addMenu(QtGui.QIcon("./icons/help-content.svg"), "&Help")
        helpMenu.addAction("&Help Content")
        helpMenu.addAction("&About")
        parent.addWidget(menubar)

    def add_label(self,title,width,alignment,fontsize):
        label_princ = QtWidgets.QLabel(title, self)
        label_princ.setStyleSheet("border: "+str(width)+"px solid black;")
        label_princ.setAlignment(alignment)
        label_princ.setFont(QtGui.QFont('Times',fontsize))
        self.bigLayout.addWidget(label_princ)
    def add_file_browser_layer1(self):
        self.fileBrowser=FileBrowser('Open File')
        self.vLayout1.addWidget(self.fileBrowser)
        self.buttonAnayze = QtWidgets.QPushButton('Analyze')
        self.buttonAnayze.clicked.connect(self.analize_file)
        self.buttonAnayze.setMaximumWidth(200)
        self.vLayout1.addWidget(self.buttonAnayze)
        self.layout.addLayout(self.vLayout1)
    def add_submit_url_layer2(self):
        self.url_label= QtWidgets.QLineEdit( self) 
        self.url_label.setPlaceholderText("Submit url or hash")    
        
        self.url_label.setAlignment(Qt.AlignLeft | Qt.AlignHCenter)
        self.url_label.setStyleSheet("border: 1px solid black; background-color: rgb(229, 228, 226);")
        self.url_label.setFixedSize(400,200)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(25, 45, 210, 30)
        self.progressBar.hide()
        

        buttonClose = QtWidgets.QPushButton('Submit')
        buttonClose.clicked.connect(self.action_submit)

        self.vLayout2.addWidget(self.url_label)
        self.vLayout2.addWidget(buttonClose)

        self.vLayout2.addWidget(self.progressBar)
        self.layout.addLayout(self.vLayout2)
    def handle_progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize
 
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QtWidgets.QApplication.processEvents()
    def action_submit(self):
        #down_url=https://www.travelandleisure.com/thmb/n4LZNPWDaJnGGl4jz988ms4u-Pk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/header-PARISPANDA1221-87f0c4cc46bf423ebcaf669c50912c3c.jpg
        self.progressBar.show()
        down_url=self.url_label.text()
        save_loc='./file.dat'
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', '*')
        filename, headers = opener.retrieve(down_url, save_loc,self.handle_progress)

        print(self.url_label.text())
    def analize_file(self):
        try:
            file=self.fileBrowser.getPaths()[0]
        except:
            file='./table.py'
    
        # icon_1=QtWidgets.QLabel()
        # pixmap=QtGui.QPixmap('./icons/done.svg')
        # pixmap= pixmap.scaled(30, 30,Qt.KeepAspectRatio)
        # icon_1.setPixmap(pixmap)
        # icon_1.setAlignment(Qt.AlignLeft)
        # self.vLayout1.addWidget(icon_1)

        label_2 = QtWidgets.QLabel("Summary", self)       
        label_2.setStyleSheet("border: 1px solid black;")
        label_2.setAlignment(Qt.AlignLeft | Qt.AlignHCenter)
        self.vLayout1.addWidget(label_2)

        tableWidget=QtWidgets.QTableWidget()
        cols=2
        rows=8
        tableWidget.setColumnCount(cols)
        tableWidget.setRowCount(rows)

        tableWidget.setAlternatingRowColors(True)
        tableWidget.setWindowTitle("File analysis")
        tableWidget.setHorizontalHeaderLabels(data[0].keys()) 
        [tableWidget.horizontalHeader().setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeToContents) for i in range(cols-1)]
        tableWidget.horizontalHeader().setSectionResizeMode(cols-1,QtWidgets.QHeaderView.Stretch)
        self.vLayout1.addWidget(tableWidget)

        with open(file,'rb') as f:
            content=f.read()
        file_data={"Filename":file,"File type":"binary data","MD5":hashlib.md5(content).hexdigest(),"Sha256":hashlib.sha256(content).hexdigest(),"Sha512":hashlib.sha512(content).hexdigest(),"CRC32":hex(zlib.crc32(content) & 0xffffffff),"Yara":"None Matched","Score":"32"}
        for i, (k, v) in enumerate(file_data.items()):
            tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(k))
            tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(v))
       
        self.buttonAnayze.hide()
        self.fileBrowser.hide()
        
        self.bigLayout.addWidget(self.buttonClose)