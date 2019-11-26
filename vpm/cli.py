#!/usr/bin/env python3
# coding: utf-8

import os
import re
import sys
import vpm
import yaml
import argparse

from collections import namedtuple

Package = namedtuple('Package', ['name', 'operator', 'version'])

DEFAULT_PKG = "package.yml"


def read_package(path: str = None):
    # create package file if none
    pkg_file = get_package_path(path)
    # check in the package file
    with open(pkg_file, "r+") as fp:
        pkg = yaml.load(fp, Loader=yaml.FullLoader)
    return pkg


def write_package(pkg, path: str = None):
    # create package file if none
    pkg_file = get_package_path(path)
    with open(pkg_file, "w+") as fp:
        yaml.dump(pkg, fp)


def get_package_path(path: str = None):
    pkg_file = _create_req_file() if path is None else path
    if os.path.isdir(pkg_file):
        pkg_file = os.path.join(pkg_file, DEFAULT_PKG)
    return pkg_file


def parse_pkgname(name: str):
    if not isinstance(name, str):
        return None
    # assume <name><operator><version>
    RE_PKG_NAME_VERSION = r"([\w\_\-]+)\s*(>|>=|=|<|<=)?\s*([\w\d\.\-]*)?$"
    m = re.findall(RE_PKG_NAME_VERSION, name, flags=re.MULTILINE)
    return Package(*m[0])


def version_to_num(version: str):
    if not '.' in version:
        return 999999
    return sum([int(s, 10)*10**(3*k) for k, s in enumerate(version.split('.'))])


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


def cli_main():
    parser, args = cli_args()
    if not args.install is None:
        vpm.install_package(args.install.lower())
    elif not args.update is None:
        pass
    elif not args.list is None:
        if args.list.lower() == "installed":
            vpm.list_installed()
        elif args.list.lower() == "outdated":
            vpm.list_outdated()
        elif args.list.lower() == "available":
            vpm.list_available()
        elif args.list.lower() == "corrupted":
            vpm.list_corrupted()
        else:
            print("unknown option")
    elif not args.remove is None:
        pass
    else:
        print("unknown actions")
        parser.print_help()
        exit(1)
    exit(0)


if __name__ == "__main__":
    cli_main()
