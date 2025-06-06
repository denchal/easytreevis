from easytreevis import Tree, draw_tree

bin_tree = [x for x in range(150)]
tree = Tree.from_binary_tree(bin_tree)

draw_tree(tree, "tree.svg", Y_SPACING=100, FONT_SIZE=2)