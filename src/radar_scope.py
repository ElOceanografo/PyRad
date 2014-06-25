from pico_python.picoscope import ps3000a
import numpy as np
import scipy as sp
from scipy.io import netcdf
import time
from ctypes import *
import os
import threading

# collect 5% more samples than nominally necessary
SAMPLE_SAFETY_MARGIN = 1.05
LIGHTSPEED = 2.99e8
METADATA_LENGTH = 200


class RadarScope(object):
	"""Interface to picoscope, connected to radar"""

	def __init__(self, ps, rotation_period=2.4, pulse_rate=2100,
		range_resolution=10.0, max_range=1e3, video_chan="A", 
		video_voltage=[-0.1, 2], trigger_voltage=0.6,
		heading_chan="B", heading_voltage=[1, -10], heading_threshold=-0.8, data_dir="."):
		'''
		Set up interface to PicoScope for radar data collection.

		Parameters
		----------
		ps : ps3000a object
		rotation_period : float
			Nominal antenna rotation period.
		pulse_rate : int
			Nominal radar pulse rate.
		max_range : float
			range, in meters, to which samples will be recorderd
		range_resolution : float
			Nominal range resolution for radar data capturing. This is
			translated to the digital (time) sampling rate.  The actual
			physical range resolution is limited by the radar pulse length.
		video_chan, heading_chan : String
			Oscilloscope channels (e.g. "A", "B") connected to the radar's 
			video and heading pulse signals.
		video_voltage, heading_voltage : List
			Lists containing the minimum and maximum DC voltages needed
			to capture the input signals
		trigger_voltage : float
			Trigger data collection when video rises past this threshold
		'''
		super(RadarScope, self).__init__()
		self.ps = ps
		self.rotation_period = rotation_period
		self.pulse_rate = pulse_rate
		self.max_range = max_range
		self.range_resolution = range_resolution
		self.video_chan = video_chan
		self.heading_chan = heading_chan
		self.video_voltage = video_voltage
		self.heading_voltage = heading_voltage
		self.trigger_voltage = trigger_voltage
		self.heading_threshold = heading_threshold
		self.n_captures = int(self.pulse_rate * rotation_period * 
			SAMPLE_SAFETY_MARGIN)
		self.sample_interval = 2 * self.range_resolution / LIGHTSPEED
		self.capture_duration = self.max_range * 2 / LIGHTSPEED
		self.data_dir = data_dir

		self.setup_sweep()
		self.video_buffer = np.zeros((self.n_captures, self.samples_per_segment), 
			dtype=np.int16)
		self.heading_buffer = np.zeros((self.n_captures, self.samples_per_segment), 
			dtype=np.int16)

	def setup_sweep(self):
		# set up oscilloscope channels, trigger, and sampling rate
		self.ps.setChannel(channel=self.video_chan, coupling="DC", 
			VRange=max([abs(x) for x in self.video_voltage]))
		self.ps.setChannel(channel=self.heading_chan, coupling="DC", 
			VRange=max([abs(x) for x in self.heading_voltage]))
		self.ps.setSamplingInterval(self.sample_interval, self.capture_duration)
		
		self.ps.setSimpleTrigger(self.video_chan, threshold_V=self.trigger_voltage)
		# self.ps.setSimpleTrigger("External", direction="Falling", threshold_V=-0.2, timeout_ms=0)
		self.max_samples_per_segment = self.ps.memorySegments(self.n_captures)
		self.samples_per_segment = self.ps.noSamples#int(self.capture_duration / self.sample_interval)
		self.ps.setNoOfCaptures(self.n_captures)



	def wait_zero_heading(self):
		print "waiting for heading..."
		self.ps.setChannel(channel=self.heading_chan, coupling="DC", 
			VRange=max([abs(x) for x in self.heading_voltage]))
		self.ps.setSamplingInterval(1e-3, 0.5)
		
		self.ps.setSimpleTrigger(self.heading_chan, direction="Falling", 
			threshold_V=self.heading_threshold, timeout_ms=int(2.4*1000))		
		self.ps.memorySegments(1)
		self.ps.setNoOfCaptures(1)
		self.ps.runBlock()
		self.ps.waitReady()
		print "heading fired"
		self.setup_sweep()

		
	def run_sweep(self):
		'''
		Tells the PicoScope to run one rapid block of radar pulses
		according to the pre-specified settings.  Does not transfer the data
		collected from the PicoScope's memory to the computer.
		'''
		t1 = time.time()
		self.wait_zero_heading()
		t2 = time.time()
		print "Waited", str(time.time() - t1), "seconds for sweep"
		self.last_sweep_time = time.strftime("%Y%m%d_%H%M%S")
		self.ps.runBlock()

	def transfer_data(self, downsample_ratio=0, downsample_mode=0):
		'''
		Transfers stored data from the PicoScope's buffers to the computer's
		memory.
		'''
		t1 = time.time()
		self.ps.getDataRawBulk(channel=self.video_chan, data=self.video_buffer)
		self.ps.getDataRawBulk(channel=self.heading_chan, data=self.heading_buffer)
		print "Time to transfer data: ", str(time.time() - t1)

	def transfer_data2(self, threshold=1000, skip=2, downsample_ratio=0, 
			downsample_mode=0):
		heading = sp.zeros(self.n_captures / skip + 1)
		for i, segment in enumerate(range(0, self.n_captures, skip)):
			heading_tuple = self.ps.getDataRaw(self.heading_chan, numSamples=1,
				segmentIndex=segment)
			heading[i] = heading_tuple[0][0]
		print "transferred heading"
		i1, i2 = sp.where(sp.diff(heading) > threshold)[0][0:2]
		print "found heading zeros"
		for i, segment in enumerate(range(i1, i2, skip)):
			self.ps.getDataRaw(self.video_chan, segmentIndex=segment, 
				data=self.video_buffer[i, :])


	def capture_sweep(self, downsample_ratio=0, downsample_mode=0):
		'''
		Runs a sweep and then transfers the data to the RadarScope's memory
		buffers (i.e., on the computer).
		'''
		t1 = time.time()
		self.run_sweep()
		self.ps.waitReady()
		print "Time to capture data: ", str(time.time() - t1)
		self.transfer_data(downsample_ratio, downsample_mode)

	def zero_heading_indices(self, threshold=1000):
		'''
		Returns the indices of the data blocks where the heading signal
		indicates that the antenna was at the zero point.
		'''
		heading = self.heading_buffer[:, -1]
		i1, i2 = sp.where(sp.diff(heading) > threshold)[0][0:2]
		return i1, i2

	def trim_current_sweep(self, threshold=1000):
		i1, i2 = self.zero_heading_indices(threshold)
		self.trimmed_sweep = self.video_buffer[i1:i2, :]#((self.n_captures, -1))

	def capture_trimmed_sweep(self, downsample_ratio=0, downsample_mode=0,
		threshold=1000):
		self.capture_sweep(downsample_ratio, downsample_mode)
		self.trim_current_sweep()

	def metadata(self):
		fields = ["last_sweep_time", "max_range", "range_resolution", 
			"pulse_rate", "samples_per_segment", "rotation_period"]
		metadata_string = ""
		for f in fields:
			metadata_string = metadata_string + f + " : "
			metadata_string = metadata_string + str(self.__getattribute__(f)) + ";\n"
		metadata_string += " " * (METADATA_LENGTH - len(metadata_string))
		return metadata_string


	def to_file(self, dir=None, echo=False):
		t1 = time.time()
		if dir is None:
			dir = self.data_dir
		filename = "sweep_" + self.last_sweep_time + ".swp"
		filename = os.path.join(dir, filename)
		output_file = open(filename, "wb")
		output_file.write(self.metadata())
		output_file.write(self.trimmed_sweep)
		# output_file.write(self.heading_buffer)
		output_file.close()
		if echo:
			print filename
		print "Time to write data: ", str(time.time() - t1)

	def to_netcdf_file(self, dir=None, echo=False):
		t1 = time.time()
		if dir is None:
			dir = self.data_dir
		filename = "sweep_" + self.last_sweep_time + ".nc"
		filename = os.path.join(dir, filename)
		nc_file = netcdf.netcdf_file(filename, 'w')
		n_range = self.trimmed_sweep.shape[1]
		n_pulse = self.trimmed_sweep.shape[0]
		pulse_dim = nc_file.createDimension("pulse_number", n_pulse)
		pulse_var = nc_file.createVariable("pulse_number", int, ("pulse_number", ))
		pulse_var.units = "pulse_number"
		range_dim = nc_file.createDimension("range", n_range)
		range_var = nc_file.createVariable("range", float, ("range", ))
		range_var.units = "meters"
		amplitude = nc_file.createVariable("amplitude", self.trimmed_sweep.dtype,
			("pulse_number", "range"))
		range_var[:] = sp.arange(0, self.range_resolution * n_range, self.range_resolution)
		pulse_var[:] = sp.arange(n_pulse, dtype=int)
		amplitude[:] = self.trimmed_sweep
		amplitude.units = "ADC_counts"
		amplitude.max_counts = self.ps.getMaxValue()
		amplitude.min_counts = self.ps.getMinValue()
		nc_file.max_range = self.max_range
		nc_file.range_resolution = self.range_resolution
		nc_file.sweep_time = self.last_sweep_time
		nc_file.pulse_rate_nominal = self.pulse_rate
		nc_file.rotation_period_nominal = self.rotation_period
		nc_file.samples_per_segment = self.samples_per_segment
		nc_file.close()
		if echo:
			print filename
			print "Time to write data: ", str(time.time() - t1)


	def record(self, minimum_interval=5, netcdf=True):
		'''
		Record sweeps continuously, waiting no less than minimum_interval
		in between them.
		'''
		i = 0
		t1 = minimum_interval + 1
		while True:#
			try:
				while time.time() - t1 < minimum_interval:
					time.sleep(0)
				t1 = time.time()
				try:
					self.capture_trimmed_sweep()
				except:
					print "failed to capture " + self.last_sweep_time
				if netcdf:
					rec_thread = threading.Thread(target=self.to_netcdf_file, kwargs={"echo" : True})
				else:
					rec_thread = threading.Thread(target=self.to_file, kwargs={"echo" : True})
				rec_thread.setDaemon(True)
				rec_thread.start()
				print "\n"
			except KeyboardInterrupt:
				break

	def disconnect(self):
		'''
		Closes the PicoScope API, releasing the oscilloscope.
		'''
		self.ps.close()

