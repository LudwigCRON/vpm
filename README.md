![Python package](https://github.com/LudwigCRON/vpm/workflows/Python%20package/badge.svg)
![Python versions](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)
![issues](https://img.shields.io/github/issues/LudwigCRON/vpm)
![activity](https://img.shields.io/github/last-commit/LudwigCRON/vpm)

# Verilog Package Manager (vpm)

The purpose of VPM is to manage a verilog project. In a project, keeping track of IP versions is a challenging task.
Package manager tools like apt, or yum, provide an easy interface for the user to maintain and keep uptodate softwares and the distro.
In many ways, a project can benefit from such tools adapted for verilog.

VPM is one of these. An IP can be stored on a remote repository (github, gitlab, cvs, svn, ...), on a remote disk mounted (nfs, ...), or locally.

## Back to basic
VPM relies on two files:
1. sources.list
2. package.yml

sources.list corresponds to the list of repositories'url to inspect. package.yml listing important information on a package. Their format description will
be presented later on.

The basic interface to the user is the following:

**vpm create**

create the blank package.yml file is there is none in current directory

**vpm install [url or package name]**

install a package from either its url or its name. The name of a package and the version of the package can be specified.
In that case, the command will be
```bash
vpm install my-package=3.4.1
```
In fact, the one can select to install any version more recent the version specified by using the operator ">" or ">=".
To compare two version, vpm assumes a 3-number numeration system of the version as major-minor-release.
    
**vpm list installed**

list installed packages and their version number. It does not display the status of a package (healthy/outdated/corrupted)

**vpm list outdated**

list installed packages where a newer version exists in the list of repositories specified by the user.
    
**vpm list availabled**

list packages availabled in the repositories enumerated in sources.list

**vpm list corrupted**

list packages whose checksum does not match the one of the repository with the same version number. It is sometime useful to spot customized block.

**vpm update [package name]**

update to the most recent version the package specified.

**vpm remove [package name]**

remove the package from the project

## project structure
For the current version of VPM, the project structure is:

    platform
      |
      +--> constraints
      |     |
      |     +--> sdc
      |     +--> tcl
      |     +--> ...
      +--> documents
      +--> designs
      |     |
      |     +--> verilog files
      |     +--> assertions files 
      +--> libraries
      |     |
      |     +--> technology files
      |     +--> pdk files
      +--> models
            |
            +--> simulation files only

## sources.list
one single file with one line per repository in the format [driver name]|[repository url]

*if no driver is provided, we assume it is a local repository.*

## package.yml
TBD
