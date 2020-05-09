#!/usr/bin/env python3
# coding: utf-8

import os
import sys

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm
import unittest


class ListTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.dirname(os.path.abspath(__file__))

    def test_sources(self):
        # move into platform
        os.chdir("%s/platform" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=True))
        assert len(srcs) == 3
        # move into resync
        os.chdir("%s/resync" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=True))
        assert len(srcs) == 0
        # move into sar
        os.chdir("%s/sar" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=True))
        assert len(srcs) == 2

    def test_installed(self):
        # move into platform
        os.chdir("%s/platform" % self.tests_dir)
        pkgs = list(vpm.list_installed(no_print=True))
        assert len(pkgs) == 2
        assert pkgs[0].name == "adc_sar"
        assert pkgs[1].name == "resync"
        # move into resync
        os.chdir("%s/resync" % self.tests_dir)
        pkgs = list(vpm.list_installed(no_print=True))
        assert len(pkgs) == 0
        # move into sar
        os.chdir("%s/sar" % self.tests_dir)
        pkgs = list(vpm.list_installed(no_print=True))
        assert len(pkgs) == 1
        assert pkgs[0].name == "resync"

    def test_available(self):
        # move in platform
        os.chdir("%s/platform" % self.tests_dir)
        pkgs = list(vpm.list_available(no_print=True))
        assert len(pkgs) == 3
        assert pkgs[0].name == "my super project"
        assert pkgs[1].name == "resync"
        assert pkgs[2].name == "adc_sar"
        # move in resync
        os.chdir("%s/resync" % self.tests_dir)
        pkgs = list(vpm.list_available(no_print=True))
        assert len(pkgs) == 0
        # move in sar
        os.chdir("%s/sar" % self.tests_dir)
        pkgs = list(vpm.list_available(no_print=True))
        assert len(pkgs) == 2

    def test_outdated(self):
        # move in platform
        os.chdir("%s/platform" % self.tests_dir)
        pkgs = list(vpm.list_outdated(no_print=True))
        assert len(pkgs) == 1
        assert pkgs[0].name == "resync"
        # move in sar
        os.chdir("%s/sar" % self.tests_dir)
        pkgs = list(vpm.list_outdated(no_print=True))
        print(pkgs)
        assert len(pkgs) == 1

    def test_corrupted(self):
        self.skipTest("Not implemented yet")


if __name__ == "__main__":
    unittest.main()
