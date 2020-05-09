#!/usr/bin/env python3
# coding: utf-8

import os
import sys

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm
import unittest


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.a = vpm.Version()
        self.b = vpm.Version(None)
        self.c = vpm.Version(1)
        self.d = vpm.Version(2.1)
        self.e = vpm.Version("1.0.0")
        self.f = vpm.Version("0. 9.9 ")
        self.g = vpm.Version("   1 .0.1")
        self.h = vpm.Version("0.9.8")
        self.i = vpm.Version("1.1.0")
        self.j = vpm.Version("1.A.7")
        self.k = vpm.Version("A. B .C")
        self.l = vpm.Version("     dev          ")
        self.m = vpm.Version(" ")
        self.n = vpm.Version("1.B.7")

    def test_definition(self):
        assert self.a.value is None
        assert not self.a.is_mmr()
        assert self.b.value is None
        assert not self.b.is_mmr()
        assert self.c.value == 1
        assert self.c.major == 1 and self.c.minor == 0 and self.c.release == 0
        assert self.c.is_mmr()
        assert self.d.value == 2.1
        assert self.d.major == 2 and self.d.minor == 100 and self.d.release == 0
        assert self.d.is_mmr()
        assert self.e.value == "1.0.0"
        assert self.e.major == 1 and self.e.minor == 0 and self.e.release == 0
        assert self.e.is_mmr()
        assert self.f.value == "0.9.9"
        assert self.f.major == 0 and self.f.minor == 9 and self.f.release == 9
        assert self.f.is_mmr()
        assert self.g.value == "1.0.1"
        assert self.g.major == 1 and self.g.minor == 0 and self.g.release == 1
        assert self.g.is_mmr()
        assert self.h.value == "0.9.8"
        assert self.h.major == 0 and self.h.minor == 9 and self.h.release == 8
        assert self.h.is_mmr()
        assert self.i.value == "1.1.0"
        assert self.i.major == 1 and self.i.minor == 1 and self.i.release == 0
        assert self.i.is_mmr()
        assert self.j.value == "1.A.7"
        assert self.j.major == 1 and self.j.minor == "A" and self.j.release == 7
        assert self.j.is_mmr()
        assert self.k.value == "A.B.C"
        assert self.k.major == "A" and self.k.minor == "B" and self.k.release == "C"
        assert self.k.is_mmr()
        assert self.l.value == "dev"
        assert self.l.major is None and self.l.minor is None and self.l.release is None
        assert not self.l.is_mmr()
        assert self.m.value == ""
        assert self.m.major is None and self.m.minor is None and self.m.release is None
        assert not self.m.is_mmr()
        assert self.n.value == "1.B.7"
        assert self.n.major == 1 and self.n.minor == "B" and self.n.release == 7
        assert self.n.is_mmr()

    def test_comparison(self):
        assert self.a == self.b
        assert self.a != self.m
        assert self.c >= self.d
        assert not self.c > self.b
        assert not self.b > self.c
        assert not self.c == self.b
        assert self.f < self.e
        assert self.e != self.g
        assert self.i >= self.g
        assert self.j < self.n
        assert self.m > self.d
        assert self.m >= self.j
        assert not self.m < self.n
        assert not self.m <= self.b

    def test_pkg_comparison(self):
        pkg_A = vpm.Package("youpi", "0.0.1")
        pkg_B = vpm.Package("tada", "0.0.1")
        pkg_C = vpm.Package("youpi ", "0.0.2")
        assert pkg_A.name == "youpi"
        assert pkg_B.name == "tada"
        assert pkg_C.name == "youpi"
        assert pkg_A.version == pkg_B.version
        assert pkg_A < pkg_C
        assert pkg_C > pkg_A
        assert pkg_B != pkg_A
        assert pkg_C != pkg_B


if __name__ == "__main__":
    unittest.main()
