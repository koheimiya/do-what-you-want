""" REPL for tagged ordered trees """
import editor

from taggedtree.core import save_tree, load_tree, show_tree, show_leaves, normalized_tree, sort_tree, read_tree

GREETINGS = "---- Running REPL on {} ----"
PROMPT = "REPL > "
HELP = "l: list current goals, s/S: show the entire tree, e: edit the tree, " +\
    "n/N: sort and normalize, w: save the tree, q: quit REPL"


def repl(fname: str):
    global_commands = {
        "l": _list,
        "s": _show,
        "S": lambda c: _show(c, show_done=True),
        "n": _normalize,
        "N": lambda c: _normalize(c, eager=True),
        "e": _edit,
        "w": _save,
        "q": _quit
    }

    tree = load_tree(fname)
    config = {"tree": tree, "fname": fname, "quit": False}
    print(GREETINGS.format(fname))
    while not config["quit"]:
        cmd = input(PROMPT)
        if cmd in global_commands:
            try:
                global_commands[cmd](config)
            except Exception as e:
                print("Failed:")
                print(e)
        else:
            print(HELP)


def _list(config: dict):
    print(show_leaves(config["tree"]))


def _show(config: dict, show_done: bool = False):
    print(show_tree(config["tree"], show_done=show_done))


def _edit(config: dict):
    msg = show_tree(config["tree"], show_done=True).encode("utf-8")
    result = editor.edit(contents=msg).decode("utf-8")
    config["tree"] = read_tree(result)
    _show(config, show_done=True)


def _normalize(config: dict, eager=False):
    config["tree"] = sort_tree(config["tree"])
    if eager:
        config["tree"] = normalized_tree(config["tree"])
    _show(config, show_done=True)


def _save(config: dict):
    save_tree(config["tree"], config["fname"])
    print("Saved.")


def _quit(config: dict):
    config["quit"] = True
