import os, time
from ggit.write_tree import write_tree
from ggit.commit_tree import commit_tree

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

def git_commit(message: str):
    tree_sha = write_tree()           # crée l’arbre depuis l’index
    if not tree_sha:                  # write_tree peut retourner None si index vide
        print("Nothing to commit.")
        return
    parent = _read_HEAD()             # HEAD actuel (None si premier commit)

    commit_sha = commit_tree(tree_sha, message, parent)
    _update_HEAD(commit_sha)          # avance HEAD

    print(f"[commit] {commit_sha}")
