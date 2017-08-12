# -*- coding:utf-8 -*-

import os
import time
import functools
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtWidgets
from utils import loadJson
from punggol_rpc import punggol_exec, punggol_eval


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self._config = loadJson()
        self.ctrlpanelWidth = self._config['controlpanel']['width']
        self.ctrlpanelHeight = self._config['controlpanel']['height']
        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_update)
        self.timer.start(50)

    def initUI(self):
        self.ui = uic.loadUi(os.path.join(
            os.path.dirname(__file__), "res/ctrlpanel.ui"), self)
        self.setFixedSize(self.ctrlpanelWidth, self.ctrlpanelHeight)
        self.buttonGroup = []
        for attr in dir(self.ui):
            obj = getattr(self.ui, attr)
            if isinstance(obj, QtWidgets.QPushButton) or \
               isinstance(obj, QtWidgets.QToolButton):
                obj.setAutoRepeat(True)
                obj._repeate = False
                obj.clicked.connect(
                    functools.partial(self.on_handleClicked, obj))
                self.buttonGroup.append(obj)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.sys_ctrl.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.machine_ctrl.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1))

    def on_update(self):
        try:
            for btn in self.buttonGroup:
                if btn.property("checked_cmd") is not None:
                    btn.setCheckable(True)
                    btn.setChecked(bool(punggol_eval(btn.property("checked_cmd"))))
                if btn.property("enabled_cmd") is not None:
                    btn.setEnabled(bool(punggol_eval(btn.property("enabled_cmd"))))
        except Exception as e:
            print(e)
            self.timer.stop()
            return
            
    def on_handleClicked(self, btn):
        if btn.isDown():
            if btn._repeate is False:
                btn._repeate = True
                btn.setAutoRepeatInterval(50)
            else:
                self.on_pressed(btn)
        elif btn._repeate is True:
            btn._repeate = False
            self.on_released(btn)
        else:
            self.on_clicked(btn)

    def on_clicked(self, btn):
        try:
            if btn.property("clicked_cmd") is not None:
                punggol_exec(btn.property("clicked_cmd"))
            else:
                if btn.property("pressed_cmd") is not None:
                    punggol_exec(btn.property("pressed_cmd"))
                time.sleep(0.05)
                if btn.property("released_cmd") is not None:
                    punggol_exec(btn.property("released_cmd"))
        except Exception as e:
            print(e)
            return

    def on_pressed(self, btn):
        try:
            if btn.property("pressed_cmd") is not None:
                punggol_exec(btn.property("pressed_cmd"))
        except Exception as e:
            print(e)
            return

    def on_released(self, btn):
        try:
            if btn.property("released_cmd") is not None:
                punggol_exec(btn.property("released_cmd"))
        except Exception as e:
            print(e)
            return
