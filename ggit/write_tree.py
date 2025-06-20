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
            sha1, path = line.strip().split(" ", 1)

            # 3. Prépare l’entrée binaire du tree
            mode = b"100644"                     # fichier « normal »
            name = os.path.basename(path).encode()
            raw_sha = bytes.fromhex(sha1)        # SHA1 brut sur 20 octets

            # 4. Ajoute l’entrée à la liste
            entries.append(mode + b" " + name + b"\0" + raw_sha)

    # 5. Construit le contenu complet de l’objet tree
    tree_content = b"".join(entries)

    # 6. Crée l’en-tête (header) et concatène
    header = f"tree {len(tree_content)}\0".encode()
    store = header + tree_content

    # 7. Stocke l’objet (compression + écriture) et récupère son SHA
    tree_sha = compute_sha1_and_store(store)

    # 8. Affiche le SHA du tree
    print(tree_sha)

    return tree_sha
