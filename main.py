import sys
from mygit.commands import add, ls_files, rm

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "add":
        add.add(args[1:])
    elif args[0] == "ls-files":
        ls_files.ls_files()
    elif args[0] == "rm":
        rm.rm(args[1:])
    else:
        print("Commande inconnue :", args[0])

def main():
    print("Welcome to Git from Scratch")

if __name__ == "__main__":
    main()
