import scipy as sp
GGI_LAT = 41 + 12./60 + 6./3600
GGI_LON = 72 + 7./60 + 9./3600
KM_TO_DEGREES = 111.12


def latlon(distance, bearing, printout="DDM"):
	x = distance * sp.cos(sp.radians(bearing))
	y = distance * sp.sin(sp.radians(bearing))
	xdeg = x / KM_TO_DEGREES * sp.cos(sp.radians(GGI_LAT)) + GGI_LON
	ydeg = x / KM_TO_DEGREES + GGI_LAT
	x_decimal_min = (xdeg % 1) * 60
	y_decimal_min = (xdeg % 1) * 60
	x_sec = (x_decimal_min % 1) * 60
	y_sec = (y_decimal_min % 1) * 60
	if printout == "DDM":
		print "%i %f', %i %f'" % (int(ydeg), y_decimal_min, int(xdeg), x_decimal_min)
	elif printout == "DMS":
		print "%i %i' %i\", %i %i' %i\"" % (int(ydeg), int(y_decimal_min), round(y_sec),
			int(ydeg), int(y_decimal_min), round(y_sec))
	else:
		print ydeg, xdeg

