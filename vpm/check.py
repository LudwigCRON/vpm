#!/usr/bin/env python3
# coding: utf-8

import vpm


def is_package_installed(p: vpm.Package, path: str = None):
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.name:
        return pkg >= p if p.version not in ('', None) else True
    # check newer version of a package
    # or same version is installed
    # if version is '' or None does not ensure latest but just have package name
    for dep in pkg.dependencies:
        if p.name == dep.name:
            return dep >= p
    return False


def is_package(p: vpm.Package, path: str = None, identical: bool = False):
    # create package file if none
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.name and identical:
        return pkg == p
    # if version is '' or None, the latest version match only the
    # the package name find in repository
    if p.name == pkg.name:
        return pkg >= p if p.version not in ('', None) else True
