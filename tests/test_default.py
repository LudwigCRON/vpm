#!/usr/bin/env python3
# coding: utf-8

import os
import sys

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm
import yaml
import unittest


class DefaultTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        sys.stdout, sys.stderr = None, None

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_package(self):
        pkg_file = os.path.join(self.tests_dir, "package.yml")
        vpm.default_package()
        assert os.path.exists(pkg_file)
        pkg = vpm.read_package(pkg_file)
        assert pkg.name == "basic_package"
        assert pkg.version == vpm.Version("0.0.1")
        os.remove(pkg_file)

    def test_config(self):
        config_file = os.path.join(self.tests_dir, "vpm.config")
        # create basic version
        vpm.default_config()
        assert os.path.exists(config_file)
        cfg = vpm.read_config(config_file)
        assert cfg.has_section("default")
        assert cfg.has_section("repositories")
        assert cfg["repositories"].get("sources") == "./"
        os.remove(config_file)
        # create complete version
        vpm.default_config(complete=True)
        assert os.path.exists(config_file)
        cfg = vpm.read_config(config_file)
        assert cfg.has_section("default")
        assert cfg["default"].get("MODELS_DIR") == "${PLATFORM}/model"
        assert cfg.has_section("repositories")
        assert cfg["repositories"].get("sources") == "./"
        # check already exists is not overwritten
        vpm.default_config()
        assert os.path.exists(config_file)
        cfg = vpm.read_config(config_file)
        assert cfg.has_section("default")
        assert cfg["default"].get("MODELS_DIR") == "${PLATFORM}/model"
        assert cfg.has_section("repositories")
        assert cfg["repositories"].get("sources") == "./"
        os.remove(config_file)
