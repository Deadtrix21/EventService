import pytest
from tools.LoggerInjectable import DataProcessor, NotificationSender

class DummyLogger:
    def __init__(self):
        self.messages = []
    def info(self, msg):
        self.messages.append(msg)
    def bind(self, **kwargs):
        return self
    def add(self, *args, **kwargs):
        pass

def test_data_processor_logs():
    logger = DummyLogger()
    processor = DataProcessor(logger=logger)
    processor.perform_action()
    assert "Processing data in DataProcessor." in logger.messages

def test_notification_sender_logs():
    logger = DummyLogger()
    sender = NotificationSender(logger=logger)
    sender.perform_action()
    assert "Sending notification in NotificationSender." in logger.messages
