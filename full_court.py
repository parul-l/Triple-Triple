import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.collections as mc

plt.ion()

def draw_court(ax=None, linewidth=2, color='black'):
    if ax is None:
        ax = plt.gca()
    
    out = ax.set_xlim([0, 94])
    out = ax.set_ylim([0, 50])
    # set full court dimension
    ax.add_patch(patches.Rectangle(
        xy=(0, 0),               # (x, y)
        width=94,                # width    
        height=50,               # length
        fill=False
    ))
    # half court line segments            
    lines = [   
        [(0, 3), (14, 3)],       # 3 point sideline
        [(0, 47), (14, 47)],     # 3 point sideline
        [(0, 19), (19, 19)],     # key
        [(0, 31), (19, 31)],     # key 
        [(4, 22), (4, 28)],      # backboard
        [(4, 25), (4.5, 25)],    # rim line
        [(47, 0), (47, 50)]
    ]
    # other side half court line segments
    lines_other = [
        [(94, 3), (80, 3)],      # 3 point sideline
        [(94, 47), (80, 47)],    # 3 point sideline
        [(94, 19), (75, 19)],    # key
        [(94, 31), (75, 31)],    # key 
        [(90, 22), (90, 28)],    # backboard
        [(90, 25), (89.5, 25)],  # rim line
        [(47, 0), (47, 50)]
    ]            
    lc = mc.LineCollection(lines, color='black', linewidths=2)
    lc_other = mc.LineCollection(lines_other, color='black', linewidths=2)
    ax.add_collection(lc_other)
    ax.add_collection(lc)
     
    # half court rectangles
    ax.add_patch(patches.Rectangle((0, 17), 19, 16, fill=False))
    ax.add_patch(patches.Rectangle((75, 17), 19, 16, fill=False))
    
    # little hash marks (2in wide x 6in height)
    for p in [
        patches.Rectangle((7, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((8, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((11, 16.5), 0.17, 0.5, color='black'), 
        patches.Rectangle((14, 16.5), 0.17, 0.5, color='black'),
        
        patches.Rectangle((89, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((88, 16.5), 0.17, 0.5, color='black'),
        patches.Rectangle((85, 16.5), 0.17, 0.5, color='black'), 
        patches.Rectangle((82, 16.5), 0.17, 0.5, color='black'),
        ###################
        # other side
        ###################
        patches.Rectangle((7, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((8, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((11, 33), 0.17, 0.5, color='black'),        
        patches.Rectangle((14, 33), 0.17, 0.5, color='black'), 
        
        patches.Rectangle((89, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((88, 33), 0.17, 0.5, color='black'),
        patches.Rectangle((85, 33), 0.17, 0.5, color='black'),        
        patches.Rectangle((82, 33), 0.17, 0.5, color='black'),  
        #####################
        # marks on sidelines
        #####################
        patches.Rectangle((28, 0), 0.17, 3, color='black'),
        patches.Rectangle((28, 47), 0.17, 3, color='black'),
        
        patches.Rectangle((66, 0), 0.17, 3, color='black'),
        patches.Rectangle((66, 47), 0.17, 3, color='black'),     
        ]:
        ax.add_patch(p)
                 
    # half court arcs
    for p in [
        # center court
        patches.Arc((47, 25), 12, 12, theta1=0, theta2= 360,
            linewidth=2, fill=False),
        # center court
        patches.Arc((47, 25), 4, 4, theta1=0, theta2=360,
            linewidth=2,fill=False),
        # top of the key
        patches.Arc((19, 25), 12, 12, theta1=270, theta2=90.0,
            fill=False),
    
        patches.Arc((75, 25), 12, 12, theta1=90, theta2=270.0,
            fill=False),    
    
        patches.Arc((19, 25), 12, 12, theta1=90.0, theta2=270.0,
            linestyle='dashed'),
        patches.Arc((75, 25), 12, 12, theta1=270.0, theta2=90.0,
            linestyle='dashed'),    
        
        # 3 point line            
        patches.Arc((5.25, 25), 47.5, 47.5, theta1=-68.38, theta2=68.38, 
            linewidth=2), 
        patches.Arc((88.75, 25), 47.5, 47.5, theta1=111.62, theta2=248.38, 
            linewidth=2), 
        # in the key
        patches.Arc((5.25, 25), 8, 8, theta1=270, theta2=90.0,
            fill=False),
        patches.Arc((88.75, 25), 8, 8, theta1=90, theta2=270.0,
            fill=False),    
            
        # hoop
        patches.Arc((5.25, 25), 1.5, 1.5, theta1=0.0, theta2=360.0, 
            fill=False), 
        patches.Arc((88.75, 25), 1.5, 1.5, theta1=0.0, theta2=360.0, 
            fill=False),        
        
        ]:
        ax.add_patch(p)    
    return ax


  
