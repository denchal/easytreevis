# Assume the following State and Timestamp classes:
from easytreevis.utils import StringWrapper
from easytreevis import Tree, draw_tree

class State:
    def __init__(self, score, depth):
        self.score = score
        self.depth = depth
    
    def __eq__(self, other):
        return isinstance(other, State) and (self.score, self.depth) == (other.score, other.depth)

    def __hash__(self):
        return hash((self.score, self.depth))

class Timestamp:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.time = end - begin
    
    def __eq__(self, other):
        return isinstance(other, Timestamp) and (self.begin, self.end) == (other.begin, other.end)

    def __hash__(self):
        return hash((self.begin, self.end))

# We can represent them in a tree
state_tree_dict = {
    # (TreeKey, TreeObj) : [Children]
    # Keep in mind keys should be unique, or hash to unique values
    (Timestamp(0, 1), State(100, 1)) : [Timestamp(1, 2), Timestamp(1, 3)],
    (Timestamp(1, 2), State(50, 2)) : [Timestamp(2, 3)],
    (Timestamp(2, 3), State(10, 3)) : [],
    (Timestamp(1, 3), State(55, 2)) : [],
}
tree = Tree.from_dict(state_tree_dict)

# With an overwrite to utils/StringWrapper we can show State as node label
# We can even overwrite it to be a multiline text!
class CustomWrapper(StringWrapper):
    def string_wrap(self, obj: State) -> str:
        return [
            f"score={obj.score}",
            f"depth={obj.depth}"
        ]
    
# Let's also order them by score descending
tree.order(lambda x: -x.object.score)

# And finally render it
draw_tree(tree, "tree.svg", CustomWrapper(), FONT_SIZE=8)