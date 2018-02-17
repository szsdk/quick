import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,\
    QPushButton, QAction, QLineEdit, QMessageBox, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
### For high dpi screen
# from PyQt5 import QtCore
# if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    # QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

import click


def text_param(opt):
    param = QLabel(opt.name)
    value = QLineEdit()
    param.setToolTip(opt.help)

    def to_command():
        return [opt.opts[0], value.text()]
    return [param, value], to_command


class App(QWidget):

    def __init__(self, func):
        super().__init__()
        self.func = func
        self.title = func.name
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.params_func = []
        for i, para in enumerate(self.func.params):
            widget, value_func = text_param(para)
            self.params_func.append(value_func)
            for idx, w in enumerate(widget):
                if isinstance(w, QtWidgets.QLayout):
                    self.grid.addLayout(w, i, idx)
                else:
                    self.grid.addWidget(w, i, idx)
        # Create a button in the window
        self.button = QPushButton('run', self)
        self.grid.addWidget(self.button, i+1, 0)
        # self.button.move(20, 80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.setLayout(self.grid)

        self.show()

    @pyqtSlot()
    def on_click(self):
        sys.argv = [self.func.name]
        for value_func in self.params_func:
            sys.argv += value_func()
        print(sys.argv)
        self.func()

def gui_it(click_func):
    app = QApplication(sys.argv)
    ex = App(click_func)
    sys.exit(app.exec_())
