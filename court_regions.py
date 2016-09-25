# defines different regions in the court

def region(x, y, shooting_side):
    if shooting_side =='left':        
        if (0<=x<=19 and 19<=y<= 31):
            return 'paint'
        elif ((19<= x<= 26 and (x-19)**2 + (y-25)**2 <= 36) ):
            return 'key'
        elif ((0<=x<=14 and (y<=3 or y>=47)) or 
            (14<=x<=47 and ((x-5.25)**2 + (y-25)**2 >= (23.75)**2))):
            return 'perimeter'
        elif 0<=x<=47: 
            # in between paint+key and perimeter
            return 'inside 3-point line'
        elif 47<x<=94:
            return 'back court'
        else:
            return 'out of bounds'         
    elif shooting_side=='right':
        if (75<=x<= 94 and 19<=y<= 31):
            return 'paint'
        elif ((69<=x<= 75 and (x-75)**2 + (y-25)**2 <= 6**2)):
            return 'key'
        elif ( (80<=x<=94 and (y<=3 or y>=47)) or 
             (47<=x<=80 and ((x-88.75)**2 + (y-25)**2 >=     (23.75)**2))):
            return 'perimeter'
        elif 47<x <= 94: 
            # in between paint+key and perimeter
            return 'inside 3-point line'
        elif 0<=x<=47:
            return 'back court'
        else:
            return 'out of bounds'    
