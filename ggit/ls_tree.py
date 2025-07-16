import os
from ggit.utils import get_object, get_object_type

def git_ls_tree(tree_sha):
    try:
        tree_data = get_object(tree_sha)
    except Exception:
        print(f"fatal: tree object {tree_sha} not found")
        return

    # On enlève le header (ex: "tree 123\0") et on ne garde que les données binaires utiles
    nul_index = tree_data.find(b'\x00')
    if nul_index == -1:
        print("[ERREUR] Objet tree mal formé (pas de header terminator)")
        return
    tree_data = tree_data[nul_index + 1:]

    i = 0
    while i < len(tree_data):
        # Trouver espace qui sépare mode du nom de fichier
        space_idx = tree_data.find(b' ', i)
        if space_idx == -1:
            break
        mode = tree_data[i:space_idx].decode()
        i = space_idx + 1

        # Trouver octet nul qui sépare nom de fichier du SHA1
        null_idx = tree_data.find(b'\x00', i)
        if null_idx == -1:
            break
        filename = tree_data[i:null_idx].decode()
        i = null_idx + 1

        # Lire 20 octets du SHA1 binaire
        sha_bin = tree_data[i:i+20]
        if len(sha_bin) < 20:
            print(f"[ERREUR] SHA1 incomplet pour {filename}")
            break
        sha = sha_bin.hex()
        i += 20

        # Déterminer le type d'objet
        obj_type = get_object_type(sha)

        print(f"{mode} {obj_type} {sha}\t{filename}") 