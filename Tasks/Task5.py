import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QGroupBox, QCheckBox, QRadioButton, QPushButton, QLabel
from PyQt6 import uic


class LunchOrderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task5.ui', self)
        self.init_ui()


    def init_ui(self):
        self.submit_button = self.findChild(QWidget, 'oformit')
        self.submit_button.clicked.connect(self.submit_order)
        self.submit_button.setEnabled(False)

        self.result_label = self.findChild(QLabel, 'label')

        self.desert = self.findChild(QGroupBox, 'desert')
        self.pirozh = self.findChild(QRadioButton, 'pirozh')
        self.pirozh.toggled.connect(self.update_submit_button)
        self.tiramisy = self.findChild(QRadioButton, 'tiramisy')
        self.tiramisy.toggled.connect(self.update_submit_button)

        self.drink = self.findChild(QGroupBox, 'drink')
        self.coffee = self.findChild(QRadioButton, 'coffee')
        self.coffee.toggled.connect(self.update_submit_button)
        self.tea = self.findChild(QRadioButton, 'tea')
        self.tea.toggled.connect(self.update_submit_button)

        self.first = self.findChild(QGroupBox, 'first')
        self.borstch = self.findChild(QRadioButton, 'borstch')
        self.borstch.toggled.connect(self.update_submit_button)
        self.solyanka = self.findChild(QRadioButton, 'solyanka')
        self.solyanka.toggled.connect(self.update_submit_button)

        self.salad = self.findChild(QGroupBox, 'salad')
        self.grecheskiy = self.findChild(QRadioButton, 'grecheskiy')
        self.grecheskiy.toggled.connect(self.update_submit_button)
        self.tsezar = self.findChild(QRadioButton, 'tsezar')
        self.tsezar.toggled.connect(self.update_submit_button)

        self.second = self.findChild(QGroupBox, 'second')
        self.kotleta = self.findChild(QRadioButton, 'kotleta')
        self.kotleta.toggled.connect(self.update_submit_button)
        self.pasta = self.findChild(QRadioButton, 'pasta')
        self.pasta.toggled.connect(self.update_submit_button)

        self.menu = {self.desert: [self.pirozh, self.tiramisy],
                     self.drink: [self.coffee, self.tea],
                     self.first: [self.borstch, self.solyanka],
                     self.salad: [self.grecheskiy, self.tsezar],
                     self.second: [self.kotleta, self.pasta]}

    def submit_order(self):
        order = []

        for i in self.menu.keys():
            for j in self.menu[i]:
                if j.isChecked():
                    order.append(j.text())

        if len(order) >= 2:
            self.result_label.setText("Заказ успешно оформлен: " + ", ".join(order))
        else:
            self.result_label.setText("Выберите не менее двух позиций для заказа")

    def update_submit_button(self):
        selected_count = 0

        for i in self.menu.keys():
            for j in self.menu[i]:
                if j.isChecked():
                    selected_count += 1

        self.submit_button.setEnabled(selected_count >= 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LunchOrderApp()
    window.show()
    sys.exit(app.exec())
