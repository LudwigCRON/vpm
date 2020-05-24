![Python package](https://github.com/LudwigCRON/vpm/workflows/Python%20package/badge.svg)
![Python versions](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)
![issues](https://img.shields.io/github/issues/LudwigCRON/vpm)
![activity](https://img.shields.io/github/last-commit/LudwigCRON/vpm)

# Verilog Package Manager (vpm)

The purpose of VPM is to manage a verilog project. In a project, keeping track of IP versions is a challenging task.
Package manager tools like apt, yum, dnf, pacman, ..., provide an easy interface for the user to maintain and keep up to date softwares and the distro.
In many ways, a project can benefit from such tools adapted for verilog.

VPM is one of these. An IP can be stored on a remote repository (github, gitlab, cvs, svn, ...), on a remote disk mounted (nfs, ...), or locally.

## Installation
The installation is rather simple:

```sh
# checked in regression as is
# update pip in case of
pip install --upgrade pip
# the lonely dependency
pip install pyyaml
# the package
pip install git+git://github.com/LudwigCRON/vpm.git#egg=vpm
```

From now on, on can call `vpm` in any terminal.

If a python environment is needed, just load your environment first:
```sh
# with pyenv installed
pyenv activate <vpm-env>
# or with virtualenv
source <vpm-env>/bin/activate
```

## Features
vpm is focused on the simplicity and relies on two files:
1. vpm.config

    _vpm.config corresponds to the list of repositories'url to inspect. This configuration file also contains information for dispatching files inside a project_

2. package.yml

    _package.yml list important information on a package such as dependencies, files to export, ..._

Their format description will be presented later on.

### vpm create [package | config]

```sh
vpm create config
```

the command line above generates a template of the configuration file to precise the list of repositories'url or repositories'path to look on.

```sh
vpm create package
```

this command line creates the blank package.yml file if there is none in current directory.
This files will defines the files to export and their roles (design/testcase/model/assertions/...)

### vpm install [url or package name]

install a package from either its url or its name. The name of a package and the version of the package can be specified.

In that case, the command will be
```bash
vpm install my-package=3.4.1
```

In fact, the one can select to install any version more recent the version specified by using the operator ">" or ">=".

To compare two version, vpm assumes a 3-number numeration system of the version as `major`.`minor`.`release`.
    
### vpm list installed

list installed packages and their version number. It does not display the status of a package (healthy/outdated/corrupted)

### vpm list outdated

list installed packages where a newer version exists in the list of repositories specified by the user.
    
### vpm list availabled

list packages availabled in the repositories enumerated in sources.list

### vpm list corrupted

list packages whose checksum does not match the one of the repository with the same version number. It is sometime useful to spot customized block.

### vpm update [package name]

update to the most recent version the package specified.

### vpm remove [package name]

remove the package from the project

## vpm.config
one single file with one line per repository in the following format
`[driver name]@[repository url]`

if no driver is provided, we assume it is a local repository such that in the example below, `./` and `../resync`are considered locally while
`git@github.com/LudwigCRON/vpm/tests/sar` is a url pointing to an IP on a github.com repository using the `git`driver.

```ini
[default]
# default variables to dispatch files
# during IP installations
DESIGNS_DIR=${PLATFORM}/design
MODELS_DIR=${PLATFORM}/model
LIBRARY_DIR=${PLATFORM}/library
TESTCASES_DIR=${PLATFORM}/testcases
DOCUMENTATION_DIR=${PLATFORM}/documents
CONSTRAINTS_DIR=${PLATFORM}/constraints

[repositories]
# at least have the current directory
sources = ./
          ../resync
          git@github.com/LudwigCRON/vpm/tests/sar
```

## package.yml
TBD

## Example
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

However, this is not mainstream. So one can edit where files are dispatched in its project by adding more information in the vpm.config file.

the default is the following:

```ini
[default]
# default variables to dispatch files
# during IP installations
DESIGNS_DIR=${PLATFORM}/design
MODELS_DIR=${PLATFORM}/model
LIBRARY_DIR=${PLATFORM}/library
TESTCASES_DIR=${PLATFORM}/testcases
DOCUMENTATION_DIR=${PLATFORM}/documents
CONSTRAINTS_DIR=${PLATFORM}/constraints
```

the environment variable `${PLATFORM}` is generated by the tool and corresponds to the path where the vpm.config is.

By editing the `*_DIR` variables, one change the dispatching for only its project.

Let's suppose the project structure is:

    platform
      |
      +--> customs
      |     |
      |     +--> sdc
      |     +--> tcl
      |     +--> verilog
      |     +--> ...
      +--> documents
      +--> vendors
      |     |
      |     +--> verilog files
      |     +--> assertions files 
      +--> techno
      |     |
      |     +--> technology files
      |     +--> pdk files
      +--> verification
            |
            +--> models
            +--> testbenches
            +--> testcases

the vpm.config file can be adapted to:

```ini
[default]
# default variables to dispatch files
# during IP installations
DESIGNS_DIR=${PLATFORM}/vendors
MODELS_DIR=${PLATFORM}/verification/models
LIBRARY_DIR=${PLATFORM}/techno
TESTCASES_DIR=${PLATFORM}/verification/testcases
DOCUMENTATION_DIR=${PLATFORM}/documents
CONSTRAINTS_DIR=${PLATFORM}/customs
```
