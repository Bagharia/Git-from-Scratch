import os

INDEX_PATH = ".ggit/index"

def git_ls_files():
    if not os.path.exists(INDEX_PATH):
        print("(index vide)")
        return
    with open(INDEX_PATH, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                _, path = parts
                print(path) 