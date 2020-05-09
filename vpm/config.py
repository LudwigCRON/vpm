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
    with open(DEFAULT_CONFIG, "r+") as fp:
        config.read_file(fp)
    config.read([filepath])
    return config


def find_config():
    # find a vpm.config file in the current directory tree
    cfgs = Path(os.getcwd()).glob("**/vpm.config")
    for cfg in cfgs:
        if cfg.is_file():
            return read_config(str(cfg))


def config_interp(cfg, section, key):
    value = cfg[section].get(key)
    matches = re.findall(r"\${([\w\_\-\. ]+)}", value)
    for m in matches:
        value = value.replace("${%s}" % m, os.getenv(m, ""))
    return value
