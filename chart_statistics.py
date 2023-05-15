from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt

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
        chartview.setRenderHint(QtGui.QPainter.Antialiasing)
        return chartview

