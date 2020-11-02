from src.solve_and_plot import *
from scipy.signal import argrelextrema

a = 0.2
b = 0.2
c = 5.7

n_tpoints = int(1e8)

y0 = [0.001, 0.001, 0.001]
times = np.linspace(0, 1e6, n_tpoints)

def rossler(t, x_vec):
    x, y, z = x_vec
    dxdt = -y-z
    dydt = x + a*y
    dzdt = b+z*(x-c)

    return [dxdt, dydt, dzdt]

# Call these functions for 2d or 3d plots
def rossler_2d():
    sol = solve_diff_eq(rossler, y0, times)
    plot_solution(times, sol, 'Rössler')

def rossler_3d():
    sol = solve_diff_eq(rossler, y0, times)
    plot_solution(times, sol, 'Rössler', projection='3D')

def rossler_tz():
    sol = solve_diff_eq(rossler, y0, times)
    plot_solution(times, sol, 'Rössler', projection='tz')

def rossler_mapping():
    x, y, z = solve_diff_eq(rossler, y0, times)
    max_ind = argrelextrema(z, np.greater)
    p = Plotter((1,1))
    p.add_data(subplot_index=(0, 0), x_data=z[max_ind][:-1], y_data=z[max_ind][1:], marker='o', linestyle='None',
               markersize=0.2, line_name='Lorenz map')
    p.add_data(subplot_index=(0, 0), x_data=np.arange(-1, 41), y_data=np.arange(-1, 41), line_name="$z_{n+1} = z_n$")
    p.show_legend(subplot_index='all', location='upper left')
    plt.title('Lorenz map of the Rössler attractor for $z(t)$')
    p.name_axis((0, 0), x_desc='$z_n$', y_desc='$z_{n+1}$')
    p.show_plot()

rossler_mapping()