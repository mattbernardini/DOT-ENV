#!/env/python3
from __future__ import division, print_function, absolute_import

import os
import stat
import urllib.request
import ssl
import glob
import multiprocessing

ssl._create_default_https_context = ssl._create_unverified_context

def create_directory(path, mode = None):
    try:
        os.makedirs(path)
    except OSError:
        pass
    if mode is not None:
        os.chmod(path, mode)

if __name__ == "__main__":
    LFS = os.path.expanduser('~/lfs/')
    lfs_sources = LFS + "sources/"
    # Section 3
    create_directory(LFS + "sources", stat.S_IRWXU + stat.S_ISVTX + stat.S_IWGRP + stat.S_IWOTH)
    wget_list_path = LFS + "sources/wget-list.txt"
    files = urllib.request.urlretrieve("http://www.linuxfromscratch.org/lfs/view/stable/wget-list", wget_list_path)
    with open(wget_list_path, 'r') as f, multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        for line in f:
            urllib.request.urlretrieve(line, filename=LFS + "sources/" + line.split("/")[-1].strip())

    # Section 4
    create_directory(LFS + "tools", None)

    """
    Section 5
    """
    list_of_files = []
    for f in glob.glob(lfs_sources + "*.tar.gz"):
        create_directory('.'.join(f.split(".")[:-2]))
        list_of_files.append('.'.join(f.split(".")[:-2]).split("/")[-1])
        os.system("tar -xzvf " + f + " --directory " + '.'.join(f.split(".")[:-2]) + " --strip-components=1")
    for f in glob.glob(lfs_sources + "*.tar.xz"):
        create_directory('.'.join(f.split(".")[:-2]))
        list_of_files.append('.'.join(f.split(".")[:-2]).split("/")[-1])
        os.system("tar -xJvf " + f + " --directory " + '.'.join(f.split(".")[:-2]) + " --strip-components=1")
    for f in glob.glob(lfs_sources + "*.tar.bz2"):
        create_directory('.'.join(f.split(".")[:-2]))
        list_of_files.append('.'.join(f.split(".")[:-2]).split("/")[-1])
        os.system("tar -xjvf " + f + " --directory " + '.'.join(f.split(".")[:-2]) + " --strip-components=1")

    # Binutils
    list_of_files.sort()
    print(list_of_files[9])
    os.system("cd " + lfs_sources + list_of_files[8] + " && mkdir -v build && cd build && " \
        " ../configure "
        "--prefix=/tools "
        "--with-sysroot=" + LFS +
        " --with-lib-path=" + LFS + "/tools/lib"
        "--disable-nls --disable-werror")