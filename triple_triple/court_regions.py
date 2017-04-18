# defines different regions in the court
# uses function shooting_side from team_shooting_side.py
import triple_triple.class_court_regions as ccr


def get_region_bounds(shooting_side):
    PERIMETER = ccr.CourtRegions(
        xbounds=ccr.perimeter[shooting_side]['xbounds'],
        ybounds=ccr.perimeter[shooting_side]['ybounds'],
        polygon_region=ccr.perimeter[shooting_side]['polygon']
    )
    MID_RANGE = ccr.CourtRegions(
        xbounds=ccr.mid_range[shooting_side]['xbounds'],
        ybounds=ccr.mid_range[shooting_side]['ybounds'],
        polygon_region=ccr.mid_range[shooting_side]['polygon']
    )
    KEY = ccr.CourtRegions(
        xbounds=ccr.key[shooting_side]['xbounds'],
        ybounds=ccr.key[shooting_side]['ybounds'],
        polygon_region=ccr.key[shooting_side]['polygon']
    )
    PAINT = ccr.CourtRegions(
        xbounds=ccr.paint[shooting_side]['xbounds'],
        ybounds=ccr.paint[shooting_side]['ybounds'],
        polygon_region=ccr.paint[shooting_side]['polygon']
    )
    BACK_COURT = ccr.CourtRegions(
        xbounds=ccr.back_court[shooting_side]['xbounds'],
        ybounds=ccr.back_court[shooting_side]['ybounds'],
        polygon_region=ccr.back_court[shooting_side]['polygon']
    )
    OUT_OF_BOUNDS = ccr.CourtRegions(
        xbounds=ccr.out_of_bounds['xbounds'],
        ybounds=ccr.out_of_bounds['ybounds'],
        polygon_region=ccr.out_of_bounds['polygon']
    )
    return PERIMETER, MID_RANGE, KEY, PAINT, BACK_COURT, OUT_OF_BOUNDS


def get_region(x, y, shooting_side):
    PERIMETER, MID_RANGE, KEY, PAINT, BACK_COURT, OUT_OF_BOUNDS = get_region_bounds(shooting_side=shooting_side)
    if [x, y] in PERIMETER:
        return 'perimeter'
    elif [x, y] in MID_RANGE:
        return 'mid_range'
    elif [x, y] in KEY:
        return 'key'
    elif [x, y] in PAINT:
        return 'paint'
    elif [x, y] in BACK_COURT:
        return 'back_court'
    elif [x, y] in OUT_OF_BOUNDS:
        return 'out_of_bounds'
    else:
        raise ValueError('check x, y, shooting_side inputs')

    # # make sure entries are correct types:
    # if (
    #     type(x) not in [float, int] or
    #     type(y) not in [float, int] or
    #     shooting_side not in ['left', 'right']
    # ):
    # 
    #     raise ValueError("Input (x, y, shooting_side='left'/'right')")
    # 
    # # check out of bounds
    # if (x <= 0 or x >= 94 or
    #    y <= 0 or y >= 50):
    #     return 'out_of_bounds'
    # 
    # if shooting_side == 'left':
    #     if (0 <= x <= 19 and
    #        19 <= y <= 31): # if (x, y) in PAINT
    #         return 'paint'
    #     elif (19 <= x <= 25 and
    #           ((x - 19)**2 + (y - 25)**2 <= 6**2)):
    #         return 'key'
    #     elif ((0 <= x <= 14 and (0 <= y <= 3 or 47 <= y <= 50)) or
    #             (14 <= x <= 47 and ((x - 5.25)**2 + (y - 25)**2 >= (23.75)**2))):
    #         return 'perimeter'
    #     elif (0 <= x <= 47 and
    #           0 <= y < 50):
    #         return 'mid_range'
    #     elif (47 <= x < 94 and
    #           0 <= y < 50):
    #         return 'back_court'
    # 
    # elif shooting_side == 'right':
    #     if (75 <= x <= 94 and
    #        19 <= y <= 31):
    #         return 'paint'
    #     elif (69 <= x <= 75 and
    #          (x - 75)**2 + (y - 25)**2 <= 6**2):
    #         return 'key'
    #     elif ((80 <= x <= 94 and (0 <= y <= 3 or 47 <= y <= 50)) or
    #             (47 <= x <= 80 and ((x - 88.75)**2 + (y - 25)**2 >= (23.75)**2))):
    #         return 'perimeter'
    #     elif (47 < x < 94 and
    #           0 <= y < 50):
    #         return 'mid_range'
    #     elif (0 <= x <= 47 and
    #           0 <= y < 50):
    #         return 'back_court'
