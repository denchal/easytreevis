from easytreevis import Tree, draw_tree

if __name__ == "__main__":
    tree_data = {
        "A": ["B", "C", "G"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [], "E": [], "F": [], 
        "G": ["H"],
        "H": ["I"],
        "I": ["J"],
        "J": ["K", "L"],
        "K": [], "L": []
    }
    tree = Tree.from_dict(tree_data)
    draw_tree(tree, "tree.svg")