import os

def create_directory(path, *mode):
    os.makedirs(path)
    os.chmod(path, mode)

if __name__ == "__main__":
    LFS = os.path.expanduser('~/lfs/')
    create_directory(LFS + "sources", )
