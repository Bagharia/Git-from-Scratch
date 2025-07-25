import argparse
from ggit.init import git_init
from ggit.hash_object import hash_object
from ggit.cat_file import cat_file
from ggit.write_tree import write_tree     
from ggit.commit_tree import commit_tree
from ggit.add import git_add
from ggit.rm import git_rm
from ggit.commit import git_commit  
from ggit.status import git_status
from ggit.checkout import git_checkout
from ggit.log import git_log
from ggit.ls_files import git_ls_files
from ggit.ls_tree import git_ls_tree
from ggit.show_ref import git_show_ref
from ggit.rev_parse import git_rev_parse

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

    # remove
    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("paths", nargs="+") 

    # commit  
    commit_porcelain = subparsers.add_parser("commit")
    commit_porcelain.add_argument("-m", "--message", required=True)

    # status
    subparsers.add_parser("status")

    # checkout
    checkout_parser = subparsers.add_parser("checkout")
    checkout_parser.add_argument("target")
    checkout_parser.add_argument("-b", "--branch", action="store_true")

    # log
    subparsers.add_parser("log")

    # ls-files
    subparsers.add_parser("ls-files")

    # ls-tree
    ls_tree_parser = subparsers.add_parser("ls-tree")
    ls_tree_parser.add_argument("tree_sha")

    # show-ref
    subparsers.add_parser("show-ref")

    # rev-parse
    rev_parse_parser = subparsers.add_parser("rev-parse")
    rev_parse_parser.add_argument("ref")

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
    elif args.command == "rm":
        git_rm(args.paths)
    elif args.command == "commit":
        git_commit(args.message)
    elif args.command == "status":
        git_status()
    elif args.command == "checkout":
        from ggit.checkout import git_checkout
        git_checkout(args.target, args.branch)
    elif args.command == "log":
        git_log()
    elif args.command == "ls-files":
        git_ls_files()
    elif args.command == "ls-tree":
        git_ls_tree(args.tree_sha)
    elif args.command == "show-ref":
        git_show_ref()
    elif args.command == "rev-parse":
        git_rev_parse(args.ref)
    else:
        print(f"Unknown command {args.command}")

if __name__ == "__main__":
    main()
