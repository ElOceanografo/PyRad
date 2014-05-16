import threading
from Queue import Queue
import time
import numpy as np

class DataAcquisitionThread(threading.Thread):
	"""docstring for DataAcquisitionThread"""
	def __init__(self, data_q, radar_scope):
		super(DataAcquisitionThread, self).__init__()
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


class DataProcessingThread(threading.Thread):
	"""docstring for DataProcessingThread"""
	def __init__(self, data_q, radar_scope, radar_console):
		super(DataProcessingThread, self).__init__()
		self.data_q = data_q
		self.radar_scope = radar_scope
		self.radar_console = radar_console
		self.alive = threading.Event()
		self.alive.set()

	def run(self):
		while self.alive.isSet():
			timestamp, data = self.data_q.get()
			self.radar_console.data = data
			self.radar_console.timestamp = timestamp
			self.radar_console.update_ppi()
			self.data_q.task_done()

	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)