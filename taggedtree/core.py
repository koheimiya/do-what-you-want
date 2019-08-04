""" Ordered tree with tags """

import json
from copy import deepcopy
from typing import Dict, Any, Tuple, List, Optional, Set

Tree = Tuple['Attr', List['Tree']]
Attr = Dict[str, Any]


def root() -> Attr:
    return new_attr("root", priority="0")


def new_attr(label: str, priority: str = "", tags: List[str] = None, done: bool = False) -> Attr:
    if tags is None:
        tags = []
    assert valid_priority(priority)
    assert all(valid_tag(t) for t in tags)
    return {"label": label, "priority": priority, "tags": tags, "done": done}


def valid_priority(p: str) -> bool:
    try:
        float(p)
    except ValueError:
        pass
    else:
        return True

    return p == ""


def valid_tag(tag: str) -> bool:
    return all(c not in tag for c in [" ", "　", "#"])


def underscore_label(label: str) -> str:
    return label.strip().replace(' ', '_').replace('　', '_')


def new_tree(attr: Attr, subtrees: List[Tree] = None) -> Tree:
    if subtrees is None:
        subtrees = []
    return attr, subtrees


def is_done(attr: Attr):
    return attr["done"]


def normalized_tree(tree: Tree) -> Tree:
    _children = [normalized_tree(t) for t in subtrees(tree)]
    _attr = deepcopy(attributes(tree))
    if subtrees(tree):
        _attr["done"] = all(is_done(attributes(t)) for t in _children)
    return new_tree(_attr, _children)


def sort_tree(tree: Tree) -> Tree:
    children = subtrees(tree)
    if not children:
        return deepcopy(tree)

    _children = [sort_tree(t) for p, t in children]
    return new_tree(attributes(tree), sorted(_children, key=_key_sort_tree))


def _key_sort_tree(tree: Tree) -> float:
    priority = attributes(tree)["priority"]
    try:
        return float(priority)
    except ValueError:
        if priority == "":
            return float("inf")
        else:
            raise ValueError("priority= {}".format(priority))


def attributes(tree: Tree) -> Attr:
    attr, _ = tree
    return attr


def subtrees(tree: Tree) -> List[Tree]:
    _, st = tree
    return st


def save_tree(tree: Tree, fname: str):
    with open(fname, "w") as f:
        json.dump(tree, f)


def load_tree(fname: str) -> Tree:
    with open(fname, "r") as f:
        _tree = json.load(f)
    return _dejsonize(_tree)


def _dejsonize(tree) -> Tree:
    return new_tree(attributes(tree), [_dejsonize(t) for t in subtrees(tree)])


def show_tree(tree: Tree, prefix: str = "", last: bool = True, show_done: bool = False) -> str:
    s = prefix + "+- " + show_attr(attributes(tree)) + "\n"

    prefix_new = prefix + ("|   " if not last else "    ")
    children = subtrees(tree) if show_done else [t for t in subtrees(tree) if not is_done(attributes(t))]
    n_children = len(children)
    for i, child in enumerate(children):
        last_child = i == n_children - 1
        s += show_tree(child, prefix=prefix_new, last=last_child, show_done=show_done)
        if last_child and not last:
            s += prefix_new + "\n"
    return s


def show_attr(attr: Attr) -> str:
    done_mark = "(DONE) " if attr["done"] else ""
    s = done_mark + "[" + attr["priority"] + "] "
    s += attr["label"]
    for t in attr["tags"]:
        s += " #" + t
    return s


def show_leaves(tree: Tree, tags: list=None, address=" ", buffer="", urgent_only=True, show_done=False):
    if tags is None:
        tags = []

    if not subtrees(tree):
        buffer += show_attr(attributes(tree)) + ''.join((" #" + t) for t in tags) + address + "\n"
    else:
        tags = tags + attributes(tree)["tags"]
        address = address + "/" + underscore_label(attributes(tree)["label"])
        min_p = min(attributes(t)["priority"] for t in subtrees(tree) if not attributes(t)["done"])
        for st in subtrees(tree):
            if urgent_only and attributes(st)["priority"] > min_p:
                continue
            if not show_done and attributes(st)["done"]:
                continue
            buffer = show_leaves(st, tags, address, buffer)
    return buffer
