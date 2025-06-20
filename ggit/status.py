import os
import json
import hashlib

INDEX_PATH = os.path.join(".ggit", "index")

def compute_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()

def git_status():
    if not os.path.exists(INDEX_PATH):
        print("No index found. Did you run `ggit add`?")
        return

    index = {}
    with open(INDEX_PATH, "r") as f:
        for line in f:
            sha, path = line.strip().split(" ", 1)
            index[path] =sha

    modified = []
    deleted = []

    for path, sha in index.items():
        if not os.path.exists(path):
            deleted.append(path)
            continue
        with open(path, "rb") as f:
            content = f.read()
        current_sha = compute_sha1(content)
        if current_sha != sha:
            modified.append(path)

    # fichiers non suivis
    untracked = []
    for root, dirs, files in os.walk("."):
        # Supprime les dossiers .git et .ggit de la liste des dossiers à parcourir
        if ".git" in dirs:
            dirs.remove(".git")
        if ".ggit" in dirs:
            dirs.remove(".ggit")

        for name in files:
            relpath = os.path.relpath(os.path.join(root, name))
            if relpath not in index:
                untracked.append(relpath)

    if modified or deleted:
        print("Changes not staged for commit:")
        if modified:
            for f in modified:
                print(f"  modified:   {f}")
        if deleted:
            for f in deleted:
                print(f"  deleted:    {f}")
        print()

    if untracked:
        print("Untracked files:")
        for f in untracked:
            print(f"  {f}")
        print()

    if not (modified or deleted or untracked):
        print("Nothing to commit. Working directory clean.")
