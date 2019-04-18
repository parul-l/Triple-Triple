import numpy as np

# This module partitions each of the regions from 
# COURT_REGIONS triple_triple/constants.py
# into smaller regions and chooses a point to represent
# that region. 

# See Triple-Triple/img/full_court_approx_region_block.png 
# for a break down of the regions:
# backcourt: center of the rectangle
# mid-range: 3 points
# key: center of the half-circle
# perimeter: 5 points
# paint: center of rectangle
# out_of_bounds: 1 point under the rim

# TODO: Break in to smaller paritions.
# TODO: Update the plot

# FROM OLD:
# removed get_reg_to_num and court_region_from_num
# need to determine where this was needed
# added COURT_REGIONS in constants.py file


def check_pts_make_triangle(
        p1: list,
        p2: list,
        p3: list
):
    if (p1[0] == p2[0] and p2[0] == p3[0]) \
    or (p1[1] == p2[1] and p2[1] == p3[1]):
        return False
    else:
        return True


def centroid_triangle(
        p1: list,
        p2: list,
        p3: list
):
    if check_pts_make_triangle(p1, p2, p3):
        x_coord = (p1[0] + p2[0] + p3[0]) / 3.0
        y_coord = (p1[1] + p2[1] + p3[1]) / 3.0

        return [x_coord, y_coord]

    else:
        raise ValueError('Points do not form a triangle')



def generate_back_court(shooting_side: str):
    # Use midpoint of the region as the simulated coordinate
    if shooting_side == 'left':
        return [70.5, 25]
    elif shooting_side == 'right':
        return [23.5, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_mid_range(
        shooting_side: str,
        num_components: int=3
):
    # break down the region in to 3 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles
    component = np.random.choice(np.arange(num_components))
    if shooting_side == 'left':
        if component == 0:
            return [9.5, 11]
        elif component == 1:
            return [9.5, 39]
        elif component == 2:
            return [27.5, 25]

    elif shooting_side == 'right':
        if component == 0:
            return [84.5, 11]
        elif component == 1:
            return [84.5, 39]
        elif component == 2:
            return [67, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_key(shooting_side: str):
    # approximate with rectangle

    if shooting_side == 'left':
        return [22, 25]
    elif shooting_side == 'right':
        return [72, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_paint(shooting_side: str):
    if shooting_side == 'left':
        return [9.5, 25]
    elif shooting_side == 'right':
        return [84.5, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_out_of_bounds(shooting_side: str):
    # use behind the rim
    if shooting_side == 'left':
        return [-2, 25]
    elif shooting_side == 'right':
        return [96, 25]
    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_perimeter(
        shooting_side: str,
        num_components: int=4
):
    # break down the region in to 4 components
    # randomly choose one of the components
    # generate coordinates in that component
    # approximate with rectangles and triangles
    component = np.random.choice(np.arange(num_components))
    if shooting_side == 'left':
        if component == 0:
            return [7, 1.5]
        elif component == 1:
            return [7, 48.5]
        elif component == 2:
            # centroid of triangle: [36, 8.33]
            return centroid_triangle(
                p1=[14, 0],
                p2=[47, 0],
                p3=[47, 25]
            )
        elif component == 3:
            # centroid of triangle [36, 41.67]
            return centroid_triangle(
                p1=[14, 50],
                p2=[47, 50],
                p3=[47, 25]
            )

    elif shooting_side == 'right':
        if component == 0:
            return [89, 1.5]
        elif component == 1:
            return [89, 48.5]
        elif component == 2:
            # centroid of triangle: [58, 8.33]
            return centroid_triangle(
                p1=[80, 0],
                p2=[47, 0],
                p3=[47, 25]
            )
        elif component == 3:
            # centroid of triangle [58, 41.67]
            return centroid_triangle(
                p1=[80, 50],
                p2=[47, 50],
                p3=[47, 25]
            )

    else:
        raise ValueError("Input 'left' or 'right' to specify shooting_side")


def generate_rand_regions(court_region: str, shooting_side: str):
    """
    This function provides a random coordinate in
    the specified region.
    Parameters
    ----------
        court_region: `set`
            One of {
              'back_court', 'mid_range',
              'key','out_of_bounds',
              'paint','perimeter'
            }
        shooting_side: `str`
            Either 'left' or 'right' depending on which side of the court
            the offensive team is shooting.

    Returns
    -------
        `list` with 2 elements, [x, y], given the coordinates
        of a point from the region.
        See img/full_court_approx_region_block.png
    """

    if court_region == 'back_court':
        return generate_back_court(shooting_side)

    elif court_region == 'mid_range':
        return generate_mid_range(shooting_side)

    elif court_region == 'key':
        return generate_key(shooting_side)

    elif court_region == 'out_of_bounds':
        return generate_out_of_bounds(shooting_side)

    elif court_region == 'paint':
        return generate_paint(shooting_side)

    elif court_region == 'perimeter':
        return generate_perimeter(shooting_side)

    else:
        raise ValueError(
            "Court region: {'back_court','mid_range','key','out_of_bounds','paint','perimeter'}\
            Shooting side: {'left','right'}"
        )
