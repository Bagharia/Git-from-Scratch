import os

def git_show_ref():
    refs_dir = os.path.join('.ggit', 'refs', 'heads')
    if not os.path.exists(refs_dir):
        print('(aucune ref)')
        return
    for ref_name in os.listdir(refs_dir):
        ref_path = os.path.join(refs_dir, ref_name)
        with open(ref_path, 'r') as f:
            sha = f.read().strip()
        print(f"{sha} refs/heads/{ref_name}") 