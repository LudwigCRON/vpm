#!/usr/bin/env python3
# coding: utf-8

import os
import json
import base64
from urllib.request import urlopen, Request

# According to https://developer.github.com/v3/#rate-limiting
# 60 reqs/h if unauth and 5000 reqs/h if basic
# For search api respectivly 10 and 30 reqs/min

# valid user-agent is mandatory
USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 Edg/81.0.416.68"

# user/repo or user/repo as username:password
BASEURL = "https://api.github.com/repos/%s/git/trees/master?recursive=1"

# basic auth is deprecated and will be removed
VPM_TOKEN = "b13284edd3cb7a32ff5b8d167ff7e02e5ef62c3d"


def github_request(url):
    req = Request(url)
    req.add_header("Authorization", "token %s" % VPM_TOKEN)
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
            print(github_content(file.get("url")))
