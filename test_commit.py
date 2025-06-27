from ggit.write_tree import write_tree
from ggit.commit_tree import commit_tree
from ggit.utils import get_object_type

tree_sha = write_tree()  # Génère l'arbre à partir de l'index (ajout de fichiers)
if not tree_sha:
    print("Rien à committer, index vide")
    exit(1)

message = "Test commit automatique"
commit_sha = commit_tree(tree_sha, message)

print(f"SHA créé : {commit_sha}")
print(f"Type de l'objet créé : {get_object_type(commit_sha)}")
