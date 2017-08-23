# -*- coding:utf-8 -*-

import os
import time
import functools
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from utils import loadJson
from _rpc import _exec, _eval


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self._config = loadJson()
        self.ctrlpanelWidth = self._config['controlpanel']['width']
        self.ctrlpanelHeight = self._config['controlpanel']['height']
        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.on_update)
        self.timer.start()

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
        self.onCheckSatus(self.ui.stackedWidget.currentIndex())
        self.ui.sys_ctrl.clicked.connect(self.onSys_ctrl)
        self.ui.machine_ctrl.clicked.connect(self.onMachine_ctrl)
        self.ui.sys_ctrl_2.clicked.connect(self.onSys_ctrl_2)
    
    def onSys_ctrl(self):
        # 切换至系统操作面板
        self.ui.stackedWidget.setCurrentIndex(0)
        self.onCheckSatus(self.ui.stackedWidget.currentIndex())

    def onMachine_ctrl(self):
        # 切换至机床操作面板
        self.ui.stackedWidget.setCurrentIndex(2)
        self.onCheckSatus(self.ui.stackedWidget.currentIndex())

    def onSys_ctrl_2(self):
        # 切换至系统操作面板2
        self.ui.stackedWidget.setCurrentIndex(1)
        self.onCheckSatus(self.ui.stackedWidget.currentIndex())
    
    def onCheckSatus(self, s):
        self.ui.machine_ctrl.setChecked(True if s==2 else False)
        self.ui.sys_ctrl.setChecked(True if s==0 else False)
        self.ui.sys_ctrl_2.setChecked(True if s==1 else False)

    def on_update(self):
        for btn in self.buttonGroup:
            if btn.property("checked_cmd") is not None:
                if str(btn.property("checked_cmd")) != "":
                    btn.setCheckable(True)
                    try:
                        result = _eval(btn.property("checked_cmd"))
                        btn.setChecked(bool(result))
                    except BaseException as e:
                        return
            if btn.property("enabled_cmd") is not None:
                if str(btn.property("enabled_cmd")) != "":
                    try:
                        result = _eval(btn.property("enabled_cmd"))
                        btn.setEnabled(bool(result))
                    except BaseException as e:
                        return

    def on_handleClicked(self, btn):
        if btn.isDown():
            if btn._repeate is False:
                btn._repeate = True
                btn.setAutoRepeatInterval(50)
                btn.setAutoRepeatDelay(0)
                self.on_pressed(btn)
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
                _exec(btn.property("clicked_cmd"))
            else:
                if btn.property("pressed_cmd") is not None:
                    _exec(btn.property("pressed_cmd"))
                time.sleep(0.05)
                if btn.property("released_cmd") is not None:
                    _exec(btn.property("released_cmd"))
        except BaseException as e:
            print(e)
            return

    def on_pressed(self, btn):
        try:
            if btn.property("pressed_cmd") is not None:
                _exec(btn.property("pressed_cmd"))
        except BaseException as e:
            print(e)
            return

    def on_released(self, btn):
        try:
            if btn.property("released_cmd") is not None:
                _exec(btn.property("released_cmd"))
        except BaseException as e:
            print(e)
            return
