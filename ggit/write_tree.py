import os
import hashlib
from ggit.utils import compute_sha1_and_store


def write_tree():
    entries = []
    index_path = ".ggit/index"

    if not os.path.exists(index_path):
        print("Nothing to write. Index is empty.")
        return

    with open(index_path, "r") as f:
        lines = f.readlines()

    # Trie les lignes de l'index par nom de fichier pour respecter le format de Git
    lines.sort(key=lambda line: line.strip().split(" ", 1)[1])

    for line in lines:
        sha, path = line.strip().split(" ", 1)
        mode = b"100644"
        filename = path.encode("utf-8")
        sha_bin = bytes.fromhex(sha)

        if len(sha_bin) != 20:
            print(f"[ERREUR] SHA1 mal formé pour {path} : {sha}")
            continue

        entry = mode + b" " + filename + b"\x00" + sha_bin
        entries.append(entry)

    tree_content = b"".join(entries)
    tree_sha = compute_sha1_and_store(tree_content, obj_type="tree")
    print(f"[DEBUG] Writing object to .ggit/objects/{tree_sha[:2]}/{tree_sha[2:]}")
    print(tree_sha)
    return tree_sha
