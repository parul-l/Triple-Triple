# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# 
# def update(i, fig, scat):
#     scat.set_offsets(([0,i], [50,i], [100,i] ))
#     return scat,
#     
# fig = plt.figure()
# 
# x = [0, 50, 100]
# y = [0, 0, 0]
# 
# ax = fig.add_subplot(111)
# ax.set_xlim([-50, 200])
# ax.set_ylim([-50, 200])
# 
# scat = plt.scatter(x, y, c = x)
# scat.set_alpha(0.8)
# 
# anim = animation.FuncAnimation(fig, update, fargs =(fig, scat),
#         frames=100, interval=100,repeat=False)
# 
# kwargs = {
#     'filename': 'test.mp4',
#     'frames': 300,
#     'fps': 30,
#     'writer': 'mencoder',
#     'figsize': (4, 4),
#     'vertex_size': 15
# }
# 
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800) 
# 
# anim.save('/Users/pl/Desktop/test.m4v', writer=writer)       
# #plt.show()            


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mpeg', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
