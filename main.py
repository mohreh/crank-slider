import math
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# given information
a_b = 0.5 # distance between A and B in m
b_c = 1   # distance between B and C in m
w = 30  # in rpm

t = sym.symbols('t')
phi = 1/2 * t # in radian per second, w * 1/60 

# position of joint A 
x_a = 0 
y_a = 0 

# position of joint B 
x_b = sym.cos(phi) * a_b
y_b = sym.sin(phi) * a_b

# y position of c  
y_c = 0  
x_c = sym.symbols('x_c')

# expressions we need
expr_1 = x_b * sym.sin(phi) - y_b * sym.cos(phi) # tan(phi) = y_b / x_b
expr_2 = (x_b - x_c) ** 2 + (y_b - y_c) ** 2 - b_c ** 2 # b_c^2 = (x_b - x_c)^2 + (y_b - y_c)^2 

v_x_b = x_b.diff(t)
v_y_b = y_b.diff(t)

a_x_b = v_x_b.diff(t)
a_y_b = v_y_b.diff(t)

# drawing plot
fig = plt.figure(figsize=(16,8), dpi=80)
grid_spec = fig.add_gridspec(
        nrows=2, 
        ncols=2,
        left=0.05, 
        right=0.99,              
        hspace=0.3, 
        wspace=0.2
    )

ax_position = fig.add_subplot(
        grid_spec[:, 0], 
        aspect='equal', 
        autoscale_on=True,                   
        xlim=(-0.8, 1.8), # x axis preiod 
        ylim=(-1, 1), # y axis preiod
        xlabel="X Label",
        ylabel="Y Label"
    )

position_line, = ax_position.plot(
        [], 
        [], 
        color='green', # color of lines
        linestyle='dashed', # line styles 
        linewidth = 1, # line width
        marker='o', # each crank will be a circle in plot
        markerfacecolor='blue', #
        markersize=10 # circle's diameter size
    )

ax_position.set_title('Position Analysis') # plot title
ax_position.set_xticks(np.arange(-0.8, 1.8, 0.2)) # x axis grid
ax_position.set_yticks(np.arange(-1, 1, 0.2)) # y axis grid
time_text = ax_position.text(0.02, 0.95, '', transform=ax_position.transAxes) # time text in plot, with position of it
ax_position.grid() # draw grid

frames = 360 # total frames of animation, in this proje also is growing scale of angle 
interval = (4 * math.pi / frames) * 1000 # time before next frame in mili seconds, which is total time of full circle circumferenceof system divided on number of frames 

ax_velocity_b = fig.add_subplot(
        grid_spec[0, 1],
        autoscale_on=True,
        xlabel=r"$T (s)$",
        ylabel=r"$v_b (m/s)$",
        xlim=(0, 13),
        ylim=(-0.3, 0.3),
    )

ax_velocity_b.set_title('Velocity Over Seconds') # plot title
ax_velocity_b.set_xticks(np.arange(0, 12.556, 1)) # x axis grid
ax_velocity_b.set_yticks(np.arange(-0.3, 0.3, 0.1)) # y axis grid
ax_velocity_b.grid()

ax_acceleration_b = fig.add_subplot(
        grid_spec[1, 1],
        autoscale_on=True,
        xlabel=r"$T (s)$",
        ylabel=r"$a (m/s^2)$",
        xlim=(0, 13),
        ylim=(-0.15, 0.15),
    )

ax_acceleration_b.set_title('Acceleration Over Seconds') # plot title
ax_acceleration_b.set_xticks(np.arange(0, 12.556, 1)) # x axis grid
ax_acceleration_b.set_yticks(np.arange(-0.15, 0.15, 0.05)) # y axis grid
ax_acceleration_b.grid()

V_x_b = []
V_y_b = []
A_x_b = []
A_y_b = []
T = []

for i in range(frames):
    T.append((4 * math.pi / frames) * i)
    V_x_b.append(v_x_b.subs({ t: T[-1] }).evalf())
    V_y_b.append(v_y_b.subs({ t: T[-1] }).evalf())
    A_x_b.append(a_x_b.subs({ t: T[-1] }).evalf())
    A_y_b.append(a_y_b.subs({ t: T[-1] }).evalf())

velocity_x_b_line = ax_velocity_b.plot(
        T,
        V_x_b,
        color='green',
        label='v_x_b'
    )

