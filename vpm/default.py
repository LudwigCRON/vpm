#!/usr/bin/env python3
# coding: utf-8

import os


def default_package():
    CURRENT_FILE = os.path.join(os.getcwd(), "package.yml")
    if not os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "w+") as fp:
            fp.write('name: "basic package"\n')
            fp.write('version: "0.0.1"\n')
            fp.write("# description of the package\n")
            fp.write('description: ""\n')
            fp.write("# list of files for the design\n")
            fp.write("designs:\n")
            fp.write("# list of files for the constraints\n")
            fp.write("constraints:\n")
            fp.write("# files only needed for simulations\n")
            fp.write("models:\n")
            fp.write("# formal verification files\n")
            fp.write("assertions:\n")
            fp.write("libraries:\n")
            fp.write("# list of package names\n")
            fp.write("dependencies:\n")
    return CURRENT_FILE


def default_config(complete: bool = False):
    CURRENT_FILE = os.path.join(os.getcwd(), "vpm.config")
    if not os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "w+") as fp:
            if complete:
                fp.write("[default]\n")
                fp.write("# default variables to dispatch files\n")
                fp.write("# during IP installations\n")
                fp.write("DESIGNS_DIR=${PLATFORM}/design\n")
                fp.write("MODELS_DIR=${PLATFORM}/model\n")
                fp.write("LIBRARY_DIR=${PLATFORM}/library\n")
                fp.write("TESTCASES_DIR=${PLATFORM}/testcases\n")
                fp.write("DOCUMENTATION_DIR=${PLATFORM}/documents\n")
                fp.write("CONSTRAINTS_DIR=${PLATFORM}/constraints\n")
            fp.write("[repositories]\n")
            fp.write("# at least have the current directory\n")
            fp.write("sources = ./\n")
    return CURRENT_FILE
