import os, time
from ggit.write_tree import write_tree
from ggit.commit_tree import commit_tree
from ggit.utils import get_object

def read_tree_recursive(tree_sha, prefix=""):
    entries = {}
    tree_data = get_object(tree_sha)
    i = 0
    while i < len(tree_data):
        space_idx = tree_data.find(b' ', i)
        if space_idx == -1:
            break
        mode = tree_data[i:space_idx].decode()
        i = space_idx + 1

        null_idx = tree_data.find(b'\x00', i)
        if null_idx == -1:
            break
        filename = tree_data[i:null_idx].decode()
        i = null_idx + 1

        sha_bin = tree_data[i:i+20]
        if len(sha_bin) < 20:
            raise Exception("SHA1 incomplet dans l'objet tree")
        sha = sha_bin.hex()
        i += 20

        full_path = os.path.join(prefix, filename)
        if mode == "40000":  # dossier (tree)
            entries.update(read_tree_recursive(sha, full_path))
        else:
            entries[full_path] = sha
    return entries

def _read_HEAD():
    head_ref = ".ggit/HEAD"
    if not os.path.exists(head_ref):
        return None
    with open(head_ref) as f:
        ref = f.read().strip()
    if ref.startswith("ref: "):
        ref_path = os.path.join(".ggit", ref[5:])
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                return f.read().strip()
    return None

def _update_HEAD(new_sha):
    with open(".ggit/HEAD") as f:
        ref = f.read().strip()
    if not ref.startswith("ref: "):
        raise RuntimeError("Unsupported HEAD format")
    ref_path = os.path.join(".ggit", ref[5:])
    with open(ref_path, "w") as f:
        f.write(new_sha)

def write_index_from_tree(tree_sha):
    entries = read_tree_recursive(tree_sha)
    with open(".ggit/index", "w") as f:
        for path, sha in entries.items():
            f.write(f"{sha} {path}\n")

def git_commit(message: str):
    tree_sha = write_tree()           # crée l’arbre depuis l’index
    if not tree_sha:                  # write_tree peut retourner None si index vide
        print("Nothing to commit.")
        return
    parent = _read_HEAD()             # HEAD actuel (None si premier commit)

    commit_sha = commit_tree(tree_sha, message, parent)
    _update_HEAD(commit_sha)          # avance HEAD

    # Met à jour l’index pour refléter l’état du commit
    write_index_from_tree(tree_sha)

    print(f"[commit] {commit_sha}")