#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import json
import base64
from urllib.request import urlopen, Request

vpm_module = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(vpm_module)

import vpm

# According to https://developer.github.com/v3/#rate-limiting
# 60 reqs/h if unauth and 5000 reqs/h if basic
# For search api respectivly 10 and 30 reqs/min

# user/repo or user/repo as username:password
BASEURL = "https://api.github.com/repos/%s/git/trees/master?recursive=1"

# basic auth is deprecated and will be removed
VPM_GITHUB_TOKEN = os.getenv("VPM_GITHUB_TOKEN")


def github_request(url):
    req = Request(url)
    req.add_header("Authorization", "token %s" % VPM_GITHUB_TOKEN)
    res = urlopen(req)
    return json.load(res)


def github_content(path):
    res = github_request(path)
    encoding = res.get("encoding")
    if encoding == "base64":
        return base64.b64decode(res.get("content")).decode("utf-8")
    print(encoding)


if __name__ == "__main__":
    res = github_request(BASEURL % "LudwigCRON/vpm")
    for file in res.get("tree", []):
        if os.path.basename(file.get("path")) == "package.yml":
            file["depth"] = len(file.get("path", "").split('/'))
            print(file)
            pkg = vpm.read_package(file, content=github_content(file.get("url")))
            print(pkg.to_dict())
