import hashlib, sys, json, re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, \
    QListWidget, QMessageBox, QRadioButton, QComboBox, QInputDialog, QTextEdit


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.resize(300, 200)

        layout = QVBoxLayout(self)
        radio_layout = QHBoxLayout(self)

        self.label = QLabel(f"Добро пожаловать в информационную систему библиотечного фонда города", self)
        layout.addWidget(self.label)

        self.reader = QRadioButton('Читатель', self)
        self.librarian = QRadioButton('Библиотекарь', self)
        self.administrator = QRadioButton('Администратор', self)
        radio_layout.addWidget(self.reader)
        radio_layout.addWidget(self.librarian)
        radio_layout.addWidget(self.administrator)
        layout.addLayout(radio_layout)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.open_login_window)
        layout.addWidget(self.login_button)

    def open_registration_window(self):
        if self.reader.isChecked():
            self.registration_window = RegistrationReaderWindow()
            self.registration_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, 'error', 'Выберите группу пользователя')

    def open_login_window(self):
        if self.reader.isChecked():
            self.login_window = LoginReaderWindow()
            self.login_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, 'error', 'Выберите группу пользователя')


class RegistrationReaderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.label = QLabel("Форма регистрации", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Логин:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.email_label = QLabel("Email:", self)
        layout.addWidget(self.email_label)
        self.email_edit = QLineEdit(self)
        layout.addWidget(self.email_edit)

        self.password_label = QLabel("Пароль:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def register_user(self):
        username = self.username_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()

        if not (username and email and password):
            QMessageBox.warning(self, "Error", "Не все поля заполнены")
            return

        login_pattern = r'^[a-zA-Z0-9]{5,}$'
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,.<>?]).{8,}$'
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'

        if re.match(login_pattern, username):
            pass
        else:
            QMessageBox.warning(self, "Error", "неверный ввод логина")
            self.username_edit.clear()
            return

        if re.match(password_pattern, password):
            pass
        else:
            QMessageBox.warning(self, "Error", "неверный ввод пароля")
            self.password_edit.clear()
            return

        if re.match(email_pattern, email):
            pass
        else:
            QMessageBox.warning(self, "Error", "неверный ввод email")
            self.email_edit.clear()
            return


        try:
            with open("user.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                user_data = data["reader"]
                for user in user_data:
                    if user_data[user]["username"] == username:
                        QMessageBox.warning(self, "Error", "Данный юз уже используется")
                        self.username_edit.clear()
                        return
                    elif user_data[user]["email"] == email:
                        QMessageBox.warning(self, "Error", "Данный email уже используется")
                        self.username_edit.clear()
                        return
        except FileNotFoundError:
            data = {"reader": {}, "librian": {}, "administration": {}}
            user_data = data["reader"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        id = f'id{len(user_data) + 1}'
        user_data[id] = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "account_status": "ok",
            "books": [],
            "problem": {
                "text": "",
                "status": "Обращений нет"
            }
        }

        with open("user.json", "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Success", "Регистрация прошла успешно")
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()

    def back_to_welcome(self):
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()
        self.hide()


class LoginReaderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.label = QLabel("Форма входа", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Логин:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.password_label = QLabel("Пароль:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        self.back_button = QPushButton("Назад", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def login_user(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Пожалуйста, заполните необходимые поля")
            return

        with open("user.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            user_data = data["reader"]
            for user in user_data:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user_data[user]["username"] == username and (user_data[user]["password"] == hashed_password or user_data[user]["password"] == ''):
                    if user_data[user]["account_status"] != "ok":
                        QMessageBox.information(self, "Отказано", "Вы заблокированы!")
                        self.close()
                        return
                    if user_data[user]["password"] == '':
                        user_data[user]["password"] = hashed_password
                        with open("user.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)

                    QMessageBox.information(self, "Success", "Вы успешно вошли в систему")
                    app = QApplication.instance()
                    self.Catalog_reader = Catalog_reader()
                    self.Catalog_reader.show()
                    app.user_id = user
                    self.hide()
                    return

        QMessageBox.warning(self, "Error", "Invalid username or password!")
        self.password_edit.clear()

    def back_to_welcome(self):
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()


class Catalog_reader(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        self.find_book = None

        layout = QVBoxLayout(self)
        layout_find = QHBoxLayout()
        layout_criterion = QHBoxLayout()

        self.find_button = QPushButton("Поиск книги")
        self.find_button.clicked.connect(self.find)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Введите в соответствии с критерием поиска название книги, автора или жанр")

        self.lable_text = QLabel("Я ищу: ")

        self.catalog = QListWidget()
        self.catalog.itemDoubleClicked.connect(self.change_status)

        self.account = QPushButton("Личный кабинет")
        self.account.clicked.connect(self.account_win)

        self.lable_text_2 = QLabel("Критерий поиска:")
        self.criterion = QComboBox()
        self.criterion.addItems(["", "Название", "Автор", "Жанр"])
        self.criterion.currentIndexChanged.connect(self.switch_criterion)

        layout_find.addWidget(self.lable_text)
        layout_find.addWidget(self.input_text)
        layout_find.addWidget(self.find_button)
        layout_criterion.addWidget(self.lable_text_2)
        layout_criterion.addWidget(self.criterion)
        layout.addWidget(self.account)
        layout.addLayout(layout_criterion)
        layout.addLayout(layout_find)
        layout.addWidget(self.catalog)

        self.load_data()

    def switch_criterion(self):
        self.find_book = self.criterion.currentText()

    def load_data(self):
        try:
            with open('books.json', 'r', encoding='utf-8') as file:
                self.books_data = json.load(file)
                self.catalog.clear()
                for book in self.books_data:
                    if self.books_data[book]["Статус"] == "в наличии":
                        self.catalog.addItem(f'"{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}')
                if len(self.catalog) == 0:
                    self.catalog.addItem("На данный момент свободных книг нет")
        except FileNotFoundError:
            self.catalog.addItem("На данный момент книг в библиотеке нет")

    def find(self):
        if self.find_book:
            criterion = self.input_text.text()
            self.catalog.clear()
            for book in self.books_data:
                if self.books_data[book][self.find_book].lower() == criterion.lower() and self.books_data[book]["Статус"] == "в наличии":
                    self.catalog.addItem(f'"{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}')
        else:
            QMessageBox.warning(self, "Error", "Выберите критерий поиска")

    def change_status(self, item):
        selected_text = item.text()
        for book_id, book_info in self.books_data.items():
            if f'"{book_info["Название"]}" {book_info["Автор"]}, жанр: {book_info["Жанр"]}' == selected_text:
                confirm_box = QMessageBox()
                confirm_box.setIcon(QMessageBox.Icon.Question)
                confirm_box.setWindowTitle("Подтверждение изменения статуса")
                confirm_box.setText("Вы уверены, что хотите изменить статус этой книги?")
                confirm_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
                confirm_result = confirm_box.exec()
                app = QApplication.instance()
                user_id = app.user_id
                if confirm_result == QMessageBox.StandardButton.Yes:
                    if book_info["Статус"] == "в наличии":
                        book_info["Статус"] = f"бронь {user_id}"
                    else:
                        book_info["Статус"] = "в наличии"
                    with open('books.json', 'w', encoding='utf-8') as file:
                        json.dump(self.books_data, file, ensure_ascii=False, indent=4)

                    self.update_user_file(user_id, book_id)
                    self.load_data()
                break

    def update_user_file(self, user_id, book_id):
        try:
            with open("user.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open("user.json", "r+", encoding="utf-8") as file:
                data["reader"][user_id]["books"].append(book_id)
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл пользователя не найден.")


    def account_win(self):
        self.account_window = account_window()
        self.account_window.show()
        self.hide()


class account_window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Личный кабинет")
        self.resize(400, 300)

        self.username = QLabel("")
        self.username_change = QPushButton("изменить имя")
        self.username_change.clicked.connect(self.change_username)

        self.email = QLabel("")
        self.email_change = QPushButton("изменить почту")
        self.email_change.clicked.connect(self.change_email)

        self.list = QLabel("")
        self.book_list = QListWidget()
        self.book_list.itemDoubleClicked.connect(self.change_status)

        self.back = QPushButton("Вернуться назад")
        self.back.clicked.connect(self.back_to_catalog)

        self.technical_support = QPushButton("Обратиться в тех поддержку")
        self.technical_support.clicked.connect(self.support)

        layout_name = QHBoxLayout()
        layout_name.addWidget(self.username)
        layout_name.addWidget(self.username_change)
        layout_email = QHBoxLayout()
        layout_email.addWidget(self.email)
        layout_email.addWidget(self.email_change)

        layout.addLayout(layout_name)
        layout.addLayout(layout_email)
        layout.addWidget(self.list)
        layout.addWidget(self.book_list)
        layout.addWidget(self.technical_support)
        layout.addWidget(self.back)

        self.load_data()

    def load_data(self):
        try:
            with open('user.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
                app = QApplication.instance()
                user_id = app.user_id
                self.user_data = self.data["reader"][user_id]
                self.book_list.clear()
                self.username.setText(f'имя: {self.user_data["username"]}')
                self.email.setText(f'email: {self.user_data["email"]}')
                for book in self.user_data["books"]:
                    with open("books.json", 'r', encoding='utf-8') as f:
                        self.books_data = json.load(f)
                    self.book_list.addItem(f'"{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}')
        except FileNotFoundError:
            pass

    def change_username(self):
        user_name, ok = QInputDialog.getText(self, "сменить юз", "Введите новый юзернэйм:")
        if ok:
            with open("user.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                user_data = data["reader"]
                for user in user_data:
                    if user_data[user]["username"] == user_name:
                        QMessageBox.warning(self, "Error", "Данный юз уже используется")
                        return
            self.user_data["username"] = user_name
            self.username.setText(f'имя: {self.user_data["username"]}')
            with open('user.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        else:
            return

    def change_email(self):
        user_email, ok = QInputDialog.getText(self, "сменить email", "Введите новый email:")
        if ok:
            with open("user.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                user_data = data["reader"]
                for user in user_data:
                    if user_data[user]["email"] == user_email:
                        QMessageBox.warning(self, "Error", "Данный email уже используется")
                        return
            self.user_data["email"] = user_email
            self.email.setText(f'email: {self.user_data["email"]}')
            with open('user.json', 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        else:
            return

    def change_status(self, item):
        selected_text = item.text()
        for book_id, book_info in self.books_data.items():
            if f'"{book_info["Название"]}" {book_info["Автор"]}, жанр: {book_info["Жанр"]}' == selected_text:
                confirm_box = QMessageBox()
                confirm_box.setIcon(QMessageBox.Icon.Question)
                confirm_box.setWindowTitle("Подтверждение изменения статуса")
                confirm_box.setText("Вы уверены, что хотите изменить статус этой книги?")
                confirm_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
                confirm_result = confirm_box.exec()
                app = QApplication.instance()
                user_id = app.user_id
                print(1)
                if confirm_result == QMessageBox.StandardButton.Yes:
                    if book_info["Статус"] != "в наличии":
                        print(2)
                        book_info["Статус"] = f"возвращена {user_id}"
                    with open('books.json', 'w', encoding='utf-8') as file:
                        json.dump(self.books_data, file, ensure_ascii=False, indent=4)
                        print(3)

                    self.load_data()
                break

    def back_to_catalog(self):
        self.hide()
        self.CatalogWindow = Catalog_reader()
        self.CatalogWindow.show()

    def support(self):
        self.hide()
        self.support_window = support_window()
        self.support_window.show()


class support_window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Тех поддержка")
        self.resize(400, 300)

        self.label = QLabel("Укажите проблему и на ваш email-адрес будет отправлено письмо с решением проблемы")
        self.problem_text = QTextEdit()
        self.send_button = QPushButton("отправить обращение")
        self.send_button.clicked.connect(self.send)
        self.back_button = QPushButton("Вернуться назад")
        self.back_button.clicked.connect(self.back)

        layout.addWidget(self.label)
        layout.addWidget(self.problem_text)
        layout.addWidget(self.send_button)
        layout.addWidget(self.back_button)

        self.update_display()

    def send(self):
        with open('user.json', 'r', encoding='utf-8') as file:
            text = self.problem_text.toPlainText()
            self.data = json.load(file)
            app = QApplication.instance()
            user_id = app.user_id
            self.user_data = self.data["reader"][user_id]
            self.user_data["problem"] = {"text": text, "status": "отправлен"}
            with open('user.json', 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.problem_text.clear()
        self.problem_text.setPlaceholderText(f"Ваше обращение отправлено. Статус обращения: {self.user_data["problem"]["status"]}")

    def update_display(self):
        with open('user.json', 'r', encoding='utf-8') as file:
            text = self.problem_text.toPlainText()
            self.data = json.load(file)
            app = QApplication.instance()
            user_id = app.user_id
            self.user_data = self.data["reader"][user_id]
            self.problem_text.clear()
            self.problem_text.setPlaceholderText(f"Статус обращения: {self.user_data["problem"]["status"]}")

    def back(self):
        self.hide()
        self.account_window = account_window()
        self.account_window.show()


def main():
    app = QApplication(sys.argv)

    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
