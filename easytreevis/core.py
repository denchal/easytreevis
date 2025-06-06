from typing import Any, Callable, Dict, List, Optional

class TreeNode:
    def __init__(self, id: Any, children: List["TreeNode"], object: Any = None):
        self.id: Any = id
        self.children: List = [] if not children else children
        self.object: Any = object

    def sort(self, key: Callable) -> None:
        self.children.sort(key=key)

    def order(self, key: Callable) -> None:
        for child in self.children:
            child.order(key)
        self.sort(key)

class Tree:
    def __init__(self, root: TreeNode):
        self.root = root
    
    def order(self, key: Callable = lambda x : x.id) -> None:
        """
        Orders all children for all nodes in tree.
        """
        self.root.order(key)

    @staticmethod
    def from_dict(adj_dict: Dict[Any, List[Any]], root: Any = None) -> "Tree":
        def extract_key_id_obj(key):
            return (key, None) if not isinstance(key, tuple) else (key[0], key[1])

        structured = {}
        for key, children in adj_dict.items():
            node_id, node_obj = extract_key_id_obj(key)
            structured[node_id] = (node_obj, children)

        def build_tree(root_id: Any, structured: dict) -> TreeNode:
            stack = [(root_id, False)]
            node_map = {}

            while stack:
                node_id, visited = stack.pop()

                if visited:
                    node_obj, children_keys = structured.get(node_id, (None, []))
                    children = []
                    for child_key in children_keys:
                        if isinstance(child_key, tuple):
                            child_id, _ = extract_key_id_obj(child_key)
                        else:
                            child_id = child_key
                        children.append(node_map[child_id])

                    node_map[node_id] = TreeNode(node_id, children, node_obj)

                else:
                    stack.append((node_id, True))

                    _, children_keys = structured.get(node_id, (None, []))
                    for child_key in reversed(children_keys):
                        if isinstance(child_key, tuple):
                            child_id, _ = extract_key_id_obj(child_key)
                        else:
                            child_id = child_key
                        stack.append((child_id, False))

            return node_map[root_id]

        if root is None:
            first_key = next(iter(adj_dict))
            root = first_key[0] if isinstance(first_key, tuple) else first_key

        if root not in [extract_key_id_obj(k)[0] for k in adj_dict.keys()]:
            raise KeyError("Invalid root")
        
        root_node = build_tree(root, structured)
        return Tree(root_node)

    
    @staticmethod
    def from_binary_tree(tree: List[Optional[Any]]) -> "Tree":
        if not tree or tree[0] is None:
            return Tree(None)

        nodes = [TreeNode(val, []) if val is not None else None for val in tree]
        n = len(tree)

        for i in range(n):
            node = nodes[i]
            if node is not None:
                left_index = 2 * i + 1
                right_index = 2 * i + 2

                if left_index < n and nodes[left_index] is not None:
                    node.children.append(nodes[left_index])
                if right_index < n and nodes[right_index] is not None:
                    node.children.append(nodes[right_index])

        return Tree(nodes[0])