import os

def git_rev_parse(ref):
    # 1. HEAD
    if ref == "HEAD":
        head_path = os.path.join(".ggit", "HEAD")
        if not os.path.exists(head_path):
            print("fatal: HEAD not found")
            return
        with open(head_path) as f:
            val = f.read().strip()
        if val.startswith("ref: "):
            ref_path = os.path.join(".ggit", val[5:])
            if os.path.exists(ref_path):
                with open(ref_path) as f:
                    sha = f.read().strip()
                print(sha)
                return
            else:
                print("fatal: ref not found")
                return
        else:
            print(val)
            return

    # 2. Branche locale
    branch_path = os.path.join(".ggit", "refs", "heads", ref)
    if os.path.exists(branch_path):
        with open(branch_path) as f:
            sha = f.read().strip()
        print(sha)
        return

    # 3. SHA complet ou abrégé
    objects_dir = os.path.join(".ggit", "objects")
    if len(ref) >= 4 and len(ref) <= 40:
        for d in os.listdir(objects_dir):
            if len(d) != 2:
                continue
            for f in os.listdir(os.path.join(objects_dir, d)):
                sha = d + f
                if sha.startswith(ref):
                    print(sha)
                    return
    print(f"fatal: ambiguous argument {ref}: unknown revision or path not in the working tree.") 