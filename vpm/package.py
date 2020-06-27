#!/usr/bin/env python3
# coding: utf-8


import os
import re
import difflib

from collections import defaultdict


class Version(object):
    """
    Version of a package could either be
    an integer, a float, a string of character, or None

    a version is formatted in major.minor.release format

    an integer is considered as being <integer>.0.0
    a float is considered as being <integer part>.<decimal part>.0
    a string respecting major.minor.release is parsed

    Depending on the context, None can either mean any version or
    no version attributed/detected
    """
    __slots__ = ["value", "major", "minor", "release"]

    def __init__(self, value: str = None):
        self.value = value
        self.major = None
        self.minor = None
        self.release = None
        if isinstance(value, str):
            self.value = value.strip()
            if self.value:
                elements = value.split('.')
                # major.minor.release
                if len(elements) == 3:
                    self.major, self.minor, self.release = elements
                    # if values contains only digits parse them
                    # to get good comparison results
                    for attribute in self.__slots__:
                        v = getattr(self, attribute)
                        if all([c in "0123456789" for c in v.strip()]):
                            setattr(self, attribute, int(v, 10))
                        else:
                            setattr(self, attribute, v.strip())
                    self.value = "%s.%s.%s" % (self.major, self.minor, self.release)
        elif isinstance(value, int):
            self.major = value
            self.minor = 0
            self.release = 0
        elif isinstance(value, float):
            self.major = int(value)
            self.minor = int((value - int(value)) * 1000)
            self.release = 0
        else:
            self.value = value
            self.major, self.minor, self.release = None, None, None

    def is_mmr(self):
        return (self.major is not None) and \
               (self.minor is not None) and (self.release is not None)

    def __eq__(self, version):
        if isinstance(version, Version):
            if isinstance(version.value, type(self.value)):
                return self.value == version.value
            return (self.major == version.major) and \
                   (self.minor == version.minor) and \
                   (self.release == version.release)
        return self == Version(version)

    def __ne__(self, version):
        if isinstance(version, Version):
            if isinstance(version.value, type(self.value)):
                return self.value != version.value
            return (self.major != version.major) or \
                   (self.minor != version.minor) or \
                   (self.release != version.release)
        return self != Version(version)

    def __gt__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major > version.major:
                    return True
                if self.minor is None or version.minor is None:
                    return False
                if self.minor > version.minor:
                    return True
                if self.release is None or version.release is None:
                    return False
                return self.release > version.release
            # always latest value if '' or None
            if self.value in ('', None):
                return version.value not in ('', None)
            if version.value in ('', None):
                return False
            return self.value > version.value
        return self > Version(version)

    def __ge__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major > version.major:
                    return True
                if self.minor is None or version.minor is None:
                    return False
                if self.minor > version.minor:
                    return True
                if self.release is None or version.release is None:
                    return False
                return self.release >= version.release
            # always latest value if '' or None
            if self.value in ('', None):
                return True
            if version.value in ('', None):
                return self.value in ('', None)
            return self.value >= version.value
        return self >= Version(version)

    def __le__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major < version.major:
                    return True
                if self.minor is None or version.minor is None:
                    return False
                if self.minor < version.minor:
                    return True
                if self.release is None or version.release is None:
                    return False
                return self.release <= version.release
            # always latest value if '' or None
            if version.value in ('', None):
                return True
            if self.value in ('', None):
                return version.value in ('', None)
            return self.value <= version.value
        return self <= Version(version)

    def __lt__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major < version.major:
                    return True
                if self.minor is None or version.minor is None:
                    return False
                if self.minor < version.minor:
                    return True
                if self.release is None or version.release is None:
                    return False
                return self.release < version.release
            # always latest value if '' or None
            if self.value in ('', None):
                return False
            if version.value in ('', None):
                return self.value not in ('', None)
            return self.value < version.value
        return self < Version(version)

    def __str__(self):
        return str(self.value)


