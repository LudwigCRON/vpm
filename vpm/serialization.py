#!/usr/bin/env python3
# coding: utf-8

import os
import vpm
import yaml


DEFAULT_PKG = "package.yml"


def read_package(path: str = None):
    # create package file if none
    pkg_file = get_package_path(path)
    # check in the package file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # adjust file path
    for attr in vpm.Package.__slots__:
        if attr in ["name", "version", "description", "dependencies"]:
            continue
        files = pkg.get(attr, [])
        if files:
            pkg[attr] = [
                os.path.abspath(
                    os.path.join(os.path.dirname(pkg_file), file)
                ) for file in files]
    return vpm.Package.from_dict(pkg)


def write_package(pkg, path: str = None):
    # create package file if none
    pkg_file = get_package_path(path)
    with open(pkg_file, "w+") as fp:
        yaml.dump(pkg.to_dict(), fp)


def get_package_path(path: str = None):
    pkg_file = vpm.default_package() if path is None else path
    if os.path.isdir(pkg_file):
        pkg_file = os.path.join(pkg_file, DEFAULT_PKG)
    return pkg_file
