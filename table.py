from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
data=[
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:01','Rule':'Potential persitance via login hook','Severity':'medium','Risk Score':'50','Reason':'modify key-value pairs in plist files to influence system behaviors, such as hiding the execution of an application (i.e. Hidden Window) or running additional commands for persistence '},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:02','Rule':'Malware prevention alert','Severity':'high','Risk Score':'73','Reason':'malware, intrusion_detection file event with process AYHelperService'},
        {'Check':'','More':'','Details':'','@timestamp':'2023/03/12 12:00:00','Rule':'Enumeration of users or Groups','Severity':'low','Risk Score':'21','Reason':'process event with process dsmemberutil, parent process bash, by root'}
]
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Alerts Table")
        MainWindow.resize(566, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.create_piechart()

        #https://www.elastic.co/guide/en/security/current/alerts-ui-manage.html
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.tableWidget.setWindowTitle("Alerts Table")

        cols=len(data[0].keys())
        rows=len(data)

        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setHorizontalHeaderLabels(data[0].keys()) 
        [self.tableWidget.horizontalHeader().setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeToContents) for i in range(cols-1)]
        self.tableWidget.horizontalHeader().setSectionResizeMode(cols-1,QtWidgets.QHeaderView.Stretch)
        for row in range(rows):
            for i, (k, v) in enumerate(data[row].items()):
               
                if i == 0:
                    item=QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked) 
                    self.tableWidget.setItem(row,i,item)
                elif i == 1:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/more.svg'))
                    self.tableWidget.setItem(row, i, item)
                elif i==2:
                    item = QtWidgets.QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setIcon(QtGui.QIcon('./icons/expand.svg'))
                    self.tableWidget.setItem(row, i, item)


                else:
                    self.tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem(v))

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("This is table")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
        self.verticalLayout_2.addWidget(chartview)
        # self.setCentralWidget(chartview)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
