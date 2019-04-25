#!/env/python3
from __future__ import division, print_function, absolute_import

import os
import stat
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def create_directory(path, mode):
    try:
        os.makedirs(path)
    except OSError:
        pass
    if mode is not None:
        os.chmod(path, mode)

if __name__ == "__main__":
    LFS = os.path.expanduser('~/lfs/')
    # Section 3
    create_directory(LFS + "sources", stat.S_IRWXU + stat.S_ISVTX + stat.S_IWGRP + stat.S_IWOTH)
    wget_list_path = LFS + "sources/wget-list.txt"
    files = urllib.request.urlretrieve("http://www.linuxfromscratch.org/lfs/view/stable/wget-list", wget_list_path)
    with open(wget_list_path, 'r') as f:
        for line in f:
            urllib.request.urlretrieve(line, filename=LFS + "sources/" + line.split("/")[-1].strip())

    # Section 4
    create_directory(LFS + "tools", None)

    # Section 5
    # os.system("tar -xzvf")
    # os.system("cd " )