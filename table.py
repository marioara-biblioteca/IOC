from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt,QSortFilterProxyModel

from PyQt5.QtGui import QPainter, QPen
from itertools import groupby
from operator import itemgetter

from file_scan import *
from table_model import *
from chart_statistics import *
from alerts_table import *
from snort_rules import *
from help_page import *
import qrc_resources



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.PieChartWindow=None
        self.FileScanWindow=None
        self.TableWindow=None
        self.RuleWindow=None
        self.HelpPage=None

        self.MainWindow=MainWindow
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
        self.verticalLayout_2.addLayout(self.horizontalLayout_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.add_icon()
        #menuBar
        self.create_actions()
        self.create_menu_bar()
        self.connect_actions()

        #statistics as piechart
        self.create_piechart()

        #statistics by count
        self.group()

        #filtering method by content 
        self.filter_alerts()
        #all alerts
        self.create_alert_table()
        self.create_status_bar()

        toolbar=QtWidgets.QToolBar("My main toolbar")
        self.verticalLayout_2.addWidget(toolbar)
        cutAction = QtWidgets.QAction(QtGui.QIcon("./icons/edit-cut.svg"), "&Delete", self.MainWindow)
        cutAction.setText("Detele alerts")
        cutAction.triggered.connect(self.delete_row)
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(cutAction)
        

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
    
    def add_icon(self):
        image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('panda.png')
        pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_1.addWidget(image)

    def create_actions(self):
        # File actions
        self.newAction = QtWidgets.QAction(self.MainWindow)
        self.newAction.setText("&Scan file")
        self.newAction.setIcon(QtGui.QIcon("./icons/bug.png"))
        self.openAction = QtWidgets.QAction(QtGui.QIcon("./icons/file-open.svg"), "&Detailed Alerts", self.MainWindow)
        self.addRuleAction =QtWidgets.QAction(QtGui.QIcon("./icons/file-new.svg"), "&Add new rule", self.MainWindow)
        
        # Help tips
        newTip = "Scan a possibly malicious file"
        self.newAction.setStatusTip(newTip)
        self.newAction.setToolTip(newTip)
      
        
        # Help actions
        self.helpContentAction = QtWidgets.QAction("&Help Content...", self.MainWindow)
        self.aboutAction = QtWidgets.QAction("&About...", self.MainWindow)
    def connect_actions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.create_new_file_scan)    
        self.openAction.triggered.connect(self.open_alerts_table)
        self.addRuleAction.triggered.connect(self.create_new_rule)
        
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.create_help_page)
        self.aboutAction.triggered.connect(self.about)
        # Connect Open Recent to dynamically populate it
        self.openRecentMenu.aboutToShow.connect(self.populate_create_statistic)
    def create_menu_bar(self):
        menuBar = self.MainWindow.menuBar()
        
        fileMenu =QtWidgets.QMenu("&Actions", self.MainWindow)
        menuBar.addMenu(fileMenu)

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.addRuleAction)
       
        self.openRecentMenu = fileMenu.addMenu(QtGui.QIcon("./icons/expand.svg"),"Open State Charts")

        helpMenu = menuBar.addMenu(QtGui.QIcon("./icons/help-content.svg"), "&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

        self.horizontalLayout_1.addWidget(menuBar)
    def create_new_rule(self):
        if self.RuleWindow is None:
            self.RuleWindow=SnortRuleForm(self)
            self.RuleWindow.show()
                 
        else:
            self.RuleWindow.close()
            self.RuleWindow=None
    def create_help_page(self):
        if self.HelpPage is None:
            self.HelpPage=Ui_HelpPage()
            self.HelpPage.show()
                 
        else:
            self.HelpPage.close()
            self.HelpPage=None
    def create_alert_table(self):

        QtWidgets.QToolTip.setFont(QtGui.QFont('Arial', 16))
        
        #https://www.elastic.co/guide/en/security/current/alerts-ui-manage.html
        tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        tableWidget.setToolTip('Alerts table')  
        tableWidget.setObjectName("tableWidget")
        self.verticalLayout_2.addWidget(tableWidget)

        self.alertsCols=len(data[0].keys())
        self.alertsRows=len(data)
        cols=self.alertsCols
        rows=self.alertsRows

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
                    item.setToolTip('Check') 
                    tableWidget.setItem(row,i,item)
                elif i == 1:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/more.svg'))
                    item.setToolTip('More') 
                    tableWidget.setItem(row, i, item)
                elif i==2:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/expand.svg'))
                    item.setToolTip('Expand') 
                    tableWidget.setItem(row, i, item)
                else:
                    tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem(v))
        self.alertsTable=tableWidget
    def delete_row(self):
        cols=self.alertsCols
        rows=self.alertsRows
        for row in range(rows):
            try:
                if self.alertsTable.item(row,0).checkState() == QtCore.Qt.Checked:
                    self.alertsTable.removeRow(row)
            except:
                pass
    
        
    
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
        chartview.setToolTip('This is a chart.')  
        self.horizontalLayout_2.addWidget(chartview)

    def create_status_bar(self):
        menubar = QtWidgets.QMenuBar(self.MainWindow)
        menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(menubar)
        statusbar = QtWidgets.QStatusBar(self.MainWindow)
        statusbar.setObjectName("statusbar")
        statusbar.showMessage("This is table")
        self.MainWindow.setStatusBar(statusbar)
   
    def group(self):
        
        data2 = sorted(data,
                    key = itemgetter('Rule'))        
        
        self.tableGroupedAlerts = QtWidgets.QTableWidget()
        self.tableGroupedAlerts.setObjectName("tableGroupedAlerts")
        self.tableGroupedAlerts.setWindowTitle("Alerts Table")
        self.horizontalLayout_2.addWidget(self.tableGroupedAlerts)

        cols=2
        rows=len(data2)
        self.tableGroupedAlerts.setColumnCount(cols)
        self.tableGroupedAlerts.setRowCount(rows)
        self.tableGroupedAlerts.setAlternatingRowColors(True)
        self.tableGroupedAlerts.setHorizontalHeaderLabels(['Rule','Count']) 
        self.tableGroupedAlerts.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        self.tableGroupedAlerts.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)

        for i,(key, value) in enumerate(groupby(data2,
                                key = itemgetter('Rule'))):

            self.tableGroupedAlerts.setItem(i,0,QtWidgets.QTableWidgetItem(key))
            self.tableGroupedAlerts.setItem(i,1,QtWidgets.QTableWidgetItem(str(len(list(value)))))
        
            

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
   

    def open_alerts_table(self):
        if self.TableWindow is None:
            self.TableWindow=Ui_AlertsTable()
            self.TableWindow.show()

        else:
            self.TableWindow.close()
            self.TableWindow=None

    def help_content(self):
        
        return

    def about(self):
        #TODO
        return

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
