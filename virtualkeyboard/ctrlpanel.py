# -*- coding:utf-8 -*-
import os
import sys
import json
import math
import logging
import functools
from PyQt5 import QtGui
from PyQt5 import QtCore, uic
from PyQt5 import QtWidgets
from punggol_rpc import punggol_eval, punggol_exec
import utils
from panelbutton import PanelButton

_configpath = os.path.abspath('ini/ctrlpanel.json')


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        with open(_configpath, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

        self.panelWidth = self._config['geometry']['width']
        self.panelHeight = self._config['geometry']['height']

        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(os.path.join(
            os.path.dirname(__file__), "res/ctrlpanel.ui"), self)
        self.setFixedSize(self.panelWidth, self.panelHeight)
        for attr in dir(self.ui):
            obj = getattr(self.ui, attr)
            if isinstance(obj, QtWidgets.QPushButton):
                # 这里有一个坑,闭包的问题
                obj.clicked.connect(functools.partial(self.on_clicked, obj))
                # obj.clicked.connect(lambda: punggol_exec(obj.property("btn_cmd")))

    def on_clicked(self, btn):
        punggol_exec(btn.property("btn_cmd"))

    def createLayout(self):
        self.grid0 = QtWidgets.QGridLayout()
        if 'spindelCtrl' in self._config.keys():
            self.grid1 = QtWidgets.QGridLayout()
            self.groupBox1 = QtWidgets.QGroupBox('spindelCtrl')
            self.groupBox1.setLayout(self.grid1)
            self.grid0.addWidget(self.groupBox1, 0, 0, 0, 2)
        if 'toolCtrl' in self._config.keys():
            self.grid2 = QtWidgets.QGridLayout()
            self.groupBox2 = QtWidgets.QGroupBox('toolCtrl')
            self.groupBox2.setLayout(self.grid2)
            self.grid0.addWidget(self.groupBox2, 0, 2, 0, 3)
            # self.hbox.addWidget(self.groupBox2)
        if 'programCtrl' in self._config.keys():
            self.grid3 = QtWidgets.QGridLayout()
            self.groupBox3 = QtWidgets.QGroupBox('programCtrl')
            self.groupBox3.setLayout(self.grid3)
            self.grid0.addWidget(self.groupBox3, 0, 6, 0, 2)
            # self.hbox.addWidget(self.groupBox3)
        if 'machineCtrl' in self._config.keys():
            self.grid4 = QtWidgets.QGridLayout()
            self.groupBox4 = QtWidgets.QGroupBox('machineCtrl')
            self.groupBox4.setLayout(self.grid4)
            self.grid0.addWidget(self.groupBox4, 0, 8, 0, 3)
            # self.hbox.addWidget(self.groupBox4)
        self.setLayout(self.grid0)
        # self.setLayout(self.hbox)

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
        btns_text = [self._config['machineCtrl'][item]['zh_CN']
                     for item in sorted(self._config['machineCtrl'].keys())]
        btns_name = sorted(self._config['machineCtrl'].keys())
        positions = self.setBtnsLayout(len(btns_text))
        self.machineCtrlBtnGroup = QtWidgets.QButtonGroup()
        for index, btn_text in enumerate(btns_text):
            btn_name = btns_name[index]
            button = PanelButton(
                text=btn_text, cmd=self._config['machineCtrl'][btn_name]['btn_cmd'])
            self.machineCtrlBtnGroup.addButton(button)
            self.grid4.addWidget(
                button, positions[index][0], positions[index][1])
