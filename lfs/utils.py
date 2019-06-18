#!/env/python3
from __future__ import absolute_import, division, print_function
import os
import pathlib


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
