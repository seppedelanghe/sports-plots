import matplotlib.pyplot as plt
import numpy as np

class BasePlot:
    def __init__(self, figsize: tuple = (12, 7)):
        self.scale = (0.0, 1.0)
        self.figsize = figsize

    def _normalize(self, x: np.ndarray):
        return (x - self.scale[0]) / (self.scale[1] - self.scale[0])

    def _set_fig(self):
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor(self.bg)
        ax.set_facecolor(self.bg)
        ax.set_xlim(0, 1)
        ax.set_ylim(1, 0) # 1, 0 to make y go from top to bottom

        self.fig = fig
        self.ax = ax

    def close(self):
        plt.close(self.fig)

    def show(self):
        self.fig.show()

    def save(self, path):
        self.fig.savefig(path)

    def to_numpy(self):
        self.fig.canvas.draw()
        data = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        return data