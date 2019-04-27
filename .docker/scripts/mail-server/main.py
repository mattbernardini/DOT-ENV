from __future__ import absolute_import, division, print_function

import os

from ..utils.load_env import load_env

env = load_env()

def useage():
    print("Us")

def install_packages():
    os.system("sudo apt-get update -q --fix-missing && "\
        "sudo apt-get -y install postfix")