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
            mode = b"100644"                     # fichier « normal »
            filename = path.encode()  # encodage en bytes UTF-8
            sha_bin = bytes.fromhex(sha)

            # 4. Ajoute l’entrée à la liste
            entry = mode + b" " + filename+ b"\x00" + sha_bin
            entries.append(entry)

    # 5. Construit le contenu complet de l’objet tree
    tree_content = b"".join(entries)
    # Attention : on doit passer le contenu *sans* header à compute_sha1_and_store car la fonction
    # elle-même ajoute le header (cf. ta fonction)
    tree_sha = compute_sha1_and_store(tree_content, obj_type="tree")
    print(tree_sha)
    return tree_sha

    # # 6. Crée l’en-tête (header) et concatène
    # header = f"tree {len(tree_content)}\0".encode()
    # store = header + tree_content

    # # 7. Stocke l’objet (compression + écriture) et récupère son SHA
    # tree_sha = compute_sha1_and_store(tree_content, obj_type="tree")

    # # 8. Affiche le SHA du tree
    # print(tree_sha)

    # return tree_sha
