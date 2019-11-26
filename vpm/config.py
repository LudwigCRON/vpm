#!/usr/bin/env python3
# coding: utf-8

import os
import vpm
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
