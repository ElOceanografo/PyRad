from threading import Thread
from Queue import Queue
import time
import picopy
import numpy as np

C = 2.99e8
PRI = 1/2100.0 #pulse repetition interval
PULSE_LENGTH = 0.08e-6
MAX_VOLTAGE = 4.0 # or whatever
PULSE_CHANNEL = "A"
TRIGGER_CHANNEL = "B"
BEARING_CHANNEL = "C"
ROTATION_RATE = 2 * pi / 1.4 # or whatever...radians/sec
D_THETA = PRI * ROTATION_RATE
SAMPLING_INTERVAL = 0.1 # not the real number
MAX_SAMPLE_RANGE = 10E3 # kilometers
MAX_SAMPLING_TIME = 2 * MAX_SAMPLE_RANGE / C # timebase
N_PULSE_SAMPLES = 1024 # figure out how many this actually is
D_RANGE = C * PULSE_LENGTH / 2 # range distance between samples
SAMPLE_RANGE_ARRAY = np.arange(0, MAX_SAMPLE_RANGE, by=D_RANGE)



# setup pulse buffer array
output_file = open(filename, "wb")

picoscope = picopy.ps3000a()
# set channels, triggers

gui = somethingorother()


def collect_data(scope, queue):
	scope.runBlock()
	while not scope.isReady():
		pass
	pulse_data = scope.getDataRaw(PULSE_CHANNEL)
	bearing_at_zero = scope.getDataRaw(BEARING_CHANNEL)
	bearing += D_THETA
	pulse_index += 1
	q.put((pulse_index, bearing, bearing_at_zero, pulse_data))


def write_pulse(output_file, bearing, pulse_index, pulse_data, proc_funcs=None):
	'''
	takes the state variables, pulse data, and possibly some processing functions
	that operate on the pulse before saving the pulse data
	'''
	output_file.write("whatever\n")

def update_plot(bearing, pulse_index, pulse_data):
	# update the plot
	for i in 1:len(pulse_data):
		color = map_to_color(pulse_data[i])
		i, j = get_pixel_coordinates(bearing, SAMPLE_RANGE_ARRAY[i])
		image_array[i, j] = color
	plot_object.update()


bearing = 0.0
pulse_index = 0
q = Queue()

while gui.running():


	Thread(target=collect_data).start()
	Thread(target=process_data).start()
	# stackoverflow threading in python


#############################
# test some read/write speeds

FILENAME = "test.dat"
DURATION = 5.0

def do_test(duration):
	f = open(FILENAME, "wb")
	start = time.time()
	while True:
		t = time.time()
		if t - start > duration:
			break
		f.write(randn(1024))
		f.write('\n')
	f.close()

def count_lines(filename):
	f = open(filename, 'rb')
	n = len(f.readlines())
	f.close()
	return(n)

do_test(DURATION)
count_lines(FILENAME) / DURATION
