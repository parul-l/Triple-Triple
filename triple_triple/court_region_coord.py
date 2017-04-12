import numpy as np


def check_pts_make_triangle(p1, p2, p3):
    if (p1[0] == p2[0] and p2[0] == p3[0]) \
    or (p1[1] == p2[1] and p2[1] == p3[1]):
        return False
    else:
        return True


def centroid_triangle(p1, p2, p3):
    if check_pts_make_triangle(p1, p2, p3):
        x_coord = (p1[0] + p2[0] + p3[0]) / 3.0
        y_coord = (p1[1] + p2[1] + p3[1]) / 3.0

        return [x_coord, y_coord]

    else:
        raise ValueError('Points do not form a triangle')
        
    
# Use midpoint of the region as the simulated coordinate
def generate_back_court(shooting_side):
    if shooting_side == 'left':
        return [70.5, 25]
    elif shooting_side == 'right':
        return [23.5, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


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
        # centroid of triangle [36, 8.33]
        if shooting_side == 'left':
            return centroid_triangle(p1=[14, 0], p2=[47, 0], p3=[47, 25])
        # centroid of triangle [58, 8.33]
        elif shooting_side == 'right':
            return centroid_triangle(p1=[80, 0], p2=[47, 0], p3=[47, 25])

    if component == 3:
        # centroid of triangle [36, 41.67]
        if shooting_side == 'left':
            return centroid_triangle(p1=[14, 50], p2=[47, 50], p3=[47, 25])
        # centroid of triangle [58, 41.67]
        elif shooting_side == 'right':
            return centroid_triangle(p1=[80, 50], p2=[47, 50], p3=[47, 25])


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
