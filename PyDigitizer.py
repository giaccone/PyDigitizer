# PySide2
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PySide2.QtWidgets import QGroupBox, QPushButton, QFileDialog
from PySide2.QtWidgets import QRadioButton, QInputDialog, QLabel, QLineEdit
from PySide2.QtGui import QGuiApplication
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib as mpl
import sys
from math import log10, floor
import numpy as np
# initialization
plt.ion()
mpl.rcParams["keymap.back"] = ['left', 'c']


# Main Windows
class Windows(QMainWindow):

    def __init__(self):
        super().__init__()
        #
        size_object = QGuiApplication.primaryScreen().availableGeometry()
        screen_ratio = size_object.height() / size_object.width()
        self.title = "PyDigitizer"
        self.top = 100
        self.left = 100
        self.width = floor(size_object.width() * 0.2)
        self.height = floor(self.width * screen_ratio)
        #
        self.CentralWidget = self.InitWindow()
        #
        self.show()

    def InitWindow(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        central_widget = MainWidget(self)
        self.setCentralWidget(central_widget)
        #
        return central_widget


# Main Widget
class MainWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        # image
        self.img = None
        self.line_counter = 0
        # input
        self.xpic_min = None
        self.xpic_max = None
        self.ypic_min = None
        self.ypic_max = None
        #
        self.xreal_min = None
        self.yreal_min = None
        self.xreal_max = None
        self.yreal_max = None
        #
        self.x_scale_type = 'linear'
        self.y_scale_type = 'linear'

        # output
        self.x_sampled = None
        self.y_sampled = None
        #
        self.x = None
        self.y = None

        (self.x_linear,
        self.x_log,
        self.y_linear,
        self.y_log,
        self.hint_label,
        self.x_min_label,
        self.y_min_label,
        self.x_max_label,
        self.y_max_label,
        self.r_value,
        self.g_value,
        self.b_value,
        self.tol_value) = self.initUI()

        self.show()


    def initUI(self):

        # First Column (Commands)
        # ----------------------------------
        v_box_sx1 = QGroupBox()
        layout_sx1 = QGridLayout()
        #
        load_file_button = QPushButton('Load Image',self)
        load_file_button.clicked.connect(self.load_image)
        #
        layout_sx1.addWidget(load_file_button,0,0)
        v_box_sx1.setLayout(layout_sx1)
        # ----------------------------------
        v_box_sx2 = QGroupBox()
        v_box_sx2.setTitle('Picture limits')
        layout_sx2 = QGridLayout()
        #
        xmin_button = QPushButton('Pick X_min',self)
        xmin_label = QLabel(self)
        xmin_label.setStyleSheet(('background-color : white; color: black'))
        ymin_button = QPushButton('Pick Y_min',self)
        ymin_label = QLabel(self)
        ymin_label.setStyleSheet(('background-color : white; color: black'))
        xmax_button = QPushButton('Pick X_max',self)
        xmax_label = QLabel(self)
        xmax_label.setStyleSheet(('background-color : white; color: black'))
        ymax_button = QPushButton('Pick Y_max',self)
        ymax_label = QLabel(self)
        ymax_label.setStyleSheet(('background-color : white; color: black'))
        #
        xmin_button.clicked.connect(self.pick_xmin)
        ymin_button.clicked.connect(self.pick_ymin)
        xmax_button.clicked.connect(self.pick_xmax)
        ymax_button.clicked.connect(self.pick_ymax)
        #
        layout_sx2.addWidget(xmin_button,0,0)
        layout_sx2.addWidget(xmin_label,0,1)
        layout_sx2.addWidget(ymin_button,1,0)
        layout_sx2.addWidget(ymin_label,1,1)
        layout_sx2.addWidget(xmax_button,2,0)
        layout_sx2.addWidget(xmax_label,2,1)
        layout_sx2.addWidget(ymax_button,3,0)
        layout_sx2.addWidget(ymax_label,3,1)
        #
        v_box_sx2.setLayout(layout_sx2)
        # ----------------------------------
        v_box_sx3 = QGroupBox()
        v_box_sx3.setTitle('x scale')
        layout_sx3 = QGridLayout()
        xlinear = QRadioButton('linear')
        xlinear.setChecked(True)
        xlolg = QRadioButton('log')
        layout_sx3.addWidget(xlinear,0,0)
        layout_sx3.addWidget(xlolg,0,1)
        #
        xlinear.clicked.connect(self.set_x_scale_type)
        xlolg.clicked.connect(self.set_x_scale_type)
        #
        v_box_sx3.setLayout(layout_sx3)
        # ----------------------------------
        v_box_sx4 = QGroupBox()
        v_box_sx4.setTitle('y scale')
        layout_sx4 = QGridLayout()
        ylinear = QRadioButton('linear')
        ylinear.setChecked(True)
        ylog = QRadioButton('log')
        layout_sx4.addWidget(ylinear,0,0)
        layout_sx4.addWidget(ylog,0,1)
        #
        ylinear.clicked.connect(self.set_y_scale_ype)
        ylog.clicked.connect(self.set_y_scale_ype)
        #
        v_box_sx4.setLayout(layout_sx4)
        # ----------------------------------
        v_box_sx5 = QGroupBox()
        layout_sx5 = QGridLayout()

        pick_point_button = QPushButton('Pick Points',self)
        pick_point_button.clicked.connect(self.pick_points)

        layout_sx5.addWidget(pick_point_button,0,0)
        v_box_sx5.setLayout(layout_sx5)
        # ----------------------------------
        v_box_sx6 = QGroupBox()
        layout_sx6 = QGridLayout()

        color_selection_button = QPushButton('Select by color',self)
        color_selection_button.clicked.connect(self.select_by_color)
        clean_plot_button = QPushButton('Clean plot',self)
        clean_plot_button.clicked.connect(self.clean_plot)
        exclude_area_button = QPushButton('Exclude area',self)
        exclude_area_button.clicked.connect(self.exclude_area)

        #
        r_label = QLabel(self, text="R value (0 - 255)")
        r_label.setStyleSheet(('qproperty-alignment: AlignCenter'))
        g_label = QLabel(self, text="G value (0 - 255)")
        g_label.setStyleSheet(('qproperty-alignment: AlignCenter'))
        b_label = QLabel(self, text="B value (0 - 255)")
        b_label.setStyleSheet(('qproperty-alignment: AlignCenter'))
        tol_label = QLabel(self, text="Tolerance (%)")
        tol_label.setStyleSheet(('qproperty-alignment: AlignCenter'))
        #
        r_value = QLineEdit(self, text="31")
        r_value.setStyleSheet(('background-color : white; color: black; qproperty-alignment: AlignCenter'))
        g_value = QLineEdit(self, text="119")
        g_value.setStyleSheet(('background-color : white; color: black; qproperty-alignment: AlignCenter'))
        b_value = QLineEdit(self, text="180")
        b_value.setStyleSheet(('background-color : white; color: black; qproperty-alignment: AlignCenter'))
        tol_value = QLineEdit(self, text="2")
        tol_value.setStyleSheet(('background-color : white; color: black; qproperty-alignment: AlignCenter'))


        layout_sx6.addWidget(color_selection_button, 0, 0, 1, 2)
        layout_sx6.addWidget(r_label,1,0)
        layout_sx6.addWidget(r_value,1,1)
        layout_sx6.addWidget(g_label,2,0)
        layout_sx6.addWidget(g_value,2,1)
        layout_sx6.addWidget(b_label,3,0)
        layout_sx6.addWidget(b_value,3,1)
        layout_sx6.addWidget(tol_label,4,0)
        layout_sx6.addWidget(tol_value,4,1)
        layout_sx6.addWidget(exclude_area_button, 5, 0, 1, 2)
        layout_sx6.addWidget(clean_plot_button, 6, 0, 1, 2)
        v_box_sx6.setLayout(layout_sx6)

        # ----------------------------------
        v_box_sx7 = QGroupBox()
        layout_sx7 = QGridLayout()

        save_to_file_button = QPushButton('Save to File',self)
        test_data_button = QPushButton('Test data',self)
        save_to_file_button.clicked.connect(self.save_to_file)
        test_data_button.clicked.connect(self.test_data)

        layout_sx7.addWidget(save_to_file_button,0,0)
        layout_sx7.addWidget(test_data_button,1,0)
        v_box_sx7.setLayout(layout_sx7)
        # ----------------------------------
        v_box_sx8 = QGroupBox()
        layout_sx8 = QGridLayout()
        hint_label = QLabel(self)
        hint_label.setWordWrap(True)
        hint_label.setMaximumHeight(80)
        hint_label.setStyleSheet(('background-color : white; color: black'))
        hint_label.setText('')

        layout_sx8.addWidget(hint_label,1,0)
        v_box_sx8.setLayout(layout_sx8)
        # ----------------------------------
        # ----------------------------------
        # Compose Windows
        window_layout = QGridLayout()
        window_layout.addWidget(v_box_sx1, 0, 0)
        window_layout.addWidget(v_box_sx2, 1, 0)
        window_layout.addWidget(v_box_sx3, 2, 0)
        window_layout.addWidget(v_box_sx4, 3, 0)
        window_layout.addWidget(v_box_sx5, 4, 0)
        window_layout.addWidget(v_box_sx6, 5, 0)
        window_layout.addWidget(v_box_sx7, 6, 0)
        window_layout.addWidget(v_box_sx8, 7, 0)
        #
        self.setLayout(window_layout)
        # ----------------------------------
        # ----------------------------------
        return (xlinear, xlolg, ylinear, ylog, hint_label,
                xmin_label, ymin_label, xmax_label, ymax_label, r_value, g_value, b_value, tol_value)

    def load_image(self):

        filename, _ = QFileDialog.getOpenFileName()
        self.img = plt.imread(filename)
        self.handle = plt.figure()
        plt.imshow(self.img)
        plt.axis('off')
        # plt.show()

    def pick_xmin(self):

        self.hint_label.setText('Click at a point having minimum x value.')
        plt.figure(self.handle.number)
        pt = plt.ginput(n=1)
        # self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        # self.FigCanvas.setFocus()
        # pt = self.FigCanvas.figure.ginput(n=1)
        self.xpic_min = pt[0][0]

        self.hint_label.setText('Provide the minimum x value.')
        self.xreal_min, okPressed = QInputDialog.getDouble(self, "Set X_min value", "Value:", value=0, decimals=4)
        self.hint_label.setText('')
        self.x_min_label.setText(str(self.xreal_min))

    def pick_ymin(self):

        self.hint_label.setText('Click at a point having minimum y value.')
        plt.figure(self.handle.number)
        pt = plt.ginput(n=1)
        # self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        # self.FigCanvas.setFocus()
        # pt = self.FigCanvas.figure.ginput(n=1)
        self.ypic_min = pt[0][1]

        self.hint_label.setText('Provide the minimum y value.')
        self.yreal_min, okPressed = QInputDialog.getDouble(self, "Set Y_min value", "Value:", value=0, decimals=4)
        self.hint_label.setText('')
        self.y_min_label.setText(str(self.yreal_min))

    def pick_xmax(self):

        self.hint_label.setText('Click at a point having maximum x value.')
        plt.figure(self.handle.number)
        pt = plt.ginput(n=1)
        # self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        # self.FigCanvas.setFocus()
        # pt = self.FigCanvas.figure.ginput(n=1)
        self.xpic_max = pt[0][0]

        self.hint_label.setText('Provide the maximum x value.')
        self.xreal_max, okPressed = QInputDialog.getDouble(self, "Set X_max value", "Value:", value=0, decimals=4)
        self.hint_label.setText('')
        self.x_max_label.setText(str(self.xreal_max))

    def pick_ymax(self):

        self.hint_label.setText('Click at a point having maximum y value.')
        plt.figure(self.handle.number)
        pt = plt.ginput(n=1)
        # self.FigCanvas.setFocusPolicy( Qt.ClickFocus )
        # self.FigCanvas.setFocus()
        # pt = self.FigCanvas.figure.ginput(n=1)
        self.ypic_max = pt[0][1]

        self.hint_label.setText('Provide the maximum y value.')
        self.yreal_max, okPressed = QInputDialog.getDouble(self, "Set Y_max value", "Value:", value=0, decimals=4)
        self.hint_label.setText('')
        self.y_max_label.setText(str(self.yreal_max))

    def set_x_scale_type(self):
        if self.x_linear.isChecked():
            self.x_scale_type = 'linear'
        elif self.x_log.isChecked():
            self.x_scale_type = 'log'

    def set_y_scale_ype(self):
        if self.y_linear.isChecked():
            self.y_scale_type = 'linear'
        elif self.y_log.isChecked():
            self.y_scale_type = 'log'

    def pick_points(self):

        self.hint_label.setText('Pick points: please note that if you zoom, '
                               'the first click (for zooming) is registered. '
                               'Remove it with backspace.')

        plt.figure(self.handle.number)
        pt = plt.ginput(n=-1, timeout=-1)

        self.x_sampled = []
        self.y_sampled = []

        for ptx, pty in pt:
            self.x_sampled.append(ptx)
            self.y_sampled.append(pty)

        self.hint_label.setText('')
    
    def select_by_color(self):
        
        # create an image with target color
        tgt = np.zeros_like(self.img[:, :, :3])
        tgt[:, :, 0] = int(self.r_value.text()) / 255
        tgt[:, :, 1] = int(self.g_value.text()) / 255
        tgt[:, :, 2] = int(self.b_value.text()) / 255

        # compute distance
        distance = self.img[:,:,:3] - tgt
        d = np.sqrt(np.sum(distance**2, axis=2))

        # find distance < tolerance
        tol = float(self.tol_value.text()) / 100
        y_sampled, x_sampled = np.where(d < tol)

        # get unique values
        xu = np.unique(x_sampled)
        yu = []
        for ele in xu:
            y_loc = y_sampled[x_sampled == ele]
            yu.append(np.average(y_loc))
        yu = np.array(yu)

        # superpose acquisition
        plt.figure(self.handle.number)
        plt.plot(xu, yu, f'C{self.line_counter+1}--')
        self.line_counter += 1

        # convert to list
        self.x_sampled = xu.tolist()
        self.y_sampled = yu.tolist()

    def clean_plot(self):
        # focus on original image
        plt.figure(self.handle.number)
        a = plt.gca()
        # delete each trace of the acquisitions
        for k in range(self.line_counter - 1, -1, -1):
            a.lines.pop(k)
        self.line_counter = 0

    def exclude_area(self):
        # get two corners
        self.hint_label.setText("Select two opposite corners of a rectange")
        pt = plt.ginput(n=2)
        self.hint_label.setText("")

        # reorder corners
        ix = sorted([int(pt[0][1]), int(pt[1][1])]) 
        iy = sorted([int(pt[0][0]), int(pt[1][0])]) 

        # fill with np.nan corresponding area
        self.img[ix[0]:ix[1], iy[0]:iy[1], :] = np.nan

        # put rectangle on the original image to show excluded area
        plt.figure(self.handle)
        patch = Rectangle((iy[0], ix[0]), iy[1] - iy[0], ix[1] - ix[0], edgecolor='k', linewidth=3, facecolor='k', alpha=0.2)
        ax = plt.gca()
        ax.add_patch(patch)

    def save_to_file(self):

        if self.xpic_min is None:
            self.hint_label.setText('Please pick X_min')
            return
        elif self.ypic_min is None:
            self.hint_label.setText('Please pick Y_min')
            return
        elif self.xpic_max is None:
            self.hint_label.setText('Please pick X_max')
            return
        elif self.ypic_max is None:
            self.hint_label.setText('Please pick Y_max')
            return
        elif self.xreal_min is None:
            self.hint_label.setText('Please pick X_min')
            return
        elif self.yreal_min is None:
            self.hint_label.setText('Please pick Y_min')
            return
        elif self.xreal_max is None:
            self.hint_label.setText('Please pick X_max')
            return
        elif self.yreal_max is None:
            self.hint_label.setText('Please pick Y_max')
            return
        elif self.x_sampled is None:
            self.hint_label.setText('Please pick data')
            return
        elif self.y_sampled is None:
            self.hint_label.setText('Please pick data')
            return
        else:
            self.hint_label.setText('')

        self.x = []
        self.y = []

        if self.x_scale_type == 'linear':
            for xs in self.x_sampled:
                self.x.append(self.xreal_min + (self.xreal_max - self.xreal_min) / (self.xpic_max - self.xpic_min) * ( xs - self.xpic_min))
        elif self.x_scale_type == 'log':
            x_real_min = log10(self.xreal_min)
            x_real_max = log10(self.xreal_max)
            for xs in self.x_sampled:
                self.x.append(10 ** (x_real_min + (xs - self.xpic_min)/(self.xpic_max - self.xpic_min) * (x_real_max - x_real_min)))

        if self.y_scale_type == 'linear':
            for ys in self.y_sampled:
                self.y.append(self.yreal_min + (self.yreal_max - self.yreal_min) / (self.ypic_max - self.ypic_min) * ( ys - self.ypic_min))
        elif self.y_scale_type == 'log':
            y_real_min = log10(self.yreal_min)
            y_real_max = log10(self.yreal_max)
            for ys in self.y_sampled:
                self.y.append(10 ** (y_real_min + (ys - self.ypic_min)/(self.ypic_max - self.ypic_min) * (y_real_max - y_real_min)))

        fname , _ = QFileDialog.getSaveFileName(self)

        try:
            with open(fname, 'w') as fid:
                for xpt, ypt in zip(self.x, self.y):
                    fid.write("{} {}\n".format(xpt, ypt))
        except FileNotFoundError:
            self.hint_label.setText('File not found')

    def test_data(self):

        filename, _ = QFileDialog.getOpenFileName()

        try:
            xs = []
            ys = []
            with open(filename, 'r') as fid:
                for line in fid:
                    line = line.split(' ')
                    xs.append(float(line[0]))
                    ys.append(float(line[1]))
            hf = plt.figure()
            plt.plot(xs, ys,'C0-o')
            ax = hf.gca()
            ax.set_xlabel('x variable')
            ax.set_ylabel('y variable')
            ax.set_xscale(self.x_scale_type)
            ax.set_yscale(self.y_scale_type)
            plt.show()
        except FileNotFoundError:
            self.hint_label.setText('File not found')


# Start App
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Windows()
    sys.exit(App.exec_())
