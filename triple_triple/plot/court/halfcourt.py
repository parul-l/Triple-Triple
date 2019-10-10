import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.collections as mc


def halfcourt_vert(ax=None, linewidth=2, color='black'):
    if ax is None:
        ax = plt.gca()
    # set full court dimension
    ax.add_patch(patches.Rectangle(
        (0, 0),             # (x, y)
        50,                 # width    
        94,                 # length
        fill=False)
    )
    # half court line segments            
    lines = [   
        [(3, 0), (3, 14)],    # 3 point sideline
        [(47, 0), (47, 14)],  # 3 point sideline
        [(19, 0), (19, 19)],  # key
        [(31, 0), (31, 19)],  # key 
        [(22, 4), (28, 4)],   # backboard
        [(25, 4), (25, 4.5)], # rim line
        [(0, 47), (50, 47)]
    ]
    
    lc = mc.LineCollection(lines, color='black', linewidths=2)
    ax.add_collection(lc)
     
    # half court rectangles
    ax.add_patch(patches.Rectangle((17, 0), 16, 19, fill=False))

    # little hash marks (2in wide x 6in height)
    for p in [
        patches.Rectangle((16.5, 7), 0.5, 0.17, color='black'),
        patches.Rectangle((16.5, 8), 0.5, 0.17, color='black'),
        patches.Rectangle((16.5, 11), 0.5, 0.17,color='black'), 
        patches.Rectangle((16.5, 14), 0.5, 0.17,color='black'),
        ###################
        # other side
        ###################
        patches.Rectangle((33, 7), 0.5, 0.17, color='black'),
        patches.Rectangle((33, 8), 0.5, 0.17, color='black'),
        patches.Rectangle((33, 11), 0.5, 0.17, color='black'),        
        patches.Rectangle((33, 14), 0.5, 0.17, color='black'),  
        #####################
        # marks on sidelines
        #####################
        patches.Rectangle((0, 28), 3, 0.17, color='black'),
        patches.Rectangle((47, 28), 3, 0.17, color='black'),    
        ]:
        ax.add_patch(p)
                 
    # half court arcs
    for p in [
        # center court
        patches.Arc((25, 47), 12, 12, theta1=180, theta2= 360,
            linewidth=2, fill=False),
        # center court
        patches.Arc((25, 47), 4, 4, theta1=180, theta2=360,
            linewidth=2,fill=False),
        # top of the key
        patches.Arc((25, 19), 12, 12, theta1=0.0, theta2=180.0,
            fill=False),

        patches.Arc((25, 19), 12, 12, theta1=180.0, theta2=360.0,
            linestyle='dashed'),
        
        # 3 point line            
        patches.Arc((25, 5.25), 47.5, 47.5, theta1=21.62, theta2=158.38, 
            linewidth=),
        
        # in the key
        patches.Arc((25, 5.25), 8, 8, theta1=0.0, theta2=180.0, 
            fill=False),
            
        # hoop
        patches.Arc((25, 5.25), 1.5, 1.5, theta1=0.0, theta2=360.0, 
            fill=False),    
        
        ]:
        ax.add_patch(p)    
    return ax
