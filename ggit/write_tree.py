import os
import hashlib
from ggit.utils import compute_sha1_and_store


def write_tree():
    entries = []

    index_path = ".ggit/index"

    # 1. Vérifie si l'index existe
    if not os.path.exists(index_path):
        print("Nothing to write. Index is empty.")
        return

    # 2. Parcourt les fichiers listés dans l'index
    with open(index_path, "r") as f:
        for line in f:
            sha, path = line.strip().split(" ", 1)

            # 3. Prépare l’entrée binaire du tree
            mode = b"100644"  # fichier « normal »
            filename = path.encode("utf-8")
            sha_bin = bytes.fromhex(sha)
            if len(sha_bin) != 20:
                print(f"[ERREUR] SHA1 mal formé pour {path} : {sha}")
                continue
            # Debug :
            # print(f"DEBUG: mode={mode}, filename={filename}, sha={sha}, sha_bin={sha_bin.hex()}, len(sha_bin)={len(sha_bin)}")
            entry = mode + b" " + filename + b"\x00" + sha_bin
            entries.append(entry)

    # 5. Construit le contenu complet de l’objet tree
    tree_content = b"".join(entries)
    tree_sha = compute_sha1_and_store(tree_content, obj_type="tree")
    print(tree_sha)
    return tree_sha
