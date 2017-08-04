# -*- coding:utf-8 -*-
import os
import json
import functools
import configparser
from PyQt5 import QtCore
from PyQt5 import QtGui

_touchpanelconfigpath = os.path.abspath('ini/touchpanel.json')


# 加载ini配置文件
def loadConfig(config_path):
    cf = configparser.ConfigParser()
    cf.optionxform = str
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cf.read_file(f)
            return cf
    except Exception as e:
        print(e)
        print("load {} failed.".format(config_path))
        return None


# 加载json配置文件
def loadJson():
    try:
        with open(_touchpanelconfigpath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None


# @functools.lru_cache(maxsize=None)
def _readRes(path):
    f = QtCore.QFile(path)
    f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    ts = QtCore.QTextStream(f)
    ts.setCodec("utf-8")
    return ts.readAll()


def loadApplicationStyleSheet(app):
    """加载应用程序样式表"""
    qss_text = _readRes(os.path.abspath("style/default/main.qss"))
    app.setStyleSheet(qss_text)


def _eval(script):
    value = _builtin_eval(_compile_eval(script), _basic_dict, {})
    return value


def _exec(script):
    # _DEBUG("exec {!r}".format(script))
    _builtin_exec(_compile_exec(script), _basic_dict, {})


def _delayExec(script):
    QtCore.QTimer.singleShot(0, functools.partial(_exec, script))
