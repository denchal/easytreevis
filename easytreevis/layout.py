def compute_positions(root, x_spacing, y_spacing):
    positions = {}
    next_x = [0]

    stack = [(root, 0, False)]

    while stack:
        node, depth, visited = stack.pop()

        if visited:
            children_x = []
            for child in node.children:
                children_x.append(positions[child.id][0][0])

            if children_x:
                x = sum(children_x) / len(children_x)
            else:
                x = next_x[0] * x_spacing
                next_x[0] += 1

            y = depth * y_spacing
            positions[node.id] = [(x, y), node.object]

        else:
            stack.append((node, depth, True))
            for child in reversed(node.children):
                stack.append((child, depth + 1, False))

    return positions

