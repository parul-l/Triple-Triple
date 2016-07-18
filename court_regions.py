import numpy as np

#############
# The Paint
#############
# 0<=x<=19 and 19<=y<= 31
# 75<=x<= 31 and 19<=y<= 31

#############
# The Key
#############
# 19<= x<= 26 and (x-19)^2 + (y-25)^2 <= 6^2
# 69<=x<= 75 and (x-75)^2 + (y-25)^2 <= 6^2

#############
# The Perimeter
#############
# 0<=x<=14 and y<=3 or y>=47
# 80<=x<=94 and y<=3 or y>=47
# 14<=x<=47 and (x-5.25)^2 + (y-25)^2 >= (23.75)^2
# 47<=x<=80 and (x-88.75)^2 + (y-25)^2 >= (23.75)^2

#############
# In between Paint+Key and Perimeter
#############
# Else

def region(x, y):
    if ((0<=x<=19 and 19<=y<= 31) or 
        (75<=x<= 31 and 19<=y<= 31)):
        return 'paint'
    elif ((19<= x<= 26 and (x-19)**2 + (y-25)**2 <= 36) or 
         (69<=x<= 75 and (x-75)**2 + (y-25)**2 <= 6**2)):
        return 'key'
    elif ((0<=x<=14 and (y<=3 or y>=47)) or 
         (80<=x<=94 and (y<=3 or y>=47)) or 
         (14<=x<=47 and ((x-5.25)**2 + (y-25)**2 >= (23.75)**2)) or (47<=x<=80 and ((x-88.75)**2 + (y-25)**2 >= (23.75)**2))):
        return 'perimeter'
    else: 
        return 'inside 3-point line'  
        
         
