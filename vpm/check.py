#!/usr/bin/env python3
# coding: utf-8

import vpm


def is_newer(pkga, pkgb):
    return vpm._version_(pkga.version) >= vpm._version_(pkgb.version)


def is_package_installed(p, path=None):
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.get('name'):
        return is_newer(
            vpm.Package(pkg.get('name'),'', pkg.get('version')),
            p
        )
    # empty list or list of dependencies
    lst = pkg.get("dependencies", None)
    if lst is None:
        lst = []
    # check newer version of a package
    deps = [vpm._parse_pkgname(dep) for dep in lst if not dep is None]
    for dep in deps:
        if not dep is None and p.name == dep.name:
            return is_newer(dep, p)
    return False


def is_package(p, path=None):
    # create package file if none
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.get('name'):
        return is_newer(
            vpm.Package(pkg.get('name'),'', pkg.get('version')),
            p
        )
