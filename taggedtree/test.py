from .core import new_tree, new_attr, root, show_tree, sort_tree, save_tree, load_tree


def sample_tree():
    tree = new_tree(root(), [
        new_tree(new_attr("study"), [
            new_tree(new_attr("PAC-Bayesian transportation bound"), [
                new_tree(new_attr("oracle", priority="1", done=True)),
                new_tree(new_attr("empirical", priority="2", tags=["AISTATS20"])),
            ]),
            new_tree(new_attr("Neural heuristics", priority="1")),
        ]),
        new_tree(new_attr("感性"), [
            new_tree(new_attr("映画を見る")),
            new_tree(new_attr("ピアノを始める")),
        ]),
        new_tree(new_attr("体力")),
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
