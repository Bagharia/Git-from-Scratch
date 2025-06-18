import os
import hashlib
import time
from ggit.utils import compute_sha1_and_store


def commit_tree(tree_sha: str, message: str, parent: str | None = None):
    """
    Crée un objet commit pointant sur `tree_sha`.
    Affiche l'OID SHA‑1 du commit.
    """

    # Valider que le tree existe dans .ggit/objects/
    tree_path = os.path.join(".ggit", "objects", tree_sha[:2], tree_sha[2:])
    if not os.path.exists(tree_path):
        print(f"fatal: bad tree object {tree_sha}")
        return

    # Construire le corps du commit (utf‑8 → bytes)
    timestamp = int(time.time())
    tz        = "+0000"                       # UTC pour simplifier
    author    = f"You <you@example.com> {timestamp} {tz}"
    committer = author

    lines = [f"tree {tree_sha}"]
    if parent:
        lines.append(f"parent {parent}")
    lines.append(f"author {author}")
    lines.append(f"committer {committer}")
    lines.append("")                          # ligne vide séparatrice
    lines.append(message.rstrip() + "\n")     # message + LF final

    body = "\n".join(lines).encode()

    # Header + concaténation
    store = f"commit {len(body)}\0".encode() + body

    # Écrire l'objet commit et afficher le SHA
    commit_sha = compute_sha1_and_store(store)
    print(commit_sha)
