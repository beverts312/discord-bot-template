import os


def get_repo_dir():
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    )