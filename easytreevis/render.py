import svgwrite
from .layout import compute_positions
from .core import Tree
from .utils import is_string_convertible

DEFAULT_PARAMS = {
    "NODE_RADIUS": 20,
    "FONT_SIZE": 16,
    "EDGE_STROKE_WIDTH": 3,
    "FILL_NODE": "white",
    "STROKE_NODE": "black",
    "STROKE_NODE_WIDTH": 2,
    "STROKE_EDGE": "black",
    "MAX_SVG_WIDTH": float("inf"),
    "MAX_SVG_HEIGHT": float("inf"),
    "X_SPACING": 60,
    "Y_SPACING": 80,
    "MARGIN": 40
}

def draw_tree(tree: Tree, output: str, **kwargs) -> None:
    params = {**DEFAULT_PARAMS, **kwargs}
    margin = params["MARGIN"]

    root = tree.root
    positions = compute_positions(root, params["X_SPACING"], params["Y_SPACING"])

    all_coords = [p[0] for p in positions.values()]
    xs, ys = zip(*all_coords)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    tree_width = max_x - min_x
    tree_height = max_y - min_y

    svg_width = min(params["MAX_SVG_WIDTH"], tree_width + 2 * margin)
    svg_height = min(params["MAX_SVG_HEIGHT"], tree_height + 2 * margin)

    dwg = svgwrite.Drawing(output, profile='full', size=(svg_width, svg_height))

    offset_x = margin - min_x
    offset_y = margin - min_y

    def shifted(pos):
        x, y = pos
        return (x + offset_x, y + offset_y)

    def draw_edges(root, dwg, positions, params):
        stack = [root]

        while stack:
            node = stack.pop()
            x1, y1 = shifted(positions[node.id][0])
            for child in node.children:
                x2, y2 = shifted(positions[child.id][0])
                dwg.add(dwg.line(
                    start=(x1, y1), end=(x2, y2),
                    stroke=params["STROKE_EDGE"], stroke_width=params["EDGE_STROKE_WIDTH"]
                ))
                stack.append(child)

    draw_edges(root, dwg, positions, params)

    for node_id, [(x, y), object] in positions.items():
        sx, sy = shifted((x, y))
        dwg.add(dwg.circle(
            center=(sx, sy),
            r=params["NODE_RADIUS"],
            fill=params["FILL_NODE"],
            stroke=params["STROKE_NODE"],
            stroke_width=params["STROKE_NODE_WIDTH"]
        ))

        label = str(object) if object and is_string_convertible(object) else (
            str(node_id) if is_string_convertible(node_id) else None
        )
        if label:
            dwg.add(dwg.text(
                label,
                insert=(sx, sy + params["FONT_SIZE"]/3),
                text_anchor="middle",
                font_size=params["FONT_SIZE"],
            ))

    if output:
        dwg.save()
