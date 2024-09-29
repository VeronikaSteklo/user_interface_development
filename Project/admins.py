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
        if self.administrator.isChecked():
            self.registration_window = RegistrationAdministratorWindow()
            self.registration_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, 'error', 'Выберите группу пользователя')

    def open_login_window(self):
        if self.administrator.isChecked():
            self.login_window = LoginAdministratorWindow()
            self.login_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, 'error', 'Выберите группу пользователя')


class RegistrationAdministratorWindow(QWidget):
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

        self.code_label = QLabel("Специальный код: ", self)
        layout.addWidget(self.code_label)
        self.code_edit = QLineEdit(self)
        layout.addWidget(self.code_edit)

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
        code = self.code_edit.text()

        if not (username and email and password and code):
            QMessageBox.warning(self, "Error", "Не все поля заполнены")
            return

        if code != '1234567890':
            QMessageBox.warning(self, "Error", "Введен неверный код!")
            return

        try:
            with open("user.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                user_data = data["administrator"]
                for user in user_data:
                    if user_data[user]["username"] == username:
                        QMessageBox.warning(self, "Error", "Данный юз уже используется")
                        self.username_edit.clear()
                        return
        except FileNotFoundError:
            data = {"reader": {}, "librian": {}, "administration": {}}
            user_data = data["administrator"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        id = f'id{len(user_data) + 1}'
        user_data[id] = {
            "username": username,
            "email": email,
            "password": hashed_password
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


class LoginAdministratorWindow(QWidget):
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

        with open("user.json", "r") as file:
            data = json.load(file)
            user_data = data["administrator"]
            for user in user_data:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user_data[user]["username"] == username and user_data[user]["password"] == hashed_password:
                    QMessageBox.information(self, "Success", "Вы успешно вошли в систему")
                    app = QApplication.instance()
                    app.user_id = user
                    self.Catalog_admin_Window = Catalog_admin_Window()
                    self.Catalog_admin_Window.show()
                    self.close()
                    return

        QMessageBox.warning(self, "Error", "Invalid username or password!")
        self.password_edit.clear()

    def back_to_welcome(self):
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()


class ChangeWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Изменение статуса")
        self.resize(400, 300)

        self.catalog = QListWidget()
        self.catalog.itemDoubleClicked.connect(self.change_status)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(self.back_)

        layout.addWidget(self.catalog)
        layout.addWidget(self.back)

        self.load_data()

    def load_data(self):
        try:
            with open('books.json', 'r', encoding='utf-8') as file:
                self.books_data = json.load(file)
                self.catalog.clear()
                for book in self.books_data:
                    if self.books_data[book]["Статус"] != "в наличии":
                        self.catalog.addItem(f'"{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}, статус: {self.books_data[book]["Статус"]}')
                if len(self.catalog) == 0:
                    self.catalog.addItem("На данный момент все книги свободны")
        except FileNotFoundError:
            self.catalog.addItem("На данный момент книг в библиотеке нет")

    def change_status(self, item):
        selected_text = item.text()
        for book_id, book_info in self.books_data.items():
            if f'"{book_info["Название"]}" {book_info["Автор"]}, жанр: {book_info["Жанр"]}, статус: {book_info["Статус"]}' == selected_text:
                user_id = book_info["Статус"].split()[-1]
                confirm_box = QMessageBox()
                confirm_box.setIcon(QMessageBox.Icon.Question)
                confirm_box.setWindowTitle("Подтверждение изменения статуса")
                confirm_box.setText("Вы уверены, что хотите изменить статус этой книги?")
                confirm_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                confirm_box.setDefaultButton(QMessageBox.StandardButton.No)
                confirm_result = confirm_box.exec()
                if confirm_result == QMessageBox.StandardButton.Yes:
                    status_options = ["в наличии", "отдана", "утеряна"]
                    status, ok = QInputDialog.getItem(None, "Выбор статуса", "Выберите статус книги:", status_options,
                                                      0, False)
                    if ok:
                        if status == "в наличии":
                            flag = book_info["Статус"]
                            book_info["Статус"] = "в наличии"
                            if flag != "утеряна":
                                with open("user.json", "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                    data_user = data["reader"][user_id]["books"]
                                    data_user.remove(book_id)
                                with open("user.json", "w", encoding="utf-8") as f:
                                    json.dump(data, f, ensure_ascii=False, indent=4)
                        elif status == "отдана":
                            book_info["Статус"] = f"отдана {user_id}"
                        else:
                            book_info["Статус"] = status

                        with open('books.json', 'w', encoding='utf-8') as file:
                            json.dump(self.books_data, file, ensure_ascii=False, indent=4)

                        self.load_data()
                break

    def back_(self):
        self.CatalogWindow = Catalog_admin_Window()
        self.CatalogWindow.show()
        self.hide()


class Catalog_admin_Window(QWidget):
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

        self.account = QPushButton("Личный кабинет")
        self.account.clicked.connect(self.account_win)

        self.lable_text_2 = QLabel("Критерий поиска:")
        self.criterion = QComboBox()
        self.criterion.addItems(["", "Название", "Автор", "Жанр"])
        self.criterion.currentIndexChanged.connect(self.switch_criterion)

        self.add_book = QPushButton("Добавить книгу")
        self.add_book.clicked.connect(self.book_add)

        self.change_status = QPushButton("Изменить статус книги")
        self.change_status.clicked.connect(self.change)

        self.change_book = QPushButton("Изменить данные о книге")
        self.change_book.clicked.connect(self.changing_book)

        self.change_user = QPushButton("Пользователи")
        self.change_user.clicked.connect(self.changing_user)
        lay = QHBoxLayout()
        lay.addWidget(self.add_book)
        lay.addWidget(self.change_book)
        lay.addWidget(self.change_status)
        lay.addWidget(self.change_user)

        layout_find.addWidget(self.lable_text)
        layout_find.addWidget(self.input_text)
        layout_find.addWidget(self.find_button)
        layout_criterion.addWidget(self.lable_text_2)
        layout_criterion.addWidget(self.criterion)
        layout.addWidget(self.account)
        layout.addLayout(layout_criterion)
        layout.addLayout(layout_find)
        layout.addWidget(self.catalog)
        layout.addLayout(lay)

        self.load_data()

    def switch_criterion(self):
        self.find_book = self.criterion.currentText()

    def load_data(self):
        try:
            with open('books.json', 'r', encoding='utf-8') as file:
                self.books_data = json.load(file)
                self.catalog.clear()
                for book in self.books_data:
                    self.catalog.addItem(f'{book} "{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}, статус: {self.books_data[book]["Статус"]}')
        except FileNotFoundError:
            self.catalog.addItem("На данный момент книг в библиотеке нет")

    def find(self):
        if self.find_book:
            criterion = self.input_text.text()
            self.catalog.clear()
            for book in self.books_data:
                if self.books_data[book][self.find_book].lower() == criterion.lower():
                    self.catalog.addItem(f'"{self.books_data[book]["Название"]}" {self.books_data[book]["Автор"]}, жанр: {self.books_data[book]["Жанр"]}, статус: {self.books_data[book]["Статус"]}')
        else:
            QMessageBox.warning(self, "Error", "Выберите критерий поиска")

    def changing_book(self):
        selected_item = self.catalog.currentItem()

        if selected_item:
            index = self.catalog.row(selected_item)
            id = self.catalog.item(index).text().split()[0]

            self.hide()
            self.change_book_window = ChangeBookWindow(id)
            self.change_book_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для изменения данных.")

    def changing_user(self):
        self.user_change = user_change()
        self.user_change.show()
        self.hide()

    def account_win(self):
        self.account_window = account_window()
        self.account_window.show()
        self.hide()

    def book_add(self):
        self.account_window = AddBook()
        self.account_window.show()
        self.hide()

    def change(self):
        self.ChangeWindow = ChangeWindow()
        self.ChangeWindow.show()
        self.hide()


class AddBook(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        layout = QVBoxLayout(self)

        self.name_label = QLabel("Название")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите название книги")
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        self.author_label = QLabel("Автор")
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Введите автора книги")
        author_layout = QHBoxLayout()
        author_layout.addWidget(self.author_label)
        author_layout.addWidget(self.author_edit)
        layout.addLayout(author_layout)

        self.genre_label = QLabel("Жанр")
        self.genre_edit = QLineEdit()
        self.genre_edit.setPlaceholderText("Введите жанр книги")
        genre_layout = QHBoxLayout()
        genre_layout.addWidget(self.genre_label)
        genre_layout.addWidget(self.genre_edit)
        layout.addLayout(genre_layout)

        self.addbook = QPushButton("Добавить книгу")
        self.addbook.clicked.connect(self.add_book)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(self.back_to_catalog)

        layout.addWidget(self.addbook)
        layout.addWidget(self.back)

    def add_book(self):
        name = self.name_edit.text()
        author = self.author_edit.text()
        genre = self.genre_edit.text()

        try:
            with open("books.json", "r", encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        id = f'id{len(data) + 1}'
        data[id] = {
            "Название": name,
            "Автор": author,
            "Жанр": genre,
            "Статус": "в наличии"
        }
        if not (name and author and genre):
            QMessageBox.warning(self, "Error", "Не все поля заполнены")
            return
        with open("books.json", "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Success", "Книга успешно добавлена")
        self.name_edit.clear()
        self.author_edit.clear()
        self.genre_edit.clear()

    def back_to_catalog(self):
        self.CatalogWindow = Catalog_admin_Window()
        self.CatalogWindow.show()
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

        self.back = QPushButton("Вернуться назад")
        self.back.clicked.connect(self.back_to_catalog)

        layout_name = QHBoxLayout()
        layout_name.addWidget(self.username)
        layout_name.addWidget(self.username_change)
        layout_email = QHBoxLayout()
        layout_email.addWidget(self.email)
        layout_email.addWidget(self.email_change)

        layout.addLayout(layout_name)
        layout.addLayout(layout_email)
        layout.addWidget(self.back)

        self.load_data()

    def load_data(self):
        try:
            with open('user.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
                app = QApplication.instance()
                user_id = app.user_id
                self.user_data = self.data["administrator"][user_id]
                self.username.setText(f'имя: {self.user_data["username"]}')
                self.email.setText(f'email: {self.user_data["email"]}')
        except FileNotFoundError:
            pass

    def change_username(self):
        user_name, ok = QInputDialog.getText(self, "сменить юз", "Введите новый юзернэйм:")
        if ok:
            with open("user.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                user_data = data["administrator"]
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
                user_data = data["administrator"]
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


    def back_to_catalog(self):
        self.hide()
        self.CatalogWindow = Catalog_admin_Window()
        self.CatalogWindow.show()


class ChangeBookWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setWindowTitle("Изменение данных о книге")
        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.author_edit = QLineEdit()
        self.genre_edit = QLineEdit()

        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Автор:"))
        layout.addWidget(self.author_edit)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.genre_edit)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        with open("books.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
            self.book_data = self.data[self.id]
        self.title_edit.setText(self.book_data["Название"])
        self.author_edit.setText(self.book_data["Автор"])
        self.genre_edit.setText(self.book_data["Жанр"])

    def save_changes(self):
        new_title = self.title_edit.text()
        new_author = self.author_edit.text()
        new_genre = self.genre_edit.text()

        self.book_data["Название"] = new_title
        self.book_data["Автор"] = new_author
        self.book_data["Жанр"] = new_genre

        with open("books.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Изменения сохранены", "Данные о книге успешно обновлены.")
        self.Catalog = Catalog_admin_Window()
        self.Catalog.show()
        self.hide()


class user_change(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Изменение пользователей")
        self.resize(650, 450)

        self.users = QListWidget()

        self.change_us = QPushButton("Изменить данные")
        self.change_us.clicked.connect(self.change_user)
        l = QHBoxLayout()
        self.add_read = QPushButton("Добавить читателя")
        self.add_read.clicked.connect(self.add_reader)
        self.add_lib = QPushButton("Добавить библиотекаря")
        self.add_lib.clicked.connect(self.add_librian)
        l.addWidget(self.add_read)
        l.addWidget(self.add_lib)

        lay = QHBoxLayout()
        lay.addWidget(self.change_us)
        lay.addLayout(l)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(self.back_)

        layout.addWidget(self.users)
        layout.addLayout(lay)
        layout.addWidget(self.back)

        self.load_data()

    def load_data(self):
        with open("user.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.reader_data = self.data["reader"]
        self.librian_data = self.data["librian"]
        for user in self.reader_data:
            self.users.addItem(f'reader {user} юз: {self.reader_data[user]["username"]}, email: {self.reader_data[user]["email"]}, статус аккаунта: {self.reader_data[user]["account_status"]}, обращение: {self.reader_data[user]["problem"]["status"]}')
        for user in self.librian_data:
            self.users.addItem(f'librian {user} юз: {self.librian_data[user]["username"]}, email: {self.librian_data[user]["email"]}, код: {self.librian_data[user]["code"]}')

    def change_user(self):
        selected_us = self.users.currentItem()

        if selected_us:
            index = self.users.row(selected_us)
            type_us = self.users.item(index).text().split()[0]
            id = self.users.item(index).text().split()[1]

            if type_us == 'reader':
                self.change_user_window = ChangeReaderWindow(id)
                self.change_user_window.show()
                self.hide()
            else:
                self.change_user_window = ChangeLibrianWindow(id)
                self.change_user_window.show()
                self.hide()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для изменения данных.")

    def back_(self):
        self.Catalog_admin_Window = Catalog_admin_Window()
        self.Catalog_admin_Window.show()
        self.hide()

    def add_reader(self):
        self.add_users = add_readers()
        self.add_users.show()
        self.hide()

    def add_librian(self):
        self.add_users = add_librians()
        self.add_users.show()
        self.hide()


class add_librians(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        layout = QVBoxLayout(self)

        self.us_label = QLabel("Юз")
        self.us_edit = QLineEdit()
        self.us_edit.setPlaceholderText("Введите юз библиотекаря")
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.us_label)
        name_layout.addWidget(self.us_edit)
        layout.addLayout(name_layout)

        self.email_label = QLabel("email")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Введите email библиотекаря")
        author_layout = QHBoxLayout()
        author_layout.addWidget(self.email_label)
        author_layout.addWidget(self.email_edit)
        layout.addLayout(author_layout)

        self.code_label = QLabel("Код")
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("Введите код библиотекаря")
        code_layout = QHBoxLayout()
        code_layout.addWidget(self.code_label)
        code_layout.addWidget(self.code_edit)
        layout.addLayout(code_layout)

        self.addlibrian = QPushButton("Добавить библиотекаря")
        self.addlibrian.clicked.connect(self.add_librian)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(self.back_)

        layout.addWidget(self.addlibrian)
        layout.addWidget(self.back)

    def add_librian(self):
        username = self.us_edit.text()
        email = self.email_edit.text()
        code = self.code_edit.text()
        with open("user.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        id = f'id{len(data["librian"]) + 1}'
        self.data_librian = data["librian"]
        self.data_librian[id] = {
            "username": username,
            "email": email,
            "password": "",
            "code": code
        }

        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Success", "Регистрация прошла успешно")
        self.hide()
        self.user_change = user_change()
        self.user_change.show()

    def back_(self):
        self.hide()
        self.user_change = user_change()
        self.user_change.show()


class ChangeReaderWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setWindowTitle("Изменение данных о читателе")
        layout = QVBoxLayout(self)
        self.resize(650, 450)

        self.us_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.acc_status_edit = QLineEdit()
        self.obr_edit = QLineEdit()

        self.change = QPushButton("Сохранить данные")
        self.change.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Юз:"))
        layout.addWidget(self.us_edit)
        layout.addWidget(QLabel("email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Статус аккаунта"))
        layout.addWidget(self.acc_status_edit)
        layout.addWidget(QLabel("Статус обращения:"))
        layout.addWidget(self.obr_edit)
        layout.addWidget(self.change)

        self.load_data()

    def load_data(self):
        with open("user.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.user = self.data["reader"][self.id]
        self.us_edit.setText(self.user["username"])
        self.email_edit.setText(self.user["email"])
        self.acc_status_edit.setText(self.user["account_status"])
        self.obr_edit.setText(self.user["problem"]["status"])

    def save_changes(self):
        new_us = self.us_edit.text()
        new_email = self.email_edit.text()
        new_acc = self.acc_status_edit.text()
        new_obr = self.obr_edit.text()

        self.user["username"] = new_us
        self.user["email"] = new_email
        self.user["account_status"] = new_acc
        self.user["problem"]["status"] = new_obr

        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Изменения сохранены", "Данные о читателе успешно обновлены.")
        self.user_change = user_change()
        self.user_change.show()
        self.hide()


class ChangeLibrianWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setWindowTitle("Изменение данных о библиотекаре")
        layout = QVBoxLayout(self)
        self.resize(650, 450)

        self.us_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.code_edit = QLineEdit()

        self.change = QPushButton("Сохранить данные")
        self.change.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Юз:"))
        layout.addWidget(self.us_edit)
        layout.addWidget(QLabel("email:"))
        layout.addWidget(self.email_edit)
        layout.addWidget(QLabel("Код"))
        layout.addWidget(self.code_edit)
        layout.addWidget(self.change)

        self.load_data()

    def load_data(self):
        with open("user.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)
        self.user = self.data["librian"][self.id]
        self.us_edit.setText(self.user["username"])
        self.email_edit.setText(self.user["email"])
        self.code_edit.setText(self.user["code"])

    def save_changes(self):
        new_us = self.us_edit.text()
        new_email = self.email_edit.text()
        new_code = self.code_edit.text()

        self.user["username"] = new_us
        self.user["email"] = new_email
        self.user["code"] = new_code

        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Изменения сохранены", "Данные о библиотекаре успешно обновлены.")
        self.user_change = user_change()
        self.user_change.show()
        self.hide()


class add_readers(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        layout = QVBoxLayout(self)

        self.us_label = QLabel("Юз")
        self.us_edit = QLineEdit()
        self.us_edit.setPlaceholderText("Введите юз читателя")
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.us_label)
        name_layout.addWidget(self.us_edit)
        layout.addLayout(name_layout)

        self.email_label = QLabel("email")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Введите email читателя")
        author_layout = QHBoxLayout()
        author_layout.addWidget(self.email_label)
        author_layout.addWidget(self.email_edit)
        layout.addLayout(author_layout)

        self.addreader = QPushButton("Добавить читателя")
        self.addreader.clicked.connect(self.add_reader)

        self.back = QPushButton("Назад")
        self.back.clicked.connect(self.back_)

        layout.addWidget(self.addreader)
        layout.addWidget(self.back)

    def add_reader(self):
        username = self.us_edit.text()
        email = self.email_edit.text()
        with open("user.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        id = f'id{len(data["reader"]) + 1}'
        self.data_reader = data["reader"]
        self.data_reader[id] = {
            "username": username,
            "email": email,
            "password": '',
            "account_status": "ok",
            "books": [],
            "problem": {
                "text": "",
                "status": "Обращений нет"
            }
        }

        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Success", "Регистрация прошла успешно")
        self.hide()
        self.user_change = user_change()
        self.user_change.show()

    def back_(self):
        self.hide()
        self.user_change = user_change()
        self.user_change.show()


def main():
    app = QApplication(sys.argv)

    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
