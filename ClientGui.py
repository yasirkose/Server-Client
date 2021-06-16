from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QRegExpValidator,QIntValidator
from PyQt5.QtCore import QRegExp
import socket
import time
import threading
class client(QtWidgets.QMainWindow):
    def __init__(self):
        super(client, self).__init__()
        uic.loadUi('clientForm.ui', self)
        self.baslangic()
        self.buttonBaglan.clicked.connect(self.baglan)
        self.button_sendData.clicked.connect(self.islemGonder)
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
        self.lineEditIlkSayi.setValidator(QIntValidator())
        self.lineEditIkinciSayi.setValidator(QIntValidator())
        self.lineEditPort.setText("9090")

    def baglan(self):
        if (self.lineEditIP.text() != "") and (self.lineEditPort.text()!=""):
            self.kontrol=0
            try:
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientSocket.connect((self.lineEditIP.text(), int(self.lineEditPort.text())))
                self.labelDurum.setStyleSheet("background-color:rgb(143,234,118)")
                self.labelDurum.setText("Client Bağlandı...")
                self.lineEditIlkSayi.setEnabled(1)
                self.lineEditIkinciSayi.setEnabled(1)
                self.comboBox.setEnabled(1)
            except:
                self.labelDurum.setStyleSheet("background-color:rgb(234,126,118)")
                self.labelDurum.setText("Bağlantı Başarısız")
                self.lineEditIlkSayi.setDisabled(1)
                self.lineEditIkinciSayi.setDisabled(1)
                self.comboBox.setDisabled(1)
                self.kontrol=1
            if self.kontrol==0:
                self.button_sendData.setEnabled(1)
                self.labelGelen.setText("Bağlanılan adres=> "+self.lineEditIP.text()+":"+self.lineEditPort.text())
            elif self.kontrol==1:
                self.labelGelen.setText("")
                self.button_sendData.setEnabled(False)

    def islemGonder(self):
        self.labelGelen.setText("")
        self.labelGelen.setText("Bağlanılan adres=> " + self.lineEditIP.text() + ":" + self.lineEditPort.text())
        data = self.lineEditIlkSayi.text() + "#" + self.comboBox.currentText() + "#" + self.lineEditIkinciSayi.text()
        self.labelGelen.setText(self.labelGelen.text() + "\nGiden mesaj=> " + data)
        self.baslangicTime = time.time_ns()
        self.clientSocket.send(data.encode())
        dataFromServer = self.clientSocket.recv(2048)
        gelenSonuc=dataFromServer.decode()
        self.labelGelen.setText(self.labelGelen.text() + "\nGelen mesaj=> " + gelenSonuc)
        self.bitisTime = time.time_ns()
        self.labelGelen.setText(self.labelGelen.text() + "\nRTT(miliseconds)=> " + str(self.bitisTime - self.baslangicTime))
        dosya = open("dosya.txt", "a+")
        dosya.write("Sonuc="+str(gelenSonuc)+"\n")
        dosya.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = client()
    app.exec_()