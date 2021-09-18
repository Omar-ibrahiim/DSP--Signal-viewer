from PyQt5 import QtWidgets, QtCore
import UI as UI
import sys
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from txtAcsv import txt 
from mat import mat

def getData():
    # get the file and read it
    filePath= QtWidgets.QFileDialog.getOpenFileName(None,  'load', "./","All Files *;;" "*.csv;;" " *.txt;;" "*.mat")
    #getting the filename indexes in the filepath#
    BegOfTheName= filePath[0].rfind('/')+1 
    LastOfTheName= filePath[0].rfind('.')
    filename=filePath[0][BegOfTheName:LastOfTheName] 
    datatype = filePath[0][LastOfTheName+1:] #get the datatype from the filePath
    #making sure of the file type and read it#
    if(datatype=="txt" or datatype=="csv"):
        data=txt(filePath[0])
    elif(datatype=="mat"):
        data=mat(filePath[0])  
    else:
        return None
    return [data,filename]


#Colors#
green= (0,255,0,200)
red= (255,0,0,200)
blue= (0,0,255,200)
sky= (0,255,255,200)
yellow= (255,255,0,200)

class Widget():
    #The Widget OBJECT#
    def __init__(self,upperWidget,lowerWidget,checkBox,color):
        #Setting up the OBJECT data#
        self.fileName="Hello" 
        self.color=color
        self.checkBox=checkBox
        self.data=None 
        self.ptr=0
        self.Enable=False
        self.checkBox.setDisabled(True)
        
        #Setting up the upper part#
        self.upperWidget=upperWidget
        self.upperPlot=upperWidget.plotItem
        self.upperPlot.addLegend()
        self.upperCurve=upperWidget.plot(pen=self.color ,name=self.fileName )
        self.upperView=self.upperPlot.getViewBox()
        self.upperWidget.setHidden(True)
        
        #Setting up the lower part#
        self.lowerWidget=lowerWidget
        #self.lowerPlot=lowerWidget.plotItem
        #self.lowerCurve=lowerWidget.plot(pen=color)
        #self.lowerView=self.lowerPlot.getViewBox()
        self.lowerWidget.close()
        
        #Setupping the timer#
        self.timer=QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.DrawExtraPoint)
    
    def DrawExtraPoint(self):
        #make the graph move by adding one point to the data drawing every step#
        x1 = np.arange(len(self.data[:self.ptr]))/200
        y1 = self.data[0:self.ptr]
        self.upperCurve.setData(x=x1,y=y1)
        self.ptr += 1
    
    def StartPlotting(self,data):
        #taking the data from getData() to plot#
        self.data=data[0]
        self.fileName=data[1]
        self.ptr=0
        self.Enable=True
        
        #setting up the check box for the channel#
        self.checkBox.setEnabled(True)
        self.checkBox.setChecked(True)
        self.checkBox.setText(self.fileName)
        
        #setting up the new legend#
        #self.upperCurve.clear()
        self.upperPlot.legend.scene().removeItem(self.upperPlot.legend)
        self.upperPlot.addLegend()
        self.upperPlot.plot(pen=self.color,name=self.fileName)
            
        
    def start_timer(self):
        if self.data is None:
            pass
        else:
            self.timer.start()
            
    def pause_timer(self):
        if self.data is None:
            pass
        else:
            self.timer.stop()
            
    def stopPlotting(self):
        if self.Enable:
            self.upperCurve.clear()
            self.ptr=0
            self.timer.stop()
            
    def zoomIn(self):
        self.upperView.scaleBy(0.5)
        
    def zoomOut(self):
        self.upperView.scaleBy(2)
        
    def toggleCheckbox(self):
        if self.data is None:
            pass
        else:
            if self.checkBox.isChecked():
                self.Enable=True
                self.upperWidget.setHidden(False)
            else:
                self.Enable=False
                self.upperWidget.setHidden(True)
                #self.ptr=0 
                #self.upperCurve.clear()   
                  

        
        


class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self, mainwindow):
        super(ApplicationWindow,self).setupUi(mainwindow)
        
        self.Widgets = [
            Widget(self.widget,self.widget_2,self.checkBox,color=green),
            Widget(self.widget_3,self.widget_4,self.checkBox_2,color=red),
            Widget(self.widget_5,self.widget_6,self.checkBox_3,color=blue),
            Widget(self.widget_7,self.widget_8,self.checkBox_4,color=sky),
            Widget(self.widget_9,self.widget_10,self.checkBox_5,color=yellow)
                       ]
        
        self.pushButton_4.clicked.connect(self.openFile)
        self.pushButton.clicked.connect(self.start_timer)
        self.pushButton_2.clicked.connect(self.pause_timer)
        self.pushButton_7.clicked.connect(self.PlayAll)
        self.pushButton_3.clicked.connect(self.stopPlotting)
        self.pushButton_5.clicked.connect(self.zoomIn)
        self.pushButton_6.clicked.connect(self.zoomOut)
        self.checkBox.toggled.connect(self.toggle1)
        self.checkBox_2.toggled.connect(self.toggle2)
        self.checkBox_3.toggled.connect(self.toggle3)
        self.checkBox_4.toggled.connect(self.toggle4)
        self.checkBox_5.toggled.connect(self.toggle5)

        
    def openFile(self):
        #gets the data and transmit it to the channel chosen#
        channel=self.comboBox.currentIndex()
        data=None
        data = getData()
        if data is None:# if there is no data (canceled)#
            pass
        else:
            self.Widgets[int(channel)].StartPlotting(data)
            if channel+1 == 5:
                self.comboBox.setCurrentIndex(0)
            else:
                self.comboBox.setCurrentIndex(channel+1)
            
    #all of the functions below is to send the right order to the right channel#
    def start_timer(self):
        channel=self.comboBox.currentIndex()
        self.Widgets[int(channel)].start_timer()
    def pause_timer(self):
        channel=self.comboBox.currentIndex()
        self.Widgets[int(channel)].pause_timer()
    def PlayAll(self):
        for i in range(5):
            self.Widgets[int(i)].start_timer()
    def stopPlotting(self):
        for i in range(5):
            self.Widgets[int(i)].stopPlotting()
    def zoomIn(self):
        channel=self.comboBox.currentIndex()
        self.Widgets[int(channel)].zoomIn()
    def zoomOut(self):
        channel=self.comboBox.currentIndex()
        self.Widgets[int(channel)].zoomOut()
    def toggle1(self):
        self.Widgets[int(0)].toggleCheckbox()
    def toggle2(self):
        self.Widgets[int(1)].toggleCheckbox()
    def toggle3(self):
        self.Widgets[int(2)].toggleCheckbox()
    def toggle4(self):
        self.Widgets[int(3)].toggleCheckbox()
    def toggle5(self):
        self.Widgets[int(4)].toggleCheckbox()        
        
def main():
    app=QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = ApplicationWindow(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()