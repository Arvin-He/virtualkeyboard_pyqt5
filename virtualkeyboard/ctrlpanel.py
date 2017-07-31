# -*- coding:utf-8 -*-
import os
import sys
import logging

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import utils

_inipath = os.path.abspath('ctrlpanel.ini')


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
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
        self.panelWidth = 900
        self.panelHeight = 300
        self._ini = utils.loadConfig(_inipath)
        self.initUI()
        # self.show()

    def initUI(self):
        self.setFixedSize(self.panelWidth, self.panelHeight)
        # if sys.platform == "win32":
            # self.setGeometry(0, 1002, self.panelWidth, self.panelHeight)
