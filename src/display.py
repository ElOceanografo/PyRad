import numpy as np
import matplotlib.pyplot as plt

class PlanPositionIndicator(object):
	"""

	"""
	def __init__(self, sweep, maxrange):
		self.sweep = sweep
		self.theta = np.linspace(0, 2 * np.pi, sweep.shape[0])
		self.range = np.linspace(0, maxrange, sweep.shape[1])
		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111, polar=True)
		self._image = self.ax.pcolormesh(self.theta, self.range, self.sweep)
		self.fig.show()

	def update(self):
		self._image.set_array(self.sweep)