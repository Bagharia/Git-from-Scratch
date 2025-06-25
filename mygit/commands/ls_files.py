from mygit import index

def ls_files():
    entries = index.read_index()
    for entry in entries:
        print(entry["path"])
