import hashlib
import os
import zlib

def compute_sha1_and_store(content: bytes, obj_type="blob") -> str:
    header = f"{obj_type} {len(content)}\0".encode()
    store = header + content
    sha = hashlib.sha1(store).hexdigest()

    dir_path = f".ggit/objects/{sha[:2]}"
    file_path = f"{dir_path}/{sha[2:]}"

    print(f"[DEBUG] Writing object to {file_path}")

    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(zlib.compress(store))

    return sha

def get_object(sha):
    dir_path = os.path.join(".ggit", "objects", sha[:2])
    file_path = os.path.join(dir_path, sha[2:])
    with open(file_path, "rb") as f:
        decompressed = zlib.decompress(f.read())

    # On retourne le contenu complet (header + body)
    return decompressed

HEAD_PATH = os.path.join(".ggit", "HEAD")

def set_head(ref_or_sha):
    with open(HEAD_PATH, "w") as f:
        f.write(ref_or_sha)

def update_working_dir(tree_sha):
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

        content = get_object(sha)
        if mode.startswith("100"):  # fichier blob
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
        return header.decode().split()[0]
