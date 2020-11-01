from src.solve_and_plot import *

sigma = 10
rho = 28
beta = 8/3

n_tpoints = int(1e6)

y0 = [0.001, 0.001, 0.001]
times = np.linspace(0, 50, n_tpoints)

def lorentz(t, x_vec):
    x, y, z = x_vec
    dxdt = sigma*(y-x)
    dydt = x*(rho-z)-y
    dzdt = x*y-beta*z

    return [dxdt, dydt, dzdt]

# Call these functions for 2d or 3d plots
def lorenz_2d():
    sol = solve_diff_eq(lorentz, y0, times)
    plot_solution(times, sol, 'Lorenz')

def lorenz_3d():
    sol = solve_diff_eq(lorentz, y0, times)
    plot_solution(times, sol, 'Lorenz', projection='3D')
