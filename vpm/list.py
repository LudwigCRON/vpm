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
def list_installed():
    # create package file if none
    pkg = vpm.read_package()
    deps = pkg.get("dependencies", None)
    if deps is None:
        print("No dependencies installed")
        return
    for dep in deps:
        p = vpm._parse_pkgname(dep)
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
