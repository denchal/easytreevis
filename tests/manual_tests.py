from easytreevis import Tree, draw_tree

adj = {
        ('root', 'R'): ['child'],
        ('child', 'C'): []
    }
tree = Tree.from_dict(adj)

draw_tree(tree, "tree.svg", Y_SPACING=100, FONT_SIZE=2)