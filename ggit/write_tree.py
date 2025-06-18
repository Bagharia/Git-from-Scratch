import os
import hashlib
import zlib
from ggit.utils import compute_sha1_and_store

def write_tree():
    entries = []

    for root, dirs, files in os.walk("."):
        # Ignore .ggit et tout son contenu
        if root.startswith("./.ggit"):
            continue

        for filename in files:
            path = os.path.join(root, filename)

            # créer/écrire le blob et récupérer son SHA
            with open(path, "rb") as f:
                blob_sha = compute_sha1_and_store(f.read())

            # 2) constituer l’entrée binaire
            mode = b"100644"                     # fichier « normal »
            name = filename.encode()
            raw_sha = bytes.fromhex(blob_sha)    # 20 octets bruts
            entries.append(mode + b" " + name + b"\0" + raw_sha)

    # construire l'objet tree complet
    tree_content = b"".join(entries)
    header = f"tree {len(tree_content)}\0".encode()
    store = header + tree_content

    # stocker le tree (compression + écriture) et obtenir son SHA
    tree_sha = compute_sha1_and_store(store)

    # afficher le SHA du tree
    print(tree_sha)
