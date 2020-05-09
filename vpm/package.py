#!/usr/bin/env python3
# coding: utf-8


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
                        if isinstance(v, str):
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
            return (self.value == version.value)
        return self == Version(version)

    def __ne__(self, version):
        if isinstance(version, Version):
            return (self.value != version.value)
        return self != Version(version)

    def __gt__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major > version.major:
                    return True
                elif self.minor is None or version.minor is None:
                    return False
                elif self.minor > version.minor:
                    return True
                elif self.release is None or version.release is None:
                    return False
                else:
                    return self.release > version.release
            if self.value is None or version.value is None:
                return False
            # always latest value if ''
            if self.value == '':
                return True
            return self.value > version.value
        return self > Version(version)

    def __ge__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major >= version.major:
                    return True
                elif self.minor is None or version.minor is None:
                    return False
                elif self.minor >= version.minor:
                    return True
                elif self.release is None or version.release is None:
                    return False
                else:
                    return self.release >= version.release
            if self.value is None or version.value is None:
                return False
            # always latest value if ''
            if self.value == '':
                return True
            return self.value >= version.value
        return self >= Version(version)

    def __le__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major <= version.major:
                    return True
                elif self.minor is None or version.minor is None:
                    return False
                elif self.minor <= version.minor:
                    return True
                elif self.release is None or version.release is None:
                    return False
                else:
                    return self.release <= version.release
            if self.value is None or version.value is None:
                return False
            # always latest value if ''
            if self.value == '':
                return False
            return self.value <= version.value
        return self <= Version(version)

    def __lt__(self, version):
        if isinstance(version, Version):
            if self.is_mmr() and version.is_mmr():
                if self.major is None or version.major is None:
                    return False
                if self.major < version.major:
                    return True
                elif self.minor is None or version.minor is None:
                    return False
                elif self.minor < version.minor:
                    return True
                elif self.release is None or version.release is None:
                    return False
                else:
                    return self.release < version.release
            if self.value is None or version.value is None:
                return False
            # always latest value if ''
            if self.value == '':
                return False
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
        return (self.name == pkg.name) and (self.version > pkg.version)

    def __ge__(self, pkg):
        return (self.name == pkg.name) and (self.version >= pkg.version)

    def __le__(self, pkg):
        return (self.name == pkg.name) and (self.version <= pkg.version)

    def __lt__(self, pkg):
        return (self.name == pkg.name) and (self.version < pkg.version)

    def uniquify_dependencies(self):
        d = {}
        for pkg in self.dependencies:
            if pkg.name not in d:
                d[pkg.name] = pkg
            elif pkg.name in d and pkg > d[pkg.name]:
                d[pkg.name] = pkg
        self.dependencies = d.values()

    def __str__(self):
        return "%s %s" % (self.name, self.version)

    @staticmethod
    def from_dict(d):
        pkg = Package(d.get("name"), d.get("version"))
        pkg.assertions = d.get("assertions", [])
        pkg.constraints = d.get("constraints", [])
        pkg.dependencies = d.get("dependencies", [])
        pkg.description = d.get("description", "")
        pkg.designs = d.get("designs", [])
        pkg.libraries = d.get("libraries", [])
        pkg.models = d.get("models", [])
        return pkg
