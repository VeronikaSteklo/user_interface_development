import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QDialog, QTextEdit)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
       
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 305, 220)
        self.setWindowTitle('За или против')
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):

        with open('rasrabotka/prinyatie.txt', 'r') as file:
            file = file.readlines()
            self.za = int(file[0])
            self.protiv = int(file[1])

        self.button_za = QPushButton('Количество \"За\": ' + str(self.za) + '   ', self)
        self.button_za.move(55, 45)
        self.button_za.clicked.connect(self.zaclick)

        self.button_prot = QPushButton('Количество \"Против\": ' + str(self.protiv) + '   ', self)
        self.button_prot.move(55, 85)
        self.button_prot.clicked.connect(self.protivclick)

        self.button_sbros = QPushButton('Сброс', self)
        self.button_sbros.move(55, 125)
        self.button_sbros.clicked.connect(self.sbros)

    def zaclick(self):
        self.za += 1
        self.button_za.setText('Количество \"За\": ' + str(self.za))
        with open('rasrabotka/prinyatie.txt', 'w') as file:
            file.write(str(self.za) + '\n')
            file.write(str(self.protiv))

    def protivclick(self):
        self.protiv += 1
        self.button_prot.setText('Количество \"Против\": ' + str(self.protiv))
        with open('rasrabotka/prinyatie.txt', 'w') as file:
            file.write(str(self.za) + '\n')
            file.write(str(self.protiv))

    def sbros(self):
        self.za = 0
        self.protiv = 0
        self.button_za.setText('Количество \"За\": ' + str(self.za))
        self.button_prot.setText('Количество \"Против\": ' + str(self.protiv))
        with open('rasrabotka/prinyatie.txt', 'w') as file:
            file.write(str(self.za) + '\n')
            file.write(str(self.protiv))
           

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
