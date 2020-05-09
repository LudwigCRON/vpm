#!/usr/bin/env python3
# coding: utf-8

import vpm

from collections import defaultdict


# ==== Dependancy  Resolution ====
class Node:
    __slots__ = ["name", "edges", "params"]

    def __init__(self, name):
        self.name = name
        self.edges = []
        self.params = defaultdict(list)

    def addEdge(self, node):
        self.edges.append(node)

    def describe(self):
        print(self.name + ': ')
        print(''.join(['-'] * (len(self.name) + 2)))
        for edge in self.edges:
            if "Sources.list" in edge.name:
                edge.describe()
            else:
                print("- %s" % edge.name)


def resolve_dependancies(node, resolved, unresolved) -> None:
    """
    Dependency resolution algorithms taken from
    https://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/
    Args:
        - node: Node of a graph (start with the top)
        - resolved: output of nodes needed in order
        - unresolved: for circular reference detection
    """
    unresolved.append(node)
    for edge in node.edges:
        if edge not in resolved:
            if edge in unresolved:
                raise Exception('Circular reference detected: %s -> %s' % (
                    node.name,
                    edge.name
                ))
            resolve_dependancies(edge, resolved, unresolved)
    resolved.append(node)
    unresolved.remove(node)


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
        p = vpm.parse_pkgname(dep)
        if not no_print:
            print(p)
        if p:
            yield p


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
        #for pkg in pkgs:
        #    print("avail.: %s\tinst: %s\toutdated: %s" % (str(pkg), str(dep), pkg > dep))
        if any(candidates):
            print("%s %s --> %s" % (dep.name, dep.version, max(candidates)))
            count += 1
            yield dep
    if count == 0:
        print("No outdated package found")
        return


def list_corrupted():
    pass
