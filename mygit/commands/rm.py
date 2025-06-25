import os
from mygit import index

def rm(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
        index.remove_from_index(path)
