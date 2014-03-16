import numpy as np
import display

sweep = np.random.randn(900, 1000)
ppi = display.PlanPositionIndicator(sweep, 10)
raw_input()

ppi.sweep[0:100, :] = 1
self.fig