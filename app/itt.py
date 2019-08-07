from taggedtree.repl import repl

from os.path import expanduser


def main():
    repl(expanduser("~/.tt.json"))


if __name__ == "__main__":
    main()
