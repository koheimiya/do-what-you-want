from .core import new_tree, new_attr, root, show_tree, read_tree, sort_tree, save_tree, load_tree


def sample_tree():
    tree = new_tree(root(), [
        new_tree(new_attr("study"), [
            new_tree(new_attr("xxx"), [
                new_tree(new_attr("oracle", priority="1", done=True)),
                new_tree(new_attr("empirical", priority="2", tags=["SOME_CONF"])),
            ]),
            new_tree(new_attr("wow", priority="1")),
        ]),
        new_tree(new_attr("mental"), [
            new_tree(new_attr("movie")),
            new_tree(new_attr("piano")),
        ]),
        new_tree(new_attr("physical")),
    ])
    return tree


def test_show_tree():
    tree = sample_tree()
    print(show_tree(tree))
    print(show_tree(sort_tree(tree)))


def test_save_load_tree():
    tree = sample_tree()
    print(show_tree(tree))
    fname = "test.json"
    save_tree(tree, fname)
    tree1 = load_tree(fname)
    print(show_tree(tree1))
    assert tree == tree1


def test_show_loads_tree():
    tree = sample_tree()
    print(show_tree(tree))
    tree1 = read_tree(show_tree(tree, show_done=True))
    print(show_tree(tree1))
    assert tree == tree1
