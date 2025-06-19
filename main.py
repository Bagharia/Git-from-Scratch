import argparse
from ggit.init import git_init
from ggit.hash_object import hash_object
from ggit.cat_file import cat_file
from ggit.write_tree import write_tree     
from ggit.commit_tree import commit_tree
from ggit.add import git_add

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    subparsers.add_parser("init")

    # hash-object
    hash_parser = subparsers.add_parser("hash-object")
    hash_parser.add_argument("path")

    # cat-file
    cat_parser = subparsers.add_parser("cat-file")
    cat_parser.add_argument("sha")

    # write-tree
    subparsers.add_parser("write-tree")   

    # commit-tree
    commit_parser = subparsers.add_parser("commit-tree")
    commit_parser.add_argument("tree_sha")
    commit_parser.add_argument("-m", "--message", required=True)
    commit_parser.add_argument("-p", "--parent")

    # add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("path")

    args = parser.parse_args()

    if args.command == "init":
        git_init()
    elif args.command == "hash-object":
        hash_object(args.path)
    elif args.command == "cat-file":
        cat_file(args.sha)
    elif args.command == "write-tree":
        write_tree()
    elif args.command == "commit-tree":
        from ggit.commit_tree import commit_tree
        commit_tree(args.tree_sha, args.message, args.parent)
    elif args.command == "add":
        git_add(args.path)
    else:
        print(f"Unknown command {args.command}")

if __name__ == "__main__":
    main()
