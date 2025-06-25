import json
import os

INDEX_PATH = ".git/index"

def read_index():
    if not os.path.exists(INDEX_PATH):
        return []
    with open(INDEX_PATH, "r") as f:
        return json.load(f)

def write_index(entries):
    with open(INDEX_PATH, "w") as f:
        json.dump(entries, f, indent=2)

def add_to_index(path, oid, mode="100644"):
    index = read_index()
    index = [entry for entry in index if entry["path"] != path]  # Remove old version
    index.append({"path": path, "oid": oid, "mode": mode})
    write_index(index)

def remove_from_index(path):
    index = read_index()
    index = [entry for entry in index if entry["path"] != path]
    write_index(index)
