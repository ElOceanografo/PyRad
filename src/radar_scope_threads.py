import threading
from Queue import Queue
import time
import sys
import numpy as np

TIMESTAMP_FMT = "%Y%m%d_%H%M%S"

class DataAcquisitionThread(threading.Thread):
	"""docstring for DataAcquisitionThread"""
	def __init__(self, data_q, radar_scope):
		super(DataAcquisitionThread, self).__init__()
		self.radar_scope = radar_scope
		self.data_q = data_q
		self.alive = threading.Event()
		self.alive.set()

	def run(self):
		threading.Thread(target=sys.stdout.write, args=("foo",)).start()
		while self.alive.isSet():
			timestamp = time.strftime(TIMESTAMP_FMT)
			self.radar_scope.capture_trimmed_sweep()
			self.data_q.put((timestamp, self.radar_scope.trimmed_sweep))

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
			if self.radar_console.recording:
				self.radar_console.save_file()
			self.data_q.task_done()

	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)