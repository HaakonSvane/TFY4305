from src.visualizer import *
import numpy as np

p_map = lambda r: 1/np.sqrt(1+1/np.e*(1/r**2-1))
line45 = lambda r: r

def cobweb(x0, func, nsteps=100):
    cx = np.zeros(nsteps+1)
    cy = np.zeros(nsteps+1)
    cx[0], cy[0] = x0, 0
    for i in range(1, nsteps, 2):
        cx[i] = cx[i-1]
        cy[i] = func(cx[i-1])
        cx[i+1] = cy[i]
        cy[i+1] = cy[i]

    return cx, cy


def sub_prob_a():
    r_arr = np.linspace(0,2,100)
    p_arr = p_map(r_arr)
    line_arr = line45(r_arr)
    cx1, cy1 = cobweb(0.2, p_map)
    cx2, cy2 = cobweb(1.8, p_map)

    p = Plotter((1, 1))
    p.add_data(x_data=r_arr, y_data=line_arr, subplot_index=(0,0), lw=2, line_name='$y(r) = r$')
    p.add_data(x_data=r_arr, y_data=p_arr, subplot_index=(0,0), lw=2, line_name='Poincaré map $P(r)$')
    p.add_data(x_data=cx1, y_data=cy1, subplot_index=(0,0), lw=1, line_name='Cobweb starting at $r_0 = 0.2$')
    p.add_data(x_data=cx2, y_data=cy2, subplot_index=(0,0), lw=1, line_name='Cobweb starting at $r_0 = 1.8$')
    p.add_vline(subplot_index=(0,0), x=1,lw=1, linestyle='--', color='black')
    p.show_legend('all', location='upper left')
    p.name_axis((0,0), x_desc='$r$', y_desc='$P(r)$')
    plt.title('Cobweb analysis of the Poincaré map with 100 cobweb iterations')
    p.show_plot()

def sub_prob_b():
    cx, cy = cobweb(0.1, p_map, 30*2) # Since one iteration is either a move along the x-axis or the y-axis
    iters = np.arange((cx.size+1)//2)

    p = Plotter((1, 1))
    p.add_data(x_data=iters, y_data=cx[::2], subplot_index=(0,0), lw=2, line_name='Value of $r$')
    p.show_legend('all')
    p.name_axis(subplot_index=(0,0), x_desc='iterations', y_desc='$r$')
    plt.title('Value of $r$ starting from $r_0=0.1$ over 30 iterations')
    p.show_plot()

sub_prob_b()