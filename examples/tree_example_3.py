from easytreevis import Tree, draw_tree

if __name__ == "__main__":
    tree_data = [1,2,3,4,5,6,7,8,9,10,11]
    tree = Tree.from_binary_tree(tree_data)
    draw_tree(tree, "tree.svg")