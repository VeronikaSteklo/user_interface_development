import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QComboBox, QLCDNumber
from PyQt6 import uic

class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mini_project3.ui', self)

        self.decision_data = {}
        self.current_question = ""
        self.current_decision_key = None

        self.load_data()

        self.init_ui()

    def init_ui(self):
        self.question_label = self.findChild(QLabel, 'question_label')
        self.question_combo = self.findChild(QComboBox, 'question_combo')
        self.question_combo.addItems(self.decision_data.keys())
        self.question_combo.currentIndexChanged.connect(self.switch_question)

        self.question_input = self.findChild(QLineEdit, 'question_input')
        self.set_question_button = self.findChild(QPushButton, 'set_question_button')
        self.set_question_button.clicked.connect(self.set_question)

        self.arg_input_button = self.findChild(QLineEdit, 'arg_input_button')

        self.for_count_lcd = self.findChild(QLCDNumber, 'for_count_lcd')
        self.against_count_lcd = self.findChild(QLCDNumber, 'against_count_lcd')
        self.update_lcd_counts()

        self.for_button = self.findChild(QPushButton, 'for_button')
        self.for_button.clicked.connect(self.add_argument_for)

        self.against_button = self.findChild(QPushButton, 'against_button')
        self.against_button.clicked.connect(self.add_argument_against)

        self.for_up_button = self.findChild(QPushButton, 'for_up_button')
        self.for_up_button.clicked.connect(self.move_argument_up_for)

        self.for_down_button = self.findChild(QPushButton, 'for_down_button')
        self.for_down_button.clicked.connect(self.move_argument_down_for)

        self.against_up_button = self.findChild(QPushButton, 'against_up_button')
        self.against_up_button.clicked.connect(self.move_argument_up_against)

        self.against_down_button = self.findChild(QPushButton, 'against_down_button')
        self.against_down_button.clicked.connect(self.move_argument_down_against)

        self.reset_button = self.findChild(QPushButton, 'reset_button')
        self.reset_button.clicked.connect(self.reset_all)

        self.arguments_for_list = self.findChild(QListWidget, 'arguments_for_list')
        self.arguments_for_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.arguments_against_list = self.findChild(QListWidget, 'arguments_against_list')
        self.arguments_against_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.update_display()


    def switch_question(self):
        self.current_decision_key = self.question_combo.currentText()
        self.update_display()

    def set_question(self):
        new_question = self.question_input.text()
        if new_question and new_question not in self.decision_data:
            self.decision_data[new_question] = {"arguments_for": [], "arguments_against": []}
            self.question_combo.addItem(new_question)
            self.question_combo.setCurrentText(new_question)
            self.current_decision_key = new_question
            self.save_data()
        self.question_input.clear()

    def add_argument_for(self):
        if self.current_decision_key:
            argument = self.arg_input_button.text()
            self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
            self.save_data()
            self.update_display()
        self.arg_input_button.clear()

    def add_argument_against(self):
        if self.current_decision_key:
            argument = self.arg_input_button.text()
            self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
            self.save_data()
            self.update_display()
        self.arg_input_button.clear()

    def move_argument_up_for(self):
        self.move_argument_up(self.arguments_for_list)

    def move_argument_down_for(self):
        self.move_argument_down(self.arguments_for_list)

    def move_argument_up_against(self):
        self.move_argument_up(self.arguments_against_list)

    def move_argument_down_against(self):
        self.move_argument_down(self.arguments_against_list)

    def move_argument_up(self, list_widget):
        row = list_widget.currentRow()
        if row > 0:
            item = list_widget.takeItem(row)
            list_widget.insertItem(row - 1, item)
            list_widget.setCurrentRow(row - 1)

    def move_argument_down(self, list_widget):
        row = list_widget.currentRow()
        if row < list_widget.count() - 1 and row != -1:
            item = list_widget.takeItem(row)
            list_widget.insertItem(row + 1, item)
            list_widget.setCurrentRow(row + 1)

    def update_display(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            self.arguments_for_list.clear()
            self.arguments_against_list.clear()
            for argument in current_data["arguments_for"]:
                self.arguments_for_list.addItem(argument)
            for argument in current_data["arguments_against"]:
                self.arguments_against_list.addItem(argument)
            self.update_lcd_counts()

    def update_lcd_counts(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            self.for_count_lcd.display(len(current_data["arguments_for"]))
            self.against_count_lcd.display(len(current_data["arguments_against"]))

    def reset_all(self):
        if self.current_decision_key:
            del self.decision_data[self.current_decision_key]
            self.question_combo.removeItem(self.question_combo.currentIndex())
            self.current_decision_key = None
            self.update_display()
            self.save_data()

    def load_data(self):
        try:
            with open("mini_project3.json", "r") as file:
                self.decision_data = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("mini_project3.json", "w") as file:
            json.dump(self.decision_data, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
