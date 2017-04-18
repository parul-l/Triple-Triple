# defines different regions in the court
# uses function shooting_side from team_shooting_side.py
import triple_triple.class_court_regions as ccr


def get_region_bounds(shooting_side):
    if shooting_side in ['left', 'right']:
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
    else:
        raise ValueError("Input 'left' or 'right' for shooting_side")


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
