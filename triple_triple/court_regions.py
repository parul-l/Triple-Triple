# defines different regions in the court
# uses function shooting_side from team_shooting_side.py

def region(x, y, shooting_side):
    if shooting_side == 'left':
        if (0 <= x <= 19 and 19 <= y <= 31):
            return 'paint'
        elif ((19 <= x <= 25) and ((x - 19)**2 + (y - 25)**2 <= 6**2)):
            return 'key'
        elif ((0 <= x <= 14 and (0 <= y <= 3 or 47 <= y <= 50)) or
            (14 <= x <= 47 and ((x - 5.25)**2 + (y - 25)**2 >= (23.75)**2))):
            return 'perimeter'
        elif 0 <= x <= 47:
            # in between paint+key and perimeter
            return 'mid-range'
        elif 47 < x <= 94:
            return 'back court'
        else:
            return 'out of bounds'
    elif shooting_side == 'right':
        if (75 <= x <= 94 and 19 <= y <= 31):
            return 'paint'
        elif ((69 <= x <= 75 and (x - 75)**2 + (y - 25)**2 <= 6**2)):
            return 'key'
        elif ((80 <= x <= 94 and (0 <= y <= 3 or 47 <= y <= 50)) or
             (47 <= x <= 80 and ((x - 88.75)**2 + (y - 25)**2 >= (23.75)**2))):
            return 'perimeter'
        elif 47 < x <= 94:
            # in between paint+key and perimeter
            return 'mid-range'
        elif 0 <= x <= 47:
            return 'back court'
        else:
            return 'out of bounds'
