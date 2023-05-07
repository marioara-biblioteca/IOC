from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QSortFilterProxyModel, QAbstractTableModel

from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from itertools import groupby
from operator import itemgetter
import qrc_resources
data=[
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:01','Rule':'Potential persitance via login hook','Severity':'medium','Risk Score':'50','Reason':'modify key-value pairs in plist files to influence system behaviors, such as hiding the execution of an application (i.e. Hidden Window) or running additional commands for persistence '},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:02','Rule':'Malware prevention alert','Severity':'high','Risk Score':'73','Reason':'malware, intrusion_detection file event with process AYHelperService'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'}
]
class FileBrowser(QtWidgets.QWidget):
  
    OpenFile = 0
    
    def __init__(self, title):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
    
        self.filter_name = 'All files (*.*)'
        self.dirpath = QtCore.QDir.currentPath()
        
        self.label = QtWidgets.QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(265)
        self.label.setFont(QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        
        layout.addWidget(self.lineEdit)
        
        self.button = QtWidgets.QPushButton('Search')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

    def getFile(self):
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
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers=list(data[0].keys())[3:]        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][self._headers[index.column()]]

    def rowCount(self, index):
        return len(self._data)
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._headers[section])

            if orientation == Qt.Vertical:
                return str(section)

    def columnCount(self, index):
        return len(self._headers)
cpu_causes={'backend core':[8.5,QtGui.QColor("#82d3e5")],
                'bad speculations':[15.4,QtGui.QColor("#cfeef5")],
                'retring':[32.0,QtGui.QColor("#fdc4c1")],
                'frontend latency':[13.8, QtGui.QColor("#fd635c")],
                'frontend bandwith':[9.7,QtGui.QColor("#feb543")],
                'backend memory':[20.5,QtGui.QColor("#ffe3b8")]}
memory_causes={'heap':[8.5,QtGui.QColor("#82d3e5")],
                'thread':[15.4,QtGui.QColor("#cfeef5")],
                'internal':[32.0,QtGui.QColor("#fdc4c1")],
                'cache':[13.8, QtGui.QColor("#fd635c")],
                'symbol':[9.7,QtGui.QColor("#feb543")],
                'compressed class space':[20.5,QtGui.QColor("#ffe3b8")]}
class Ui_ChartStatisticsWindow(QtWidgets.QWidget):
    def __init__(self,flag):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        if flag == 'CPU':
            chart=self.create_piechart(cpu_causes,"CPU load")
        else:
            chart=self.create_piechart(memory_causes,"RAM summary")
        layout.addWidget(chart)
        self.setLayout(layout)
    
    def create_piechart(self,causes,title):
        series = QPieSeries()
        for item in causes.items():
            one_slice=QPieSlice(item[0],item[1][0])
            one_slice.setExploded(True)
            one_slice.setLabelVisible(True)
            one_slice.setLabelVisible(True)
        
            label = "<p align='center' style='color:{}'>{}%</p>".format("#82d3e5",item[0]+'\n'+str(round(item[1][0], 2)))
            one_slice.setLabel(label)
            one_slice.setColor(item[1][1])
            series.append(one_slice)
    
    
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        return chartview

