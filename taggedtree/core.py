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
    assert valid_priority(priority), f"invalid priority: {priority}"
    assert all(valid_tag(t) for t in tags), f"invalid tags: {tags}"
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

    _children = [sort_tree(t) for t in children]
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
    done_mark = "x" if attr["done"] else " "
    s = "[" + done_mark + attr["priority"] + "] "
    s += attr["label"]
    for t in attr["tags"]:
        s += " #" + t
    return s


def read_attr(s: str) -> Tuple[str, Optional[Attr]]:

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
    indent = indent.replace("|", " ").replace("+", " ")
    done_mark, priority = done_priority[:1], done_priority[1:]

    assert done_mark in " x", f"invalid done_mark: {done_mark}"
    done = done_mark == "x"
    assert valid_priority(priority), f"invalid priority: {priority}"
    label, *tags = map(str.strip, label_tags.split("#"))
    assert all(valid_tag(t) for t in tags), f"invalid tags: {tags}"
    return indent, new_attr(label=label, priority=priority, tags=tags, done=done)


def read_tree(s: str, tree_stack: List[Tuple[Optional[str], Tree]] = None) -> Tree:
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
    indent, attr = read_attr(line)

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

    return read_tree(s_next, tree_stack)


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
