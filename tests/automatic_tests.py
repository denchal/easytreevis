import unittest
from easytreevis import *
from easytreevis.core import TreeNode

from easytreevis.layout import compute_positions

class TestTree(unittest.TestCase):
    def test_from_dict_simple(self):
        adj_dict = {
            'A': ['B', 'C'],
            'B': [],
            'C': []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        self.assertEqual(tree.root.id, 'A')
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(tree.root.children[0].id, 'B')
        self.assertEqual(tree.root.children[1].id, 'C')

    def test_from_dict_with_objects(self):
        adj_dict = {
            ('A', 'objA'): ['B'],
            ('B', 'objB'): []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        self.assertEqual(tree.root.id, 'A')
        self.assertEqual(tree.root.object, 'objA')
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].id, 'B')
        self.assertEqual(tree.root.children[0].object, 'objB')

    def test_order(self):
        adj_dict = {
            'A': ['C', 'B'],
            'B': [],
            'C': []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        self.assertEqual([child.id for child in tree.root.children], ['C', 'B'])
        tree.order()
        self.assertEqual([child.id for child in tree.root.children], ['B', 'C'])

    def test_from_binary_tree(self):
        tree_list = [1, 2, 3]
        tree = Tree.from_binary_tree(tree_list)
        self.assertEqual(tree.root.id, 1)
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(tree.root.children[0].id, 2)
        self.assertEqual(tree.root.children[1].id, 3)

    def test_from_binary_tree_with_none(self):
        tree_list = [1, None, 3]
        tree = Tree.from_binary_tree(tree_list)
        self.assertEqual(tree.root.id, 1)
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(tree.root.children[0].id, 3)

    def test_empty_binary_tree(self):
        tree = Tree.from_binary_tree([])
        self.assertIsNone(tree.root)

    def test_empty_dict_from_dict(self):
        with self.assertRaises(KeyError):
            Tree.from_dict({}, root='A')

    def test_nonexistent_root_in_from_dict(self):
        adj_dict = {'A': ['B'], 'B': []}
        with self.assertRaises(KeyError):
            Tree.from_dict(adj_dict, root='Z')

    def test_order_by_object(self):
        adj_dict = {
            ('A', 2): ['B', 'C'],
            ('B', 1): [],
            ('C', 3): []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        tree.order(key=lambda node: node.object)
        children_objects = [child.object for child in tree.root.children]
        self.assertEqual(children_objects, [1, 3])

    def test_order_recursive_sort(self):
        adj_dict = {
            'A': ['C', 'B'],
            'B': ['E', 'D'],
            'C': [],
            'D': [],
            'E': []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        self.assertEqual([child.id for child in tree.root.children], ['C', 'B'])
        self.assertEqual([child.id for child in tree.root.children[1].children], ['E', 'D'])

        tree.order(key=lambda node: node.id)

        self.assertEqual([child.id for child in tree.root.children], ['B', 'C'])
        self.assertEqual([child.id for child in tree.root.children[0].children], ['D', 'E'])

    def test_sort_method_in_treenode(self):
        node = TreeNode('root', [
            TreeNode('b', []),
            TreeNode('a', []),
            TreeNode('c', [])
        ])
        node.sort(key=lambda n: n.id)
        self.assertEqual([child.id for child in node.children], ['a', 'b', 'c'])

    def test_build_tree_with_mixed_keys(self):
        adj_dict = {
            'A': ['B', 'C'],
            ('B', 'objB'): []
        }
        tree = Tree.from_dict(adj_dict, root='A')
        self.assertEqual(tree.root.id, 'A')
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(tree.root.children[0].id, 'B')
        self.assertEqual(tree.root.children[0].object, 'objB')
        self.assertEqual(tree.root.children[1].id, 'C')
        self.assertIsNone(tree.root.children[1].object)

    def test_order_does_not_change_children_count(self):
        adj_dict = {'A': ['B', 'C'], 'B': [], 'C': []}
        tree = Tree.from_dict(adj_dict, root='A')
        children_before = len(tree.root.children)
        tree.order()
        children_after = len(tree.root.children)
        self.assertEqual(children_before, children_after)

    def test_none_object_and_children_in_treenode(self):
        node = TreeNode('id', None, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.object, None)

### Render Tests
def test_draw_tree_creates_svg(tmp_path):
    adj = {'A': ['B', 'C'], 'B': [], 'C': []}
    tree = Tree.from_dict(adj)

    output_file = tmp_path / "tree.svg"
    draw_tree(tree, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "<svg" in content
    assert "<circle" in content
    assert "<line" in content

def test_draw_tree_handles_non_string_objects(tmp_path):
    adj = {
        ('A', 123): ['B'],
        ('B', 456): []
    }
    tree = Tree.from_dict(adj)

    output_file = tmp_path / "nonstring.svg"
    draw_tree(tree, str(output_file))

    content = output_file.read_text()
    assert "123" in content
    assert "456" in content

def test_draw_tree_invalid_object_skips_text(tmp_path):
    class Unprintable:
        def __str__(self):
            raise Exception("Can't convert to string")

    adj = {
        ('A', Unprintable()): ['B'],
        ('B', None): []
    }
    tree = Tree.from_dict(adj)

    output_file = tmp_path / "bad.svg"
    draw_tree(tree, str(output_file))

    content = output_file.read_text()
    assert "A" in content or "B" in content
        
def test_draw_tree_invalid_object_skips_id_text(tmp_path):
    class Unprintable:
        def __str__(self):
            raise Exception("Can't convert to string")

    adj = {
        (Unprintable(), 123): ['B'],
        ('B', None): []
    }
    tree = Tree.from_dict(adj)

    output_file = tmp_path / "bad.svg"
    draw_tree(tree, str(output_file))

    content = output_file.read_text()
    assert "123" in content and "B" in content

def test_draw_tree_invalid_object_skips_fallback(tmp_path):
    class Unprintable:
        def __str__(self):
            raise Exception("Can't convert to string")

    adj = {
        (Unprintable(), Unprintable()): ['B'],
        ('B', None): []
    }
    tree = Tree.from_dict(adj)

    output_file = tmp_path / "bad.svg"
    draw_tree(tree, str(output_file))

    content = output_file.read_text()
    assert "B" in content

def test_single_node_tree_position():
    tree = Tree.from_dict({'A': []})
    positions = compute_positions(tree.root, x_spacing=50, y_spacing=100)

    assert 'A' in positions
    (x, y), obj = positions['A']
    assert x == 0
    assert y == 0

def test_two_level_tree_positions():
    adj = {'A': ['B', 'C'], 'B': [], 'C': []}
    tree = Tree.from_dict(adj)
    positions = compute_positions(tree.root, 50, 100)

    assert positions['B'][0][1] == 100
    assert positions['C'][0][1] == 100
    x_b = positions['B'][0][0]
    x_c = positions['C'][0][0]
    x_a = positions['A'][0][0]
    assert x_a == (x_b + x_c) / 2

def test_linear_tree_positions():
    adj = {'A': ['B'], 'B': ['C'], 'C': []}
    tree = Tree.from_dict(adj)
    positions = compute_positions(tree.root, 60, 80)

    assert positions['A'][0][1] == 0
    assert positions['B'][0][1] == 80
    assert positions['C'][0][1] == 160

def test_binary_tree_structure_positions():
    adj = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [], 'E': [], 'F': [], 'G': []
    }
    tree = Tree.from_dict(adj)
    positions = compute_positions(tree.root, 70, 90)

    for node_id, ((x, y), _) in positions.items():
        depth = node_id.count('.') if isinstance(node_id, str) else 0
        assert y % 90 == 0

def test_spacing_affects_position():
    adj = {'A': ['B', 'C'], 'B': [], 'C': []}
    tree1 = Tree.from_dict(adj)
    tree2 = Tree.from_dict(adj)

    pos1 = compute_positions(tree1.root, 50, 100)
    pos2 = compute_positions(tree2.root, 100, 200)

    for node_id in ['B', 'C']:
        assert pos2[node_id][0][0] == 2 * pos1[node_id][0][0]
        assert pos2[node_id][0][1] == 2 * pos1[node_id][0][1]


if __name__ == "__main__":
    unittest.main()