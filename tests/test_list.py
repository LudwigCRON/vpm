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

    def setUp(self):
        sys.stdout, sys.stderr = None, None

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_sources(self):
        # move into platform
        # have resync + sar + itself
        os.chdir("%s/platform" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=False))
        assert len(srcs) == 3
        # move into resync
        # no vpm.config => no sources of repo
        os.chdir("%s/resync" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=False))
        assert len(srcs) == 0
        # move into sar
        # have resync + itself
        os.chdir("%s/sar" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=False))
        assert len(srcs) == 2
        # move into pkg_wo_repositories
        # check at least have itself
        os.chdir("%s/pkg_wo_repositories" % self.tests_dir)
        srcs = list(vpm.list_sources(no_print=False))
        assert len(srcs) == 1
        assert srcs[0] == "./"

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
        pkgs = list(vpm.list_installed(no_print=False))
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
        pkgs = list(vpm.list_available(no_print=False))
        assert len(pkgs) == 2

    def test_outdated(self):
        # move in platform
        os.chdir("%s/platform" % self.tests_dir)
        pkgs = list(vpm.list_outdated(no_print=True))
        assert len(pkgs) == 0
        # move in sar
        os.chdir("%s/sar" % self.tests_dir)
        pkgs = list(vpm.list_outdated(no_print=True))
        assert len(pkgs) == 0
        # move in outdated
        os.chdir("%s/outdated" % self.tests_dir)
        pkgs = list(vpm.list_outdated(no_print=True))
        assert len(pkgs) == 1
        assert pkgs[0].name == "resync"

    def test_corrupted(self):
        # move in platform
        os.chdir("%s/platform" % self.tests_dir)
        pkgs = list(vpm.list_corrupted(no_print=True))
        assert len(pkgs) == 1
        assert "core.v" in pkgs[0]["designs"]
        assert "port.v" not in pkgs[0]["designs"]
        # move in sar
        os.chdir("%s/sar" % self.tests_dir)
        pkgs = list(vpm.list_corrupted(no_print=True))
        assert len(pkgs) == 1
        assert "core.v" not in pkgs[0]["designs"]
        assert "port.v" not in pkgs[0]["designs"]
        assert "edge_resync.v" in pkgs[0]["designs"]
        # move in outdated
        os.chdir("%s/outdated" % self.tests_dir)
        pkgs = list(vpm.list_corrupted(no_print=True))
        assert len(pkgs) == 0
        # move in new_files_in_ip
        os.chdir("%s/new_files_in_ip" % self.tests_dir)
        pkgs = list(vpm.list_corrupted(no_print=False))
        assert len(pkgs) == 1
        assert "toggle_resync.v" in pkgs[0]["designs"]["new"]
        # move in rem_files_in_ip
        os.chdir("%s/rem_files_in_ip" % self.tests_dir)
        pkgs = list(vpm.list_corrupted(no_print=True))
        assert len(pkgs) == 1
        assert "toggle_resync.v" in pkgs[0]["designs"]["new"]
        assert "edge_resync.v" in pkgs[0]["designs"]["removed"]
