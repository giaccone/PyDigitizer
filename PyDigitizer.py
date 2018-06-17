# modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QPushButton, QFileDialog, QSizePolicy
#
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.ion()
#
import sys


# FigureCanvas
class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, filename=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure(filename)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self,  filename):

        if filename is None:
            self.axes.clear()
        else:
            img = plt.imread(filename)
            self.axes.clear()
            self.axes.imshow(img)
            self.axes.axis('off')


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

        self.CentralWidget = MainWidget(self)
        self.setCentralWidget(self.CentralWidget)

        self.show()

# Main Widget
class MainWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.initUI()


    def initUI(self):

        # First Column (Commands)
        VBox1 = QGroupBox()
        Layout1 = QGridLayout()
        #
        LoadFileButton = QPushButton('Load Image',self)
        LoadFileButton.clicked.connect(self.loadImage)
        #
        Layout1.addWidget(LoadFileButton,0,0)
        VBox1.setLayout(Layout1)

        # First Column (Figure)
        VBox2 = QGroupBox()
        Layout2 = QGridLayout()
        #
        self.FigCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.FigCanvas, VBox2)
        #
        Layout2.addWidget(self.FigCanvas,0,0)
        Layout2.addWidget(toolbar,1,0)
        VBox2.setLayout(Layout2)

        # Compose Windows
        windowLayout = QGridLayout()
        windowLayout.addWidget(VBox1, 0, 0)
        windowLayout.addWidget(VBox2, 0, 1)
        # Stretches
        windowLayout.setColumnStretch(0, 0)
        windowLayout.setColumnStretch(1, 2)
        #
        self.setLayout(windowLayout)
        self.show()


    def loadImage(self):
        filename, _ = QFileDialog.getOpenFileName()
        img = plt.imread(filename)
        self.FigCanvas.axes.clear()
        self.FigCanvas.axes.imshow(img)
        self.FigCanvas.axes.axis('off')
        self.FigCanvas.draw_idle()


# Start App
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Windows()
    sys.exit(App.exec())