class Package(object):
    __slots__ = [
        "name",
        "version",
        "description",
        "assertions",
        "constraints",
        "designs",
        "dependencies",
        "libraries",
        "models"
    ]

    def __init__(self, name: str = None, version: str = None):
        if isinstance(name, str):
            self.name = name.strip()
        else:
            self.name = name
        self.version = Version(version)
        self.assertions = []
        self.constraints = []
        self.dependencies = []
        self.description = ""
        self.designs = []
        self.libraries = []
        self.models = []

    def __eq__(self, pkg):
        return (self.name == pkg.name) and (self.version == pkg.version)

    def __ne__(self, pkg):
        return (self.name != pkg.name) or (self.version != pkg.version)

    def __gt__(self, pkg):
        return (self.name == pkg.name) and \
               (self.version > pkg.version)

    def __ge__(self, pkg):
        return (self.name == pkg.name) and \
               (self.version >= pkg.version)

    def __le__(self, pkg):
        return (self.name == pkg.name) and \
               (self.version <= pkg.version)

    def __lt__(self, pkg):
        return (self.name == pkg.name) and \
               (self.version < pkg.version)

    def uniquify_dependencies(self):
        d = {}
        for pkg in self.dependencies:
            # remove None pkg or empty one
            if not pkg:
                continue
            if pkg.name not in d:
                d[pkg.name] = pkg
            elif pkg.name in d and pkg > d[pkg.name]:
                d[pkg.name] = pkg
        self.dependencies = d.values()

    def __str__(self):
        return "%s %s" % (self.name, self.version)

    def to_dict(self):
        p = {}
        for attr in self.__slots__:
            values = getattr(self, attr)
            if attr == "dependencies":
                p[attr] = [str(v) for v in values]
            elif isinstance(values, list):
                p[attr] = [v.to_dict() if "to_dict" in dir(v) else v for v in values]
            elif isinstance(values, dict):
                p[attr] = {i: v.to_dict() if "to_dict" in dir(v) else v
                           for i, v in values.items()}
            elif "to_dict" in dir(values):
                p[attr] = values.to_dict()
            elif isinstance(values, Version):
                p[attr] = str(values)
            else:
                p[attr] = values
        return p

    @staticmethod
    def from_dict(d):
        pkg = Package(d.get("name"), d.get("version"))
        pkg.assertions = d.get("assertions") or []
        pkg.constraints = d.get("constraints") or []
        pkg.description = d.get("description", "")
        pkg.designs = d.get("designs") or []
        pkg.libraries = d.get("libraries") or []
        pkg.models = d.get("models") or []
        # transform dependencies into package
        deps = d.get("dependencies") or []
        pkg.dependencies = [
            Package.parse_package_name(dep) if isinstance(dep, str) else dep for dep in deps
        ]
        return pkg

    @staticmethod
    def parse_package_name(pkg_name: str):
        if not isinstance(pkg_name, str):
            return None
        # assume <name><operator><version>
        RE_PKG_NAME_VERSION = r"([\w\_\-]+)\s*(?:>|>=|=|<|<=)?\s*([\w\d\.\-]*)?$"
        m = re.findall(RE_PKG_NAME_VERSION, pkg_name, flags=re.MULTILINE)
        return Package(*m[0])

    @staticmethod
    def unified_diff(pkga, pkgb, no_print: bool = False):
        db = defaultdict(dict)
        # for each category...
        for category in Package.__slots__:
            if category in ["name", "version", "description", "dependencies"]:
                continue
            # detect new and removed files
            cat_a = getattr(pkga, category) if pkga else None
            cat_b = getattr(pkgb, category) if pkgb else None
            if cat_a is None and cat_b is None:
                continue
            elif cat_a is None and cat_b is not None:
                new_files = list(set([os.path.basename(file) for file in cat_b]))
                removed_files = None
                files_in_both = None
            elif cat_a is not None and cat_b is None:
                new_files = None
                removed_files = list(set([os.path.basename(file) for file in cat_a]))
                files_in_both = None
            else:
                cat_a = set([os.path.basename(file) for file in cat_a])
                cat_b = set([os.path.basename(file) for file in cat_b])
                new_files = list(cat_b - cat_a)
                removed_files = list(cat_a - cat_b)
                files_in_both = cat_a.intersection(cat_b)
            cat_a = getattr(pkga, category)
            cat_b = getattr(pkgb, category)
            # list new files
            if new_files:
                db[category]["new"] = new_files
                if not no_print:
                    print("new files:")
                    for new_file in new_files:
                        print('\t', new_file)
            # list removed files
            if removed_files:
                db[category]["removed"] = removed_files
                if not no_print:
                    print("removed files:")
                    for removed_file in removed_files:
                        print('\t', removed_file)
            # detect diff in same files
            if files_in_both:
                for file in files_in_both:
                    file_a = [f for f in cat_a if os.path.basename(f) == file]
                    file_b = [f for f in cat_b if os.path.basename(f) == file]
                    with open(file_a[-1], "r+") as fp:
                        content_a = fp.readlines()
                    with open(file_b[-1], "r+") as fp:
                        content_b = fp.readlines()
                    diff = '\n'.join(difflib.unified_diff(
                        content_a, content_b,
                        fromfile=file_a[-1],
                        tofile=file_b[-1]
                    ))
                    if diff:
                        db[category][file] = diff
        if db:
            return db
        return None
