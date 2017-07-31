# -*- coding:utf-8 -*-
import configparser


def loadConfig(config_path):
    cf = configparser.ConfigParser()
    cf.optionxform = str
    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
            cf.read_file(f)
            return cf
    except Exception as e:
        print("load {} failed.".format(config_path))
        return None
