""" REPL for tagged ordered trees """
from typing import Optional, Tuple, List

import editor

from taggedtree.core import save_tree, load_tree, show_tree, show_leaves, subtrees, show_attr, attributes, Tree, Attr, \
    valid_priority, new_attr, valid_tag, root, new_tree

GREETINGS = "---- TOT REPL ----"
PROMPT = "TOT > "
HELP = "l: list current goals, s/S: show the entire tree, e: edit the tree, w: save the tree, q: quit REPL"


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
    msg = dumps_tree(config["tree"]).encode("utf-8")
    result = editor.edit(contents=msg).decode("utf-8")
    try:
        config["tree"] = loads_tree(result)
    except Exception as e:
        print(e)
        print("Parsing failed. Fall back to the original.")


def dumps_tree(tree: Tree, indent="", buffer="", last=True) -> str:
    buffer += indent + dumps_attr(attributes(tree)) + "\n"
    n = len(subtrees(tree))
    for i, st in enumerate(subtrees(tree)):
        last_child = i == n - 1
        buffer = dumps_tree(st, indent=indent + "   |", buffer=buffer, last=last_child)
    if not last and n > 1:
        buffer += indent + "\n"
    return buffer


def dumps_attr(attr: Attr) -> str:
    label, priority, tags, done = attr["label"], attr["priority"], attr["tags"], attr["done"]
    done_mark = "x" if done else " "
    tag_label = ''.join(' #' + t for t in tags)
    return f"- [{done_mark}{priority}] {label}{tag_label}"


def loads_attr(s: str) -> Tuple[str, Optional[Attr]]:

    def split_by(s: str, delim: List[str]) -> List[str]:
        res = []
        for d in delim:
            i = s.find(d)
            if i == -1:
                break
            res.append(s[:i])
            s = s[i + len(d):]
        res.append(s)
        return res

    delimiters = ["- [", "] "]
    ss = split_by(s, delimiters)
    if len(ss) == 1:
        return ss[0], None
    elif len(ss) != 3:
        raise ValueError(f"Unrecognized token: {s} -> {ss}")
    indent, done_priority, label_tags = ss
    done_mark, priority = done_priority[:1], done_priority[1:]

    assert done_mark in " x"
    done = done_mark == "x"
    assert valid_priority(priority)
    label, *tags = map(str.strip, label_tags.split("#"))
    assert all(valid_tag(t) for t in tags)
    return indent, new_attr(label=label, priority=priority, tags=tags, done=done)


def loads_tree(s: str, tree_stack: List[Tuple[Optional[str], Tree]] = None) -> Tree:
    if tree_stack is None:
        tree_stack = []

    if s == "":
        (_, root_tree), *_ = tree_stack
        return root_tree

    sp = s.find("\n")
    if sp == -1:
        sp = len(s) + 1
    line = s[:sp]
    s_next = s[sp + 1:]
    indent, attr = loads_attr(line)

    if attr is not None:
        tree = new_tree(attr)

        # find parent
        if tree_stack:
            prev_indent, _ = tree_stack[-1]
            if not (indent.startswith(prev_indent) and indent != prev_indent):
                while True:
                    prev_indent, prev_tree = tree_stack.pop()
                    if indent == prev_indent:
                        break
            _, parent = tree_stack[-1]
            subtrees(parent).append(tree)

        # append a node
        tree_stack.append((indent, tree))

    return loads_tree(s_next, tree_stack)


def _save(config: dict):
    save_tree(config["tree"], config["fname"])
    print("Saved.")


def _quit(config: dict):
    config["quit"] = True
