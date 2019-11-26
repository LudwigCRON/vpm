#!/usr/bin/env python3
# coding: utf-8

import os
import vpm

from collections import defaultdict

#== Dependancy  Resolution ==
class Node:
    __slots__ = ["name", "edges", "params"]

    def __init__(self, name):
        self.name = name
        self.edges = []
        self.params = defaultdict(list)

    def addEdge(self, node):
        self.edges.append(node)

    def describe(self):
        print(self.name+': ')
        print(''.join(['-']*(len(self.name)+2)))
        for edge in self.edges:
            if "Sources.list" in edge.name:
                edge.describe()
            else:
                print("- "+edge.name)

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
                raise Exception('Circular reference detected: %s -> %s' % (node.name, edge.name))
            resolve_dependancies(edge, resolved, unresolved)
    resolved.append(node)
    unresolved.remove(node)

# list functions
def list_installed(no_print: bool = False):
    # create package file if none
    pkg = vpm.read_package()
    deps = pkg.get("dependencies", None)
    if deps is None:
        print("No dependencies installed")
        return
    if no_print:
        return [vpm.parse_pkgname(dep) for dep in deps]
    for dep in deps:
        p = vpm.parse_pkgname(dep)
        if p:
            print("%s %s %s" % (p.name, p.operator, p.version))


def list_outdated():
    # get list of installed package
    deps = list_installed(no_print=True)
    # get list of available package
    pkgs = [vpm.Package(pkg.get("name"), '=', pkg.get("version")) for pkg in list_available(no_print=True)]
    # compare the version
    count = 0
    for dep in deps:
        candidates = [pkg.version for pkg in pkgs if vpm.is_newer(pkg, dep)]
        if any(candidates):
            print("%s %s --> %s" % (dep.name, dep.version, max(candidates)))
            count += 1
    if count == 0:
        print("No outdated package found")


def list_available(no_print: bool = False):
    cfg = vpm.find_config()
    if not cfg.has_section("repositories"):
        print("No repository's source defined")
        return
    srcs = cfg["repositories"].get("sources", "").split()
    if no_print:
        return [vpm.read_package(src) for src in srcs]
    for src in srcs:
        pkg = vpm.read_package(src)
        print("%s %s" % (pkg.get("name"), pkg.get("version")))


def list_corrupted():
    pass


def list_sources(no_print: bool = False):
    cfg = vpm.find_config()
    if not cfg.has_section("repositories"):
        print("No repository's source defined")
        return
    srcs = cfg["repositories"].get("sources", "").split()
    if no_print:
        return srcs
    for src in srcs:
        print(src)