velocity_y_b_line = ax_velocity_b.plot(
        T,
        V_y_b,
        color='blue',
        label='v_y_b'
    )

velocity_x_b_dot, = ax_velocity_b.plot(
        [],
        [],
        marker='o', # each crank will be a circle in plot
        markerfacecolor='red', #
        markersize=5 # circle's diameter size
    )

velocity_y_b_dot, = ax_velocity_b.plot(
        [],
        [],
        marker='o', # each crank will be a circle in plot
        markerfacecolor='red', #
        markersize=5 # circle's diameter size
    )

ax_velocity_b.legend(loc='best')


acceleration_x_b_line = ax_acceleration_b.plot(
        T,
        A_x_b,
        color='green',
        label='a_x_b'
    )

acceleration_y_b_line = ax_acceleration_b.plot(
        T,
        A_y_b,
        color='blue',
        label='a_y_b'
    )

acceleration_x_b_dot, = ax_acceleration_b.plot(
        [],
        [],
        marker='o', # each crank will be a circle in plot
        markerfacecolor='red', #
        markersize=5 # circle's diameter size
    )

acceleration_y_b_dot, = ax_acceleration_b.plot(
        [],
        [],
        marker='o', # each crank will be a circle in plot
        markerfacecolor='red', #
        markersize=5 # circle's diameter size
    )

ax_acceleration_b.legend(loc='best')

def init(): # this is way of creating animation in python, we pass this function to FuncAnimatation. see matplotlib docs for more  
    position_line.set_data([], [])
    velocity_x_b_dot.set_data([], [])
    velocity_y_b_dot.set_data([], [])
    acceleration_x_b_dot.set_data([], [])
    acceleration_y_b_dot.set_data([], [])
    time_text.set_text('')
    return position_line, velocity_x_b_dot, velocity_y_b_dot, acceleration_x_b_dot, acceleration_y_b_dot, time_text

def animate(i):
    global t, phi, x_b, y_b, y_c, x_c, expr_1, expr_2

    subs = {}

    subs[t] = (4 * math.pi / frames) * i
    subs[phi] = phi.subs(subs).evalf()

    # position of joint B 
    subs[x_b] = x_b.subs(subs).evalf()
    subs[y_b] = y_b.subs(subs).evalf()

    subs[y_c] = y_c
    subs[x_c] = 'x_c'

    sol_2 = sym.solve(expr_2.subs(subs).evalf(), 'x_c')

    x_c1 = sol_2[0]
    x_c2 = sol_2[1]

    if x_c1 > subs[x_b]:
        x_c = x_c1
    else:
        x_c = x_c2

    x = [subs[x_a], subs[x_b], x_c] # location of each crank on x-axis
    y = [subs[y_a], subs[y_b], y_c] # location of each crank on y-axis
     
    position_line.set_data(x, y) # set datas for line on plot
    velocity_x_b_dot.set_data(
            subs[t],
            v_x_b.subs(subs).evalf(),
        )
    velocity_y_b_dot.set_data(
            subs[t],
            v_y_b.subs(subs).evalf()
        )
    acceleration_x_b_dot.set_data(
            subs[t],
            a_x_b.subs(subs).evalf()
        )
    acceleration_y_b_dot.set_data(
            subs[t],
            a_y_b.subs(subs).evalf()
        )
    time_text.set_text('time = {} seconds'.format(round(interval * i / 1000, 2))) # printing times passed
    return position_line, velocity_x_b_dot, velocity_y_b_dot, acceleration_x_b_dot, acceleration_y_b_dot, time_text

# calculate wasted time of running animate(i) funcion
# running animate(i) func will take time in any comuper and will affect animation, by calculate time of running animate(i) once, we can subtarct it of calculate interval, to make better animation and real one
from time import time
t0 = time()
animate(87)
t1 = time()
interval = interval - (t1 - t0) # new interval is same last interval but we subtarct the time of running animate(i) function

print('hi there ')
anim = anim.FuncAnimation( # create animation func with matplotlib that reciew plot and animate function and create animation
        fig,
        animate, # animate(i) function will repeat in range of frame, i will start from 0
        # passing other properties to function
        init_func=init,
        frames=frames,
        interval=interval,
        blit=True
    )

anim.save('position_anime.gif', writer='imagemagick') # saving animation

