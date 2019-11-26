#!/usr/bin/env python3
# coding: utf-8

import vpm


def is_newer(pkga, pkgb):
    return vpm.version_to_num(pkga.version) > vpm.version_to_num(pkgb.version)


def is_newer_or_identical(pkga, pkgb):
    return vpm.version_to_num(pkga.version) >= vpm.version_to_num(pkgb.version)

def is_package_installed(p, path=None):
    pkg = vpm.read_package(path)
    # check name
    if p.name == pkg.get('name'):
        return is_newer_or_identical(
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
        return is_newer_or_identical(
            vpm.Package(pkg.get('name'),'', pkg.get('version')),
            p
        )
