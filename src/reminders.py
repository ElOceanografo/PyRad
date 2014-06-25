import winsound
import time
import datetime as dt

TRANSECT_MINUTES = [0]
SCAN_MINUTES = [0, 30]


def beep():
	winsound.Beep(1000, 100)

while True:
	time.sleep(60)
	minute = dt.datetime.now().minute
	if minute in TRANSECT_MINUTES:
		beep()
		print "Time for transects"
	if minute in SCAN_MINUTES:
		beep()
		print "Time for scan"