class TestPs3000a(object):
	"""docstring for TestPs3000a"""
	def __init__(self, serial):
		super(TestPs3000a, self).__init__()
		self.serial = serial
		
class TestRadarScope(object):
	"""dummy class with same methods as RadarScope for testing"""
	def __init__(self, ps, rotation_period=2.4, pulse_rate=2100,
		range_resolution=10.0, max_range=1e3, video_chan="A", 
		video_voltage=[-0.1, 2], trigger_voltage=0.4,
		heading_chan="B", heading_voltage=[1, -10], heading_threshold=-1.5, data_dir="."):
		super(TestRadarScope, self).__init__()

	def run_sweep(self):
		pass

	def transfer_data(self):
		pass

	def capture_sweep(self):
		pass

	def zero_heading_indices(self):
		pass

	def capture_trimmed_sweep(self):
		data = np.random.randn(400, 400)
		data[:, 0] = 2
		time.sleep(3)
		self.trimmed_sweep = data

	def to_file(self):
		pass

	def record(self):
		pass

	def disconnect(self):
		pass
		


if __name__ == '__main__':
	
	import matplotlib.pyplot as plt
	import datetime as dt
	from string import zfill
	# picoscope = reload(picoscope)
	# from picoscope import ps3000a
	now = dt.datetime.now()
	data_dir = "C:\\" + str(now.year) + zfill(now.month, 2) + zfill(now.day, 2)
	if not os.path.exists(data_dir):
		os.mkdir(data_dir)

	ps3000a = reload(ps3000a)

	SERIAL_NUM = 'AR911/011\x00'
	ps = ps3000a.PS3000a(SERIAL_NUM)

	max_range = 5e3
	rscope = RadarScope(ps, max_range=max_range, range_resolution=6.0, pulse_rate=2100,
		trigger_voltage=1.5, data_dir=data_dir)

	# rscope.run_sweep()
	# rscope.ps.waitReady()
	# print "transferring"
	# rscope.transfer_data2()
	# print "done"

	# rscope.capture_sweep()
	# rscope.capture_trimmed_sweep()
	# rscope.to_netcdf_file(dir=".", echo=True)
	rscope.record()
	# rscope.wait_zero_heading()
	rscope.disconnect()

	# plt.imshow(rscope.video_buffer, aspect="auto")
	# plt.show()

	# data_to_plot = rscope.trimmed_sweep[::4, :]
	# fig = plt.figure()
	# ax = fig.add_subplot(111, polar=True)

	# theta = sp.linspace(2 * sp.pi, 0, data_to_plot.shape[0])
	# R = sp.linspace(0, max_range, data_to_plot.shape[1])
	# pcm = ax.pcolormesh(theta, R, data_to_plot.T)
	# plt.colorbar(pcm)
	# plt.show()