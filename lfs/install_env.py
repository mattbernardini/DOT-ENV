#!/env/python3
from __future__ import absolute_import, division, print_function

import argparse
import glob
import multiprocessing
import os
import pathlib
import shutil
import re
import ssl
import stat
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

make_command = "make -j " + \
    str(multiprocessing.cpu_count()) + " && make install"


def test_and_untar(file_to_untar: str, tar_switch: str, strip_version: bool = False, location_to_untar_to=None):
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


def create_directory(path, mode=None):
    print("Creating directory " + path + "....")
    try:
        os.makedirs(path)
    except OSError:
        pass
    if mode is not None:
        os.chmod(path, mode)


def parse_args():
    # Arguments
    parser = argparse.ArgumentParser(
        description="Build a consistent environment for Matt")
    parser.add_argument(
        '--download', help="Whether we should download the files from remotes", action="store_true")
    parser.add_argument(
        '--gcc-pass-one', help="Whether we !DO NOT! need to run the gcc first build", action="store_const", const=True)
    parser.add_argument(
        '--clean', help="Whether we should clean out sources", action="store_true")
    #parser.add_argument('--user', help="The user under which we are currently running")
    return parser.parse_args()
"""
    ('/home/lfs/sources/Python-3.7.2.tar.xz', 0)
    ('/home/lfs/sources/XML-Parser-2.44.tar.gz', 1)
    ('/home/lfs/sources/acl-2.2.53.tar.gz', 2)
    ('/home/lfs/sources/attr-2.4.48.tar.gz', 3)
    ('/home/lfs/sources/autoconf-2.69.tar.xz', 4)
    ('/home/lfs/sources/automake-1.16.1.tar.xz', 5)
    ('/home/lfs/sources/bash-5.0.tar.gz', 6)
    ('/home/lfs/sources/bc-1.07.1.tar.gz', 7)
    ('/home/lfs/sources/binutils-2.32.tar.xz', 8)
    ('/home/lfs/sources/bison-3.3.2.tar.xz', 9)
    ('/home/lfs/sources/bzip2-1.0.6.tar.gz', 10)
    ('/home/lfs/sources/check-0.12.0.tar.gz', 11)
    ('/home/lfs/sources/coreutils-8.30.tar.xz', 12)
    ('/home/lfs/sources/dbus-1.12.12.tar.gz', 13)
    ('/home/lfs/sources/dejagnu-1.6.2.tar.gz', 14)
    ('/home/lfs/sources/diffutils-3.7.tar.xz', 15)
    ('/home/lfs/sources/e2fsprogs-1.44.5.tar.gz', 16)
    ('/home/lfs/sources/elfutils-0.176.tar.bz2', 17)
    ('/home/lfs/sources/eudev-3.2.7.tar.gz', 18)
    ('/home/lfs/sources/expat-2.2.6.tar.bz2', 19)
    ('/home/lfs/sources/expect5.45.4.tar.gz', 20)
    ('/home/lfs/sources/file-5.36.tar.gz', 21)
    ('/home/lfs/sources/findutils-4.6.0.tar.gz', 22)
    ('/home/lfs/sources/flex-2.6.4.tar.gz', 23)
    ('/home/lfs/sources/gawk-4.2.1.tar.xz', 24)
    ('/home/lfs/sources/gcc-8.2.0.tar.xz', 25)
    ('/home/lfs/sources/gdbm-1.18.1.tar.gz', 26)
    ('/home/lfs/sources/gettext-0.19.8.1.tar.xz', 27)
    ('/home/lfs/sources/glibc-2.29.tar.xz', 28)
    ('/home/lfs/sources/gmp-6.1.2.tar.xz', 29)
    ('/home/lfs/sources/gperf-3.1.tar.gz', 30)
    ('/home/lfs/sources/grep-3.3.tar.xz', 31)
    ('/home/lfs/sources/groff-1.22.4.tar.gz', 32)
    ('/home/lfs/sources/grub-2.02.tar.xz', 33)
    ('/home/lfs/sources/gzip-1.10.tar.xz', 34)
    ('/home/lfs/sources/iana-etc-2.30.tar.bz2', 35)
    ('/home/lfs/sources/inetutils-1.9.4.tar.xz', 36)
    ('/home/lfs/sources/intltool-0.51.0.tar.gz', 37)
    ('/home/lfs/sources/iproute2-4.20.0.tar.xz', 38)
    ('/home/lfs/sources/kbd-2.0.4.tar.xz', 39)
    ('/home/lfs/sources/kmod-26.tar.xz', 40)
    ('/home/lfs/sources/less-530.tar.gz', 41)
    ('/home/lfs/sources/lfs-bootscripts-20180820.tar.bz2', 42)
    ('/home/lfs/sources/libcap-2.26.tar.xz', 43)
    ('/home/lfs/sources/libffi-3.2.1.tar.gz', 44)
    ('/home/lfs/sources/libpipeline-1.5.1.tar.gz', 45)
    ('/home/lfs/sources/libtool-2.4.6.tar.xz', 46)
    ('/home/lfs/sources/linux-4.20.12.tar.xz', 47)
    ('/home/lfs/sources/m4-1.4.18.tar.xz', 48)
    ('/home/lfs/sources/make-4.2.1.tar.bz2', 49)
    ('/home/lfs/sources/man-db-2.8.5.tar.xz', 50)
    ('/home/lfs/sources/man-pages-4.16.tar.xz', 51)
    ('/home/lfs/sources/meson-0.49.2.tar.gz', 52)
    ('/home/lfs/sources/mpc-1.1.0.tar.gz', 53)
    ('/home/lfs/sources/mpfr-4.0.2.tar.xz', 54)
    ('/home/lfs/sources/ncurses-6.1.tar.gz', 55)
    ('/home/lfs/sources/ninja-1.9.0.tar.gz', 56)
    ('/home/lfs/sources/openssl-1.1.1a.tar.gz', 57)
    ('/home/lfs/sources/patch-2.7.6.tar.xz', 58)
    ('/home/lfs/sources/perl-5.28.1.tar.xz', 59)
    ('/home/lfs/sources/pkg-config-0.29.2.tar.gz', 60)
    ('/home/lfs/sources/procps-ng-3.3.15.tar.xz', 61)
    ('/home/lfs/sources/psmisc-23.2.tar.xz', 62)
    ('/home/lfs/sources/python-3.7.2-docs-html.tar.bz2', 63)
    ('/home/lfs/sources/readline-8.0.tar.gz', 64)
    ('/home/lfs/sources/sed-4.7.tar.xz', 65)
    ('/home/lfs/sources/shadow-4.6.tar.xz', 66)
    ('/home/lfs/sources/sysklogd-1.5.1.tar.gz', 67)
    ('/home/lfs/sources/systemd-240.tar.gz', 68)
    ('/home/lfs/sources/systemd-man-pages-240.tar.xz', 69)
    ('/home/lfs/sources/sysvinit-2.93.tar.xz', 70)
    ('/home/lfs/sources/tar-1.31.tar.xz', 71)
    ('/home/lfs/sources/tcl8.6.9-src.tar.gz', 72)
    ('/home/lfs/sources/texinfo-6.5.tar.xz', 73)
    ('/home/lfs/sources/tzdata2018i.tar.gz', 74)
    ('/home/lfs/sources/udev-lfs-20171102.tar.bz2', 75)
    ('/home/lfs/sources/util-linux-2.33.1.tar.xz', 76)
    ('/home/lfs/sources/vim-8.1.tar.bz2', 77)
    ('/home/lfs/sources/xz-5.2.4.tar.xz', 78)
    ('/home/lfs/sources/zlib-1.2.11.tar.xz', 79)
"""

