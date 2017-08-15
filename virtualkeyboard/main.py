# /user/bin/python3
# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets
from touchpanel import TouchPanel
from utils import loadApplicationStyleSheet
if sys.platform == "win32":
    import ctypes


def main():
    app = QtWidgets.QApplication(sys.argv)
    loadApplicationStyleSheet(app)
    touch_panel = TouchPanel()
    touch_panel.control_panel.ui.closeBtn.clicked.connect(lambda: app.exit())
    touch_panel.show()
    if sys.platform == "win32":
        # 等窗口显示以后再设置
        ctypes.windll.user32.SetWindowLongW(
            int(touch_panel.winId()), -20, 0x08000000)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
