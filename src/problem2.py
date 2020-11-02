from src.solve_and_plot import *
from scipy.signal import argrelextrema

sigma = 10
rho = 28
beta = 8/3

n_tpoints = int(1e6)

y0 = [0.001, 0.001, 0.001]
times = np.linspace(0, 50, n_tpoints)

def lorenz(t, x_vec):
    x, y, z = x_vec
    dxdt = sigma*(y-x)
    dydt = x*(rho-z)-y
    dzdt = x*y-beta*z

    return [dxdt, dydt, dzdt]

# Functions for the subproblems
def lorenz_2d():
    sol = solve_diff_eq(lorenz, y0, times)
    plot_solution(times, sol, 'Lorenz', projection='tz')

def lorenz_3d():
    sol = solve_diff_eq(lorenz, y0, times)
    plot_solution(times, sol, 'Lorenz', projection='3D')

def lorenz_tz():
    sol = solve_diff_eq(lorenz, y0, times)
    plot_solution(times, sol, 'Lorenz', projection='tz')

def lorenz_mapping():
    x, y, z = solve_diff_eq(lorenz, y0, times)
    max_ind = argrelextrema(z, np.greater)
    p = Plotter((1,1))
    p.add_data(subplot_index=(0, 0), x_data=z[max_ind][:-1], y_data=z[max_ind][1:], marker='o', linestyle='None',
               markersize=0.2, line_name='Lorenz map')
    p.add_data(subplot_index=(0, 0), x_data=np.arange(20, 61), y_data=np.arange(20, 61), line_name="$z_{n+1} = z_n$")
    p.show_legend(subplot_index='all', location='upper left')
    plt.title('Lorenz map of the Lorenz attractor for $z(t)$')
    p.name_axis((0, 0), x_desc='$z_n$', y_desc='$z_{n+1}$')
    p.show_plot()


