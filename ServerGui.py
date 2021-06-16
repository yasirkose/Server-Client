from PyQt5.QtWidgets import *
import sys
import threading
from PyQt5 import QtWidgets, uic
#from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QRegExpValidator,QIntValidator
from PyQt5.QtCore import QSize, QRegExp
import socket
class server(QtWidgets.QMainWindow):
    def __init__(self):
        super(server, self).__init__()
        uic.loadUi('serverForm.ui', self)
        self.baslangic()
        self.buttonBaglan.clicked.connect(self.baglan)
        #self.button_sendData.clicked.connect(self.islemGonder)
        self.show()
    def baslangic(self):
        self.lineEditIP.setPlaceholderText('Hedef Ip Giriniz(xxx.xx.xx.xx)')
        self.lineEditPort.setPlaceholderText('Hedef Port Giriniz')
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEditIP.setValidator(ipValidator)
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.lineEditIP.setText(local_ip)
        self.lineEditPort.setValidator(QIntValidator())
        self.lineEditPort.setText("9090")

    def threadGuiYaz(self):
        self.labelDurum.setText("Server Dinlemede...")
        self.labelGelen.setText("Dinlenilen adres=> " + self.lineEditIP.text() + ":" + self.lineEditPort.text())
        self.labelDurum.setStyleSheet("background-color:rgb(108,248,255)")
        self.update()
    def threadGuiYazBaglandi(self):
        self.labelDurum.setText("Server Bağlandı...")
        self.labelDurum.setStyleSheet("background-color:rgb(143,234,118)")
        self.labelGelen.setText("Bağlanılan adres=> " + self.lineEditIP.text() + ":" + self.lineEditPort.text())
        self.update()
    def threadGelenYaz(self):
        self.labelGelen.setText("")
        self.labelGelen.setText("Bağlanılan adres=> " + self.lineEditIP.text() + ":" + self.lineEditPort.text())
        self.labelGelen.setText(self.labelGelen.text() + "\nGelen mesaj=> " + self.gelenMesaj)
        self.update()

    def threadServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.lineEditIP.text(), int(self.lineEditPort.text())))
        serverSocket.listen()
        while (True):
            (clientConnected, clientAddress) = serverSocket.accept()
            a=threading.Thread(target=self.threadGuiYazBaglandi())
            a.start()

            while(True):
                try:
                    dataFromClient = clientConnected.recv(2048)
                    self.gelenMesaj = dataFromClient.decode()
                    gelenler = self.gelenMesaj.split("#")
                    self.sonuc = 0
                    try:
                        if gelenler[1] == '+':
                            self.sonuc = int(gelenler[0]) + int(gelenler[2])
                        elif gelenler[1] == '*':
                            self.sonuc = int(gelenler[0]) * int(gelenler[2])

                        elif gelenler[1] == '-':
                            self.sonuc = int(gelenler[0]) - int(gelenler[2])
                        elif gelenler[1] == '/':
                            self.sonuc = int(gelenler[0]) / int(gelenler[2])
                    except:
                        print()
                    clientConnected.send(str(self.sonuc).encode())
                    z = threading.Thread(target=self.threadGelenYaz)
                    z.start()
                except:
                    self.labelDurum.setStyleSheet("background-color:rgb(212,0,0)")
                    self.labelDurum.setText("Server Başlamadı....")



    def baglan(self):
        if (self.lineEditIP.text() != "") and (self.lineEditPort.text()!=""):
            y= threading.Thread(target=self.threadServer)
            x = threading.Thread(target=self.threadGuiYaz)
            x.start()
            y.start()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = server()
    app.exec_()