def find_steps_to_target(target_x, target_y):
    layer_number = 0
    previous_layer, current_layer = set(), set([(0, 0)])

    while (target_x, target_y) not in current_layer:
        next_layer = set()
        for x, y in current_layer:
            for next_cell in get_possible_moves(x, y):
                if next_cell not in previous_layer:
                    next_layer.add(next_cell)
        previous_layer, current_layer = current_layer, next_layer
        layer_number += 1

    return layer_number


def get_possible_moves(x, y):
    return [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]
