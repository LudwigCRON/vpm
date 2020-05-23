#!/usr/bin/env python3
# coding: utf-8

import vpm


def is_package_installed(p: vpm.Package, path: str = None):
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.name:
        return pkg >= p
    # check newer version of a package
    for dep in pkg.dependencies:
        if dep is not None and p.name == dep.name:
            return dep >= p
    return False


def is_package(p: vpm.Package, path: str = None, identical: bool = False):
    # create package file if none
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.name and identical:
        return pkg == p
    if p.name == pkg.name:
        return pkg >= p
