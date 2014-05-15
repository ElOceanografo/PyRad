import threading
from Queue import Queue
import time
import numpy as np

class ScopeMonitorThread(threading.Thread):
	"""docstring for ScopeMonitorThread"""
	def __init__(self, data_q, radar_scope):
		super(ScopeMonitorThread, self).__init__()
		self.radar_scope = radar_scope
		self.data_q = data_q
		self.alive = threading.Event()
		self.alive.set()

	def run(self):
		dt = 2.0 #2100.0
		while self.alive.isSet():
			timestamp = time.time()
			self.radar_scope.capture_sweep()
			self.data_q.put((timestamp, self.radar_scope.get_trimmed_sweep()))
			time.sleep(dt)

	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)

