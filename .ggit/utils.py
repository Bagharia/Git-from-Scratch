import hashlib
import os
import zlib


def compute_sha1_and_store(content):
    import traceback
    header = f"blob {len(content)}\0".encode()
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
        traceback.print_exc()
        return None

    return sha
