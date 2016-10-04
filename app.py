#!/usr/bin/python
import socket
from threading import Thread
import os
import subprocess
from PyQt4 import QtCore, QtGui
from time import sleep
import sys
import linecache


#while 1:

#		send("fanoff")
#	else:
#		send("setfan 0x%x" %(speed))
#		print "setfan 0x%x" %(speed)
#	sleep(1)


    
class MainWindow(QtGui.QMainWindow):
 	
		
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setFixedSize(180, 80)
        self.setWindowTitle('Probook Fan Control')
        self.setAutoFillBackground(True)
        scale =QtGui.QSlider(QtCore.Qt.Horizontal, self)
        scale.setRange(0,255)
        scale.setInvertedAppearance(True)
        scale.valueChanged.connect(changeValue)
        temperature = QtGui.QLabel(self)
        auto_check = QtGui.QCheckBox(self)
        auto_check.move(10,40)
        
        auto_label = QtGui.QLabel(self)
        auto_label.setText("Auto")
        auto_label.move(30,40)
        sets = QtGui.QLabel(self)
        sets.move(120,20)
        sets.setText("0");
        temperature.setText("Temperatura:")
        
        scale.setGeometry(10, 20, 100, 30)
        
 
        def updateValue():  
            temperature.setText("Temperatura:"+ getTemperature())
            tem = scale.value()
            sets.setText("PWM =" + str(tem))
            
            if auto_check.isChecked() == True:
                scale.setEnabled(False)
                auto_temp=int(getTemperature())
                speed = 0x80
                if auto_temp > 95:
                    speed = 0x00
                elif auto_temp > 90:
                    speed = 0x19
                elif auto_temp > 85:
                    speed = 0x29
                elif auto_temp > 80:
                    speed = 0x39
                elif auto_temp > 75:
                    speed = 0x49
                elif auto_temp > 70:
                    speed = 0x59
                elif auto_temp > 65:
                    speed = 0x70
                elif auto_temp > 60:
                    speed = 0x80
                else:
                    speed = 0xFF


                if speed == 0xFF:
                    send("fanoff")
                else:
                    send("setfan 0x%x" %(speed))
                  
            else:
                changeValue(tem)
                scale.setEnabled(True)
      
                

        self.Tim = QtCore.QTimer()
        QtCore.QObject.connect(self.Tim, QtCore.SIGNAL("timeout()"),updateValue)
        self.Tim.start(1000)
        
      


def changeValue(value):
    speed = value
    send("setfan 0x%x" %(speed))

     
def getTemperature():
	temp = subprocess.Popen("sensors | grep Physical | cut -b 18-19", stdout=subprocess.PIPE, shell=True).stdout.read()
	return temp.strip()

def send(cmd):
	s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	s.sendto(cmd, "/tmp/probook-socket")                
     
            
            
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())


