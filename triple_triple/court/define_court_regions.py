class CourtRegions(object):
    """ A classification of the court regions.
    Parameters
    ----------
        xbounds: :class:`~numpy.ndarray`, `None`
            An array of array that gives the x-limits for the 
            rectangular portion of the region in question. `None` value is
            assigned if region has no obvious rectangular component.
        ybounds: :class:`~numpy.ndarray`, `None`
            An array of array that gives the y-limits for the 
            rectangular portion of the region in question. `None` value is
            assigned if region has no obvious rectangular component.
        polygon: :func:, `None`
            A function describing the non-trivial components of the region.

    Methods
    -------
        __contains__: takes in a `tuple` (x, y) of floats.

    Examples
    --------
    Defining the boundaries of the `key` if the offensive team is shooting
    on the right side of the court

    >>> KEY = CourtRegions(
        xbounds=get_key(shooting_side='right')['xbounds'],
        ybounds=get_key(shooting_side='right')['ybounds'],
        polygon_region=get_key(shooting_side='right')['polygon']
    )
    >>> KEY.xbounds

    >>> KEY.ybounds

    >>> KEY.polygon_region
        <function __main__.get_polygon_key.<locals>.polygon_key>
    >>> [70, 28] in KEY
        True


    >>> PERIMETER = CourtRegions(
            xbounds=get_perimeter('left')['xbounds'],
            ybounds=get_perimeter('left')['ybounds'],
            polygon_region=get_perimeter('left')['polygon']
    )
    >>> PERIMETER.xbounds
        [[0, 14], [0, 14]]
    >>> PERIMETER.ybounds
        [[0, 3], [47, 50]]
    >>> PERIMETER.polygon_region
        <function __main__.get_polygon_perimeter.<locals>.polygon_perimeter>
    >>> [46, 3] in PERIMETER
        True
    >>> [20, 10] in PERIMETER
        False
    """


    def __init__(
            self,
            xbounds=None,
            ybounds=None,
            polygon_region=None
    ):
        self.xbounds = xbounds
        self.ybounds = ybounds
        self.polygon_region = polygon_region

    def __contains__(self, z: tuple):
        x, y = z
        if self.xbounds and self.ybounds is not None:
            for xs, ys in zip(self.xbounds, self.ybounds):
                if (xs[0] <= x <= xs[1] and ys[0] <= y <= ys[1]):
                    return True

        return self.polygon_region(x, y) if self.polygon_region is not None else False


def get_polygon_perimeter(shooting_side: str):
    """Describes the perimeter region, bounded by the 3-point line
    and the halfcourt mark.
    
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    :func: `polygon_perimeter(x, y)`, a function that takes two floats x, y as inputs
    and returns a boolean to reflect if (x, y) lies in the region.

    """

    if shooting_side == 'left':
        def polygon_perimeter(x, y):
            return (14 <= x < 47 and ((x - 5.25)**2 + (y - 25)**2 > (23.75)**2))
    elif shooting_side == 'right':
        def polygon_perimeter(x, y):
            return (47 < x <= 80 and ((x - 88.75)**2 + (y - 25)**2 > (23.75)**2))
    return polygon_perimeter


def get_perimeter(shooting_side: str):
    if shooting_side == 'left':
        xbound = [[0, 14], [0, 14]]

    elif shooting_side == 'right':
        xbound = [[80, 94], [80, 94]]    
    
    return {
        'xbounds': xbound,
        'ybounds': [[0, 3], [47, 50]],
        'polygon': get_polygon_perimeter(shooting_side=shooting_side)
    }


def get_polygon_mid_range(shooting_side: str):
    """Describes the mid-range region, bounded by the 3-point arc, 
    top of the key, and paint regions.
    
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    :func: `polygon_mid_range(x, y)`, a function that takes two floats x, y as inputs
    and returns a boolean to reflect if (x, y) lies in the region.

    """
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
                (65 <= x <= 69 and (x - 88.75)**2 + (y - 25)**2 <= (23.75)**2)
            )
    return polygon_mid_range


def get_mid_range(shooting_side: str):
    """Describes the entirety of the midrange region, including 
    both rectangular and non-rectangular components

    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    A `dict` with key: values 
        `xbounds`: x-bounds of the rectangular component,
        `ybounds`: y-bounds of the rectangular component,
        `polygon`: :func: get_polygon_mid_range(shooting_side), 
            function that describes non-rectangular region.
    """

    if shooting_side == 'left':
        xbound = [[0, 14], [0, 14]]

    elif shooting_side == 'right':
        xbound = [[80, 94], [80, 94]]

    return {
        'xbounds': xbound,
        'ybounds': [[3, 19], [31, 47]],
        'polygon': get_polygon_mid_range(shooting_side=shooting_side)
    } 


def get_polygon_key(shooting_side: str):
    """Describes the circular arc for the top of the key
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    :func: `polygon_key(x, y)`, a function that takes two floats x, y as inputs
    and returns a boolean to reflect if (x, y) lies in the region.

    """
    
    if shooting_side == 'left':
        def polygon_key(x, y):
            return (19 <= x <= 25 and (x - 19)**2 + (y - 25)**2 <= 6**2)

    elif shooting_side == 'right':
        def polygon_key(x, y):
            return (69 <= x <= 75 and (x - 75)**2 + (y - 25)**2 <= 6**2)
    return polygon_key


def get_key(shooting_side: str):
    """Describes the entirety of the top of the key region, including 
    both rectangular (None) and non-rectangular components
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    A `dict` with key: values 
        `xbounds`: None,
        `ybounds`: None,
        `polygon`: :func: get_polygon_key(shooting_side), 
            function that describes non-rectangular region.
    """

    return {
        'xbounds': None,
        'ybounds': None,
        'polygon': get_polygon_key(shooting_side=shooting_side)
    }


def get_polygon_out_of_bounds():
    def polygon_out_of_bounds(x, y):
        return (x <= 0 or x >= 94 or y <= 0 or y >= 50)
    return polygon_out_of_bounds


def get_out_of_bounds():
    """Describes the entirety of the out-of-bounds region, including 
    both rectangular (None) and non-rectangular components
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    A `dict` with key: values 
        `xbounds`: None,
        `ybounds`: None,
        `polygon`: :func: get_polygon_out_of_bounds(shooting_side), 
            function that describes non-rectangular region.
    """
    return {
        'xbounds': None,
        'ybounds': None,
        'polygon': get_polygon_out_of_bounds()
    }


def get_paint(shooting_side: str):
    """Describes the entirety of the paint region, including 
    both rectangular and non-rectangular components (None)
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    A `dict` with key: values 
        `xbounds`: x-bounds of the rectangular component,
        `ybounds`: y-bounds of the rectangular component,
        `polygon`: None
    """
    if shooting_side == 'left':
        xbound = [[0, 19]]

    elif shooting_side == 'right':
        xbound = [[75, 95]]
    
    return {
        'xbounds': xbound,
        'ybounds': [[19, 31]],
        'polygon': None
    }


def get_backcourt(shooting_side: str):
    """Describes the entirety of the backcourt region, including 
    both rectangular and non-rectangular components (None)
    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    ------
    A `dict` with key: values 
        `xbounds`: x-bounds of the rectangular component,
        `ybounds`: y-bounds of the rectangular component,
        `polygon`: None
    """

    if shooting_side == 'left':
        xbound = [[47, 94]]

    elif shooting_side == 'right':
        xbound = [[0, 47]]
    
    return {
        'xbounds': xbound,
        'ybounds': [[0, 50]],
        'polygon': None
    }
