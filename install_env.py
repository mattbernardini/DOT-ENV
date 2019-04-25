#!/env/python3
from __future__ import division, print_function, absolute_import

import os
import stat
import urllib.request
import ssl
import glob
import multiprocessing

ssl._create_default_https_context = ssl._create_unverified_context

make_command = "make -j " +str(multiprocessing.cpu_count()) + " && make install"

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
    # with open(wget_list_path, 'r') as f:
    #     for line in f:
    #         print("Downloading " + line.strip() + "....")
    #         urllib.request.urlretrieve(line, filename=LFS + "sources/" + line.split("/")[-1].strip())

    # """
    #     Section 4
    # """
    # create_directory(LFS + "tools", None)
    # # From section 5.1
    # os.system("mkdir -v " + LFS + "tools/lib && ln -sv lib " + LFS + "tools/lib64")

    """
        Section 5
        .gz = xzf
        .xz = xJf
        .bz2 = xjf
    """
    list_of_files = []
    for f in glob.glob(lfs_sources + "*.tar.*"):
        list_of_files.append(f)#'.'.join(f.split(".")[:-2]).split("/")[-1])
    list_of_files.sort()

    # Binutils
    # bin_utils = list_of_files[8]
    # create_directory('.'.join(bin_utils.split(".")[:-2]))
    # os.system("tar -xJf " + bin_utils + " --directory " + '.'.join(bin_utils.split(".")[:-2]) + " --strip-components=1")
    # os.system("cd " + '.'.join(bin_utils.split(".")[:-2]) + " && mkdir -v build && cd build && " \
    #     " ../configure "
    #     "--prefix=" + LFS + "tools "
    #     "--with-sysroot=" + LFS +
    #     " --with-lib-path=" + LFS + "/tools/lib"
    #     "--disable-nls --disable-werror && " + make_command)

    # GCC Pass 1
    gcc = list_of_files[25]
    mpfr = list_of_files[54]
    mpc = list_of_files[53]
    gmp = list_of_files[29]
    create_directory('.'.join(gcc.split(".")[:-2]))
    os.system("tar -xJf " + gcc + " --directory " + '.'.join(gcc.split(".")[:-2]) + " --strip-components=1")
    os.system("cd " + gcc.split(".")[:-2] + " && " + \
        "tar -xJf ../" + mpfr.split("/")[-1])