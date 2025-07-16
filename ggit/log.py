import os
from ggit.utils import get_object

def git_log():
    # 1. Lire HEAD
    head_path = ".ggit/HEAD"
    if not os.path.exists(head_path):
        print("fatal: not a git repository (or no HEAD)")
        return
    with open(head_path) as f:
        ref = f.read().strip()
    if ref.startswith("ref: "):
        ref_path = os.path.join(".ggit", ref[5:])
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                commit_sha = f.read().strip()
        else:
            print("fatal: HEAD points to an unknown ref")
            return
    else:
        commit_sha = ref  # detached HEAD

    # 2. Parcourir les commits
    while commit_sha:
        try:
            data = get_object(commit_sha)
        except Exception:
            print(f"fatal: commit {commit_sha} not found")
            break
        # data = b'commit <len>\0<body>'
        if b'\x00' not in data:
            print(f"[ERREUR] L'objet {commit_sha} n'est pas au format attendu (pas de header/body).")
            break
        header, body = data.split(b'\x00', 1)
        lines = body.decode().splitlines()
        # Extraire le message (après la ligne vide)
        try:
            empty_idx = lines.index("")
            message = lines[empty_idx+1] if empty_idx+1 < len(lines) else ""
        except ValueError:
            message = ""
        # Afficher SHA et message
        print(f"commit {commit_sha}\n    {message}")
        # Chercher le parent
        parent_lines = [l for l in lines if l.startswith("parent ")]
        if parent_lines:
            commit_sha = parent_lines[0].split()[1]
        else:
            break 