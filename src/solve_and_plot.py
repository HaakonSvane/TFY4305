from src.visualizer import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint


r_tol = 1.49012e-10
a_tol = r_tol

def solve_diff_eq(func, init_values, times, print_res_dict=False):
    res, res_dict = odeint(func, init_values, times, full_output=True, tfirst=True, rtol=r_tol, atol=a_tol)
    if print_res_dict:
        print(res_dict)
    return res.transpose()

def plot_solution(t, y, func_name, projection='xz'):
    projection_dict = {
        'xz': (0, 2),
        'xy': (0, 1),
        'yz': (1, 2),
        'tx': (0, 0),
        'ty': (0, 1),
        'tz': (0, 2),
    }
    proj_name = projection if projection.lower() != '3d' else '3-dimensional'
    p = None
    if projection.lower() == '3d':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(xs=y[0], ys=y[1], zs=y[2], lw=1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
    else:
        try:
            p = Plotter((1,1))
            x_ind = projection_dict[projection.lower()][0]
            y_ind = projection_dict[projection.lower()][1]
            if projection.lower()[0] == 't':
                p.add_data(x_data=t, y_data=y[y_ind], subplot_index=(0, 0), line_name="LSODA (odeint)")
            else:
                p.add_data(x_data=y[x_ind], y_data=y[y_ind], subplot_index=(0, 0), line_name="LSODA (odeint)")
            p.name_axis((0, 0), x_desc=projection.lower()[0], y_desc=projection.lower()[1])
        except KeyError as err:
            print('Projection is not valid. Error:', err)

    plt.title(f'{proj_name + ("-" if proj_name is not "3-dimensional" else " ")}plot of the {func_name} equations solved using the LSODA integrator.')

    if projection.lower() != '3d':
        p.show_plot()
    else:
        plt.show()

