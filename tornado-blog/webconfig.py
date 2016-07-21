# -*- coding: utf-8 -*-
# name: guang
# email: av1254@qq.com

import ConfigParser
import os
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ConfPath = '%s/config/config.conf' % PATH


def getConfig(setction, key):
    config = ConfigParser.ConfigParser()
    config.read(ConfPath)
    return config.get(setction, key)
