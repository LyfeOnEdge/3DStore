# 3DShop

[![3DShop](https://github.com/LyfeOnEdge/3DStore/blob/master/docu/main.png?raw=true)]()

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]() [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/3DStore/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/3DStore.svg)]() 

#### A WIP Homebrew store for the 3DS

## What is it?

A 3DS homebrew installer based on [custominstall.py](https://github.com/ihaveamac/custom-install/tree/module-rewrite) by ihaveamac.

Downloads and installs packages from a libget repository. If the package contains a cia and the user has set up 3DS up to install cias the cia will automatically be installed to the SD card using custom-install.py

#### Features:
- Download and install cias directly to the SD card
- Tool to install local cias as well

#### Requirements:
    Works on: macOS, Windows, Linux
    Python 3.6 or greater
    Dependencies vary by OS, see below.
    You will need a movable.sed and a boot9.bin dumped from you 3DS in order to install cias to the SD card.

##### Windows:
- Extract 3DStore.zip
- Install [python](https://www.python.org/downloads/windows/) if you haven't already
  - You *must* restart your pc after installing python for the first time.
  - If you do a custom installation remember to install tcl/tk, and include pip
- In a command prompt navigate to the dir you extracted the app to and type ```py -3 -m pip install --user -r requirements.txt``` to install dependencies
- Type `py -3 3DStore.py` or run the included bat file to launch the app.

##### Macintosh:
- Extract 3DStore.zip
- Mac users may already have a compatible version of python installed, try double-clicking appstoreworkbench.py
- In a command prompt navigate to the dir you extracted the app to and type ```pip3 install -r requirements.txt``` to install dependencies
  - If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work or pylauncher isn't available install [python](https://www.python.org/downloads/mac-osx/)

##### Linux:
- Extract 3DStore.zip
- Navigate to the directory in a terminal
- Type ```python3 -m pip install --user -r requirements.txt``` to install dependencies
- Type `python 3DStore.py`
  - If you are missing dependencies do the following:
  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk python3-pil.imagetk
  - Manjaro/Arch: sudo pacman -S python3 python-pip tk python-pillow
- Linux users must build [wwylele/save3ds](https://github.com/wwylele/save3ds) and place `save3ds_fuse` in `bin/linux`. Just install [rust using rustup](https://www.rust-lang.org/tools/install), then compile with: `cargo build`. Your compiled binary is located in `target/debug/save3ds_fuse`, copy it to `bin/linux`.
- Finally type `python3 3DStore.py` or run the included shell script.

## custom-install-finalize
custom-install-finalize installs a ticket, plus a seed if required. This is required for the title to appear and function.

This can be built as most 3DS homebrew projects [with devkitARM](https://www.3dbrew.org/wiki/Setting_up_Development_Environment).

## License/Credits
#### custom-install
Uses the module rewrite of [custominstall.py](https://github.com/ihaveamac/custom-install/tree/module-rewrite) by ihaveamac for cia installation.

`pyctr/` is from [ninfs `795373d`](https://github.com/ihaveamac/ninfs/tree/795373db07be0cacd60215d8eccf16fe03535984/ninfs/pyctr).

[save3ds by wwylele](https://github.com/wwylele/save3ds) is used to interact with the Title Database (details in `bin/README`).

#### GUI testers
Crafter Pika - Manages 4TU 3DS repo, gui testing and lots of patience

Archbox - Spun up app in a bunch of oses / distros to make sure it looked good cross-platform

ihaveamac - Good critiques, creator of original custom-install.py script used in this project

GlaZy - Critiques

oreo639 - Tester

LORD OF CBT - Tester

JBMagination -Tester