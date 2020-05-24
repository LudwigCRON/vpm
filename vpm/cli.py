#!/usr/bin/env python3
# coding: utf-8

import sys
import vpm
import argparse


def cli_args():
    # available actions
    mangle_args = {
        "install": "install a package from its name and version",
        "update": "update a package from its name",
        "list": "list all packages available/installed/outdated/corrupted",
        "remove": "remove a package",
        "create": "package/config"
    }
    # make sys args available
    arguments = ["--" + a if a in mangle_args.keys() else a for a in sys.argv[1:]]
    parser = argparse.ArgumentParser()
    for a in mangle_args.keys():
        parser.add_argument(
            "-" + a[0], "--" + a, help=mangle_args[a], default=None, type=str
        )
    # return the parsed actions
    return (parser, parser.parse_args(arguments))


def cli_main():
    parser, args = cli_args()
    if args.install is not None:
        vpm.install_package(args.install.lower())
    elif args.update is not None:
        vpm.install_package(args.update.lower(), force=True)
    elif args.list is not None:
        if args.list.lower() == "installed":
            vpm.list_installed()
        elif args.list.lower() == "outdated":
            vpm.list_outdated()
        elif args.list.lower() == "available":
            vpm.list_available()
        elif args.list.lower() == "corrupted":
            vpm.list_corrupted()
        elif args.list.lower() == "sources":
            vpm.list_sources()
        else:
            print("unknown option", file=sys.stderr)
    elif args.create is not None:
        if args.create.lower() == "config":
            vpm.default_config()
        elif args.create.lower() == "package":
            vpm.default_package()
        else:
            print("unknown option", file=sys.stderr)
    elif args.remove is not None:
        vpm.remove_package(args.remove.lower())
    else:
        print("unknown actions", file=sys.stderr)
        parser.print_help()
        exit(1)
    exit(0)


if __name__ == "__main__":
    cli_main()
