""" REPL for tagged ordered trees """
from taggedtree.core import save_tree, load_tree, show_tree, show_leaves, subtrees, show_attr, attributes, Tree, Attr

GREETINGS = "---- TOT REPL ----"
PROMPT = "TOT > "
HELP = "l: list current goals, s: show the entire tree, b: browse the tree, w: save the tree, q: quit"


def repl(fname: str):
    global_commands = {
        "l": _list,
        "s": _show,
        "S": lambda c: _show(c, show_done=True),
        "e": _edit,
        "w": _save,
        "q": _quit
    }

    tree = load_tree(fname)
    config = {"tree": tree, "fname": fname, "quit": False}
    print(GREETINGS)
    while not config["quit"]:
        cmd = input(PROMPT)
        if cmd in global_commands:
            global_commands[cmd](config)
        else:
            print(HELP)


def _list(config: dict):
    print(show_leaves(config["tree"]))


def _show(config: dict, show_done: bool = False):
    print(show_tree(config["tree"], show_done=show_done))


def _edit(config: dict):
    prompt_edit = "EDIT > "
    help_edit = "hit enter to edit entry"

    curr = config["tree"]
    while True:
        _ls(curr)
        cmd = input(PROMPT)
    pass


def _ls(tree: Tree):
    print(show_attr(attributes(tree)))
    for i, st in enumerate(subtrees(tree)):
        print(f"    {i}: " + show_attr(attributes(st)))


def dumps_tree(tree: Tree, indent_level=0, buffer="") -> str:
    buffer += "    " * indent_level + dumps_attr(attributes(tree)) + "\n"
    for st in subtrees(tree):
        buffer = dumps_tree(st, indent_level=indent_level + 1, buffer=buffer)
    return buffer


def dumps_attr(attr: Attr) -> str:
    label, priority, tags, done = attr["label"], attr["priority"], attr["tags"], attr["done"]
    done_mark = "x" if done else " "
    tag_label = ''.join(' #' + t for t in tags)
    return f"+ [{priority}] {label}{tag_label} [{done_mark}]"


def loads_attr(s: str) -> Attr:
    pass


def loads_tree(s: str) -> Tree:

    pass


def _save(config: dict):
    save_tree(config["tree"], config["fname"])
    print("saved.")


def _quit(config: dict):
    config["quit"] = True