class Ui_FileScan(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.fileBrowser=FileBrowser('Open File')
        layout.addWidget(self.fileBrowser)
        self.setLayout(layout)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow=MainWindow
        self.PieChartWindow=None
        self.FileScanWindow=None
        self.MainWindow.setObjectName("Alerts Table")
        self.MainWindow.resize(566, 475)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label=QtWidgets.QLabel(self.centralwidget)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        #self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        #menuBar
        self.create_actions()
        self.create_menu_bar()
        self.connect_actions()
        #self.create_piechart()
        #statistics as piechart
        self.create_piechart()

        #statistics by count
        self.group()

        #filtering method by content 
        self.filter_alerts()
        #all alerts
        self.create_alert_table()
        self.create_status_bar()

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    def create_actions(self):
        # File actions
        self.newAction = QtWidgets.QAction(self.MainWindow)
        self.newAction.setText("&New")
        self.newAction.setIcon(QtGui.QIcon("./icons/file-new.svg"))
        self.openAction = QtWidgets.QAction(QtGui.QIcon("./icons/file-open.svg"), "&Open...", self.MainWindow)
        self.saveAction = QtWidgets.QAction(QtGui.QIcon("./icons/file-save.svg"), "&Save", self.MainWindow)
        self.exitAction = QtWidgets.QAction("&Exit", self.MainWindow)
        # String-based key sequences
        self.newAction.setShortcut("Ctrl+N")
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")
        # Help tips
        newTip = "Create a new file"
        self.newAction.setStatusTip(newTip)
        self.newAction.setToolTip(newTip)
        self.newAction.setWhatsThis("Create a new and empty text file")
        # Edit actions
        self.copyAction = QtWidgets.QAction(QtGui.QIcon("./icons/edit-copy.svg"), "&Copy", self.MainWindow)
        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("./icons/edit-paste.svg"), "&Paste", self.MainWindow)
        self.cutAction = QtWidgets.QAction(QtGui.QIcon("./icons/edit-cut.svg"), "C&ut", self.MainWindow)
        # Standard key sequence
        self.copyAction.setShortcut(QtGui.QKeySequence.Copy)
        self.pasteAction.setShortcut(QtGui.QKeySequence.Paste)
        self.cutAction.setShortcut(QtGui.QKeySequence.Cut)
        # Help actions
        self.helpContentAction = QtWidgets.QAction("&Help Content...", self.MainWindow)
        self.aboutAction = QtWidgets.QAction("&About...", self.MainWindow)
    def connect_actions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.MainWindow.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
        # Connect Open Recent to dynamically populate it
        self.openRecentMenu.aboutToShow.connect(self.populate_create_statistic)
    def create_menu_bar(self):
        menuBar = self.MainWindow.menuBar()
        
        fileMenu =QtWidgets.QMenu("&Open", self.MainWindow)
        menuBar.addMenu(fileMenu)

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        
        self.openRecentMenu = fileMenu.addMenu("Open State Charts")
        fileMenu.addAction(self.saveAction)
        
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        
        editMenu.addSeparator()
        
        findMenu = editMenu.addMenu("Find and Replace")
        findMenu.addAction("Find...")
        findMenu.addAction("Replace...")
        
        helpMenu = menuBar.addMenu(QtGui.QIcon("./icons/help-content.svg"), "&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

        self.horizontalLayout_1.addWidget(menuBar)
    
    def create_alert_table(self):

        #https://www.elastic.co/guide/en/security/current/alerts-ui-manage.html
        tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        tableWidget.setObjectName("tableWidget")
        self.verticalLayout_2.addWidget(tableWidget)

        cols=len(data[0].keys())
        rows=len(data)
        tableWidget.setColumnCount(cols)
        tableWidget.setRowCount(rows)

        tableWidget.setAlternatingRowColors(True)
        tableWidget.setWindowTitle("Alerts Table")
        tableWidget.setHorizontalHeaderLabels(data[0].keys()) 
        [tableWidget.horizontalHeader().setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeToContents) for i in range(cols-1)]
        tableWidget.horizontalHeader().setSectionResizeMode(cols-1,QtWidgets.QHeaderView.Stretch)
        for row in range(rows):
            for i, (k, v) in enumerate(data[row].items()):
                if i == 0:
                    item=QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked) 
                    tableWidget.setItem(row,i,item)
                elif i == 1:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/more.svg'))
                    tableWidget.setItem(row, i, item)
                elif i==2:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/expand.svg'))
                    tableWidget.setItem(row, i, item)
                else:
                    tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem(v))
    def filter_alerts(self):
        model = TableModel(data)
        proxy_model = QSortFilterProxyModel()
        proxy_model.setFilterKeyColumn(-1) # Search all columns.
        proxy_model.setSourceModel(model)
        proxy_model.sort(0, Qt.AscendingOrder)
        tableWidget=QtWidgets.QTableView()
        tableWidget.setModel(proxy_model)
        searchbar =QtWidgets.QLineEdit()
        searchbar.textChanged.connect(proxy_model.setFilterFixedString)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(searchbar)
        layout.addWidget(tableWidget)

        self.horizontalLayout_2.addLayout(layout)
       
    def create_piechart(self):
       
        series = QPieSeries()
        severity_counts=[0]*3
        for i in range(len(data)):
            if data[i]['Severity']=='low':
                severity_counts[0]+=1
            elif data[i]['Severity']=='medium':
                severity_counts[1]+=1
            else:
                severity_counts[2]+=1
        series.append("Low", severity_counts[0])
        series.append("Medium", severity_counts[1])
        series.append("High", severity_counts[2])
       

        #adding slice
        slice = QPieSlice()
        slice = series.slices()[2]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Severity levels")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.horizontalLayout_2.addWidget(chartview)

    def create_status_bar(self):
        menubar = QtWidgets.QMenuBar(self.MainWindow)
        menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        menubar.setObjectName("menubar")
        MainWindow.setMenuBar(menubar)
        statusbar = QtWidgets.QStatusBar(self.MainWindow)
        statusbar.setObjectName("statusbar")
        statusbar.showMessage("This is table")
        MainWindow.setStatusBar(statusbar)
    def group(self):
        data2 = sorted(data,
                    key = itemgetter('Rule'))

        
           
        
        tableGroupedAlerts = QtWidgets.QTableWidget()
        tableGroupedAlerts.setObjectName("tableGroupedAlerts")
        tableGroupedAlerts.setWindowTitle("Alerts Table")
        self.horizontalLayout_2.addWidget(tableGroupedAlerts)

        cols=2
        rows=len(data2)
        tableGroupedAlerts.setColumnCount(cols)
        tableGroupedAlerts.setRowCount(rows)
        tableGroupedAlerts.setAlternatingRowColors(True)
        tableGroupedAlerts.setHorizontalHeaderLabels(['Rule Name','Count']) 
        tableGroupedAlerts.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        tableGroupedAlerts.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)

        for i,(key, value) in enumerate(groupby(data2,
                                key = itemgetter('Rule'))):

            tableGroupedAlerts.setItem(i,0,QtWidgets.QTableWidgetItem(key))
            tableGroupedAlerts.setItem(i,1,QtWidgets.QTableWidgetItem(str(len(list(value)))))
            

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    def newFile(self):
        self.centralwidget.setText("<b>File > New</b> clicked")

    def openFile(self):
        self.centralwidget.setText("<b>File > Open...</b> clicked")

    def saveFile(self):
        self.centralwidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        self.centralWidget.setText("<b>Help > About...</b> clicked")

    def populate_create_statistic(self):   
        self.openRecentMenu.clear()
        
        actions = []
        metrics = ['RAM','CPU']

        for metric in metrics:
            
            action = QtWidgets.QAction(metric, self.MainWindow)
            from functools import partial

            action.triggered.connect(partial(self.create_new_statistic, metric))
            actions.append(action)
        #
        self.openRecentMenu.addActions(actions)

    def create_new_statistic(self, metric):  
        if self.PieChartWindow is None:
            self.PieChartWindow=Ui_ChartStatisticsWindow(metric)
            self.PieChartWindow.show()
        else:
            self.PieChartWindow.close()
            self.PieChartWindow=None
    def create_new_file_scan(self):
        if self.FileScanWindow is None:
            self.FileScanWindow=Ui_FileScan()
            self.FileScanWindow.show()
        else:
            self.FileScanWindow.close()
            self.FileScanWindow=None

    def getWordCount(self):
        # Logic for computing the word count goes here...
        return 42


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
