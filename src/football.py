import matplotlib.pyplot as plt
import numpy as np

from math import pi
from typing import List, Optional

class FootballPitch:
    def __init__(self, playerscolor = 'red', bg = 'darkgreen', lines = 'white', textcolor = 'black', figsize=(12, 7)):
        self.bg = bg
        self.lines = lines
        self.playerscolor = playerscolor
        self.textcolor = textcolor
        self.figsize = figsize
        
        self.flipped = False

        self.dotsize = 0.005
        self.default_scattersize = 30

    def _set_fig(self):
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor(self.bg)
        ax.set_facecolor(self.bg)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        self.fig = fig
        self.ax = ax

    def _plot_circles(self):
        w, h = self.figsize

        cx, cy = self.make_pitch_circle(0.5, 0.5, 0.2 * (h / w), 0.2)
        plt.plot(cx, cy, color=self.lines, zorder=0)

        cx, cy = self.make_pitch_circle(0.5, 0.5, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=0)
        
        pen1 = (0.5, 0.11) if self.flipped else (0.11, 0.5)
        cx, cy = self.make_pitch_circle(*pen1, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=0)

        pen2 = (0.5, 0.89) if self.flipped else (0.89, 0.5)
        cx, cy = self.make_pitch_circle(*pen2, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=0)

    def _plot_pitch_lines(self):
        xdata, ydata = self.make_pitch_lines()

        for i in range(0, xdata.shape[0]):
            if self.flipped:
                line = plt.Line2D(xdata=ydata[i], ydata=xdata[i], linewidth=2, color=self.lines, zorder=0)
            else:
                line = plt.Line2D(xdata=xdata[i], ydata=ydata[i], linewidth=2, color=self.lines, zorder=0)
            self.ax.add_line(line)
            
    def _plot_names(self, x: np.ndarray, names: List[str]):
        for i, name in enumerate(names):
            xspace = self.dotsize * (4 if x.shape[1] == 3 else 2)
            pos = x[i, :2] + np.array((xspace, -0.01))
            plt.text(*pos, name, fontsize=12, c=self.textcolor, zorder=1)

    def _validate_input(self, x: np.ndarray):
        if type(x) != np.ndarray:
            raise Exception('Input data is not a numpy array.')
        
        if x.shape[1] < 2 or x.shape[1] > 3:
            raise Exception(f'Input data has invalid shape. Last dimension of input array needs to be 2 or 3, not {x.shape[1]}.')

    def flip(self):
        self.flipped = not self.flipped
        self.figsize = (self.figsize[1], self.figsize[0])

    def plot(self, x: np.ndarray, names: Optional[List[str]] = None, custom_colors: Optional[list] = None):
        self._validate_input(x)
        
        self._set_fig()

        self._plot_pitch_lines()
        self._plot_circles()

        if self.flipped:
            x[:, 0:2] = x[:, 0:2][:, ::-1] # reorder x and y coordinates to match vertical pitch

        if type(names) != type(None):
            self._plot_names(x, names)
        
        colors = custom_colors if type(custom_colors) != type(None) else self.playerscolor

        plt.axis('off')
        size = x[:, 2] if x.shape[1] == 3 else self.default_scattersize
        plt.scatter(x[:, 0], x[:, 1], color=colors, zorder=10, s=size)

    def as_numpy(self, x: np.ndarray, names: Optional[List[str]] = None, custom_colors: Optional[list] = None):
        self.plot(x, names, custom_colors)

        self.fig.canvas.draw()
        data = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        return data

    @staticmethod
    def make_pitch_circle(x: float, y: float, rx: float, ry: float):
        t = np.linspace(0, 2*pi, 100)
        return x+rx*np.cos(t), y+ry*np.sin(t)

    @staticmethod
    def make_pitch_lines():
        x = np.array([
            # outline
            (0.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0),
            (0.0, 1.0),

            # penalty area 1
            (0.0, 0.165),
            (0.0, 0.165),
            (0.165, 0.165),

            # penalty area 2
            (0.835, 1.0),
            (0.835, 1.0),
            (0.835, 0.835),

            # penalty area 1 small
            (0.0, 0.055),
            (0.0, 0.055),
            (0.055, 0.055),

            # penalty area 2 small
            (1.0, 0.945),
            (1.0, 0.945),
            (0.945, 0.945),

            # middle line
            (0.5, 0.5)
        ])
        y = np.array([
            # outline
            (0.0, 1.0),
            (0.0, 1.0),
            (0.0, 0.0),
            (1.0, 1.0),

            # penalty area 1
            (0.2, 0.2),
            (0.8, 0.8),
            (0.2, 0.8),
            
            # penalty area 2
            (0.2, 0.2),
            (0.8, 0.8),
            (0.2, 0.8),

            # penalty area 1 small
            (0.36, 0.36),
            (0.64, 0.64),
            (0.36, 0.64),

            # penalty area 2 small
            (0.36, 0.36),
            (0.64, 0.64),
            (0.36, 0.64),

            # middle line
            (0.0, 1.0)
        ])

        return x, y