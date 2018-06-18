# modules
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtWidgets import QGroupBox, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtWidgets import QRadioButton, QInputDialog
from PyQt5.QtCore import Qt
#
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.ion()
#
import sys
from math import log10


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
        #
        self.title = "PyDigitizer"
        self.top = 100
        self.left = 100
        self.width = 900
        self.height = 500
        #
        self.CentralWidget = self.InitWindow()
        #
        self.show()

    def InitWindow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        CentralWidget = MainWidget(self)
        self.setCentralWidget(CentralWidget)
        #
        return CentralWidget


# Main Widget
class MainWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        # input
        self.Xpic_min = None
        self.Xpic_max = None
        self.Ypic_min = None
        self.Ypic_max = None
        #
        self.Xreal_min = None
        self.Yreal_min = None
        self.Xreal_max = None
        self.Yreal_max = None
        #
        self.XScaleType = 'linear'
        self.YScaleType = 'linear'

        # output
        self.Xsampled = None
        self.Ysampled = None
        #
        self.x = None
        self.y = None

        (self.Xlinear,
        self.Xlog,
        self.Ylinear,
        self.Ylog,
        self.FigCanvas) = self.initUI()

        self.show()


    def initUI(self):

        # First Column (Commands)
        # ----------------------------------
        VBoxSx1 = QGroupBox()
        LayoutSx1 = QGridLayout()
        #
        LoadFileButton = QPushButton('Load Image',self)
        LoadFileButton.clicked.connect(self.loadImage)
        #
        LayoutSx1.addWidget(LoadFileButton,0,0)
        VBoxSx1.setLayout(LayoutSx1)
        # ----------------------------------
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
        # ----------------------------------
        VBoxSx3 = QGroupBox()
        VBoxSx3.setTitle('x scale')
        LayoutSx3 = QGridLayout()
        Xlinear = QRadioButton('linear')
        Xlinear.setChecked(True)
        Xlolg = QRadioButton('log')
        LayoutSx3.addWidget(Xlinear,0,0)
        LayoutSx3.addWidget(Xlolg,0,1)
        #
        Xlinear.clicked.connect(self.setXScaleType)
        Xlolg.clicked.connect(self.setXScaleType)
        #
        VBoxSx3.setLayout(LayoutSx3)
        # ----------------------------------
        VBoxSx4 = QGroupBox()
        VBoxSx4.setTitle('y scale')
        LayoutSx4 = QGridLayout()
        Ylinear = QRadioButton('linear')
        Ylinear.setChecked(True)
        Ylog = QRadioButton('log')
        LayoutSx4.addWidget(Ylinear,0,0)
        LayoutSx4.addWidget(Ylog,0,1)
        #
        Ylinear.clicked.connect(self.setYScaleType)
        Ylog.clicked.connect(self.setYScaleType)
        #
        VBoxSx4.setLayout(LayoutSx4)
        # ----------------------------------
        VBoxSx5 = QGroupBox()
        LayoutSx5 = QGridLayout()

        PickPointButton = QPushButton('Pick Points',self)
        PickPointButton.clicked.connect(self.pickPoints)

        LayoutSx5.addWidget(PickPointButton,1,0)
        VBoxSx5.setLayout(LayoutSx5)
        # ----------------------------------
        VBoxSx6 = QGroupBox()
        LayoutSx6 = QGridLayout()

        SaveToFileButton = QPushButton('Save to File',self)
        SaveToFileButton.clicked.connect(self.saveToFile)

        LayoutSx6.addWidget(SaveToFileButton,1,0)
        VBoxSx6.setLayout(LayoutSx6)
        # ----------------------------------
        # Second Column (Figure)
        VBoxDx1 = QGroupBox()
        Layout2 = QGridLayout()
        #
        FigCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(FigCanvas, VBoxDx1)
        #
        Layout2.addWidget(FigCanvas,0,0)
        Layout2.addWidget(toolbar,1,0)
        VBoxDx1.setLayout(Layout2)
        # ----------------------------------
        # ----------------------------------
        # Compose Windows
        windowLayout = QGridLayout()
        windowLayout.addWidget(VBoxSx1, 0, 0)
        windowLayout.addWidget(VBoxSx2, 1, 0)
        windowLayout.addWidget(VBoxSx3, 2, 0)
        windowLayout.addWidget(VBoxSx4, 3, 0)
        windowLayout.addWidget(VBoxSx5, 4, 0)
        windowLayout.addWidget(VBoxSx6, 5, 0)
        #
        windowLayout.addWidget(VBoxDx1, 0, 1, 6, 1)
        # Stretches
        windowLayout.setColumnStretch(0, 0)
        windowLayout.setColumnStretch(1, 2)
        #
        self.setLayout(windowLayout)
        # ----------------------------------
        # ----------------------------------
        return Xlinear, Xlolg, Ylinear, Ylog, FigCanvas

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

        self.Xreal_min, okPressed = QInputDialog.getDouble(self, "Set X_min value", "Value:", 0)

    def pickYmin(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Ypic_min = pt[0][1]

        self.Yreal_min, okPressed = QInputDialog.getDouble(self, "Set Y_min value", "Value:", 0)

    def pickXmax(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Xpic_max = pt[0][0]

        self.Xreal_max, okPressed = QInputDialog.getDouble(self, "Set X_max value", "Value:", 0)

    def pickYmax(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=1)
        self.Ypic_max = pt[0][1]

        self.Yreal_max, okPressed = QInputDialog.getDouble(self, "Set Y_max value", "Value:", 0)

    def setXScaleType(self):
        if self.Xlinear.isChecked():
            self.XScaleType = 'linear'
        elif self.Xlog.isChecked():
            self.XScaleType = 'log'

    def setYScaleType(self):
        if self.Ylinear.isChecked():
            self.YScaleType = 'linear'
        elif self.Ylog.isChecked():
            self.YScaleType = 'log'

    def pickPoints(self):

        self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        self.FigCanvas.setFocus()
        pt = self.FigCanvas.figure.ginput(n=-1, timeout=-1)

        self.Xsampled = []
        self.Ysampled = []

        for ptx, pty in pt:
            self.Xsampled.append(ptx)
            self.Ysampled.append(pty)

        print(self.Xsampled)
        print(self.Ysampled)

    def saveToFile(self):

        self.x = []
        self.y = []

        if self.XScaleType is 'linear':
            for xs in self.Xsampled:
                self.x.append(self.Xreal_min + (self.Xreal_max - self.Xreal_min) / (self.Xpic_max - self.Xpic_min) * ( xs - self.Xpic_min))
        elif self.XScaleType is 'log':
            Xreal_min = log10(self.Xreal_min)
            Xreal_max = log10(self.Xreal_max)
            for xs in self.Xsampled:
                self.x.append(10 ** (Xreal_min + (xs - self.Xpic_min)/(self.Xpic_max - self.Xpic_min) * (Xreal_max - Xreal_min)))

        if self.YScaleType is 'linear':
            for ys in self.Ysampled:
                self.y.append(self.Yreal_min + (self.Yreal_max - self.Yreal_min) / (self.Ypic_max - self.Ypic_min) * ( ys - self.Ypic_min))
        elif self.YScaleType is 'log':
            Yreal_min = log10(self.Yreal_min)
            Yreal_max = log10(self.Yreal_max)
            for ys in self.Ysampled:
                self.y.append(10 ** (Yreal_min + (ys - self.Ypic_min)/(self.Ypic_max - self.Ypic_min) * (Yreal_max - Yreal_min)))

        fname , _ = QFileDialog.getSaveFileName(self)

        with open(fname, 'w') as fid:
            for xpt, ypt in zip(self.x, self.y):
                fid.write("{} {}\n".format(xpt, ypt))


# Start App
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Windows()
    sys.exit(App.exec())