if __name__ == "__main__":
    args = parse_args()
    LFS = os.path.expanduser('~/')
    lfs_sources = LFS + "sources/"
    # Section 3
    create_directory(LFS + "sources", stat.S_IRWXU +
                     stat.S_ISVTX + stat.S_IWGRP + stat.S_IWOTH)

    if args.download:
        wget_list_path = LFS + "sources/wget-list.txt"
        files = urllib.request.urlretrieve(
            "http://www.linuxfromscratch.org/lfs/view/stable/wget-list", wget_list_path)
        with open(wget_list_path, 'r') as f:
            for line in f:
                print("Downloading " + line.strip() + "....")
                urllib.request.urlretrieve(
                    line, filename=LFS + "sources/" + line.split("/")[-1].strip())
    else:
        tar_regex = re.compile(r'.*\.tar\..*')
        try:
            shutil.rmtree("/home/lfs/tools")
        except FileNotFoundError:
            pass
        for f in glob.glob(lfs_sources + "*"):
            if not tar_regex.match(f) and os.path.isdir(f):
                print(f)
                shutil.rmtree(f)

    """
        Section 4
    """
    create_directory(LFS + "tools", None)
    os.system("chown -v lfs /home/lfs")
    # From section 5.1
    os.system("mkdir -v " + LFS + "tools/lib && ln -sv " +
              LFS + "tools/lib " + LFS + "tools/lib64")

    # """
    #     Section 5
    #     .gz = xzf
    #     .xz = xJf
    #     .bz2 = xjf
    # """
    list_of_files = []
    for f in glob.glob(lfs_sources + "*.tar.*"):
        list_of_files.append(f)  # '.'.join(f.split(".")[:-2]).split("/")[-1])
    list_of_files.sort()

    # Binutils
    bin_utils = list_of_files[8]
    create_directory('.'.join(bin_utils.split(".")[:-2]))
    os.system("tar -xJf " + bin_utils + " --directory " +
              '.'.join(bin_utils.split(".")[:-2]) + " --strip-components=1")
    os.system("cd " + '.'.join(bin_utils.split(".")[:-2]) + " && mkdir -v build && cd build && "
              " ../configure "
              "--prefix=$LFS/tools "
              "--target=$LFS_TGT "
              "--with-sysroot=$LFS "
              "--with-lib-path=$LFS/tools/lib"
              "--disable-nls --disable-werror && " + make_command)

    # GCC Pass 1
    gcc = list_of_files[25]
    mpfr = list_of_files[54]
    mpc = list_of_files[53]
    gmp = list_of_files[29]

    create_directory('.'.join(gcc.split(".")[:-2]))
    create_directory('.'.join(gcc.split(".")[:-2]) + "/build")

    print("Untarring gcc...")
    os.system("tar -xJf " + gcc + " --directory " +
              '.'.join(gcc.split(".")[:-2]) + " --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/mpfr")
    print("Untarring mpfr...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && "
              "tar -xJf " + mpfr + " --directory mpfr --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/mpc")
    print("Untarring mpc...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && "
              "tar -xzf " + mpc + " --directory mpc --strip-components=1")

    create_directory('.'.join(gcc.split(".")[:-2]) + "/gmp")
    print("Untarring gmp...")
    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + " && "
              "tar -xJf " + gmp + " --directory gmp --strip-components=1")

    print("Changing GCC's dynamic linker to use installed tools and changing to lib...")
    os.system("cp ./gcc_pass_one.sh " + '.'.join(gcc.split(".")[:-2]) + " &&  cd " +
              '.'.join(gcc.split(".")[:-2]) + " && chmod +x gcc_pass_one.sh && ./gcc_pass_one.sh")

    os.system("cd " + '.'.join(gcc.split(".")[:-2]) + "/build && "
              "../configure "
              "--target=$LFS_TGT "
              "--prefix=$LFS/tools "
              "--with-glibc-version=2.11 "
              "--with-sysroot=$LFS "
              "--with-newlib "
              "--without-headers "
              "--with-local-prefix=/tools "
              "--with-native-system-header-dir=$LFS/tools/include "
              "--disable-nls "
              "--disable-shared "
              "--disable-multilib "
              "--disable-decimal-float "
              "--disable-threads "
              "--disable-libatomic "
              "--disable-libgomp "
              "--disable-libmpx "
              "--disable-libquadmath "
              "--disable-libssp "
              "--disable-libvtv "
              "--disable-libstdcxx "
              "--enable-languages=c,c++ "
             # "--disable-bootstrap "
              "&& " + make_command)
    # # Linux API Headers
    # linux_header_api = list_of_files[47]

    # create_directory('.'.join(linux_header_api.split(".")[:-2]))
    # print("Untarring linux headers...")
    # os.system("tar -xJf " + linux_header_api + " --directory " + '.'.join(linux_header_api.split(".")[:-2]) +
    #           " --strip-components=1")
    # os.system("cd " + '.'.join(linux_header_api.split(".")[:-2]) +
    #           " && make clean && make mrproper && make INSTALL_HDR_PATH=dest headers_install && cp -rv dest/include/* ~/tools/include")

    # # Glibc
    # glibc = list_of_files[28]
    # create_directory('.'.join(glibc.split(".")[:-2]))
    # create_directory('.'.join(glibc.split(".")[:-2]) + "/build")

    # print("Untarring glibc...")
    # os.system("tar -xJf " + glibc + " --directory " +
    #           '.'.join(glibc.split(".")[:-2]) + " --strip-components=1")
    # os.system("cd " + '.'.join(glibc.split(".")[:-2]) + "/build && "
    #           "../configure "
    #           "--prefix=$LFS/tools "
    #           "--host=$LFS_TGT "
    #           "--build=$(..scripts/config.guess) "
    #           "--enable-kernel=3.2 "
    #           "--with-headers=$LFS/tools/include && " + make_command)

    # Libstdc++ Build
    # create_directory('.'.join(gcc.split(".")[:-2]) + "/libcxx_build")
    # os.system("cd " + '.'.join(gcc.split(".")[:-2]) + "/libcxx_build && "
    #           "../libstdc++-v3/configure "
    #           "--target=$LFS_TGT "
    #           "--host=$LFS_TGT "
    #           "--prefix=$LFS/tools "
    #           "--disable-multilib "
    #           "--disable-nls "
    #           "--disable-libstdcxx-threads "
    #           "--disable-libstdcxx-pch "
    #           "--with-gxx-include-dir=$LFS/tools/$LGS_TGT/include/c++/8.2.0 "
    #           " && " + make_command)
