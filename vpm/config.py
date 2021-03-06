#!/usr/bin/env python3
# coding: utf-8

import re
import os
import configparser

from pathlib import Path

DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default.ini")


def read_config(filepath: str):
    # parse the file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read([DEFAULT_CONFIG, filepath])
    return config


def find_config():
    # find a vpm.config file in the current directory tree
    cfgs = Path(os.getcwd()).glob("**/vpm.config")
    for cfg in cfgs:
        os.environ["PLATFORM"] = os.path.dirname(str(cfg))
        return read_config(str(cfg))


def config_interp(cfg, section, key):
    value = cfg[section].get(key)
    matches = re.findall(r"\${([\w\_\-\. ]+)}", value)
    for m in matches:
        value = value.replace("${%s}" % m, os.getenv(m, ""))
    return value
