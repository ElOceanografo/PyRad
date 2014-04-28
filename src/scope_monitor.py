import threading
from Queue import Queue
import time
import numpy as np

class ScopeMonitorThread(threading.Thread):
	"""docstring for ScopeMonitorThread"""
	def __init__(self, data_q):
		super(ScopeMonitorThread, self).__init__()

		self.data_q = data_q
		self.alive = threading.Event()
		self.alive.set()

	def run(self):
		dt = 1.0 #2100.0
		while self.alive.isSet():
			timestamp = time.time()
			self.data_q.put((timestamp, np.random.randn(128)))
			time.sleep(dt)

	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)

