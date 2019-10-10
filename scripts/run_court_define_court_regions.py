from triple_triple.court.define_court_regions import (
    CourtRegions,
    get_backcourt,
    get_key,
    get_mid_range,
    get_out_of_bounds,
    get_paint,
    get_perimeter   
)


if __name__ == '__main__':
    shooting_side = 'left'
    PERIMETER = CourtRegions(
        xbounds=get_perimeter(shooting_side)['xbounds'],
        ybounds=get_perimeter(shooting_side)['ybounds'],
        polygon_region=get_perimeter(shooting_side)['polygon']
    )
    # PERIMETER.xbounds
    # PERIMETER.ybounds
    # using built-in __contains__ function
    # [14, 24] in PERIMETER
    # >> FALSE

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