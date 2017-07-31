# /user/bin/python3
# -*- coding:utf-8 -*-
import sys
import ctypes
import pyautogui
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


show_function_keys = True
show_character_keys = True
show_system_editing_navigation_keys = False
show_numeric_keys = False

board_keys = {
    "function_keys": ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6',
                      'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
    "character_keys": [
        ['~\n`', '!\n1', '@\n2', '#\n3', '$\n4', '%\n5', '^\n6', '&&\n7',
            '*\n8', '(\n9', ')\n0', '_\n-', '+\n=', 'backspace'],
        ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u',
            'i', 'o', 'p', '{\n[', '}\n]', '|\n\\'],
        ['capslock', 'a', 's', 'd', 'f', 'g', 'h',
            'j', 'k', 'l', ':\n;', '"\n\'', 'enter'],
        ['shift', 'z', 'x', 'c', 'v', 'b', 'n',
            'm', '<\n,', '>\n.', '?\n/', 'shift'],
        ['ctrl', 'win', 'alt', 'space', 'alt', 'win', '[=]', 'ctrl']],
    "system_keys": ['printscreen', 'scrolllock', 'pause'],
    "editing_keys": ['insert', 'home', 'pageup', 'delete', 'end', 'pagedown'],
    "navigation_keys": ['up', 'left', 'down', 'right'],
    "numeric_keys": ['numlock', '/', '*', '-', '7', '8', '9', '+', '4', '5', '6', '1', '2', '3', 'enter', '0', '.'],
}


class KeyButton(QtWidgets.QPushButton):
    shift_flag = False
    capslock_flag = False
    def __init__(self, parent=None, name='', width=50, height=50, scale=1):
        super(KeyButton, self).__init__(parent)
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

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.setText(name)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        key_text = self.text().lower()
        if key_text == 'capslock':
            if KeyButton.capslock_flag is True:
                KeyButton.capslock_flag = False
                self.setStyleSheet('''background-color: rgb(192,192,192);
                                    color: black''')
            else:
                KeyButton.capslock_flag = True
                self.setStyleSheet('''background-color: rgb(10,206,10);
                                   color:white''')
                
        if key_text == 'shift':
            if KeyButton.shift_flag is True:
                KeyButton.shift_flag = False
                self.setStyleSheet('''background-color: rgb(192,192,192);
                                    color: black''')
            else:
                KeyButton.shift_flag = True
                self.setStyleSheet('''background-color: rgb(10,206,10);
                                   color:white''')

        if '\n' in key_text:
            if not KeyButton.shift_flag:
                key = key_text[key_text.find('\n') + 1:]
            else:
                key = key_text[0:key_text.find('\n')]
            pyautogui.press(key)
        else:
            pyautogui.press(key_text)

    def button_pressed(self):
        pyautogui.keyDown(self.text().lower())

    def button_released(self):
        pyautogui.keyUp(self.text().lower())


class Keyboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent)
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
        self.keyboardWidth = 900
        self.keyboardHeight = 350
        self.initUI()
        self.show()

    def initUI(self):
        self.createLayout()
        self.createKeyButtons()
        self.setFixedSize(self.keyboardWidth, self.keyboardHeight)
        if not sys.platform == "win32":
            self.setGeometry(0, 0, 752, self.keyboardWidth,
                             self.keyboardHeight)

    def createLayout(self):
        self.hbox = QtWidgets.QHBoxLayout()
        if show_function_keys or show_character_keys:
            self.vbox1 = QtWidgets.QVBoxLayout()
            self.hbox.addLayout(self.vbox1)
        if show_system_editing_navigation_keys:
            self.vbox2 = QtWidgets.QVBoxLayout()
            self.sysEditNavigateGrid = QtWidgets.QGridLayout()
            self.vbox2.addLayout(self.sysEditNavigateGrid)
            self.hbox.addLayout(self.vbox2)
        if show_numeric_keys:
            self.vbox3 = QtWidgets.QVBoxLayout()
            self.numericGrid = QtWidgets.QGridLayout()
            self.vbox3.addLayout(self.numericGrid)
            self.hbox.addLayout(self.vbox3)
        if hasattr(self, 'vbox1'):
            if show_function_keys:
                self.grid0 = QtWidgets.QGridLayout()
                self.vbox1.addLayout(self.grid0)
            self.grid1 = QtWidgets.QGridLayout()
            self.vbox1.addLayout(self.grid1)
            self.grid2 = QtWidgets.QGridLayout()
            self.vbox1.addLayout(self.grid2)
            self.grid3 = QtWidgets.QGridLayout()
            self.vbox1.addLayout(self.grid3)
            self.grid4 = QtWidgets.QGridLayout()
            self.vbox1.addLayout(self.grid4)
            self.grid5 = QtWidgets.QGridLayout()
            self.vbox1.addLayout(self.grid5)
        self.setLayout(self.hbox)

    def createKeyButtons(self):
        if show_function_keys:
            self.createFunctionButtons()
        self.createCharacterButtons()
        if show_system_editing_navigation_keys:
            self.createSysEditNavigationButtons()
        if show_numeric_keys:
            self.createNumericButtons()

    def createFunctionButtons(self):
        if hasattr(self, 'grid0'):
            self.functionBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['function_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.functionBtnGroup.addButton(button)
                self.grid0.addWidget(button, 0, index)

    def createCharacterButtons(self):
        self.rowOneBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][0]):
            if key_name == "backspace":
                button = KeyButton(name=key_name.capitalize())
                self.grid1.addWidget(button, 0, index, 1, 5)
                self.rowOneBtnGroup.addButton(button)
            else:
                button = KeyButton(name=key_name.capitalize())
                self.grid1.addWidget(button, 0, index)
                self.rowOneBtnGroup.addButton(button)

        self.rowTwoBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][1]):
            button = KeyButton(name=key_name.capitalize())
            self.rowOneBtnGroup.addButton(button)
            self.grid2.addWidget(button, 0, index)
        self.rowThreeBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][2]):
            button = KeyButton(name=key_name.capitalize())
            self.rowOneBtnGroup.addButton(button)
            self.grid3.addWidget(button, 0, index)
        self.rowFourBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][3]):
            button = KeyButton(name=key_name.capitalize())
            self.rowOneBtnGroup.addButton(button)
            self.grid4.addWidget(button, 0, index)
        self.rowFiveBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][4]):
            button = KeyButton(name=key_name.capitalize())
            self.rowOneBtnGroup.addButton(button)
            if key_name == "space":
                button.setFixedWidth(200)
            self.grid5.addWidget(button, 0, index)

    def createSysEditNavigationButtons(self):
        if hasattr(self, 'vbox2'):
            self.systemBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['system_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.systemBtnGroup.addButton(button)
                self.sysEditNavigateGrid.addWidget(button, 0, index)
            self.editingBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['editing_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.editingBtnGroup.addButton(button)
                if index < 3:
                    self.sysEditNavigateGrid.addWidget(button, 1, index)
                else:
                    self.sysEditNavigateGrid.addWidget(button, 2, index - 3)
            self.navigationBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['navigation_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.navigationBtnGroup.addButton(button)
                if index == 0:
                    self.sysEditNavigateGrid.addWidget(
                        button, 3, index, 1, 3, QtCore.Qt.AlignHCenter)
                else:
                    self.sysEditNavigateGrid.addWidget(button, 4, index - 1)

    def createNumericButtons(self):
        if hasattr(self, 'vbox3'):
            self.numericBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['numeric_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.numericBtnGroup.addButton(button)
                if index in range(4):
                    self.numericGrid.addWidget(button, 0, index)
                elif index in range(4, 8):
                    if index == 7:
                        self.numericGrid.addWidget(button, 1, index - 4, 2, 1)
                    else:
                        self.numericGrid.addWidget(button, 1, index - 4)
                elif index in range(8, 11):
                    self.numericGrid.addWidget(button, 2, index - 8)
                elif index in range(11, 15):
                    if index == 14:
                        self.numericGrid.addWidget(button, 3, index - 11, 2, 1)
                    else:
                        self.numericGrid.addWidget(button, 3, index - 11)
                elif index in range(15, 17):
                    if index == 15:
                        self.numericGrid.addWidget(
                            button, 4, index - 15, 1, 2, QtCore.Qt.AlignHCenter)
                    else:
                        self.numericGrid.addWidget(button, 4, 2)


def main():
    app = QtWidgets.QApplication(sys.argv)
    key_board = Keyboard()
    if sys.platform == "win32":
        ctypes.windll.user32.SetWindowLongW(
            int(key_board.winId()), -20, 0x08000000)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
