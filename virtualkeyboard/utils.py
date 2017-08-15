# -*- coding:utf-8 -*-
import os
import json
import functools
import configparser
import subprocess

from PyQt5 import QtCore
from PyQt5 import QtGui

_touchpanelconfigpath = os.path.abspath('ini/touchpanel.json')
_res_path = os.path.abspath('res')


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


# 自动编译加载资源
RCC = """<RCC><qresource prefix="{}">\n{}</qresource></RCC>"""
FILE = """  <file mtime="{}">{}</file>\n"""


def _loadRes(res, root):
    # _logger.debug("_loadRes: {}".format(res))
    # res文件夹的路径
    package = os.path.dirname(res)
    print("package=", package)
    # 生成资源清单数据
    res_files = []
    for a, _, files in os.walk(res):
        for f in files:
            if f == "res.qrc" or f.endswith(".ts"):
                continue
            ff = os.path.join(a, f)
            res_files.append((os.path.getmtime(ff), os.path.relpath(
                ff, res).replace(os.path.sep, "/")))

    res_qrc_data = RCC.format(
        os.path.relpath(package, root).replace(os.path.sep, "/"),
        "".join([FILE.format(*x) for x in res_files]))

    # 更新资源清单
    res_qrc = os.path.join(res, "res.qrc")
    print("res_qrc=", res_qrc)
    res_updated = False

    # 检查现有资源清单是否已是最新
    if os.path.exists(res_qrc):
        with open(res_qrc, "r", encoding="utf-8") as f:
            res_updated = f.read() == res_qrc_data

    # 更新资源清单
    if not res_updated:
        with open(res_qrc, "w", encoding="utf-8") as f:
            f.write(res_qrc_data)

    # 编译资源清单
    res_rc_py = os.path.join(package, "res_rc.py")
    if not os.path.exists(res_rc_py) or \
            os.path.getmtime(res_rc_py) < os.path.getmtime(res_qrc):
        # _logger.info("compile resource: {}".format(res))
        # 通过指定 `cwd` 解决 win32 下 pyrcc5 不支持中文路径的问题
        rel_res_rc_py = os.path.relpath(res_rc_py, package)
        print("rel_res_rc_py=", rel_res_rc_py)
        
        rel_res_qrc = os.path.relpath(res_qrc, package)
        print("rel_res_qrc=", rel_res_qrc)
        
        subprocess.check_call(
            ["pyrcc5", "-o", rel_res_rc_py, rel_res_qrc], cwd=package)


# 加载资源
# for path, b, c in os.walk(_res_path):
#     if path.endswith(os.path.sep + "res"):
#         print("path=", _res_path)
#         _loadRes(path, _res_path)

# 加载翻译
# _translator_base = QtCore.QTranslator()
# _translator_base.load(QtCore.QLocale(), "", "", ":/basic/translations")
# QtWidgets.qApp.installTranslator(_translator_base)



