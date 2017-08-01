# -*- coding:utf-8 -*-
import os
import sys
import math
import logging

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import utils

_inipath = os.path.abspath('ini/ctrlpanel.ini')


class PanelButton(QtWidgets.QPushButton):

    def __init__(self, parent=None, name='', width=50, height=50, scale=1):
        super(PanelButton, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.setText(name)
        # self.clicked.connect(self.button_clicked)


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

        self._ini = utils.loadConfig(_inipath)
        self.panelWidth = int(self._ini['geometry']['width'])
        self.panelHeight = int(self._ini['geometry']['height'])
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.panelWidth, self.panelHeight)
        self.createLayout()
        self.createButtons()

    def createLayout(self):
        self.hbox = QtWidgets.QHBoxLayout()
        if 'spindelCtrl' in self._ini.sections():
            self.grid1 = QtWidgets.QGridLayout()
            self.groupBox1 = QtWidgets.QGroupBox('spindelCtrl')
            self.groupBox1.setLayout(self.grid1)
            self.hbox.addWidget(self.groupBox1)
        if 'toolCtrl' in self._ini.sections():
            self.grid2 = QtWidgets.QGridLayout()
            self.groupBox2 = QtWidgets.QGroupBox('toolCtrl')
            self.groupBox2.setLayout(self.grid2)
            self.hbox.addWidget(self.groupBox2)
        if 'programCtrl' in self._ini.sections():
            self.grid3 = QtWidgets.QGridLayout()
            self.groupBox3 = QtWidgets.QGroupBox('programCtrl')
            self.groupBox3.setLayout(self.grid3)
            self.hbox.addWidget(self.groupBox3)
        if 'machineCtrl' in self._ini.sections():
            self.grid4 = QtWidgets.QGridLayout()
            self.groupBox4 = QtWidgets.QGroupBox('machineCtrl')
            self.groupBox4.setLayout(self.grid4)
            self.hbox.addWidget(self.groupBox4)
        self.setLayout(self.hbox)
    
    def createButtons(self):
        self.createSpindleControlBtns()
        self.createToolControlBtns()
        self.createProgramControlBtns()
        self.createMachineControlBtns()

    def setBtnsLayout(self, btn_num):
        rows = cols = 1
        for row in range(1, btn_num):
            if row*row >= btn_num:
                rows = row
                break
        print("rows = ", rows)
        cols = int((btn_num+rows-1)/rows)
        print("cols = ", cols)
        positions = []
        for i in range(rows):
            for j in range(cols):
                positions.append((i, j))
        print(positions)
        return positions

    def createSpindleControlBtns(self):
        btns_text = [item.strip()
                     for item in self._ini['spindelCtrl']['btns_zh'].split(',')]
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            button = PanelButton(name=btn_text)
            self.grid1.addWidget(button, positions[index][0], positions[index][1])

    def createToolControlBtns(self):
        btns_text = [item.strip()
                     for item in self._ini['toolCtrl']['btns_zh'].split(',')]
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            button = PanelButton(name=btn_text)
            self.grid2.addWidget(button, positions[index][0], positions[index][1])

    def createProgramControlBtns(self):
        btns_text = [item.strip()
                     for item in self._ini['programCtrl']['btns_zh'].split(',')]
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            button = PanelButton(name=btn_text)
            self.grid3.addWidget(button, positions[index][0], positions[index][1])

    def createMachineControlBtns(self):
        btns_text = [item.strip()
                     for item in self._ini['machineCtrl']['btns_zh'].split(',')]
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            button = PanelButton(name=btn_text)
            self.grid4.addWidget(button, positions[index][0], positions[index][1])