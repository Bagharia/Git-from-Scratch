import os
from ggit.utils import compute_sha1_and_store

INDEX_PATH = ".ggit/index"

def git_add(path: str):
    with open(path, "rb") as f:
        data = f.read()
        sha = compute_sha1_and_store(data)

    # Ajouter à l'index : <SHA> <chemin>
    os.makedirs(".ggit", exist_ok=True)
    with open(INDEX_PATH, "a") as index:
        index.write(f"{sha} {path}\n")

    print(f"[added] {path} -> {sha}")
