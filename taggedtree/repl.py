""" REPL for tagged ordered trees """
import os
import sys
from typing import List, Dict, Tuple, Any

import editor

from taggedtree.core import save_tree, load_tree, show_tree, show_leaves, normalized_tree, sort_tree, read_tree, \
    new_tree, root

GREETINGS = "---- Running REPL on {} ----"
PROMPT = "REPL > "
HELP = "l: list current goals, s/S: show the entire tree, e: edit the tree, " +\
    "n/N: sort and normalize, q: quit REPL"


def repl(fname: str):
    repl_commands = {
        "l": _list,
        "s": _show,
        "S": lambda c: _show(c, show_done=True),
        "N": _update,
        "e": _edit,
        "q": _quit
    }

    if os.path.exists(fname):
        tree = load_tree(fname)
    else:
        tree = new_tree(root())

    config = {"tree": tree, "fname": fname, "quit": False}
    print(GREETINGS.format(fname))
    while not config["quit"]:
        cmd = input(PROMPT)
        if cmd in repl_commands:
            try:
                repl_commands[cmd](config)
            except Exception as e:
                print("Failed:")
                print(e)
        else:
            print(HELP)
            
            
def dispatch_subcommand(fname: str, cmds: Tuple[str]):
    help_subcommands = """
    list: list tasks,
    show [all]: show goal tree
    update: update done/undone status recursively
    edit: edit goal tree
    """

    sub_commands = {
        ("list",): _list,
        ("show",): _show,
        ("show", "all"): lambda c: _show(c, show_done=True),
        ("update",): _update,
        ("edit",): _edit,
    }

    def match(args: Tuple[str], commands: Dict[Tuple[str], Any]) -> Any:
        for k in commands:
            if k == args:
                return commands[k]
        else:
            print(f"Subcommand not recognized: {args}")
            print(help_subcommands)

    if os.path.exists(fname):
        tree = load_tree(fname)
    else:
        print(f"Task file not found. Creating one at {fname}")
        tree = new_tree(root())

    config = {"tree": tree, "fname": fname, "quit": False}
    sub = match(cmds, sub_commands)
    try:
        sub(config)
    except Exception as e:
        print("Failed:")
        print(e)


def _list(config: dict):
    print(show_leaves(config["tree"]))


def _show(config: dict, show_done: bool = False):
    print(show_tree(config["tree"], show_done=show_done))


def _edit(config: dict):
    msg = show_tree(config["tree"], show_done=True).encode("utf-8")
    result = editor.edit(contents=msg).decode("utf-8")
    config["tree"] = read_tree(result)
    __sort(config)
    _show(config, show_done=True)
    __save(config)


def _update(config: dict):
    config["tree"] = normalized_tree(config["tree"])
    _show(config, show_done=True)
    __save(config)


def _quit(config: dict):
    config["quit"] = True


def __sort(config: dict):
    config["tree"] = sort_tree(config["tree"])


def __save(config: dict):
    save_tree(config["tree"], config["fname"])
