from easytreevis import Tree, draw_tree

if __name__ == "__main__":
    tree_data = {
        ("A", 1): ["B", "C", "G"],
        ("B", 2): ["D", "E"],
        ("C", 3): ["F"],
        ("D", 4): [], ("E", 5): [], ("F", 6): [], ("G", 7): ["H"],
        ("H", 8): ["I"],
        ("I", 9): ["J"],
        ("J", 10): ["K", "L"],
        ("K", 11): [],
        ("L", 12): []
    }
    tree = Tree.from_dict(tree_data)
    draw_tree(tree, "tree.svg", NODE_RADIUS=40, FILL_NODE='red')