# -*- coding:utf-8 -*-
import os
import functools
from PyQt5 import uic
from PyQt5 import QtWidgets
from utils import loadJson
from punggol_rpc import punggol_exec


class ControlPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ControlPanel, self).__init__(parent)
        self._config = loadJson()
        self.ctrlpanelWidth = self._config['controlpanel']['width']
        self.ctrlpanelHeight = self._config['controlpanel']['height']
        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(os.path.join(
            os.path.dirname(__file__), "res/ctrlpanel.ui"), self)
        self.setFixedSize(self.ctrlpanelWidth, self.ctrlpanelHeight)
        for attr in dir(self.ui):
            obj = getattr(self.ui, attr)
            if isinstance(obj, QtWidgets.QPushButton) or isinstance(obj, QtWidgets.QToolButton):
                obj.clicked.connect(functools.partial(self.on_clicked, obj))

    def on_clicked(self, btn):
        try:
            if btn.property("btn_cmd") is not None:
                punggol_exec(btn.property("btn_cmd"))
        except Exception as e:
            print(e)
            return
