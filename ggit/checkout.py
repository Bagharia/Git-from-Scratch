import os
from ggit.utils import get_object, set_head, update_working_dir, get_object_type

REFS_PATH = os.path.join(".ggit", "refs", "heads")

def resolve_target_to_sha(target):
    branch_path = os.path.join(REFS_PATH, target)
    if os.path.exists(branch_path):
        with open(branch_path, "r") as f:
            return f.read().strip()
    return target  # on suppose que c’est un SHA direct si ce n’est pas une branche

def git_checkout(target, new_branch=False):
    if new_branch:
        branch_path = os.path.join(REFS_PATH, target)
        head_sha = get_current_commit_sha()
        with open(branch_path, "w") as f:
            f.write(head_sha)
        set_head(f"refs/heads/{target}")
        print(f"[branch created] {target} -> {head_sha}")
        return

    # Si target est une branche, on récupère le commit pointé par cette branche
    branch_path = os.path.join(REFS_PATH, target)
    if os.path.exists(branch_path):
        with open(branch_path) as f:
            commit_sha = f.read().strip()
    else:
        commit_sha = target  # sinon on suppose que c’est un SHA

    print(f"[DEBUG] Object {commit_sha} is of type: {get_object_type(commit_sha)}")
    print(f"[DEBUG] Checkout commit_sha: {commit_sha} (len={len(commit_sha)})")

    try:
        tree_sha, _ = parse_commit(commit_sha)
    except Exception as e:
        print(f"[ERROR] Failed to parse commit {commit_sha}: {e}")
        return

    try:
        get_object(tree_sha)
    except FileNotFoundError:
        print(f"[ERROR] Tree object {tree_sha} not found, cannot checkout.")
        return

    # Update working dir
    update_working_dir(tree_sha)

    # Update HEAD
    if os.path.exists(branch_path):
        set_head(f"refs/heads/{target}")
    else:
        set_head(commit_sha)  # detached HEAD

    print(f"[checked out] {target}")


def parse_commit(commit_sha):
    path = f".ggit/objects/{commit_sha[:2]}/{commit_sha[2:]}"
    with open(path, "rb") as f:
        import zlib
        raw = zlib.decompress(f.read())

    header, body = raw.split(b'\x00', 1)
    obj_type = header.decode().split()[0]

    if obj_type != "commit":
        raise ValueError(f"[ERREUR] SHA {commit_sha} n'est pas un commit (type = {obj_type})")

    data = body.decode()

    lines = data.splitlines()
    tree_lines = [line for line in lines if line.startswith("tree ")]
    if not tree_lines:
        raise ValueError(f"[ERREUR] Objet {commit_sha} n'est pas un commit valide.")

    tree_sha = tree_lines[0].split()[1]
    return tree_sha, lines
