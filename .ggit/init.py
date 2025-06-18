import os

def git_init():
    if os.path.exists(".ggit"):
        print("fatal: already a git repository")
        return

    # Création des dossiers de base
    os.makedirs(".ggit/objects", exist_ok=True)
    os.makedirs(".ggit/refs/heads", exist_ok=True)

    # Fichier HEAD qui pointe vers la branche par défaut
    with open(".ggit/HEAD", "w") as f:
        f.write("ref: refs/heads/master\n")

    # Référence vide pour la branche master
    open(".ggit/refs/heads/master", "w").close()
    print("Initialized empty Git repository in .ggit/")
