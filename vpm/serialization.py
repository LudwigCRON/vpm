#!/usr/bin/env python3
# coding: utf-8

import os
import vpm
import yaml


DEFAULT_PKG = "package.yml"


def read_package(path: str = None, content: str = None):
    if content is None:
        # check git package
        if vpm.is_git_path(path):
            return get_git_package(path)
        # create package file if none
        pkg_file = get_package_path(path)
        # check in the package file
        with open(pkg_file, "r+") as fp:
            pkg = yaml.load(fp, Loader=yaml.FullLoader)
    elif isinstance(content, dict):
        pkg_file = path
        pkg = content
    else:
        pkg_file = path
        pkg = yaml.load(content, Loader=yaml.FullLoader)
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


def get_git_package(path: str = None):
    match = vpm.is_git_path(path)
    if match:
        grps = [g for g in match.groups() if g]
        for pkg in vpm.github_read_packages(*grps):
            return pkg
    return None
