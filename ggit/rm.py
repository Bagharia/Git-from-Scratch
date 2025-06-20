import os
INDEX_PATH = ".ggit/index"

def git_rm(path_list):
    # 1. Charger l’index en mémoire
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r") as f:
            entries = [line.rstrip().split(" ", 1) for line in f]
            # entries = [[sha1, "chemin/fichier"], ...]
    else:
        entries = []

    # 2. Traiter chaque fichier demandé
    removed_any = False
    for victim in path_list:
        # a) Supprimer physiquement le fichier s’il existe
        if os.path.isfile(victim):
            os.remove(victim)

        # b) Filtrer l’index : conserver tout sauf le victim
        before = len(entries)
        entries = [e for e in entries if e[1] != victim]
        if len(entries) < before:
            removed_any = True
        else:
            print(f"warning: {victim} not in index")

    # 3. Ré‑écrire l’index s’il a changé
    if removed_any:
        with open(INDEX_PATH, "w") as f:
            for sha, path in entries:
                f.write(f"{sha} {path}\n")
        print("rm:", ", ".join(path_list))
    else:
        print("nothing removed")
