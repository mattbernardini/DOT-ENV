#!/env/python3
from __future__ import absolute_import, division, print_function

import argparse
import glob
import multiprocessing
import os
import pathlib
import re
import ssl
import stat
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

make_command = "make -j " + str(multiprocessing.cpu_count()) + " && make install"

def test_and_untar(file_to_untar: str, tar_switch: str, strip_version: bool = False, location_to_untar_to = None):
    """
        Args:
            file_to_untar:          The full path to the file that we wish to untar
            tar_switch:             The switches that the tar command needs in order to successfully untar the file
            strip_version:          Whether to strip the version numbers of out the file name when untarring
            location_to_untar_to:   The root location that we wish to untar to

        Example:
            WITHOUT LOCATION:
                If we wish to untar /home/lfs/sources/gcc-8.2.0.tar.xz to /home/lfs/sources/gcc-8.2.0
                we would call this function:
                    test_and_untar("/home/lfs/sources/gcc-8.2.0.tar.xz", "xJ")
                and the function would result in gcc untarred at /home/fs/sources/gcc-8.2.0
            WITH LOCATION:
                if we wish to untar /home/lfs/sources/mpfr-4.0.2.tar.xz to /home/lfs/sources/gcc-8.2.0/mpfr
                we would call it this way:
                    test_and_untar("/home/lfs/sources/mpfr-4.0.2.tar.xz", "xJ", True, "/home/lfs/sources/gcc-8.2.0")
    """
    if location_to_untar_to:
        if os.path.isdir(file_to_untar.split(".")[:-2]):
            os.rmdir(file_to_untar.split(".")[:-2])
    pass


def create_directory(path, mode = None):
    print("Creating directory " + path + "....")
    try:
        os.makedirs(path)
    except OSError:
        pass
    if mode is not None:
        os.chmod(path, mode)

def parse_args():
    # Arguments
    parser = argparse.ArgumentParser(description="Build a consistent environment for Matt")
    parser.add_argument('--download', help="Whether we should download the files from remotes", action="store_true")
    parser.add_argument('--gcc-pass-one', help="Whether we !DO NOT! need to run the gcc first build", action="store_const", const=True)
    parser.add_argument('--clean', help="Whether we should clean out sources", action="store_true")
    #parser.add_argument('--user', help="The user under which we are currently running")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    LFS = os.path.expanduser('~/')
    lfs_sources = LFS + "sources/"
    # Section 3
    create_directory(LFS + "sources", stat.S_IRWXU + stat.S_ISVTX + stat.S_IWGRP + stat.S_IWOTH)

    if args.download:
        wget_list_path = LFS + "sources/wget-list.txt"
        files = urllib.request.urlretrieve("http://www.linuxfromscratch.org/lfs/view/stable/wget-list", wget_list_path)
        with open(wget_list_path, 'r') as f:
            for line in f:
                print("Downloading " + line.strip() + "....")
                urllib.request.urlretrieve(line, filename=LFS + "sources/" + line.split("/")[-1].strip())

    """
        Section 4
    """
    create_directory(LFS + "tools", None)
    os.system("chown -v lfs /home/lfs")
    # From section 5.1
    os.system("mkdir -v " + LFS + "tools/lib && ln -sv " + LFS + "tools/lib " + LFS + "tools/lib64")

    # """
    #     Section 5
    #     .gz = xzf
    #     .xz = xJf
    #     .bz2 = xjf
    # """
    list_of_files = []
    for f in glob.glob(lfs_sources + "*.tar.*"):
        list_of_files.append(f)#'.'.join(f.split(".")[:-2]).split("/")[-1])
    list_of_files.sort()

    for i in zip(list_of_files, range(list_of_files.__len__())):
        print(i)

    # Binutils
    bin_utils = list_of_files[8]
    create_directory('.'.join(bin_utils.split(".")[:-2]))
    os.system("tar -xJf " + bin_utils + " --directory " + '.'.join(bin_utils.split(".")[:-2]) + " --strip-components=1")
    os.system("cd " + '.'.join(bin_utils.split(".")[:-2]) + " && mkdir -v build && cd build && " \
        " ../configure "
        "--prefix=/home/lfs/tools "
        "--target=$LFS_TGT "
        "--with-sysroot=/home/lfs "
        "--with-lib-path=/home/lfs/tools/lib"
        "--disable-nls --disable-werror && " + make_command)

    # GCC Pass 1
    gcc = list_of_files[25]
    mpfr = list_of_files[54]
    mpc = list_of_files[53]
    gmp = list_of_files[29]

    create_directory('.'.join(gcc.split(".")[:-2]))
    create_directory('.'.join(gcc.split(".")[:-2]) + "/build")

    print("Untarring gcc...")
    os.system("tar -xJf " + gcc + " --directory " + '.'.join(gcc.split(".")[:-2]) + " --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/mpfr")
    print("Untarring mpfr...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && " \
        "tar -xJf " + mpfr + " --directory mpfr --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/mpc")
    print("Untarring mpc...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && " \
        "tar -xzf " + mpc + " --directory mpc --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/gmp")
    print("Untarring gmp...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && " \
        "tar -xJf " + gmp + " --directory gmp --strip-components=1")

    print("Changing GCC's dynamic linker to use installed tools and changing to lib...")
    os.system("cp ./gcc_pass_one.sh " + '.'.join(gcc.split(".")[:-2]) + " &&  cd " + '.'.join(gcc.split(".")[:-2]) + " && chmod +x gcc_pass_one.sh && ./gcc_pass_one.sh")

    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + "/build && " \
        "../configure "                                  \
        "--target=$LFS_TGT "                             \
        "--prefix=/home/lfs/tools "                     \
        "--with-glibc-version=2.11 "                     \
        "--with-sysroot=/home/lfs "                    \
        "--with-newlib "                                 \
        "--without-headers "                             \
        "--with-local-prefix=/home/lfs/tools"           \
        "--with-native-system-header-dir=/home/lfs/tools/include "\
        "--disable-nls "                                 \
        "--disable-shared "                              \
        "--disable-multilib "                            \
        "--disable-decimal-float "                       \
        "--disable-threads "                             \
        "--disable-libatomic "                           \
        "--disable-libgomp "                             \
        "--disable-libmpx "                              \
        "--disable-libquadmath "                         \
        "--disable-libssp "                              \
        "--disable-libvtv "                              \
        "--disable-libstdcxx "                           \
        "--enable-languages=c,c++ "                      \
        "--disable-bootstrap"
        "&& " + make_command)

    # Linux API Headers

    linux_header_api = list_of_files[47]

    os.system("tar -xJf " + linux_header_api + " --directory " + '.'.join(linux_header_api.split(".")[:-2]) + " --strip-components=1")
    os.system("cd " + '.'.join(linux_header_api.split(".")[:-2]) + " && make clean && make mrproper && make INSTALL_HDR_PATH=dest headers_install && cp -rv dest/include/* ~/tools/include")