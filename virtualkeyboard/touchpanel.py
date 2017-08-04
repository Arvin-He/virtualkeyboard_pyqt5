# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from pyvkb import Keyboard
from ctrlpanel import ControlPanel
from utils import loadJson


class TouchPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TouchPanel, self).__init__(parent)
        self._config = loadJson()
        self.touchpanelWidth = self._config['touchpanel']['width']
        self.touchpanelHeight = self._config['touchpanel']['height']
        if sys.platform == "win32":
            self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus |
                                QtCore.Qt.Tool |
                                QtCore.Qt.FramelessWindowHint |
                                QtCore.Qt.WindowStaysOnTopHint)
            self.setGeometry(self._config['touchpanel']['left_win32'],
                             self._config['touchpanel']['top_win32'],
                             self.touchpanelWidth, self.touchpanelHeight)
        else:
            self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus |
                                QtCore.Qt.Tool |
                                QtCore.Qt.FramelessWindowHint |
                                QtCore.Qt.WindowStaysOnTopHint |
                                QtCore.Qt.X11BypassWindowManagerHint)
            self.setGeometry(self._config['touchpanel']['left'],
                             self._config['touchpanel']['top'],
                             self.touchpanelWidth, self.touchpanelHeight)

        self.initUI()

    def initUI(self):
        self.setFixedSize(self.touchpanelWidth, self.touchpanelHeight)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(6)
        self.key_board = Keyboard()
        self.control_panel = ControlPanel()
        self.vbox.addWidget(self.key_board)
        self.vbox.addWidget(self.control_panel)
        self.setLayout(self.vbox)
