# /user/bin/python3
# -*- coding:utf-8 -*-
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
# from PyQt5.QtDBus import QDBusConnection
# from PyQt5.QtDBus import QDBusConnection, QDBusInterface
import pyautogui
import sys

# ========== Configurations ====================
BUTTON_BACKGROUND = "black"
MAIN_FRAME_BACKGROUND = "cornflowerblue"
BUTTON_LOOK = "flat"  # flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE = "Python Virtual KeyBoard."
TOPBAR_BACKGROUND = "skyblue"
TRANSPARENCY = 0.7
FONT_COLOR = "white"

show_function_keys = True
show_character_keys = True
show_system_editing_navigation_keys = False
show_numeric_keys = False

board_keys = {
    "function_keys": ['esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
    "character_keys": [
        ['~\n`', '!\n1', '@\n2', '#\n3', '$\n4', '%\n5', '^\n6', '&&\n7', '*\n8', '(\n9', ')\n0', '_\n-', '+\n=', 'backspace'],
        ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '{\n[', '}\n]', '|\n\\'],
        ['capslock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':\n;', '"\n\'', 'enter'],
        ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<\n,', '>\n.', '?\n/', 'shift'],
        ['ctrl', 'win', 'alt', 'space', 'alt', 'win', '[=]', 'ctrl']],
    "system_keys": ['printscreen', 'scrolllock', 'pause'],
    "editing_keys": ['insert', 'home', 'pageup', 'delete', 'end', 'pagedown'],
    "navigation_keys": ['up', 'left', 'down', 'right'],
    "numeric_keys": ['numlock', '/', '*', '-', '7', '8', '9', '+', '4', '5', '6', '1', '2', '3', 'enter', '0', '.'],
}


# class KeyButton(QtWidgets.QPushButton):
#     def __init__(self, parent=None, name='', width=50, height=50, scale=1):
#         super(KeyButton, self).__init__(parent)
#         self.setText(name)
#         # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#         self.width = width*scale
#         self.height = height
#         # self.setMinimumSize(self.width, self.height)
#         self.setFixedSize(self.width, self.height)
#         # self.setFixedSize(62, 62)

class KeyButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, name='', width=50, height=50, scale=1):
        super(KeyButton, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setText(name)
        
        # self.width = width*scale
        # self.height = height
        # self.setMinimumSize(self.width, self.height)
        # self.setFixedSize(self.width, self.height)
        # self.setFixedSize(62, 62)
        self.clicked.connect(self.button_clicked)
        self.pressed.connect(self.button_pressed)
        self.released.connect(self.button_released)

    # def focusInEvent(self, event):
    #     return
    
    def button_clicked(self):
        # self.clearFocus()
        print(self.text().lower())
        pyautogui.press(str(self.text().lower()))

    def button_pressed(self):
        # self.clearFocus()
        print(self.text().lower())
        pyautogui.keyDown(self.text().lower())

    def button_released(self):
        # self.clearFocus()
        print(self.text().lower())
        pyautogui.keyUp(self.text().lower())


class Keyboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowDoesNotAcceptFocus | QtCore.Qt.Tool |
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        
        # self.clearFocus()
        # self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.keyboardWidth = 900
        self.keyboardHeight = 350
        self.initUI()
        self.show()
        # self.hbox.setContentsMargins(10, 10, 10, 10)
        # self.hbox.setSpacing(6)

    # def focusInEvent(self, event):
    #     return
        # super(_ParameterSpinBox, self).focusInEvent(event)
        # self._originalValue = self.value()
    # def closeEvent(self, event):
    #     print("xxxxxxx")
    #     self.close()
    #     self.des

    def initUI(self):
        self.createLayout()
        self.createKeyButtons()
        # self.setGeometry(100, 100, 900, 400)
        self.setFixedSize(self.keyboardWidth, self.keyboardHeight)
        # self.calButtonSize()

    def calButtonSize(self):
        if show_system_editing_navigation_keys and not show_numeric_keys:
            self.keyNuminRow = 18
        elif show_system_editing_navigation_keys and  show_numeric_keys:
            self.keyNuminRow = 22
        else:
            self.keyNuminRow = 15
        if not show_function_keys:
            self.keyNuminCol = 5
        else:
            self.keyNuminCol = 6
        self.keyBtnWidth = (self.keyboardWidth-self.margin*2-self.spaceing*(self.keyNuminRow-1))/self.keyNuminRow
        self.keyBtnHeight = (self.keyboardHeight-self.margin*2-self.spaceing*(self.keyNuminCol-1))/self.keyNuminCol
        print(self.keyBtnWidth, self.keyBtnHeight)

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
                # button = KeyButton(name=key_name.capitalize(), width=self.keyBtnWidth, height=self.keyBtnHeight)
                self.functionBtnGroup.addButton(button)
                self.grid0.addWidget(button, 0, index)

    def createCharacterButtons(self):
        self.rowOneBtnGroup = QtWidgets.QButtonGroup()
        for index, key_name in enumerate(board_keys['character_keys'][0]):
            if key_name == "backspace":
                button = KeyButton(name=key_name.capitalize())
                # button = KeyButton(name=key_name.capitalize(), width=self.keyBtnWidth, height=self.keyBtnHeight, scale=1.5)
                self.grid1.addWidget(button, 0, index, 1, 5)
                self.rowOneBtnGroup.addButton(button)    
            else:
                button = KeyButton(name=key_name.capitalize())
                # button = KeyButton(name=key_name.capitalize(), width=self.keyBtnWidth, height=self.keyBtnHeight)
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
                    # print(button.width())
                    button.setFixedWidth(300)
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
                    self.sysEditNavigateGrid.addWidget(button, 2, index-3)
            self.navigationBtnGroup = QtWidgets.QButtonGroup()
            for index, key_name in enumerate(board_keys['navigation_keys']):
                button = KeyButton(name=key_name.capitalize())
                self.navigationBtnGroup.addButton(button)
                if index == 0:
                    self.sysEditNavigateGrid.addWidget(button, 3, index, 1, 3, QtCore.Qt.AlignHCenter)
                else:
                    self.sysEditNavigateGrid.addWidget(button, 4, index-1)

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
                        self.numericGrid.addWidget(button, 1, index-4, 2, 1)
                    else:
                        self.numericGrid.addWidget(button, 1, index-4)
                elif index in range(8, 11):
                    self.numericGrid.addWidget(button, 2, index-8)
                elif index in range(11, 15):
                    if index == 14:
                        self.numericGrid.addWidget(button, 3, index-11, 2, 1)
                    else:
                        self.numericGrid.addWidget(button, 3, index-11)
                elif index in range(15, 17):
                    if index == 15:
                        self.numericGrid.addWidget(button, 4, index-15, 1, 2, QtCore.Qt.AlignHCenter)
                    else:
                        self.numericGrid.addWidget(button, 4, 2)
        
    def keyboardEvent(self, event):
        print("xxxx")
        pyautogui.press(event)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # if not QDBusConnection.sessionBus().registerService("com.kdab.inputmethod"):
    key_board = Keyboard()
    # if not QDBusConnection.sessionBus().registerObject("/VirtualKeyboard", &keyboard, QDBusConnection::ExportAllSignals | QDBusConnection::ExportAllSlots)) {
        # qFatal("Unable to register object at DBus");
        # return 1;
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
