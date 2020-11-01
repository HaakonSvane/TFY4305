from src.solve_and_plot import *

a = 0.2
b = 0.2
c = 5.7

n_tpoints = int(1e6)

y0 = [0.001, 0.001, 0.001]
times = np.linspace(0, 500, n_tpoints)

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

rossler_3d()