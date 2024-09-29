import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QImageReader, QImage, QTransform
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import sys


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('task4.ui', self)

        self.prevButton = self.findChild(QPushButton, 'prevButton')
        self.nextButton = self.findChild(QPushButton, 'nextButton')
        self.firstButton = self.findChild(QPushButton, 'firstButton')
        self.lastButton = self.findChild(QPushButton, 'lastButton')
        self.rotateButton = self.findChild(QPushButton, 'rotateButton')
        self.deleteButton = self.findChild(QPushButton, 'deleteButton')
        self.slideshowButton = self.findChild(QPushButton, 'slideshowButton')
        self.imageLabel = self.findChild(QLabel, 'imageLabel')

        self.image_folder = None
        self.image_list = []
        self.current_index = 0
        self.load_images_from_folder()

        self.prevButton.clicked.connect(self.show_previous_image)
        self.nextButton.clicked.connect(self.show_next_image)
        self.firstButton.clicked.connect(self.show_first_image)
        self.lastButton.clicked.connect(self.show_last_image)
        self.rotateButton.clicked.connect(self.rotate_image)
        self.deleteButton.clicked.connect(self.delete_image)
        self.slideshowButton.clicked.connect(self.start_slideshow)

        self.slideshow_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)

    def load_images_from_folder(self):
        image_files = [f for f in os.listdir('image') if any(f.lower().endswith(ext.data().decode()) for ext in QImageReader.supportedImageFormats())]
        self.image_list = [os.path.join('image', f) for f in image_files]

        if self.image_list:
            self.show_image()

    def show_image(self):
        if 0 <= self.current_index < len(self.image_list):
            image_path = self.image_list[self.current_index]
            pixmap = QPixmap(image_path)
            self.imageLabel.setPixmap(pixmap)
            self.update_buttons_state()


    def update_buttons_state(self):
        self.prevButton.setEnabled(self.current_index > 0)
        self.nextButton.setEnabled(self.current_index < len(self.image_list) - 1)
        self.firstButton.setEnabled(self.current_index > 0)
        self.lastButton.setEnabled(self.current_index < len(self.image_list) - 1)

    def show_previous_image(self):
        self.current_index -= 1
        self.show_image()

    def show_next_image(self):
        self.current_index += 1
        self.show_image()

    def show_first_image(self):
        self.current_index = 0
        self.show_image()

    def show_last_image(self):
        self.current_index = len(self.image_list) - 1
        self.show_image()

    def rotate_image(self):
        if 0 <= self.current_index < len(self.image_list):
            image_path = self.image_list[self.current_index]
            image = QImage(image_path)
            rotated_image = image.transformed(QTransform().rotate(90))
            rotated_image.save(image_path)
            self.show_image()

    def delete_image(self):
        if 0 <= self.current_index < len(self.image_list):
            image_path = self.image_list[self.current_index]
            os.remove(image_path)
            del self.image_list[self.current_index]

    def start_slideshow(self):
        if self.slideshow_running:
            self.timer.stop()
        else:
            self.timer.start(500)
        self.slideshow_running = not self.slideshow_running
        self.slideshowButton.setChecked(self.slideshow_running)
        self.update_buttons_state()


if __name__ == "__main__":
    app = QApplication([])
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
