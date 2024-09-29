import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, \
    QListWidget, QTabWidget, QLCDNumber, QCheckBox
from PyQt6.QtCore import Qt


class DecisionMaker(QWidget):
    def __init__(self):
        super().__init__()

        self.decision_data = {}
        self.current_decision_key = None
        self.decision_accepted = {}
        self.decision_checkboxes = {}

        self.tab_widget = QTabWidget()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Decision Maker")

        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        self.add_tab_button = QPushButton("Добавить вопрос")
        self.add_tab_button.clicked.connect(self.add_tab)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Введите новый вопрос")

        self.for_count_lcd = QLCDNumber()
        self.against_count_lcd = QLCDNumber()
        self.update_lcd_counts()

        self.arg_input_button = QLineEdit()
        self.arg_input_button.setPlaceholderText("Введите аргумент")

        self.for_button = QPushButton("Добавить аргумент За")
        self.for_button.clicked.connect(self.add_argument_for)

        self.against_button = QPushButton("Добавить аргумент Против")
        self.against_button.clicked.connect(self.add_argument_against)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_all)


        self.for_up_button = QPushButton("▲")
        self.for_up_button.clicked.connect(self.move_argument_for_up)
        self.for_down_button = QPushButton("▼")
        self.for_down_button.clicked.connect(self.move_argument_for_down)

        self.against_up_button = QPushButton("▲")
        self.against_up_button.clicked.connect(self.move_argument_against_up)
        self.against_down_button = QPushButton("▼")
        self.against_down_button.clicked.connect(self.move_argument_against_down)

        self.arguments_for_list = QListWidget()
        self.arguments_for_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.arguments_against_list = QListWidget()
        self.arguments_against_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.update_display()

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.tab_widget)
        v_layout.addWidget(self.add_tab_button)
        v_layout.addWidget(self.question_input)

        des_layout = QHBoxLayout()
        des_layout.addWidget(QLabel("Количество за: "))
        des_layout.addWidget(self.for_up_button)
        des_layout.addWidget(self.for_down_button)
        des_layout.addWidget(QLabel("Количество против: "))
        des_layout.addWidget(self.against_up_button)
        des_layout.addWidget(self.against_down_button)
        v_layout.addLayout(des_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.arguments_for_list)
        h_layout.addWidget(self.arguments_against_list)
        v_layout.addLayout(h_layout)

        hx_layout = QHBoxLayout()
        hx_layout.addWidget(self.for_count_lcd)
        hx_layout.addWidget(self.against_count_lcd)
        v_layout.addLayout(hx_layout)

        v_layout.addWidget(self.arg_input_button)
        v_layout.addWidget(self.for_button)
        v_layout.addWidget(self.against_button)
        v_layout.addWidget(self.reset_button)

        self.setLayout(v_layout)

        self.populate_tabs()
        self.tab_widget.currentChanged.connect(self.switch_question)

    def populate_tabs(self):
        for question in self.decision_data.keys():
            self.add_tab(question)

    def add_tab(self, question=None):
        try:
            if not question:
                question = self.question_input.text().strip()
                if not question:
                    question = f"Вопрос {self.tab_widget.count() + 1}"
            self.decision_data[question] = {"arguments_for": [], "arguments_against": []}
            self.decision_accepted[question] = False
            tab_index = self.tab_widget.addTab(QWidget(), question)
            tab_layout = QVBoxLayout()
            decision_accepted_checkbox = QCheckBox("Решение принято")
            decision_accepted_checkbox.setChecked(self.decision_accepted[question])
            decision_accepted_checkbox.stateChanged.connect(lambda state, q=question: self.toggle_decision_accepted(q, state))
            tab_layout.addWidget(decision_accepted_checkbox)
            self.decision_checkboxes[question] = decision_accepted_checkbox
            self.tab_widget.widget(tab_index).setLayout(tab_layout)
            self.tab_widget.setCurrentIndex(tab_index)
            self.tab_widget.setTabText(tab_index, question)
            self.tab_widget.currentChanged.connect(self.switch_question)
            self.current_decision_key = question
            self.save_data()
            self.update_display()
            self.question_input.clear()
        except Exception as e:
            print("An exception occurred:", e)

    def remove_tab(self, index):
        try:
            tab_text = self.tab_widget.tabText(index)
            del self.decision_data[tab_text]
            del self.decision_accepted[tab_text]
            del self.decision_checkboxes[tab_text]
            self.tab_widget.removeTab(index)
            self.current_decision_key = None
            self.save_data()
            self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def toggle_decision_accepted(self, question, state):
        try:
            self.decision_accepted[question] = state == 2
            self.save_data()
            self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def toggle_buttons_enabled(self):
        try:
            enabled = self.decision_accepted[self.current_decision_key]
            self.for_button.setDisabled(enabled)
            self.against_button.setDisabled(enabled)
            self.for_button.setDisabled(enabled)
            self.against_button.setDisabled(enabled)
            self.for_up_button.setDisabled(enabled)
            self.for_down_button.setDisabled(enabled)
            self.against_up_button.setDisabled(enabled)
            self.against_down_button.setDisabled(enabled)
            self.arg_input_button.setDisabled(enabled)
        except Exception as e:
            print("An exception occurred:", e)

    def load_data(self):
        try:
            with open("mini_project4.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.decision_data = data["decision_data"]
                self.decision_accepted = data["decision_accepted"]
                for question, arguments in self.decision_data.items():
                    tab = QWidget()
                    tab.setObjectName(question)
                    self.tab_widget.addTab(tab, question)
                    decision_accepted_checkbox = QCheckBox("Решение принято")
                    decision_accepted_checkbox.setChecked(self.decision_accepted[question])
                    decision_accepted_checkbox.stateChanged.connect(lambda state, q=question: self.toggle_decision_accepted(q, state))
                    self.decision_checkboxes[question] = decision_accepted_checkbox
                    tab_layout = QVBoxLayout()
                    tab_layout.addWidget(decision_accepted_checkbox)
                    tab.setLayout(tab_layout)
                self.switch_question(self.tab_widget.currentIndex())
        except Exception as e:
            print("An exception occurred:", e)
            self.decision_data = {}
            self.decision_accepted = {}

    def save_data(self):
        try:
            with open("mini_project4.json", "w", encoding='utf-8') as f:
                json.dump({"decision_data": self.decision_data, "decision_accepted": self.decision_accepted}, f, ensure_ascii=False, indent=4, sort_keys=True)
        except Exception as e:
            print("An exception occurred:", e)

    def add_argument_for(self):
        try:
            if self.current_decision_key and not self.decision_accepted[self.current_decision_key]:
                argument = self.arg_input_button.text()
                self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
                self.update_display()
                self.save_data()
                self.arg_input_button.clear()
                # Устанавливаем доступность кнопок в зависимости от состояния флажка
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def add_argument_against(self):
        try:
            if self.current_decision_key and not self.decision_accepted[self.current_decision_key]:
                argument = self.arg_input_button.text()
                self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
                self.update_display()
                self.save_data()
                self.arg_input_button.clear()
                # Устанавливаем доступность кнопок в зависимости от состояния флажка
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def move_argument_for_up(self):
        self.move_argument_up(self.arguments_for_list)

    def move_argument_for_down(self):
        self.move_argument_down(self.arguments_for_list)

    def move_argument_against_up(self):
        self.move_argument_up(self.arguments_against_list)

    def move_argument_against_down(self):
        self.move_argument_down(self.arguments_against_list)

    def move_argument_up(self, list_widget):
        current_row = list_widget.currentRow()
        if current_row > 0:
            current_item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row - 1, current_item)
            list_widget.setCurrentRow(current_row - 1)
            self.swap_arguments(list_widget, current_row, current_row - 1)

    def move_argument_down(self, list_widget):
        current_row = list_widget.currentRow()
        if current_row < list_widget.count() - 1 and current_row != -1:
            current_item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row + 1, current_item)
            list_widget.setCurrentRow(current_row + 1)
            self.swap_arguments(list_widget, current_row, current_row + 1)

    def swap_arguments(self, list_widget, index1, index2):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            if list_widget is self.arguments_for_list:
                current_data["arguments_for"][index1], current_data["arguments_for"][index2] = \
                    current_data["arguments_for"][index2], current_data["arguments_for"][index1]
            elif list_widget is self.arguments_against_list:
                current_data["arguments_against"][index1], current_data["arguments_against"][index2] = \
                    current_data["arguments_against"][index2], current_data["arguments_against"][index1]
            self.save_data()

    def update_display(self):
        try:
            if self.current_decision_key:
                current_data = self.decision_data[self.current_decision_key]
                self.arguments_for_list.clear()
                self.arguments_against_list.clear()
                for argument in current_data["arguments_for"]:
                    self.arguments_for_list.addItem(argument)
                for argument in current_data["arguments_against"]:
                    self.arguments_against_list.addItem(argument)
                self.update_lcd_counts()
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def update_lcd_counts(self):
        try:
            if self.current_decision_key:
                current_data = self.decision_data[self.current_decision_key]
                self.for_count_lcd.display(len(current_data["arguments_for"]))
                self.against_count_lcd.display(len(current_data["arguments_against"]))
        except Exception as e:
            print("An exception occurred:", e)

    def switch_question(self, index):
        try:
            self.current_decision_key = self.tab_widget.tabText(index)
            self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def reset_all(self):
        try:
            if self.current_decision_key:
                del self.decision_data[self.current_decision_key]
                del self.decision_accepted[self.current_decision_key]
                del self.decision_checkboxes[self.current_decision_key]
                self.tab_widget.removeTab(self.tab_widget.currentIndex())
                self.current_decision_key = None
                self.update_display()
                self.save_data()
        except Exception as e:
            print("An exception occurred:", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
