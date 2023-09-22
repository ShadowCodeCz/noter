import json
import os
import ctypes
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import *

import qdarktheme
import datetime
import alphabetic_timestamp as ats

from . import app_core
from . import gui
from . import notificator
from . import profile


class Application:
    def __init__(self):
        self.app = None
        self.window = None
        self.profile = None
        self.profiles = profile.all

        self.clipboard_flag = False
        self.core = app_core.AppCore()
        self.core.set_standard_logger()
        self.core.create_records_directory()

        self.notifier = notificator.SingletonNotificationProvider()
        self.notifier.subscribe(notificator.Messages.load, self.load)
        self.notifier.subscribe(notificator.Messages.save, self.save)
        self.notifier.subscribe(notificator.Messages.copy_to_clip_board, self.copy_to_clipboard)
        self.notifier.subscribe(notificator.Messages.load_profile, self.load_new_profile)

    def run(self, profile):
        # TODO: Dark theme for window frame
        # TODO: Images
        # TODO: Profile widget
        # TODO: CTRL + V insert image
        self.profile = profile

        self.app = QApplication([])
        qdarktheme.setup_theme(corner_shape="sharp")

        my_app_id = 'shadowcode.noter.0.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        self.window = gui.MainWindow()

        self.window.setWindowTitle("Noter")
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resource", 'logo.png')

        self.window.setWindowIcon(QIcon(path))
        self.app.setWindowIcon(QIcon(path))
        self.window.show()
        self.load_profile()
        self.app.exec()

    def load_profile(self):
        data = self.profiles[self.profile]
        self.window.load(data)

    def load_new_profile(self, notification):
        self.profile = self.window.app_widget.profile.box.currentText()
        self.load_profile()

    def profile_data(self):
        try:
            return self.profiles[self.profile]
        except Exception as e:
            return {
                "title": "",
                "tags": "",
                "predefined.tags": [""],
                "helpers": ["<b></b>", "<i></i>"],
                "text": ""
            }

    def save(self, notification):
        self.window.statusBar.showMessage("save")

        now = datetime.datetime.now()
        directory_title = self.window.app_widget.title.input.text().replace(" ", "-")
        directory_template = f"%Y.%m.%d_%H-%M-%S_{directory_title}"

        aw = self.window.app_widget

        data = {
                "version": 1,
                "id": ats.base62.from_datetime(now, time_unit=ats.TimeUnit.seconds),
                "time": str(now),
                "title": aw.title.input.text(),
                "tags": aw.tags.input.text(), # TODO: Consider list
                "predefined.tags": aw.tags.all_tags_items(),
                "helpers": aw.helper.all_tags_items(),
                "text": aw.text.input.toPlainText() # TODO: Consider list
        }

        directory = os.path.join(self.core.records_directory(), now.strftime(directory_template))
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "noter.json")
        with open(path, "w+") as output_file:
            json.dump(data, output_file, indent=4)

        self.window.statusBar.showMessage(f"Saved {path}")

    def load(self, notification):
        file_path, _ = QFileDialog.getOpenFileName(self.window, 'Open file', self.core.records_directory(), 'Noter (noter.json)')

        with open(file_path, "r") as input_file:
            data = json.load(input_file)
            self.window.load(data)
        self.window.statusBar.showMessage(f"Loaded {file_path}")

    def copy_to_clipboard(self, notification):
        # Skip first call
        if self.clipboard_flag:
            clip_board = QApplication.clipboard()
            clip_board.setText(self.window.app_widget.helper.box.currentText())
        self.clipboard_flag = True


def run(arguments):
    _run(arguments.profile)


def _run(profile):
    app = Application()
    app.run(profile)