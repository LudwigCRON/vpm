#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import shutil
import unittest

from pathlib import Path

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm


def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        if a in order and b not in order:
            return -1
        elif a not in order and b in order:
            return 1
        elif a not in order and b not in order:
            return 0
        return -1 if order[a] < order[b] else 1

    return ordered, compare


ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare


class DefaultTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.dirname(os.path.abspath(__file__))
        # remove directory
        if os.path.exists(os.path.join(cls.tests_dir, "empty_platform/package.yml")):
            os.remove(os.path.join(cls.tests_dir, "empty_platform/package.yml"))
            shutil.rmtree(os.path.join(cls.tests_dir, "empty_platform/design"),
                          ignore_errors=True)

    @staticmethod
    def exact_list(lista: list, refs: list):
        assert len(lista) == len(refs)
        for file in lista:
            assert file in refs

    @staticmethod
    def exact_filelist(lista: list, refs: list, base: str):
        a = [str(f) for f in lista]
        b = [os.path.normpath(os.path.join(base, f)) for f in refs]
        DefaultTests.exact_list(a, b)

    def setUp(self):
        sys.stdout, sys.stderr = None, None

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    @ordered
    def test_install(self):
        # move into empty_platform
        os.chdir("%s/empty_platform" % self.tests_dir)
        vpm.default_package()
        # list files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml"
        ], os.getcwd())
        # install resync
        vpm.install_package("resync")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v"
        ], os.getcwd())
        # install sar (does not exist)
        vpm.install_package("sar")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v"
        ], os.getcwd())
        # install adc_sar
        vpm.install_package("adc_sar")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())
        # check fail is not a string
        vpm.install_package(None)
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())
        # check already installed
        vpm.install_package("resync")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())

    @ordered
    def test_remove(self):
        # move into empty_platform
        os.chdir("%s/empty_platform" % self.tests_dir)
        # list files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())
        # remove sar (not existing)
        vpm.remove_package("sar")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())
        # check fail is not a string
        vpm.remove_package(None)
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())
        # remove adc_sar
        vpm.remove_package("adc_sar")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v"
        ], os.getcwd())
        # remove resync
        vpm.remove_package("resync")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml"
        ], os.getcwd())

    @ordered
    def test_install_with_deps(self):
        # move into empty_platform
        os.chdir("%s/empty_platform" % self.tests_dir)
        # list files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml"
        ], os.getcwd())
        # install adc_sar + resync
        vpm.install_package("adc_sar")
        # check files
        files = list(Path(os.getcwd()).rglob("*.*"))
        DefaultTests.exact_filelist(files, [
            "./vpm.config",
            "./package.yml",
            "./design/resync/edge_resync.v",
            "./design/adc_sar/core.v",
            "./design/adc_sar/ports.v"
        ], os.getcwd())

    @ordered
    def test_installed(self):
        # move into empty_platform
        os.chdir("%s/empty_platform" % self.tests_dir)
        # just check there is a package called * do not care of the version so add -1
        assert not vpm.is_package_installed(vpm.Package.parse_package_name("sar -1"))
        assert vpm.is_package_installed(vpm.Package.parse_package_name("basic_package -1"))
        assert vpm.is_package_installed(vpm.Package.parse_package_name("resync -1"))
        assert vpm.is_package_installed(vpm.Package.parse_package_name("adc_sar -1"))

    @ordered
    def test_update(self):
        # move into outdated
        os.chdir("%s/outdated" % self.tests_dir)
        # installed outdated version
        pkg01 = vpm.Package.parse_package_name("resync 0.0.1")
        assert vpm.is_package_installed(pkg01)
        # latest version
        pkg02 = vpm.Package.parse_package_name("resync 0.0.2")
        assert not vpm.is_package_installed(pkg02)
        assert not vpm.is_package_installed(vpm.Package.parse_package_name("resync"))
        vpm.install_package("resync")
        assert vpm.is_package_installed(pkg02)
        # still make it outdated
        with open("./package.yml", "r") as fp:
            data = fp.readlines()
        with open("./package.yml", "w+") as fp:
            for line in data:
                if "resync" in line:
                    fp.write("- resync 0.0.1\n")
                else:
                    fp.write(line)
