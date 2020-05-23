#!/usr/bin/env python3
# coding: utf-8

import vpm


# list functions
def list_sources(no_print: bool = False):
    cfg = vpm.find_config()
    if not cfg:
        return []
    # expect sources of repositories
    if not cfg.has_section("repositories"):
        print("No repository's source defined")
        return []
    # return each sources
    srcs = cfg["repositories"].get("sources", "").split()
    for src in srcs:
        if not no_print:
            print(src)
        yield src


def list_installed(no_print: bool = False):
    # create package file if none
    pkg = vpm.read_package()
    if not pkg.dependencies:
        print("No dependencies installed")
        return []
    for dep in pkg.dependencies:
        if not no_print:
            print(dep)
        yield dep


def list_available(no_print: bool = False):
    for src in list_sources(no_print):
        pkg = vpm.read_package(src)
        if not no_print:
            print(pkg)
        yield pkg


def list_outdated(no_print: bool = False):
    # get list of available package
    pkgs = list(list_available(no_print=no_print))
    # compare the version
    count = 0
    for dep in list_installed(no_print=no_print):
        candidates = [pkg.version for pkg in pkgs if pkg > dep]
        # for debug print all checks
        # for pkg in pkgs:
        #     print("avail.: %s\tinst: %s\toutdated: %s" % (str(pkg), str(dep), pkg > dep))
        if any(candidates):
            print("%s %s --> %s" % (dep.name, dep.version, max(candidates)))
            count += 1
            yield dep
    if count == 0:
        print("No outdated package found")
        return


def list_corrupted(no_print: bool = False):
    # get list of available package
    pkgs = list(list_available(no_print=no_print))
    # compare packages
    for dep in list_installed(no_print=no_print):
        for candidate in [pkg for pkg in pkgs if pkg == dep]:
            # for debug
            # print("dep: %s\tcandidate: %s" % (dep, candidate))
            pkg_inst = vpm.retrieve_files(dep.name)
            pkg_inst.version = dep.version
            pkg_diff = vpm.Package.unified_diff(candidate, pkg_inst)
            yield pkg_diff
