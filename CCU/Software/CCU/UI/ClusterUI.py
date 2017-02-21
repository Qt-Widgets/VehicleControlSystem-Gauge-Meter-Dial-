'''
Created on 18 feb. 2017

@author: c
'''

from PySide import QtGui, QtCore, QtSvg
import serial
from PySide.QtGui import *



class ClusterUI(QtGui.QWidget):
    
    def __init__(self):
        super(ClusterUI, self).__init__()
        global ser 
        ser = serial.Serial('COM8',9600)
        self.setupUpdateThread()  # thread
        self.initUI()
        
       
    def initUI(self):
        self.speed = 0
        self.speedFade = 0
        global errorIconOn
        errorIconOn = 1
        
        self.renderer = QtSvg.QSvgRenderer('outiline.svg')        
        
        self.speedPointerRenderer = QtSvg.QSvgRenderer('speedPointer.svg')        
        self.clusterDisplayHight = 480
        self.clusterDisplayWidth = 1280
        self.setGeometry(300, 200, 1280,480)  # window size
        self.show()
        
    def paintEvent(self, event):
             
        painter = QtGui.QPainter(self);
        self.renderer.render(painter);
        painter.end()
        
        qtime = QtGui.QPainter(self)
        atime = QtCore.QTime.currentTime()
        qtime.setPen(QtGui.QColor(220, 220, 220))
        qtime.setFont(QtGui.QFont('Decorative', 10))
        qtime.drawText(QtCore.QRect(430,10,80,50),QtCore.Qt.AlignCenter,str(atime.hour()) + ":" + str(atime.minute()) + ":" + str(atime.second()))
        qtime.end()
        
        qspeed = QtGui.QPainter(self)
        qspeed.setPen(QtGui.QColor(220, 220, 220))
        qspeed.setFont(QtGui.QFont('LCDMono2', 40))
        qspeed.drawText(QtCore.QRect((self.clusterDisplayWidth / 2) ,(self.clusterDisplayHight / 2) - 40 ,120,55),QtCore.Qt.AlignVCenter, str(self.speed))
        qspeed.end()
                
        qp3 = QtGui.QPainter(self)
        qp3.translate((self.clusterDisplayWidth / 2) ,(self.clusterDisplayHight / 2))
        qp3.rotate(-209 + (int(self.speed)/1.175))
        self.speedPointerRenderer.render(qp3);
        qp3.end() 

        if (errorIconOn == 1):
            qp3 = QtGui.QPainter(self)
            errorIconImage = QtGui.QImage("errorIcon.png")
            qp3.drawImage(QtCore.QRect(160,100,50,50),errorIconImage)
            qp3.end()



        #self.update()
             
        # update GUI current time label  
    def updateSpeed(self,text):
        
        self.speed = int(text)
        self.update()

    # update GUI current time label
    def updateTime(self):
        time = QtCore.QTime.currentTime()
        self.timeLabel.setText(str(time.hour()) + ":" + str(time.minute()) + ":" + str(time.second())) 
            
    def setupUpdateThread(self):  
        self.updateThread = upateThread()  
        self.updateThread.progress.connect(self.updateSpeed, QtCore.Qt.QueuedConnection)  

        if not self.updateThread.isRunning():  # if the thread has not been started let's kick it off  
            self.updateThread.start() 


#inherit from Qthread and setup our own thread class  #
class upateThread(QtCore.QThread):  
    progress = QtCore.Signal(str)  # create a custom signal we can subscribe to to emit update commands  
    def __init__(self, parent=None):  
        super(upateThread, self).__init__(parent)  
        self.exiting = False  
        self.aSpeed = 0
        self.fadeSpeed = 0
    def run(self):
        while True:  
            self.msleep(0.1)
            #QSound.play("beep1.wav")
            #print QSound.isAvailable()
            
            '''
            if (self.fadeSpeed == 0):
                self.aSpeed = self.aSpeed + 1
                if (self.aSpeed >= 280):
                    self.fadeSpeed = 1
            else:
                self.aSpeed = self.aSpeed - 1
                if (self.aSpeed <= 0 ):
                    self.fadeSpeed = 0 
            self.progress.emit(str(self.aSpeed))       
            '''
            #print (ser.readline().strip())
            self.progress.emit(ser.readline().strip())
    