from matplotlib.animation import FuncAnimation as f_anim
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib import rcParams
import seaborn as sns
sns.set(font_scale=1.1)
rcParams['figure.figsize'] = [7, 6]

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='HaakonSvane'), bitrate=3600)


class Visualizer:
    '''General parent class for the Animator and the Plotter classes. Works as a wrapper for the
       pyplot library. Upon initialization, the constructor takes a parameter subplot_index: a list of
       two elements that describe the amount of subplots that are to be created ([columns], [rows]).
       The class contains a set of dictoinaries that keep track of data added to the different subplots.
       Note that in order to best illustrate the data, the legend must be
       added in last before either the animation or the plot is shown'''

    def __init__(self, subplot_index, frameon=True):
        self.fig, self.axes = plt.subplots(subplot_index[0], subplot_index[1])
        plt.subplots_adjust(left=0.09, bottom=0.088, right=0.995, top=0.957, wspace=None, hspace=0.3)
        self.axes = np.array(self.axes).reshape(subplot_index)
        for i in self.axes.flatten():
            i.set_frame_on(frameon)
        self.data = {}
        self.lines = {}
        self.artists = []
        self.legends = []
        self.shapes = {}

        self.add_counter = 0
        self.lim_fac = 0.15


    def _handle_subplot_index(self, subplot_index):
        # Internal function to handle the different cases for subplot_index
        if subplot_index == "all":
            inds = list(self.data.keys())
        else:
            inds = [tuple(subplot_index)]
        return inds

    def add_circle(self, subplot_index, pos, radius, fill=True):
        ind = tuple(subplot_index)
        c = plt.Circle(pos, radius, fill=fill)
        if ind in self.shapes:
            self.shapes[ind].append(c)
        else:
            self.shapes[ind] = [c]

        self.artists.append(c)

    def add_vline(self, subplot_index, x, y_min=0, y_max=1, **kwargs):
        inds = self._handle_subplot_index(subplot_index)
        try:
            for ind in inds:
                self.axes[ind].axvline(x=x, ymin=y_min, ymax=y_max, **kwargs)
        except IndexError as err:
            print("No such subplot exists to enter data. Did you specify the correct sublot index?\nError:", err)


    def name_axis(self, subplot_index, x_desc, y_desc, title=None):
        # Used to name an axis at a given subplot_index (or "all" to apply to all subplots)
        inds = self._handle_subplot_index(subplot_index)
        try:
            for ind in inds:
                self.axes[ind].set_xlabel(x_desc)
                self.axes[ind].set_ylabel(y_desc)
                if title:
                    self.axes[ind].set_title(title)
        except IndexError as err:
            print("No such subplot exists to enter data. Did you specify the correct sublot index?\nError:", err)

    def set_subplot_pos(self, subplot_index, from_coords, to_coords):
        # The function takes the tuples from "from_coords" and transfers them to "to_coords".
        # Alternatively, the from_coords can be exchanged with "origo" to_coords with "origo" and/or "center".
        # For example, ..(subplot_index, "origo", "center") moves (0,0) to the center of the axis
        inds = self._handle_subplot_index(subplot_index)

        try:
            for ind in inds:
                a = self.axes[ind]

                x_min, x_max = a.get_xlim()
                y_min, y_max = a.get_ylim()
                dx = x_max-x_min
                dy = y_max-y_min

                xm = 0
                ym = 0
                if from_coords == "origo":
                    from_coords = tuple([0, 0])

                if to_coords == "center":
                    to_coords = tuple([x_min + dx/2, y_min + dy/2])

                elif to_coords == "origo":
                    to_coords = tuple([x_min, y_min])

                xm = from_coords[0] - to_coords[0]
                ym = from_coords[1] - to_coords[1]

                a.set_xlim(x_min + xm, x_max + xm)
                a.set_ylim(y_min + ym, y_max + ym)

        except IndexError as err:
            print("No such subplot exists to enter data. Did you specify the correct sublot index?\nError:", err)


    def set_subplot_aspect_ratio(self, subplot_index, aspect_ratio):
        # The function upscales the unit axis on a plot to a aspect ratio (type: tuple).
        inds = self._handle_subplot_index(subplot_index)

        try:
            for ind in inds:
                a = self.axes[ind]

                x_min, x_max = a.get_xlim()
                y_min, y_max = a.get_ylim()
                dx = x_max-x_min
                dy = y_max-y_min
                Ar = aspect_ratio[0]/aspect_ratio[1]

                sx = 1 if Ar*dy/dx < 1 else Ar
                cx = 1 if Ar*dy/dx < 1 else dy/dx
                gx = cx*sx

                sy = 1 if 1/Ar*dx/dy < 1 else 1/Ar
                cy = 1 if 1/Ar*dx/dy < 1 else dx/dy
                gy = cy*sy

                a.set_xlim(1/2 * (x_min * (1 + gx) + x_max * (1 - gx)), 1/2 * ((x_min * (1 - gx)) + x_max * (1 + gx)))
                a.set_ylim(1/2 * (y_min * (1 + gy) + y_max * (1 - gy)), 1/2 * ((y_min * (1 - gy)) + y_max * (1 + gy)))

        except IndexError as err:
            print("No such subplot exists to enter data. Did you specify the correct sublot index?\nError:", err)
        except ZeroDivisionError as err:
            return print("Aspect ratio tuple can not contain zeros.\nError:", err)



    def show_legend(self, subplot_index, location="upper right"):
        # Used to show the legend on an axis at a given subplot_index (or "all" to apply to all subplots)
        inds = self._handle_subplot_index(subplot_index)
        for ind in inds:
            if ind in self.legends:
                print("Already showing legend for this subplot..")
                return
            self.axes[ind].legend(loc=location, frameon=False)

    def add_data(self, x_data, y_data, subplot_index, line_name="line_name", color=None, linestyle=None, marker=None, lw=1, **kwargs):
        # Adds data to the Solver. Takes an array of x-values and a matrix (1d or 2d) of y-data to be plotted
        ind = tuple(subplot_index)

        try:
            if type(y_data) == list:
                y_data = np.array(y_data)
            y_data = y_data.reshape(-1, 1) if y_data.ndim == 1 else y_data

            if type(x_data) == list:
                x_data = np.array(x_data)
            x_data = x_data.reshape(-1, 1) if x_data.ndim == 1 else x_data

            if ind in self.data:
                self.data[ind].append((x_data, y_data))
            else:
                self.data[ind] = [(x_data, y_data)]

            entry, = self.axes[ind].plot([], [], lw=lw, label=line_name, linestyle=linestyle, marker=marker, color=color, **kwargs)
            self.artists.append(entry)

            force_limits = False
            if ind in self.lines:
                self.lines[ind].append(entry)
            else:
                self.lines[ind] = [entry]
                force_limits = True

            # For scaling the plot properly (x and y axis)
            x_max = np.amax(np.abs(x_data))
            x_min = np.amin(x_data)
            y_max = np.amax(np.abs(y_data))
            ax = self.axes[ind].get_xlim()
            ay = self.axes[ind].get_ylim()
            if force_limits:
                self.axes[ind].set_xlim(x_min * (1 - self.lim_fac), x_max * (1 + self.lim_fac))
                self.axes[ind].set_ylim(-y_max * (1 + self.lim_fac) if (y_data < 0).any()
                                        else 0, y_max * (1 + self.lim_fac))
            else:
                self.axes[ind].set_xlim(x_min if x_min < ax[0] else ax[0],
                                        x_max if x_max > ax[1] else ax[1])
                self.axes[ind].set_ylim((-y_max * (1 + self.lim_fac), y_max * (1 + self.lim_fac))
                                        if (y_max * (1 + self.lim_fac) > ay[1] and (y_data < 0).any())
                                        else (ay[0], ay[1]))

            self.add_counter += 1
        except IndexError as err:
            print("No such subplot exists to enter data. Did you specify the correct subplot index?\nError:", err)


