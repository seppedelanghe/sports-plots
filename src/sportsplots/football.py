import matplotlib.pyplot as plt
import numpy as np

from math import pi
from typing import List, Optional

from sportsplots.base import BasePlot

class FootballPitch(BasePlot):
    def __init__(self, playerscolor = 'red', bg = 'darkgreen', lines = 'white', textcolor = 'black', figsize=(12, 7)):
        super().__init__(figsize=figsize)

        self.bg = bg
        self.lines = lines
        self.playerscolor = playerscolor
        self.textcolor = textcolor
        
        self.flipped = False

        self.dotsize = 0.005
        self.default_scattersize = 30

        self.z_pitch = 0
        self.z_links = 1
        self.z_dots = 2
        self.z_names = 3

    def _plot_circles(self):
        w, h = self.figsize

        cx, cy = self.make_pitch_circle(0.5, 0.5, 0.2 * (h / w), 0.2)
        plt.plot(cx, cy, color=self.lines, zorder=self.z_pitch)

        cx, cy = self.make_pitch_circle(0.5, 0.5, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=self.z_pitch)
        
        pen1 = (0.5, 0.11) if self.flipped else (0.11, 0.5)
        cx, cy = self.make_pitch_circle(*pen1, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=self.z_pitch)

        pen2 = (0.5, 0.89) if self.flipped else (0.89, 0.5)
        cx, cy = self.make_pitch_circle(*pen2, self.dotsize * (h / w), self.dotsize)
        plt.fill(cx, cy, color=self.lines, zorder=self.z_pitch)

    def _plot_pitch_lines(self):
        xdata, ydata = self.make_pitch_lines()

        for i in range(0, xdata.shape[0]):
            if self.flipped:
                line = plt.Line2D(xdata=ydata[i], ydata=xdata[i], linewidth=2, color=self.lines, zorder=self.z_pitch)
            else:
                line = plt.Line2D(xdata=xdata[i], ydata=ydata[i], linewidth=2, color=self.lines, zorder=self.z_pitch)
            self.ax.add_line(line)

    def _plot_names(self, x: np.ndarray, names: list):
        valid = type(names[0]) == str or (type(names[0]) == tuple and type(names[0][0]) == int and type(names[0][1]) == str)
        if not valid:
            raise Exception('Names is invalid format. Names parameter needs to be list of strings or list of Tuple[int, str] containing the index of the player and the name.')
        
        names = [(i, name) for i, name in enumerate(names)] if type(names[0]) == str else names
        
        x[:, 0:2] = self._normalize(x[:, 0:2])

        for i, name in names:
            xspace = self.dotsize * (4 if x.shape[1] == 3 else 2)
            pos = x[i, :2] + np.array((xspace, -0.01))
            plt.text(*pos, name, fontsize=12, c=self.textcolor, zorder=self.z_names)

    def _validate_input(self, x: np.ndarray):
        if type(x) != np.ndarray:
            raise Exception('Input data is not a numpy array.')
        
        if x.shape[1] < 2 or x.shape[1] > 3:
            raise Exception(f'Input data has invalid shape. Last dimension of input array needs to be 2 or 3, not {x.shape[1]}.')

    def flip(self):
        self.flipped = not self.flipped
        self.figsize = (self.figsize[1], self.figsize[0])

    def plot(self, x: np.ndarray, names: Optional[list] = None, custom_colors: Optional[list] = None):
        self._validate_input(x)
        
        self._set_fig()

        self._plot_pitch_lines()
        self._plot_circles()

        x[:, 0:2] = self._normalize(x[:, 0:2])

        if self.flipped:
            x[:, 0:2] = x[:, 0:2][:, ::-1] # reorder x and y coordinates to match vertical pitch

        if type(names) != type(None) and len(names) > 0:
            self._plot_names(x, names)
        
        colors = custom_colors if type(custom_colors) != type(None) else self.playerscolor

        plt.axis('off')
        size = x[:, 2] if x.shape[1] == 3 else self.default_scattersize
        plt.scatter(x[:, 0], x[:, 1], color=colors, zorder=self.z_dots, s=size)

    def plot_links(self, pos, links,
            names: Optional[List[str]] = None,
            custom_player_colors: Optional[List[str]] = None,
            custom_link_colors: Optional[List[str]] = None):
        self.plot(pos, names, custom_player_colors)

        colors = custom_link_colors if type(custom_link_colors) != type(None) else ['white' for _ in range(links.shape[0])]

        for idx, (f, t, s) in enumerate(links):
            pos[f, :2] = self._normalize(pos[f, :2])
            pos[t, :2] = self._normalize(pos[t, :2])
            
            fx, fy = pos[f, :2]
            tx, ty = pos[t, :2]
            line = plt.Line2D(xdata=(fx, tx), ydata=(fy, ty), linewidth=s, color=colors[idx], zorder=self.z_links)
            self.ax.add_line(line)

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