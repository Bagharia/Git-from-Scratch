import os
from ggit.utils import get_object, get_object_type
from ggit.commit import read_tree_recursive

def git_ls_tree(tree_sha):
    try:
        entries = read_tree_recursive(tree_sha)
    except Exception as e:
        print(f"fatal: tree object {tree_sha} not found or invalid: {e}")
        return

    for path, sha in entries.items():
        try:
            obj_type = get_object_type(sha)
            # Pour ls-tree, le mode est généralement récupéré de l'entrée tree elle-même,
            # mais notre read_tree_recursive ne le renvoie pas.
            # On utilise donc un mode fixe pour l'affichage, ce qui est suffisant ici.
            mode = "100644"  # Mode pour un fichier blob
            print(f"{mode} {obj_type} {sha}\t{path}")
        except Exception as e:
            print(f"could not read object {sha} for path {path}: {e}") 