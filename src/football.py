import matplotlib.pyplot as plt
import numpy as np
from math import pi

class FootballPitch:
    def __init__(self, players = 'red', bg = 'green', lines = 'white', figsize=(12, 7)):
        self.bg = bg
        self.lines = lines
        self.players = players
        self.figsize = figsize
        
        self.flipped = False

    def set_fig(self):
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor(f'xkcd:{self.bg}')
        ax.set_facecolor(f'xkcd:{self.bg}')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        self.fig = fig
        self.ax = ax

    def flip(self):
        self.flipped = not self.flipped
        self.figsize = (self.figsize[1], self.figsize[0])

    def plot_circles(self):
        w, h = self.figsize

        cx, cy = self.make_pitch_circle(0.5, 0.5, 0.2 * (h / w), 0.2)
        plt.plot(cx, cy, color=self.lines)

        cx, cy = self.make_pitch_circle(0.5, 0.5, 0.005 * (h / w), 0.005)
        plt.fill(cx, cy, color=self.lines)
        
        pen1 = (0.5, 0.11) if self.flipped else (0.11, 0.5)
        cx, cy = self.make_pitch_circle(*pen1, 0.005 * (h / w), 0.005)
        plt.fill(cx, cy, color=self.lines)

        pen2 = (0.5, 0.89) if self.flipped else (0.89, 0.5)
        cx, cy = self.make_pitch_circle(*pen2, 0.005 * (h / w), 0.005)
        plt.fill(cx, cy, color=self.lines)

    def plot_lines(self):
        xdata, ydata = self.make_pitch_lines()

        for i in range(0, xdata.shape[0]):
            if self.flipped:
                line = plt.Line2D(xdata=ydata[i], ydata=xdata[i], linewidth=2, color=self.lines)
            else:
                line = plt.Line2D(xdata=xdata[i], ydata=ydata[i], linewidth=2, color=self.lines)
            self.ax.add_line(line)

    def plot(self, x):
        self.set_fig()

        self.plot_lines()
        self.plot_circles()

        plt.axis('off')
        plt.scatter(x[:, 0], x[:, 1], color=self.players)

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
    