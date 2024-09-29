import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 250, 180)
        self.setWindowTitle("проверка")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        self.times_pressed = 0
        self.button = QPushButton(str(self.times_pressed), self)
        self.button.move(85, 45)
        self.button.clicked.connect(self.buttonClicked)

        self.but = QPushButton('Нажми меня', self)
        self.but.move(85, 10)
        self.but.clicked.connect(self.move_btn)

        self.but_da = QPushButton('Да', self)
        self.but_da.move(30, 80)
        self.but_da.clicked.connect(self.da)

        self.but_net = QPushButton('Нет', self)
        self.but_net.move(45 + self.but_da.width(), 80)
        self.but_net.clicked.connect(self.net)

        self.lable = QLabel('       ', self)
        self.lable.move(self.but_da.width() + 15, 83)

        self.btn = QPushButton('Выполните условия и откроете пасхалку', self)
        self.btn.move(10, 115)
        self.btn.clicked.connect(self.pash)

        self.pask = QLabel('                     ', self)
        self.pask.move(10, 150)


    def buttonClicked(self):
        self.times_pressed += 1
        self.button.setText(str(self.times_pressed))

    def move_btn(self):
        self.but.move(self.but.x() + 5, 20)
        if self.but.x() > 240:
            self.but.move(-70, 20)
   
    def da(self):
        self.lable.setText('Да')
    def net(self):
        self.lable.setText('Нет')

    def pash(self):
        danet = self.lable.text()
        if danet == 'Нет' and self.times_pressed == 10:
            self.pask.setText('Пасхалка')
        else:
            self.close()
            print('Условия не были выполнены')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
