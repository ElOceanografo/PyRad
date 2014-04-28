import sys
import time
import random
import threading
from PyQt4 import QtGui, QtCore
import Queue
from scope_monitor import ScopeMonitorThread


class RadarConsole(QtGui.QWidget):

	def __init__(self):
		super(RadarConsole, self).__init__()

		self.initUI()
		self.scope_monitor = None
		self.recording = False
		self.radar_data_q = None
		self.connect_scope()
		self.set_output_file()
		self.status_text.setText("Ready")

	def initUI(self):
		# control panel
		self.recordBtn = QtGui.QPushButton("Record", self)
		self.recordBtn.setStyleSheet("color : black; background-color: green")
		self.recordBtn.setCheckable(True)
		self.recordBtn.clicked[bool].connect(self.setRecording)
		controlsLayout = QtGui.QVBoxLayout()
		controlsLayout.addWidget(self.recordBtn)
		controlsLayout.addStretch(1)
		self.status_text = QtGui.QLabel('Ready')
		controlsLayout.addWidget(self.status_text)

		# display panel
		displaySplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.ppi = QtGui.QLabel(self)
		self.ascope = QtGui.QLabel(self)
		displaySplitter.addWidget(self.ppi)
		#### Just for now
		displaySplitter.addWidget(self.ascope)
		self.ascope.setText("A-Scope")
		####

		# entire layout
		overallLayout = QtGui.QHBoxLayout()
		# "1" argument means make this one stretch
		overallLayout.addWidget(displaySplitter, 1)
		overallLayout.addLayout(controlsLayout)

		self.setLayout(overallLayout)

		self.setWindowTitle("PyRad Console")
		self.setGeometry(100, 20, 1000, 800)
		self.show()

	def connect_scope(self):
		self.status_text.setText("(Connecting to scope)")
		time.sleep(2)

	def set_output_file(self):
		self.status_text.setText("(Choosing output file)")
		time.sleep(2)

	def setRecording(self, on):
		if on:
			self.startRecording()
		else:
			self.stopRecording()

	def startRecording(self):
		if self.scope_monitor is not None: # i.e., if we're already recording
			return

		self.recordBtn.setStyleSheet("color : black; background-color: red")
		self.recording = True
		self.radar_data_q = Queue.Queue()
		self.scope_monitor = ScopeMonitorThread(self.radar_data_q)
		self.status_text.setText("Starting data acquisition...")
		self.scope_monitor.start()
		self.status_text.setText("Recording")

		#self.update_plot()



	def stopRecording(self):

		if self.scope_monitor is not None:
			self.scope_monitor.join()
			#self.plot_thread.join()
			self.status_text.setText("Stopping data acquisition...")
			self.scope_monitor = None

		self.status_text.setText("Ready")
		self.recordBtn.setStyleSheet("color : black; background-color: green")
		self.recording = False

	def update_plots(self):
		while self.recording:
			try:
				timestamp, data = self.radar_data_q.get(True)
				self.ascope.setText(repr(timestamp))
				self.ppi.setText(repr(data[0:10]))
			except Queue.empty:
				pass

		
def main():
	app = QtGui.QApplication(sys.argv)
	ex = RadarConsole()
	app.exec_()

if __name__ == '__main__':
	main()