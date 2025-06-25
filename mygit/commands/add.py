import os
from mygit import index, utils, objects

def add(paths):
    for path in paths:
        if os.path.isdir(path):
            raise Exception("Adding directories is not supported.")
        data = utils.read_file(path)
        oid = objects.hash_object(data.encode(), "blob")
        index.add_to_index(path, oid)
