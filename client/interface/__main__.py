from PyQt5.QtWidgets import QApplication, QMainWindow
from clint import Ui_MainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        send_request_btn = self.ui.sendRequestPushButton
        
        send_request_btn.setCheckable(True)
        send_request_btn.clicked.connect(self.send_request)

    def send_request(self):
        self.ui.cancelRequestPushButton.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.progressBar.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
