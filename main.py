import argparse
from ggit.init import git_init
from ggit.hash_object import hash_object
from ggit.cat_file import cat_file
from ggit.write_tree import write_tree     

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

    args = parser.parse_args()

    if args.command == "init":
        git_init()
    elif args.command == "hash-object":
        hash_object(args.path)
    elif args.command == "cat-file":
        cat_file(args.sha)
    elif args.command == "write-tree":
        write_tree()
    else:
        print(f"Unknown command {args.command}")

if __name__ == "__main__":
    main()
