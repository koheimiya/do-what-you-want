import sys

from taggedtree.repl import dispatch_subcommand

from os.path import expanduser


def main():
    fname = expanduser("~/.tt.json")
    cmds = tuple(sys.argv[1:])
    dispatch_subcommand(fname, cmds)


if __name__ == "__main__":
    main()
