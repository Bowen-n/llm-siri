import os


def norm_path(path: str):
    return os.path.realpath(os.path.expanduser(path))
