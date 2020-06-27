#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
import yaml
import base64
import tempfile

from urllib.request import urlopen, Request

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm

# According to https://developer.github.com/v3/#rate-limiting
# 60 reqs/h if unauth and 5000 reqs/h if basic
# For search api respectivly 10 and 30 reqs/min

# user/repo or user/repo as username:password
BASEURL = "https://api.github.com/repos/%s/git/trees/%s?recursive=1"

# basic auth is deprecated and will be removed
VPM_GITHUB_TOKEN = os.getenv("VPM_GITHUB_TOKEN")


def github_request(url: str):
    req = Request(url)
    req.add_header("Authorization", "token %s" % VPM_GITHUB_TOKEN)
    res = urlopen(req)
    return json.loads(res.read(), encoding=res.headers.get_content_charset())


def github_content(path: str):
    res = github_request(path)
    encoding = res.get("encoding")
    if encoding == "base64":
        return base64.b64decode(res.get("content")).decode("utf-8")
    print("unknown encoding %s" % encoding, file=sys.stderr)
    return ""


def github_download(file: dict, dir: str):
    filename = os.path.basename(file.get("path"))
    url = file.get("url")
    filepath = os.path.join(dir, filename)
    with open(filepath, "w+") as fp:
        fp.write(github_content(url))
    return filepath


def github_findfiles(tree: list = [], path: str = ""):
    for file in tree:
        if path in file.get("path"):
            yield file


def github_findfile(tree: list = [], path: str = ""):
    for file in tree:
        if path in file.get("path"):
            return file
    return {}


def github_read_packages(repository: str, branch: str = "master", path: str = ""):
    res = github_request(BASEURL % (repository, branch))
    tree = res.get("tree", [])
    for yml in github_findfiles(tree, "%s/package.yml" % path):
        url = yml.get("url")
        base_path = os.path.dirname(yml.get("path"))
        content = github_content(url)
        print(yml.get("path"), url)
        # parse to dict
        d = yaml.load(content, Loader=yaml.FullLoader)
        # make temporary directory
        dir = tempfile.mkdtemp()
        # download all files
        for attr in vpm.Package.__slots__:
            if attr in ["name", "version", "description", "dependencies"]:
                continue
            if attr not in d.keys():
                continue
            df = d.get(attr) or []
            files = [os.path.normpath(os.path.join(base_path, f)) for f in df]
            files = [github_findfile(tree, f) for f in files]
            d[attr] = [github_download(f, dir) for f in files if f]
        # generate a new yml pointing to tmp file
        d["depth"] = len(yml.get("path", "").split('/'))
        yield vpm.read_package(path=yml.get("path"), content=d)
