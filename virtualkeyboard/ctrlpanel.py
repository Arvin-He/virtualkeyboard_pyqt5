# -*- coding:utf-8 -*-
import os
import sys
import json
import math
import logging
from PyQt5 import QtGui
from PyQt5 import QtCore, uic
from PyQt5 import QtWidgets
from punggol_rpc import punggol_eval, punggol_exec


_configpath = os.path.abspath('ini/ctrlpanel.json')


class PanelButton(QtWidgets.QPushButton):

    def __init__(self, parent=None, text='', cmd=''):
        super(PanelButton, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.setText(text)
        self.cmd = cmd
        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        try:
            punggol_exec(self.cmd)
        except Exception as e:
            # print(e)
            return


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        with open(_configpath, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

        self.panelWidth = self._config['geometry']['width']
        self.panelHeight = self._config['geometry']['height']

        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "res/ctrlpanel.ui"), self)
        self.setFixedSize(self.panelWidth, self.panelHeight)
        self.ui.btn1.cmd = "basic.mdi('M3')"
        # self.createLayout()
        # self.createButtons()

    def createLayout(self):
        self.hbox = QtWidgets.QHBoxLayout()
        # if 'spindelCtrl' in self._ini.sections():
        if 'spindelCtrl' in self._config.keys():
            self.grid1 = QtWidgets.QGridLayout()
            self.groupBox1 = QtWidgets.QGroupBox('spindelCtrl')
            self.groupBox1.setLayout(self.grid1)
            self.hbox.addWidget(self.groupBox1)
        if 'toolCtrl' in self._config.keys():
            self.grid2 = QtWidgets.QGridLayout()
            self.groupBox2 = QtWidgets.QGroupBox('toolCtrl')
            self.groupBox2.setLayout(self.grid2)
            self.hbox.addWidget(self.groupBox2)
        if 'programCtrl' in self._config.keys():
            self.grid3 = QtWidgets.QGridLayout()
            self.groupBox3 = QtWidgets.QGroupBox('programCtrl')
            self.groupBox3.setLayout(self.grid3)
            self.hbox.addWidget(self.groupBox3)
        if 'machineCtrl' in self._config.keys():
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
            if row * row >= btn_num:
                rows = row
                break
        cols = int((btn_num + rows - 1) / rows)
        positions = []
        for i in range(rows):
            for j in range(cols):
                positions.append((i, j))
        return positions

    def createSpindleControlBtns(self):
        btns_text = [self._config['spindelCtrl'][item]['zh_CN']
                     for item in sorted(self._config['spindelCtrl'].keys())]
        btns_name = sorted(self._config['spindelCtrl'].keys())
        positions = self.setBtnsLayout(len(btns_text))
        self.spindleCtrlBtnGroup = QtWidgets.QButtonGroup()
        for index, btn_text in enumerate(btns_text):
            btn_name = btns_name[index]
            button = PanelButton(
                text=btn_text, cmd=self._config['spindelCtrl'][btn_name]['btn_cmd'])
            self.spindleCtrlBtnGroup.addButton(button)
            self.grid1.addWidget(
                button, positions[index][0], positions[index][1])

    def createToolControlBtns(self):
        btns_text = [self._config['toolCtrl'][item]['zh_CN']
                     for item in sorted(self._config['toolCtrl'].keys())]
        btns_name = sorted(self._config['toolCtrl'].keys())
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            btn_name = btns_name[index]
            button = PanelButton(
                text=btn_text, cmd=self._config['toolCtrl'][btn_name]['btn_cmd'])
            self.grid2.addWidget(
                button, positions[index][0], positions[index][1])

    def createProgramControlBtns(self):
        btns_text = [self._config['programCtrl'][item]['zh_CN']
                     for item in sorted(self._config['programCtrl'].keys())]
        btns_name = sorted(self._config['programCtrl'].keys())
        positions = self.setBtnsLayout(len(btns_text))
        for index, btn_text in enumerate(btns_text):
            btn_name = btns_name[index]
            button = PanelButton(
                text=btn_text, cmd=self._config['programCtrl'][btn_name]['btn_cmd'])
            self.grid3.addWidget(
                button, positions[index][0], positions[index][1])

    def createMachineControlBtns(self):