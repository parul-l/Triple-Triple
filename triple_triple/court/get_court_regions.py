from triple_triple.court.define_court_regions import (
    CourtRegions,
    get_backcourt,
    get_key,
    get_mid_range,
    get_out_of_bounds,
    get_paint,
    get_perimeter   
)


def get_region_bounds(shooting_side: str):
    """ This function collects the court regions of the offensive team
    given the shooting side of the offensive team.

    Parameters
    ----------
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    -------
        `dict`
        A dictionary of the region classes for the offensive team.
        The key: values are of the form 
        {
            'perimeter': PERIMETER, 
            'mid_range': MID_RANGE, 
            'key': KEY, 
            'paint': PAINT, 
            'back_court': BACK_COURT, 
            'out_of_bounds': OUT_OF_BOUNDS
        }
    
    Raises
    ------
        ValueError
        Raises a :exc:`~ValueError` if the inputs are not correct.
    """

    if shooting_side in ['left', 'right']:
        PERIMETER = CourtRegions(
            xbounds=get_perimeter(shooting_side)['xbounds'],
            ybounds=get_perimeter(shooting_side)['ybounds'],
            polygon_region=get_perimeter(shooting_side)['polygon']
        )
        MID_RANGE = CourtRegions(
            xbounds=get_mid_range(shooting_side)['xbounds'],
            ybounds=get_mid_range(shooting_side)['ybounds'],
            polygon_region=get_mid_range(shooting_side)['polygon']
        )
        KEY = CourtRegions(
            xbounds=get_key(shooting_side)['xbounds'],
            ybounds=get_key(shooting_side)['ybounds'],
            polygon_region=get_key(shooting_side)['polygon']
        )
        PAINT = CourtRegions(
            xbounds=get_paint(shooting_side)['xbounds'],
            ybounds=get_paint(shooting_side)['ybounds'],
            polygon_region=get_paint(shooting_side)['polygon']
        )
        BACK_COURT = CourtRegions(
            xbounds=get_backcourt(shooting_side)['xbounds'],
            ybounds=get_backcourt(shooting_side)['ybounds'],
            polygon_region=get_backcourt(shooting_side)['polygon']
        )
        OUT_OF_BOUNDS = CourtRegions(
            xbounds=get_out_of_bounds()['xbounds'],
            ybounds=get_out_of_bounds()['ybounds'],
            polygon_region=get_out_of_bounds()['polygon']
        )
        return {
            'perimeter': PERIMETER, 
            'mid_range': MID_RANGE, 
            'key': KEY, 
            'paint': PAINT, 
            'back_court': BACK_COURT, 
            'out_of_bounds': OUT_OF_BOUNDS
        }
    else:
        raise ValueError("Input 'left' or 'right' for shooting_side")


def get_region(x: float, y: float, shooting_side: str):
    """ Determines the region of the offensive team, given (x, y) coordinates.
    
    Parameters
    ----------
    x: `float`
    y: `float`
    shooting_side: `str`
        Either 'left' or 'right' depending on which side of the court
        the offensive team is shooting.

    Returns
    -------
    A `str` indicating the region of the offensive team given the (x, y) coordinates.

    Raises
    ------
        ValueError
        Raises a :exc:`~ValueError` if the inputs are not correct.

    """
    region = get_region_bounds(shooting_side=shooting_side)

    if [x, y] in region['paint']:
        return 'paint'
    elif [x, y] in region['perimeter']:
        return 'perimeter'
    elif [x, y] in region['mid_range']:
        return 'mid_range'
    elif [x, y] in region['key']:
        return 'key'
    elif [x, y] in region['back_court']:
        return 'back_court'
    elif [x, y] in region['out_of_bounds']:
        return 'out_of_bounds'
    else:
        raise ValueError('check x, y, shooting_side inputs')
