#!/usr/bin/env python3
# coding: utf-8

import os
import vpm

from shutil import copyfile

PACKAGE_FIELDS = ["designs", "constraints", "assertions", "models", "library", "testcases"]
PACKAGE_DIRS = {
    "assertions" : "MODELS_DIR",
    "constraints": "CONSTRAINTS_DIR",
    "designs": "DESIGNS_DIR",
    "documents": "DOCUMENTATION_DIR",
    "library": "LIBRARY_DIR",
    "models": "MODELS_DIR",
    "testcases": "TESTCASES_DIR",
}

def unify_package(deps):
    ans, done = [], []
    names = list(set([vpm.parse_pkgname(dep).name for dep in deps if dep is not None]))
    for name in names:
        p = [vpm.parse_pkgname(dep) for dep in deps if dep is not None and vpm.parse_pkgname(dep).name == name]
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
    deps = pkg.get("dependencies")
    if deps is None:
        deps = []
    new_deps = [dep for dep in deps if not vpm.parse_pkgname(dep).name == p.name]
    pkg["dependencies"] = unify_package(new_deps)
    # update the db
    vpm.write_package(pkg)


def dispatch_files(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the config
    cfg = vpm.find_config()
    # read the package file
    pkg = vpm.read_package(path)
    # dispath files
    for items in PACKAGE_FIELDS:
        if pkg.get(items):
            cfg_dir = vpm.config_interp(cfg, "default", PACKAGE_DIRS[items])
            DEST_DIR = os.path.join(os.getcwd(), cfg_dir, pkg.get("name"))
            os.makedirs(DEST_DIR, exist_ok=True)
            for file in pkg.get(items):
                copyfile(
                    os.path.join(path, file),
                    os.path.join(DEST_DIR, file)
                )
    # return the version of the package installed
    return vpm.Package(pkg.get("name"), '=', pkg.get("version"))


def remove_files(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the config
    cfg = vpm.find_config()
    # read the package file
    pkg = vpm.read_package(path)
    # dispath files
    for items in PACKAGE_FIELDS:
        if pkg.get(items):
            cfg_dir = vpm.config_interp(cfg, "default", PACKAGE_DIRS[items])
            DEST_DIR = os.path.join(os.getcwd(), cfg_dir, pkg.get("name"))
            for file in pkg.get(items):
                if os.path.exists(os.path.join(DEST_DIR, file)):
                    os.remove(os.path.join(DEST_DIR, file))
            if os.path.exists(DEST_DIR):
                os.rmdir(DEST_DIR)
    # return the version of the package installed
    return vpm.Package(pkg.get("name"), '=', pkg.get("version"))


def check_dependencies(path=None, force: bool = False):
    if path is None or not os.path.exists(path):
        return
    # read the package file
    if os.path.isdir(path):
        pkg_file = os.path.join(path, vpm.DEFAULT_PKG)
    else:
        pkg_file = path
    pkg = vpm.read_package(pkg_file)
    # read dependencies
    deps = pkg.get("dependencies")
    if deps is None:
        deps = []
    for dep in deps:
        install_package(dep, force)


def install_package(name: str, force: bool = False):
    if not isinstance(name, str):
        print("verify the typed package name")
        return
    pkg = vpm.parse_pkgname(name)
    # check not already installed
    if not force and vpm.is_package_installed(pkg):
        print("package %s already satisfied" % name)
        return
    # find the source
    src = [s for s in vpm.list_sources(no_print=True) if vpm.is_package(pkg, path=s)]
    if not src:
        print(name+" is not found")
        return
    # check dependencies
    check_dependencies(src[0], force)
    # download sources
    pkg = dispatch_files(src[0])
    # register in the package.yml
    register_package(pkg)
    print("%s %s installed" % (pkg.name, pkg.version))


def remove_package(name: str):
    if not isinstance(name, str):
        print("verify the typed package name")
        return
    pkg = vpm.parse_pkgname(name)
    # find the source
    srcs = [s for s in vpm.list_sources(no_print=True) if vpm.is_package(pkg, path=s)]
    if not srcs:
        print(name+" is not found")
        return
    # remove each files
    for src in srcs:
        remove_files(src)
    # unregister in the package.yml
    unregister_package(pkg)
