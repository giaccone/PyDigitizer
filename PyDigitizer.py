# modules
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# Main Windows
class Windows(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "PyDigitizer"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.InitWindow()

    def InitWindow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


# Start App
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Windows()
    sys.exit(App.exec())
