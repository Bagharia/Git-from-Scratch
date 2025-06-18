import os
from ggit.utils import compute_sha1_and_store

def hash_object(path):
    if not os.path.exists(path):
        print(f"fatal: {path} does not exist")
        return

    if os.path.isdir(path):
        print(f"fatal: {path} is a directory")
        return

    with open(path, "rb") as f:
        content = f.read()

    sha = compute_sha1_and_store(content)
    print(sha)
