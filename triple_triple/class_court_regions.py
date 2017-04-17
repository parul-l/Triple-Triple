class CourtRegions(object):
    def __init__(self, xbounds=None, ybounds=None, polygon_region=None):
        self.xbounds = xbounds
        self.ybounds = ybounds
        self.polygon_region = polygon_region

    def __contains__(self, z):
        x, y = z
        if self.xbounds and self.ybounds is not None:
            for xs, ys in zip(self.xbounds, self.ybounds):
                if (xs[0] <= x <= xs[1] and ys[0] <= y <= ys[1]):
                    return True

        return self.polygon_region(x, y) if self.polygon_region is not None else False


def get_polygon_perimeter(shooting_side):
    if shooting_side == 'left':
        def polygon_perimeter(x, y):
            return (14 <= x <= 47 and ((x - 5.25)**2 + (y - 25)**2 >= (23.75)**2))
    elif shooting_side == 'right':
        def polygon_perimeter(x, y):
            return (47 <= x <= 80 and ((x - 88.75)**2 + (y - 25)**2 >= (23.75)**2))
    return polygon_perimeter


def get_polygon_mid_range(shooting_side):
    if shooting_side == 'left':
        def polygon_mid_range(x, y):
            return (
                (14 <= x <= 19 and (x - 5.25)**2 + (y - 25)**2 <= (23.75)**2 and
                    (y <= 19 or y >= 31)) or
                (19 <= x <= 25 and (x - 5.25)**2 + (y - 25)**2 <= (23.75)**2 and
                    (x - 19)**2 + (y - 25)**2 >= 6**2) or
                (25 <= x <= 29 and (x - 5.25)**2 + (y - 25)**2 <= (23.75)**2)
            )
    elif shooting_side == 'right':
        def polygon_mid_range(x, y):
            return (
                (75 <= x <= 80 and (x - 88.75)**2 + (y - 25)**2 <= (23.75)**2 and
                    (y <= 19 or y >= 31)) or
                (69 <= x <= 75 and (x - 88.75)**2 + (y - 25)**2 <= (23.75)**2 and
                    (x - 75)**2 + (y - 25)**2 >= 6**2) or
                (65 <= x <= 69 and (x - 88.755)**2 + (y - 25)**2 <= (23.75)**2)
            )
    return polygon_mid_range


def get_polygon_key(shooting_side):
    if shooting_side == 'left':
        def polygon_key(x, y):
            return (19 <= x <= 25 and (x - 19)**2 + (y - 25)**2 <= 6**2)

    elif shooting_side == 'right':
        def polygon_key(x, y):
            return (69 <= x <= 75 and (x - 75)**2 + (y - 25)**2 <= 6**2)
    return polygon_key


def get_polygon_out_of_bounds():
    def polygon_out_of_bounds(x, y):
        return (x <= 0 or x >= 94 or y <= 0 or y >= 50)
    return polygon_out_of_bounds

perimeter = {
    'left': {
        'xbounds': [[0, 14], [0, 14]],
        'ybounds': [[0, 3], [47, 50]],
        'polygon': get_polygon_perimeter(shooting_side='left')
    },
    'right': {
        'xbounds': [[90, 94], [80, 94]],
        'ybounds': [[0, 3], [47, 50]],
        'polygon': get_polygon_perimeter(shooting_side='right')
    }
}

mid_range = {
    'left': {
        'xbounds': [[0, 14], [0, 14]],
        'ybounds': [[3, 19], [31, 47]],
        'polygon': get_polygon_mid_range(shooting_side='left')
    },
    'right': {
        'xbounds': [[80, 94], [80, 94]],
        'ybounds': [[3, 19], [31, 47]],
        'polygon': get_polygon_mid_range(shooting_side='right')
    }
}

key = {
    'left': {
        'xbounds': None,
        'ybounds': None,
        'polygon': get_polygon_key(shooting_side='left')
    },
    'right': {
        'xbounds': None,
        'ybounds': None,
        'polygon': get_polygon_key(shooting_side='right')
    }
}

paint = {
    'left': {
        'xbounds': [[0, 19]],
        'ybounds': [[19, 31]],
        'polygon': None
    },
    'right': {
        'xbounds': [[75, 95]],
        'ybounds': [[19, 31]],
        'polygon': None
    }
}

back_court = {
    'left': {
        'xbounds': [[47, 94]],
        'ybounds': [[0, 50]],
        'polygon': None
    },
    'right': {
        'xbounds': [[0, 47]],
        'ybounds': [[0, 50]],
        'polygon': None
    }
}

out_of_bounds = {
    'xbounds': None,
    'ybounds': None,
    'polygon': get_polygon_out_of_bounds()
}