class Animator(Visualizer):
    ''' Child class of Visualizer. This class is used to create animations of the data added. Note that
        animations in a jupyter notebook is very hard to get to work on different hardware. It is advisable to
        run this in a python IDE.
    '''

    def __init__(self, subplot_index, fps=60, anim_time=5, speed_fac=1):
        super().__init__(subplot_index)
        self.ani = None
        self.FPS = fps
        self.anim_time = anim_time
        self.speed_fac = speed_fac
        self.frames = int(self.FPS * self.anim_time / self.speed_fac)

    def _anim_init(self):
        # Init function used by the animator. Sets all the lines to empty arrays so that blitting works well
        for (i, j), n in self.data.items():
            for k, l in enumerate(self.lines[(i, j)]):
                l.set_xdata(self.data[(i, j)][k][0])

            for m in self.shapes[(i, j)]:
                self.axes[i][j].add_patch(m)

        return self.artists

    def _anim_update(self, frame):
        # Updating function for the animator. Updates all data with fitting timesteps according to the anim_time
        f = frame / self.frames
        # For each subplot index in and the corresponding list of data for this subplot
        for (i, j), n in self.data.items():
            # Enumerate all the lines that correspond to this index
            for k, l in enumerate(self.lines[(i, j)]):
                # TODO: Performance loss for size calc every iteration. Not needed (?)
                s = self.data[(i, j)][k][1][0, :].size
                l.set_xdata(self.data[(i, j)][k][0][:, int(s * f)])
                l.set_ydata(self.data[(i, j)][k][1][:, int(s * f)])

        return self.artists

    def show_animation(self):
        self.ani = f_anim(self.fig, func=self._anim_update, init_func=self._anim_init,
                          repeat=True, frames=self.frames, interval=1 / self.FPS * 1e3, blit=True)

        plt.show()


class Plotter(Visualizer):
    ''' Child class of Visualizer. This class is used to create still plots of the data added.
    '''

    def __init__(self, subplot_index):
        super().__init__(subplot_index)

    def show_plot(self, t_plot_frac=0):
        '''Shows the plot for the data added. The default parameter t_plot_frac is a fraction in the
           closed interval [0, 1] used to set the timestep displayed on screen. By setting t_plot_frac to
           an integer, all subplots follow this fraction. Alternatively, a dictionary of the form
           {subplot_index: t_plot_frac,...} can be used to set the timestep for each subplots. In this case,
           any subplots not set to a fraction will default to 0'''
        if type(t_plot_frac) == int:
            fracs = {}
        else:
            fracs = t_plot_frac

        for (i, j), n in self.data.items():
            if (i, j) in fracs:
                frac = fracs[(i, j)]
            else:
                frac = t_plot_frac if type(t_plot_frac) == int else 0

            for k, l in enumerate(self.lines[(i, j)]):
                s = self.data[(i, j)][k][1][0, :].size - 1
                l.set_data(self.data[(i, j)][k][0], self.data[(i, j)][k][1][:, int(s * frac)])

        plt.show()



