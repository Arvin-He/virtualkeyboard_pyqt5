# /user/bin/python3
# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets
from pyvkb import Keyboard
from ctrlpanel import ControlPanel
if sys.platform == "win32":
    import ctypes


def main():
    app = QtWidgets.QApplication(sys.argv)
    key_board = Keyboard()
    control_panel = ControlPanel()
    key_board.setGeometry(100, 100, key_board.keyboardWidth,
                          key_board.keyboardHeight)
    key_board.show()
    
    if sys.platform == "win32":
        # 等窗口显示以后再设置
        ctypes.windll.user32.SetWindowLongW(
            int(key_board.winId()), -20, 0x08000000)
    else:
        key_board.setGeometry(0, 752, key_board.keyboardWidth,
                              key_board.keyboardHeight)

    control_panel.setGeometry(100,
                              102+key_board.keyboardHeight,
                              control_panel.panelWidth,
                              control_panel.panelHeight)
    control_panel.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
