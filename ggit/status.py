import os
import hashlib
from ggit.utils import get_object
from ggit.commit import read_tree_recursive

def read_index():
    index_path = ".ggit/index"
    index_files = {}
    if not os.path.exists(index_path):
        return index_files
    with open(index_path, "r") as f:
        for line in f:
            sha, path = line.strip().split(" ", 1)
            index_files[path] = sha
    return index_files

def read_head_tree():
    head_path = ".ggit/HEAD"
    if not os.path.exists(head_path):
        return {}

    with open(head_path) as f:
        ref = f.read().strip()

    if ref.startswith("ref: "):
        ref = ref[5:].strip()

    # Si HEAD pointe vers une ref
    if ref.startswith("refs/"):
        ref_path = os.path.join(".ggit", ref)
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                commit_sha = f.read().strip()
        else:
            return {}

    else:  # Detached HEAD (direct SHA)
        commit_sha = ref

    # Extraire tree SHA du commit
    try:
        commit_data = get_object(commit_sha)
        # commit_data = b"commit <len>\0<body>"
        header, body = commit_data.split(b'\x00', 1)
        lines = body.decode().splitlines()
        tree_line = next(line for line in lines if line.startswith("tree "))
        tree_sha = tree_line.split()[1]
    except Exception:
        return {}

    # Lire les entrées tree en utilisant la fonction partagée
    return read_tree_recursive(tree_sha)

def read_working_dir():
    working_files = {}

    for root, dirs, files in os.walk('.'):
        if '.ggit' in dirs:
            dirs.remove('.ggit')
        if '.git' in dirs:
            dirs.remove('.git')
        if 'ggit' in dirs:
            dirs.remove('ggit')
        if 'tests' in dirs:
            dirs.remove('tests')
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                data = f.read()
            header = f"blob {len(data)}\0".encode()
            store = header + data
            sha = hashlib.sha1(store).hexdigest()
            rel_path = os.path.relpath(path, '.')
            working_files[rel_path] = sha

    return working_files

def git_status():
    print("=== Git Status ===")

    head_files = read_head_tree()
    index_files = read_index()
    working_files = read_working_dir()

    # Fichiers modifiés et non ajoutés
    modified = []
    # Fichiers ajoutés à l'index mais modifiés depuis (staged)
    staged = []
    # Fichiers non suivis
    untracked = []

    for path, sha in working_files.items():
        if path in index_files:
            if sha != index_files[path]:
                # contenu diffère entre index et working dir => modifié (unstaged)
                modified.append(path)
        else:
            # fichier présent dans working dir mais pas dans index
            untracked.append(path)

    for path, sha in index_files.items():
        head_sha = head_files.get(path)
        if head_sha != sha:
            # fichier diffère entre index et HEAD => staged
            staged.append(path)

    # Affichage simple
    if staged:
        print("Changes to be committed:")
        for f in staged:
            print(f"  modified: {f}")
    if modified:
        print("Changes not staged for commit:")
        for f in modified:
            print(f"  modified: {f}")
    if untracked:
        print("Untracked files:")
        for f in untracked:
            print(f"  {f}")
    if not (staged or modified or untracked):
        print("Working directory clean.")
