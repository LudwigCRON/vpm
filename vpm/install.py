#!/usr/bin/env python3
# coding: utf-8

import os
import vpm

from shutil import copyfile


def unify_package(deps):
    ans, done = [], []
    names = list(set([vpm._parse_pkgname(dep).name for dep in deps if dep is not None]))
    for name in names:
        p = [vpm._parse_pkgname(dep) for dep in deps if dep is not None and _parse_pkgname(dep).name == name]
        # duplicates detected
        v = max(p)
        if v.operator:
            ans.append(
                "%s %s %s" % (v.name, v.operator, v.version)
            )
        else:
            ans.append(v.name)
    return ans


def register_package(p):
    pkg = vpm.read_package()
    # add dependencies
    deps = pkg.get("dependencies")
    if deps is None:
        deps = []
    if p.operator.strip():
        deps.append(
            "%s %s %s" % (p.name, p.operator, p.version)
        )
    else:
        deps.append(p.name)
    # filter the dependencies
    pkg["dependencies"] = unify_package(deps)
    vpm.write_package(pkg)


def unregister_package(p):
    pkg = vpm.read_package()
    # remove the package p from pkg
    
    # update the db
    vpm.write_package(pkg)

def dispatch_files(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the package file
    pkg = vpm.read_package(path)
    # dispath files
    for items in ["designs", "constraints", "assertions", "models"]:
        if pkg.get(items):
            DEST_DIR = os.path.join(os.getcwd(), "design/"+pkg.get("name"))
            os.makedirs(DEST_DIR)
            for file in pkg.get(items):
                copyfile(
                    os.path.join(os.path.dirname(pkg_file), file),
                    os.path.join(DEST_DIR, file)
                )
    # return the version of the package installed
    return vpm.Package(pkg.get("name"), '=', pkg.get("version"))


def check_dependencies(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the package file
    if os.path.isdir(path):
        pkg_file = os.path.join(path, vpm.DEFAULT_PKG)
    else:
        pkg_file = path
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # read dependencies
    deps = pkg.get("dependencies")
    if deps is None:
        deps = []
    for dep in deps:
        install_package(dep)


def install_package(name: str):
    if not isinstance(name, str):
        print("verify the typed package name")
        return
    pkg = vpm.parse_pkgname(name)
    # check not already installed
    if vpm.is_package_installed(pkg):
        print("package already satisfied")
        return
    # find the source
    src = [s for s in vpm.list_sources() if vpm.is_package(pkg, path=s)]
    if not src:
        print(name+" is not found")
        return
    # check dependencies
    check_dependencies(src[0])
    # download sources
    pkg = dispatch_files(src[0])
    # register in the package.yml
    register_package(pkg)

def remove_package(name: str):
    if not isinstance(name, str):
        print("verify the typed package name")
        return
    pkg = vpm.parse_pkgname(name)
    # find the source
    src = [s for s in vpm.list_sources() if vpm.is_package(pkg, path=s)]
    if not src:
        print(name+" is not found")
        return
    # remove each files
    # unregister in the package.yml
