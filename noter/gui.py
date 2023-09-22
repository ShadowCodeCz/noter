from PyQt6.QtGui import QDoubleValidator, QFont
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from . import notificator
from . import profile


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_widget = AppWidget()
        self.setCentralWidget(self.app_widget)
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.resize(700, 550)

    def load(self, data):
        self.app_widget.load(data)


class AppWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(AppWidget, self).__init__(*args, **kwargs)
        self.custom_layout = QVBoxLayout(self)
        self.profile_label = QLabel("Profile")
        self.profile = ProfileFrame(self)
        self.title_label = QLabel("Title")
        self.title = TitleFrame(self)
        self.tags_label = QLabel("Tags")
        self.tags = TagsFrame(self)
        self.text_label = QLabel("Text")
        self.text = TextFrame(self)
        self.helper_label = QLabel("Copy To Clipboard")
        self.helper = HelperFrame(self)
        self.control = ControlFrame(self)

        self.custom_layout.addWidget(self.profile_label)
        self.custom_layout.addWidget(self.profile)
        self.custom_layout.addWidget(self.title_label)
        self.custom_layout.addWidget(self.title)
        self.custom_layout.addWidget(self.tags_label)
        self.custom_layout.addWidget(self.tags)
        self.custom_layout.addWidget(self.text_label)
        self.custom_layout.addWidget(self.text)
        self.custom_layout.addWidget(self.helper_label)
        self.custom_layout.addWidget(self.helper)
        self.custom_layout.addWidget(self.control)

        self.setLayout(self.custom_layout)
        self.custom_layout.setSpacing(3)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
        self.setStyles()

    def load(self, data):
        self.title.load(data)
        self.tags.load(data)
        self.text.load(data)
        self.helper.load(data)

    def setStyles(self):
        self.title_label.setStyleSheet("color: gray; font-weight: bold")
        self.tags_label.setStyleSheet("color: gray; font-weight: bold")
        self.text_label.setStyleSheet("color: gray; font-weight: bold")
        self.helper_label.setStyleSheet("color: gray; font-weight: bold")


class ProfileFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notifier = notificator.SingletonNotificationProvider()

        self.custom_layout = QVBoxLayout(self)
        self.box = QComboBox()
        self.custom_layout.addWidget(self.box)
        self.setLayout(self.custom_layout)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

        self.box.clear()
        self.box.addItems(list(profile.all))
        self.box.currentTextChanged.connect(self.new_profile_selected)

    def new_profile_selected(self):
        notification = notificator.Notification(notificator.Messages.load_profile)
        self.notifier.notify(notification)


class TitleFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_layout = QVBoxLayout(self)
        self.input = QLineEdit()
        self.custom_layout.addWidget(self.input)
        self.setLayout(self.custom_layout)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

    def load(self, data):
        # TODO: Exception
        self.input.clear()
        self.input.setText(data["title"])


class TagsFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_layout = QHBoxLayout(self)
        self.input = QLineEdit()
        self.tags_box = QComboBox()
        self.add_button = QPushButton("+")
        self.custom_layout.addWidget(self.input, 7)
        self.custom_layout.addWidget(self.tags_box, 3)
        self.custom_layout.addWidget(self.add_button)
        self.setLayout(self.custom_layout)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

        self.tags_box.currentTextChanged.connect(self.new_tag_selected)
        self.add_button.clicked.connect(self.add_new_tag)

    def load(self, data):
        # TODO: Exception
        self.input.clear()
        self.tags_box.clear()
        self.input.setText(data["tags"])
        self.tags_box.addItems(data["predefined.tags"]) # TODO: Not correct

    def new_tag_selected(self):
        original = self.input.text()
        new_input_text = f"{original} {self.tags_box.currentText()}"
        self.input.setText(new_input_text)

    def add_new_tag(self):
        dlg = QInputDialog(self)
        dlg.setMinimumWidth(250)
        self.text, ok = dlg.getMultiLineText(self, 'Tags', 'Tags', "\n".join(self.all_tags_items()))
        self.tags_box.clear()
        self.tags_box.addItems([i.strip() for i in self.text.split("\n")])

    def all_tags_items(self):
        return [self.tags_box.itemText(i) for i in range(self.tags_box.count())]


class TextFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_layout = QVBoxLayout(self)
        self.input = QPlainTextEdit()
        self.custom_layout.addWidget(self.input)
        self.setLayout(self.custom_layout)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

    def load(self, data):
        self.input.clear()
        self.input.setPlainText(data["text"])


class HelperFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notifier = notificator.SingletonNotificationProvider()

        self.custom_layout = QHBoxLayout(self)
        self.box = QComboBox()
        self.add_button = QPushButton("+")
        self.custom_layout.addWidget(self.box, 1)
        self.custom_layout.addWidget(self.add_button)
        self.setLayout(self.custom_layout)

        self.box.currentTextChanged.connect(self.new_helper_selected)
        self.add_button.clicked.connect(self.add_new_helper)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

    def load(self, data):
        self.box.clear()
        self.box.addItems(data["helpers"])

    def new_helper_selected(self):
        notification = notificator.Notification(notificator.Messages.copy_to_clip_board)
        self.notifier.notify(notification)

    def add_new_helper(self):
        dlg = QInputDialog(self)
        dlg.setMinimumWidth(250)
        self.text, ok = dlg.getMultiLineText(self, 'Helpers', 'Helpers', "\n".join(self.all_tags_items()))
        self.box.clear()
        self.box.addItems([i.strip() for i in self.text.split("\n")])

    def all_tags_items(self):
        return [self.box.itemText(i) for i in range(self.box.count())]


class ControlFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notifier = notificator.SingletonNotificationProvider()

        self.custom_layout = QHBoxLayout(self)
        self.load_button = QPushButton("Load")
        self.save_button = QPushButton("Save")
        self.custom_layout.addWidget(self.load_button)
        self.custom_layout.addWidget(self.save_button)
        self.setLayout(self.custom_layout)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)

        self.load_button.clicked.connect(self.load)
        self.save_button.clicked.connect(self.save)

    def save(self):
        notification = notificator.Notification(notificator.Messages.save)
        self.notifier.notify(notification)

    def load(self):
        notification = notificator.Notification(notificator.Messages.load)
        self.notifier.notify(notification)

