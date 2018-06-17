# modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtCore import Qt
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

        self.Xpic_min = None
        self.Xpic_max = None
        self.Ypic_min = None
        self.Ypic_max = None

        self.XScaleType = 'linear'
        self.YScaleType = 'linear'

        self.initUI()


    def initUI(self):

        # First Column (Commands)
        VBoxSx1 = QGroupBox()
        LayoutSx1 = QGridLayout()
        #
        LoadFileButton = QPushButton('Load Image',self)
        LoadFileButton.clicked.connect(self.loadImage)
        #
        LayoutSx1.addWidget(LoadFileButton,0,0)
        VBoxSx1.setLayout(LayoutSx1)

        VBoxSx2 = QGroupBox()
        VBoxSx2.setTitle('Picture limits')
        LayoutSx2 = QGridLayout()
        #
        XminButton = QPushButton('Pick X_min',self)
        YminButton = QPushButton('Pick Y_min',self)
        XmaxButton = QPushButton('Pick X_max',self)
        YmaxButton = QPushButton('Pick Y_max',self)
        #
        LayoutSx2.addWidget(XminButton,0,0)
        LayoutSx2.addWidget(YminButton,1,0)
        LayoutSx2.addWidget(XmaxButton,2,0)
        LayoutSx2.addWidget(YmaxButton,3,0)
        #
        XminButton.clicked.connect(self.pickXmin)
        YminButton.clicked.connect(self.pickYmin)
        XmaxButton.clicked.connect(self.pickXmax)
        YmaxButton.clicked.connect(self.pickYmax)
        #
        VBoxSx2.setLayout(LayoutSx2)

        VBoxSx3 = QGroupBox()
        VBoxSx3.setTitle('x scale')
        LayoutSx3 = QGridLayout()
        self.Xlinear = QRadioButton('linear')
        self.Xlinear.setChecked(True)
        self.Xlog = QRadioButton('log')
        LayoutSx3.addWidget(self.Xlinear,0,0)
        LayoutSx3.addWidget(self.Xlog,0,1)
        #
        self.Xlinear.clicked.connect(self.setXScaleType)
        self.Xlog.clicked.connect(self.setXScaleType)
        #
        VBoxSx3.setLayout(LayoutSx3)

        VBoxSx4 = QGroupBox()
        VBoxSx4.setTitle('y scale')
        LayoutSx4 = QGridLayout()
        self.Ylinear = QRadioButton('linear')
        self.Ylinear.setChecked(True)
        self.Ylog = QRadioButton('log')
        LayoutSx4.addWidget(self.Ylinear,0,0)
        LayoutSx4.addWidget(self.Ylog,0,1)
        #
        self.Ylinear.clicked.connect(self.setYScaleType)
        self.Ylog.clicked.connect(self.setYScaleType)
        #
        VBoxSx4.setLayout(LayoutSx4)



        VBoxSx5 = QGroupBox()
        LayoutSx5 = QGridLayout()

        PickPointButton = QPushButton('Pick Point',self)
        PickPointButton.clicked.connect(self.pickPoints)

        LayoutSx5.addWidget(PickPointButton,1,0)
        VBoxSx5.setLayout(LayoutSx5)

        # Second Column (Figure)
        VBoxDx1 = QGroupBox()
        Layout2 = QGridLayout()
        #
        self.FigCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.FigCanvas, VBoxDx1)
        #
        Layout2.addWidget(self.FigCanvas,0,0)
        Layout2.addWidget(toolbar,1,0)
        VBoxDx1.setLayout(Layout2)

        # Compose Windows
        windowLayout = QGridLayout()
        windowLayout.addWidget(VBoxSx1, 0, 0)
        windowLayout.addWidget(VBoxSx2, 1, 0)
        windowLayout.addWidget(VBoxSx3, 2, 0)
        windowLayout.addWidget(VBoxSx4, 3, 0)
        windowLayout.addWidget(VBoxSx5, 4, 0)
        #
        windowLayout.addWidget(VBoxDx1, 0, 1, 5, 1)
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


    def pickXmin(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Xpic_min = pt[0][0]

        print(self.Xpic_min)


    def pickYmin(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Ypic_min = pt[0][1]

        print(self.Ypic_min)


    def pickXmax(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Xpic_max = pt[0][0]

        print(self.Xpic_max)

    def pickYmax(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Ypic_max = pt[0][1]

        print(self.Ypic_max)

    def setXScaleType(self):
        if self.Xlinear.isChecked():
            self.XScaleType = 'linear'
        elif self.Xlog.isChecked():
            self.XScaleType = 'log'

        print('Xscale is ' + self.XScaleType)

    def setYScaleType(self):
        if self.Ylinear.isChecked():
            self.YScaleType = 'linear'
        elif self.Ylog.isChecked():
            self.YScaleType = 'log'

        print('Yscale is ' + self.YScaleType)



    def pickPoints(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=-1)

        print(pt)



# Start App
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Windows()
    sys.exit(App.exec())
