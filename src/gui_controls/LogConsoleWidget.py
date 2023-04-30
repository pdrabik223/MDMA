from logging import LogRecord
from PyQt5.QtCore import QMutex, QMutexLocker
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit
import logging


class LogConsoleWidgetLoggingHandler(logging.Handler):
    def __init__(self, log_console_widget : "LogConsoleWidget"):
        super().__init__()
        self.log_console_widget = log_console_widget
        
    def createLock(self) -> None:
        self.mutex = QMutex()

    def acquire(self):
        self.mutex.lock()

    def release(self):
        self.mutex.unlock()

    def handleError(self, record: LogRecord) -> None:
        return super().handleError(record)

    def emit(self, record: logging.LogRecord):
        try:
            self.log_console_widget.add_record(self.format(record), record.levelno)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

class LogConsoleWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.LEVEL_TO_COLOR = {
            logging.CRITICAL: "red",
            logging.ERROR: "red",
            logging.WARNING: "orange",
            logging.INFO: "black",
        }
        self.setReadOnly(True)
        self.setFont(QFont("Courier New"))
        self.mutex = QMutex()

    def _color_text_according_to_log_level(self, text, log_level):
        color = self.LEVEL_TO_COLOR[log_level]
        return f"<div style='color: {color}'> {text} </div>"

    def add_record(self, message: str, log_level: int):
        with QMutexLocker(self.mutex):
            self.append(self._color_text_according_to_log_level(message, log_level))
            self.sync()

    def finish_connection(self):
        with QMutexLocker(self.mutex):
            self.insertHtml("(Logger closed)<br>")
            self.sync()

    def sync(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

