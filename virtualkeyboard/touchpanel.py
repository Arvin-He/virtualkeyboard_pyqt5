import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from pyvkb import Keyboard
from ctrlpanel import ControlPanel


class TouchPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TouchPanel, self).__init__(parent)
        if sys.platform == "win32":
            self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus |
                                QtCore.Qt.Tool |
                                QtCore.Qt.FramelessWindowHint |
                                QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus |
                                QtCore.Qt.Tool |
                                QtCore.Qt.FramelessWindowHint |
                                QtCore.Qt.WindowStaysOnTopHint |
                                QtCore.Qt.X11BypassWindowManagerHint)
        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 650)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(6)
        self.key_board = Keyboard()
        self.control_panel = ControlPanel()
        self.vbox.addWidget(self.key_board)
        self.vbox.addWidget(self.control_panel)
        self.setLayout(self.vbox)
