import re


class Messages:
    save = "save"
    load = "load"
    copy_to_clip_board = "copy.to.clip.board"
    load_profile = "load_profile"


class Notification(object):
    def __init__(self, message, publisher=None):
        self.message = message
        self.publisher = publisher


class SingletonNotificationProvider:
    subscription = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonNotificationProvider, cls).__new__(cls)
        return cls.instance

    def subscribe(self, message, subscriber):
        self.subscription.setdefault(message, []).append(subscriber)

    def unsubscribe(self, message, subscriber):
        self.subscription[message].remove(subscriber)

    def notify(self, notification):
        for subscriber in self.subscription.setdefault(notification.message, []):
            subscriber(notification)