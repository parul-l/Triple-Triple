import numpy as np

# Use midpoint of the region as the simulated coordinate


def generate_back_court(shooting_side):
    if shooting_side == 'left':
        return [70.5, 25]
    elif shooting_side == 'right':
        return [23.5, 25]


def generate_mid_range(shooting_side):
    # break down the region in to 3 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles

    component = np.random.choice(np.arange(3))
    if component == 0:
        if shooting_side == 'left':
            return [9.5, 11]
        elif shooting_side == 'right':
            return [84.5, 11]

    if component == 1:
        if shooting_side == 'left':
            return [9.5, 39]
        elif shooting_side == 'right':
            return [84.5, 39]

    if component == 2:
        if shooting_side == 'left':
            return [27.5, 25]
        elif shooting_side == 'right':
            return [67, 25]


def generate_key(shooting_side):
    # approximate with rectangle

    if shooting_side == 'left':
        return [22, 25]
    elif shooting_side == 'right':
        return [72, 25]


def generate_paint(shooting_side):
    if shooting_side == 'left':
        return [9.5, 25]
    elif shooting_side == 'right':
        return [84.5, 25]


def generate_out_of_bounds(shooting_side):
    # use behind the rim
    if shooting_side == 'left':
        return [-2, 25]

    elif shooting_side == 'right':
        return [96, 25]


def generate_perimeter(shooting_side):
    # break down the region in to 4 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles

    component = np.random.choice(np.arange(4))
    if component == 0:
        if shooting_side == 'left':
            return [7, 1.5]
        elif shooting_side == 'right':
            return [89, 1.5]

    if component == 1:
        if shooting_side == 'left':
            return [7, 48.5]
        elif shooting_side == 'right':
            return [89, 48.5]

    if component == 2:
        # centroid of triangle (14, 0), (47, 0), (47, 25)
        if shooting_side == 'left':
            return [36, 8.33]
        # centroid of triangle (80, 0), (47, 0), (47, 25)
        elif shooting_side == 'right':
            return [58, 8.33]

    if component == 3:
        # centroid of triangle (14, 50), (47, 25), (47, 50)
        if shooting_side == 'left':
            return [36, 41.67]
        # centroid of triangle (80, 50), (47, 25), (47, 50)
        elif shooting_side == 'right':
            return [58, 41.67]


def generate_rand_positions(pos_num, shooting_side):
    # back court
    if pos_num == 0:
        return generate_back_court(shooting_side)

    # mid-range
    elif pos_num == 1:
        return generate_mid_range(shooting_side)

    # key
    elif pos_num == 2:
        return generate_key(shooting_side)

    # out of bounds
    elif pos_num == 3:
        return generate_out_of_bounds(shooting_side)

    # paint
    elif pos_num == 4:
        return generate_paint(shooting_side)

    # perimeter
    elif pos_num == 5:
        return generate_perimeter(shooting_side)
