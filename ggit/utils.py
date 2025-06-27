import hashlib
import os
import zlib


def compute_sha1_and_store(content: bytes, obj_type="blob") -> str:
    header = f"{obj_type} {len(content)}\0".encode()
    store = header + content
    sha = hashlib.sha1(store).hexdigest()

    dir_path = f".ggit/objects/{sha[:2]}"
    file_path = f"{dir_path}/{sha[2:]}"
    
    print(f"[DEBUG] dir_path = {dir_path}")
    print(f"[DEBUG] file_path = {file_path}")

    try:
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(zlib.compress(store))
    except Exception as e:
        print("[ERROR] Exception while writing object:")
        import traceback
        traceback.print_exc()
        return None

    return sha

def get_object(sha):
    dir_path = os.path.join(".ggit", "objects", sha[:2])
    file_path = os.path.join(dir_path, sha[2:])
    with open(file_path, "rb") as f:
        return zlib.decompress(f.read())

HEAD_PATH = os.path.join(".ggit", "HEAD")

def set_head(ref_or_sha):
    with open(HEAD_PATH, "w") as f:
        f.write(ref_or_sha)

def update_working_dir(tree_sha):
    import os
    from ggit.utils import get_object

    tree_data = get_object(tree_sha)  # bytes
    print(tree_data)

    i = 0
    while i < len(tree_data):
        # lire mode (jusqu'à espace)
        space_idx = tree_data.find(b' ', i)
        if space_idx == -1:
            break  # fin
        mode = tree_data[i:space_idx].decode()  # doit être une chaîne ASCII
        i = space_idx + 1

        # lire filename (jusqu'à null)
        null_idx = tree_data.find(b'\x00', i)
        if null_idx == -1:
            break  # fin
        filename = tree_data[i:null_idx].decode()
        i = null_idx + 1

        # lire SHA1 (20 bytes binaires)
        sha_bin = tree_data[i:i+20]
        if len(sha_bin) < 20:
            raise Exception("SHA1 incomplet dans l'objet tree")
        sha = sha_bin.hex()
        i += 20

        content = get_object(sha)
        if mode.startswith("100"):  # fichier blob
            # Retirer l'entête blob <size>\0
            body = content.split(b'\x00', 1)[1]
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(body)
        elif mode == "40000":  # dossier (tree)
            os.makedirs(filename, exist_ok=True)
            update_working_dir(sha)


def get_object_type(sha):
    path = os.path.join(".ggit", "objects", sha[:2], sha[2:])
    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())
        header = raw.split(b'\x00', 1)[0]
        return header.decode().split()[0]  # 'blob', 'tree', 'commit', etc.

