#!/usr/bin/env python3
# coding: utf-8

import os
import vpm

from shutil import copyfile


PACKAGE_DIRS = {
    "assertions": "MODELS_DIR",
    "constraints": "CONSTRAINTS_DIR",
    "designs": "DESIGNS_DIR",
    "documents": "DOCUMENTATION_DIR",
    "library": "LIBRARY_DIR",
    "models": "MODELS_DIR",
    "testcases": "TESTCASES_DIR",
}


def register_package(p: vpm.Package):
    pkg = vpm.read_package()
    # add dependencies
    pkg.dependencies.append(p)
    # clean deps
    pkg.uniquify_dependencies()
    # update the db
    vpm.write_package(pkg)


def unregister_package(p):
    pkg = vpm.read_package()
    # remove the package p from pkg
    pkg.dependencies = [dep for dep in pkg.dependencies if not dep.name == p.name]
    # clean deps
    pkg.uniquify_dependencies()
    # update the db
    vpm.write_package(pkg)


def retrieve_files(pkg_name: str = None):
    # read the config
    cfg = vpm.find_config()
    # read the package
    pkg = vpm.Package(pkg_name)
    # find files
    for attr in vpm.Package.__slots__:
        if attr not in PACKAGE_DIRS:
            continue
        cfg_dir = vpm.config_interp(cfg, "default", PACKAGE_DIRS[attr])
        DEST_DIR = os.path.join(os.getcwd(), cfg_dir, pkg_name)
        if os.path.exists(DEST_DIR):
            setattr(pkg, attr, [os.path.join(DEST_DIR, f) for f in os.listdir(DEST_DIR)])
    # return the version of the package installed
    return pkg


def dispatch_files(path: str = None):
    if path is None or (not vpm.is_git_path(path) and not os.path.exists(path)):
        return None
    # read the config
    cfg = vpm.find_config()
    # read the package file
    pkg = vpm.read_package(path)
    # dispath files
    for attr in vpm.Package.__slots__:
        items = getattr(pkg, attr)
        if items and attr in PACKAGE_DIRS:
            cfg_dir = vpm.config_interp(cfg, "default", PACKAGE_DIRS[attr])
            DEST_DIR = os.path.join(os.getcwd(), cfg_dir, pkg.name)
            os.makedirs(DEST_DIR, exist_ok=True)
            for file in items:
                copyfile(
                    file,
                    os.path.join(DEST_DIR, os.path.basename(file))
                )
    # return the version of the package installed
    return pkg


def remove_files(path: str = None):
    if path is None or (not vpm.is_git_path(path) and not os.path.exists(path)):
        return None
    # read the config
    cfg = vpm.find_config()
    # read the package file
    pkg = vpm.read_package(path)
    # dispath files
    for attr in vpm.Package.__slots__:
        items = getattr(pkg, attr)
        if items and attr in PACKAGE_DIRS:
            cfg_dir = vpm.config_interp(cfg, "default", PACKAGE_DIRS[attr])
            DEST_DIR = os.path.join(os.getcwd(), cfg_dir, pkg.name)
            # remove all files
            for file in items:
                file_path = os.path.join(DEST_DIR, os.path.basename(file))
                if os.path.exists(file_path):
                    os.remove(file_path)
            # once files removed, remove the folder
            if os.path.exists(DEST_DIR):
                os.rmdir(DEST_DIR)
    # return the version of the package installed
    return pkg


def check_dependencies(path: str = None, force: bool = False):
    if path is None or (not vpm.is_git_path(path) and not os.path.exists(path)):
        return None
    # read the package file
    pkg_file = os.path.join(path, vpm.DEFAULT_PKG) if os.path.isdir(path) else path
    pkg = vpm.read_package(pkg_file)
    # read dependencies
    for dep in pkg.dependencies:
        install_package(str(dep), force)


def install_package(name: str, force: bool = False):
    if not isinstance(name, str):
        print("verify the typed package name")
        return None
    pkg = vpm.Package.parse_package_name(name)
    # check not already installed
    if not force and vpm.is_package_installed(pkg):
        print("package %s already satisfied" % name)
        return None
    # find the source
    src = [s for s in vpm.list_sources(no_print=True) if vpm.is_package(pkg, path=s)]
    if not src:
        print("%s is not found" % name)
        return None
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
        return None
    pkg = vpm.Package.parse_package_name(name)
    # find the source
    srcs = [s for s in vpm.list_sources(no_print=True) if vpm.is_package(pkg, path=s)]
    if not srcs:
        print("%s is not found" % name)
        return None
    # remove each files
    for src in srcs:
        remove_files(src)
    # unregister in the package.yml
    unregister_package(pkg)
