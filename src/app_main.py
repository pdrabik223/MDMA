import sys

from PyQt6.QtWidgets import QApplication

from functionalities.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()
