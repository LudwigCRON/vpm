#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
import yaml
import argparse

from shutil import copyfile
from collections import namedtuple

Package = namedtuple('Package', ['name', 'operator', 'version'])

DEFAULT_PKG = "package.yml"

def _parse_pkgname(name: str):
    if not isinstance(name, str):
        return None
    # assume <name><operator><version>
    RE_PKG_NAME_VERSION = r"([\w\_\-]+)\s*(>|>=|=|<|<=)?\s*([\w\d\.\-]*)?$"
    m = re.findall(RE_PKG_NAME_VERSION, name, flags=re.MULTILINE)
    return Package(*m[0])


def _version_(version: str):
    if not '.' in version:
        return 999999
    return sum([int(s, 10)*10**(3*k) for k, s in enumerate(version.split('.'))])


def is_newer(pkga, pkgb):
    return _version_(pkga.version) >= _version_(pkgb.version)


def list_installed():
    # create package file if none
    pkg_file = _create_req_file()
    # check in the package file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    deps = pkg.get("dependencies", None)
    if deps is None:
        print("No dependencies installed")
        return
    for dep in deps:
        p = _parse_pkgname(dep)
        if p:
            print("%s %s %s" % (p.name, p.operator, p.version))


def list_outdated():
    pass


def list_available():
    pass


def list_corrupted():
    pass


def list_sources():
    CURRENT_DIR = os.getcwd()
    CURRENT_FILE = os.path.join(CURRENT_DIR, "sources.list")
    if not os.path.exists(CURRENT_FILE):
        CURRENT_DIR = os.path.dirname(__file__)
        CURRENT_FILE = os.path.join(CURRENT_DIR, "sources.list")
    srcs_path = [os.getcwd()]
    with open(CURRENT_FILE, "r+") as fp:
        for line in fp:
            l = line.strip()
            if l[0] == '.':
                srcs_path.append(
                    os.path.abspath(os.path.join(CURRENT_DIR, l))
                )
            else:
                srcs_path.append(l)
    return srcs_path


def is_package_installed(p, path=None):
    # create package file if none
    pkg_file = _create_req_file() if path is None else path
    if os.path.isdir(pkg_file):
        pkg_file = os.path.join(pkg_file, DEFAULT_PKG)
    # check in the package file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # check name
    if p.name == pkg.get('name'):
        return is_newer(Package(pkg.get('name'),'', pkg.get('version')), p)
    # empty list or list of dependencies
    lst = pkg.get("dependencies")
    if lst is None:
        lst = []
    # check newer version of a package
    deps = [_parse_pkgname(dep) for dep in lst if not dep is None]
    for dep in deps:
        if not dep is None and p.name == dep.name:
            return is_newer(dep, p)
    return False


def is_package(p, path=None):
    # create package file if none
    pkg_file = _create_req_file() if path is None else path
    if os.path.isdir(pkg_file):
        pkg_file = os.path.join(pkg_file, DEFAULT_PKG)
    # check in the package file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # check name
    if p.name == pkg.get('name'):
        return is_newer(Package(pkg.get('name'),'', pkg.get('version')), p)


def unify_package(deps):
    ans, done = [], []
    names = list(set([_parse_pkgname(dep).name for dep in deps if dep is not None]))
    for name in names:
        p = [_parse_pkgname(dep) for dep in deps if dep is not None and _parse_pkgname(dep).name == name]
        # duplicates detected
        v = max(p)
        if v.operator:
            ans.append("%s %s %s" % (v.name, v.operator, v.version))
        else:
            ans.append(v.name)
    return ans


def register_package(p):
    # create package file if none
    pkg_file = _create_req_file()
    # add pkg in file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # add dependencies
    deps = pkg.get("dependencies")
    if deps is None:
        deps = []
    if p.operator.strip():
        deps.append("%s %s %s" % (p.name, p.operator, p.version))
    else:
        deps.append(p.name)
    # filter the dependencies
    pkg["dependencies"] = unify_package(deps)
    with open(pkg_file, "w+") as fp:
        yaml.dump(pkg, fp)


def install_package(name: str):
    if not isinstance(name, str):
        print("verify the typed package name")
        return
    pkg = _parse_pkgname(name)
    # check not already installed
    if is_package_installed(pkg):
        print("package already satisfied")
        return
    # find the source
    src = [s for s in list_sources() if is_package(pkg, path=s)]
    if not src:
        print(name+" is not found")
        return
    # check dependencies
    check_dependencies(src[0])
    # download sources
    pkg = dispath_files(src[0])
    # register in the package.yml
    register_package(pkg)


def dispath_files(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the package file
    if os.path.isdir(path):
        pkg_file = os.path.join(path, DEFAULT_PKG)
    else:
        pkg_file = path
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    # dispath files
    # dispath constraints files
    # dispath models
    # dispath assertions
    for items in ["designs", "constraints", "assertions", "models"]:
        if pkg.get(items):
            DEST_DIR = os.path.join(os.getcwd(), "design/"+pkg.get("name"))
            os.makedirs(DEST_DIR)
            for file in pkg.get(items):
                copyfile(
                    os.path.join(os.path.dirname(pkg_file), file),
                    os.path.join(DEST_DIR, file)
                )
    return Package(pkg.get("name"), '=', pkg.get("version"))


def check_dependencies(path=None):
    if path is None or not os.path.exists(path):
        return
    # read the package file
    if os.path.isdir(path):
        pkg_file = os.path.join(path, DEFAULT_PKG)
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


def cli_args():
    # available actions
    mangle_args = {
        "install": "install a package from its name and version",
        "update": "update a package from its name",
        "list": "list all packages available or installed",
        "remove": "remove a package"
    }
    # make sys args available
    arguments = ['--'+a if a in mangle_args.keys() else a for a in sys.argv[1:]]
    parser = argparse.ArgumentParser()
    for a in mangle_args.keys():
        parser.add_argument(
            '-'+a[0],
            '--'+a,
            help=mangle_args[a],
            default=None,
            type=str)
    # return the parsed actions
    return (parser, parser.parse_args(arguments))


def _create_req_file():
    CURRENT_FILE = os.path.join(os.getcwd(), DEFAULT_PKG)
    if not os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, "w+") as fp:
            fp.write('name: "basic package"\n')
            fp.write('version: "0.0.1"\n')
            fp.write('# description of the package\n')
            fp.write('description: ""\n')
            fp.write('# list of files for the design\n')
            fp.write('designs:\n')
            fp.write('# list of files for the constraints\n')
            fp.write('constraints:\n')
            fp.write('# files only needed for simulations\n')
            fp.write('models:\n')
            fp.write('# formal verification files\n')
            fp.write('assertions:\n')
            fp.write('libraries:\n')
            fp.write('# list of package names\n')
            fp.write('dependencies:\n')
    return CURRENT_FILE


if __name__ == "__main__":
    parser, args = cli_args()
    if not args.install is None:
        install_package(args.install.lower())
    elif not args.update is None:
        pass
    elif not args.list is None:
        if args.list.lower() == "installed":
            list_installed()
        elif args.list.lower() == "outdated":
            list_outdated()
        elif args.list.lower() == "available":
            list_available()
        elif args.list.lower() == "corrupted":
            list_corrupted()
        else:
            print("unknown option")
    elif not args.remove is None:
        pass
    else:
        print("unknown actions")
        parser.print_help()
        exit(1)
    exit(0)