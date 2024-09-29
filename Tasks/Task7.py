import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QAction

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.is_dragging = False

    def moveButton(self, new_x, new_y):
        aligned_x = round(new_x / self.grid_size_x) * self.grid_size_x
        aligned_y = round(new_y / self.grid_size_y) * self.grid_size_y
        grid_key = (aligned_x, aligned_y)

        if grid_key not in self.parent().occupied_positions:
            if hasattr(self, 'grid_position'):
                del self.parent().occupied_positions[self.grid_position]
            self.parent().occupied_positions[grid_key] = self
            self.grid_position = grid_key
            self.move(aligned_x, aligned_y)
            self.is_dragging = True

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        move_pos = event.position().toPoint() - self.drag_start_position
        new_x, new_y = self.x() + move_pos.x(), self.y() + move_pos.y()

        aligned_x = round(new_x / self.grid_size_x) * self.grid_size_x
        aligned_y = round(new_y / self.grid_size_y) * self.grid_size_y
        grid_key = (aligned_x, aligned_y)

        if not hasattr(self, 'grid_position') or self.grid_position != grid_key:
            self.updatePosition(grid_key)

    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            event.ignore()
        else:
            super().mouseReleaseEvent(event)

    def findNearestFreePosition(self, start_x, start_y, occupied, grid_size_x, grid_size_y):
        x_direction, y_direction = 1, 0
        x_delta, y_delta = 0, 0
        max_steps = 1
        step_counter = 0
        changes = 0

        while True:
            check_x = start_x + x_delta * grid_size_x
            check_y = start_y + y_delta * grid_size_y

            if (check_x, check_y) not in occupied:
                return check_x, check_y

            x_delta += x_direction
            y_delta += y_direction
            step_counter += 1
            if step_counter == max_steps:
                step_counter = 0
                changes += 1
                x_direction, y_direction = -y_direction, x_direction

                if changes == 2:
                    changes = 0
                    max_steps += 1

    def updatePosition(self, new_position):
        grid_key = (round(new_position[0] / self.grid_size_x) * self.grid_size_x,
                    round(new_position[1] / self.grid_size_y) * self.grid_size_y)

        if grid_key in self.parent().occupied_positions:
            grid_key = self.findNearestFreePosition(*grid_key, self.parent().occupied_positions, self.grid_size_x, self.grid_size_y)

        if hasattr(self, 'grid_position') and self.grid_position in self.parent().occupied_positions:
            del self.parent().occupied_positions[self.grid_position]

        self.parent().occupied_positions[grid_key] = self
        self.grid_position = grid_key
        self.move(grid_key[0], grid_key[1])

class VirtualKeyboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_caps_lock_active = False
        self.is_shift_active = False
        self.occupied_positions = {}
        self.buttons = []

    def initUI(self):
        self.setWindowTitle("Virtual Keyboard")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.textOutput = QLineEdit()
        self.layout.addWidget(self.textOutput)
        self.central_widget.setLayout(self.layout)
        self.setGeometry(100, 100, 300, 200)
        self.grid_size_x = 100
        self.grid_size_y = 50
        self.font = QFont('Arial', 10)

        self.tab_action = QAction(self)
        self.tab_action.setShortcut(Qt.Key.Key_Tab)
        self.addAction(self.tab_action)
        self.tab_action.triggered.connect(self.tab_pressed)

    def add_key(self, position):
        key, ok = QInputDialog.getText(self, "Add Key", "Choose a letter or symbol:")
        if ok and key:
            grid_x = (position.x() // self.grid_size_x) * self.grid_size_x
            grid_y = (position.y() // self.grid_size_y) * self.grid_size_y
            grid_position = (grid_x, grid_y)

            if grid_position in self.occupied_positions:
                QMessageBox.warning(self, "Position Occupied", "This grid position is already occupied.")
                return

            button = CustomButton(key, self)
            button.setGeometry(grid_x, grid_y, self.grid_size_x, self.grid_size_y)
            button.setFont(self.font)
            button.grid_size_x = self.grid_size_x
            button.grid_size_y = self.grid_size_y
            button.drag_start_position = position
            self.occupied_positions[grid_position] = button
            button.clicked.connect(lambda: self.buttonClicked(key))
            button.show()
            self.buttons.append(button)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.add_key(event.pos())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Backspace:
            self.textOutput.backspace()
        elif event.key() == Qt.Key.Key_Enter:
            self.textOutput.insert('\n')
        elif event.key() == Qt.Key.Key_Space:
            self.textOutput.insert(' ')

    def buttonClicked(self, key):
        if key.lower() == "shift":
            self.is_shift_active = not self.is_shift_active
        elif key.lower() == "caps lock":
            self.is_caps_lock_active = not self.is_caps_lock_active
        elif key.lower() == "backspace":
            self.textOutput.backspace()
        elif key.lower() == "enter":
            self.textOutput.insert('\n')
        elif key.lower() == 'space':
            self.textOutput.insert(' ')
        else:
            final_key = key
            if self.is_shift_active or self.is_caps_lock_active:
                final_key = key.upper()
                self.is_shift_active = False
            self.textOutput.insert(final_key)

    def tab_pressed(self):
        self.focusNextPrevChild(True)

def main():
    app = QApplication(sys.argv)
    window = VirtualKeyboardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
