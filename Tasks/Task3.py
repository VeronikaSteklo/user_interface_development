import sys
import shelve
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QCalendarWidget, QTimeEdit, QListWidget)
from PyQt6.QtCore import QDateTime
from PyQt6 import uic


class DailyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task3.ui', self)

        self.load_data()

        self.event_label = self.findChild(QLabel, 'name')
        self.event_edit = self.findChild(QLineEdit, 'name_input')
        self.date_label = self.findChild(QLabel, 'date')
        self.calendar_widget = self.findChild(QCalendarWidget, 'date_input')
        self.time_label = self.findChild(QLabel, 'time')
        self.time_edit = self.findChild(QTimeEdit, 'time_input')
        self.remove_button = self.findChild(QPushButton, 'delete_event')
        self.add_button = self.findChild(QPushButton, 'add')
        self.events_list = self.findChild(QListWidget, 'event_list')

        self.add_button.clicked.connect(self.add_event)
        self.remove_button.clicked.connect(self.remove_event)

        self.load_events()

    def add_event(self):
        event_name = self.event_edit.text()
        event_date = self.calendar_widget.selectedDate()
        event_time = self.time_edit.time()

        event_datetime = QDateTime(event_date, event_time)

        self.events_list.addItem(f'{event_datetime.toString("dd.MM.yyyy HH:mm")} - {event_name}')
        self.events.append({'datetime': event_datetime, 'name': event_name})
        self.events.sort(key=lambda x: x['datetime'])

        self.save_data()

    def remove_event(self):
        selected_item = self.events_list.currentItem()

        if selected_item:
            index = self.events_list.row(selected_item)
            del self.events[index]
            self.events_list.takeItem(index)

            self.save_data()

    def save_data(self):
        with shelve.open('daily_planner_data') as shelf:
            shelf['events'] = self.events

    def load_data(self):
        with shelve.open('daily_planner_data') as shelf:
            self.events = shelf.get('events', [])

    def load_events(self):
        self.events.sort(key=lambda x: x['datetime'])
        for event in self.events:
            self.events_list.addItem(f'{event["datetime"].toString("dd.MM.yyyy HH:mm")} - {event["name"]}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DailyPlanner()
    window.show()
    sys.exit(app.exec())
