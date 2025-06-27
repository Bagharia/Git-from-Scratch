import os
from ggit.utils import compute_sha1_and_store

def hash_object(data_or_path, write=True):
    import os

    if isinstance(data_or_path, bytes):
        content = data_or_path
    else:
        path = data_or_path
        if not os.path.exists(path):
            print(f"fatal: {path} does not exist")
            return
        if os.path.isdir(path):
            print(f"fatal: {path} is a directory")
            return
        with open(path, "rb") as f:
            content = f.read()

    sha = compute_sha1_and_store(content) if write else hashlib.sha1(content).hexdigest()
    return sha
