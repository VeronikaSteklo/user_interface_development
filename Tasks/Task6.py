import sys
import json
import hashlib
import os
import re
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.label = QLabel("Welcome to Our App!", self)
        layout.addWidget(self.label)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.open_login_window)
        layout.addWidget(self.login_button)

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.hide()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.label = QLabel("Registration Form", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Username:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.email_label = QLabel("Email:", self)
        layout.addWidget(self.email_label)
        self.email_edit = QLineEdit(self)
        layout.addWidget(self.email_edit)

        self.phone_label = QLabel("Phone:", self)
        layout.addWidget(self.phone_label)
        self.phone_edit = QLineEdit(self)
        layout.addWidget(self.phone_edit)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.confirm_password_label = QLabel("Confirm Password:", self)
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_edit)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def register_user(self):
        username = self.username_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not (username and email and phone and password and confirm_password):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Error", "Invalid email address!")
            return



        with open("users.json", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["username"] == username:
                    QMessageBox.warning(self, "Error", "Username already exists!")
                    return

        # Хэширование пароля
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            "username": username,
            "email": email,
            "phone": phone,
            "password": hashed_password
        }

        with open("users.json", "a") as file:
            json.dump(user_data, file)
            file.write('\n')

        QMessageBox.information(self, "Success", "Registration successful!")
        self.close()

    def back_to_welcome(self):
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()
        self.hide()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.label = QLabel("Login Form", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Username:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def login_user(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return

        with open("users.json", "r") as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["username"] == username:
                    # Хэширование введенного пароля и сравнение с хэшем в файле
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if user_data["password"] == hashed_password:
                        QMessageBox.information(self, "Success", "Login successful!")
                        self.close()
                        return

        QMessageBox.warning(self, "Error", "Invalid username or password!")
        self.password_edit.clear()

    def back_to_welcome(self):
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()



# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Main Window")
#         self.resize(300, 200)
#
#         self.label = QLabel("Welcome to the Main Window!", self)
#         self.label.setGeometry(50, 50, 200, 30)


def main():
    app = QApplication(sys.argv)

    # Проверка наличия файла с пользователями
    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            pass

    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
