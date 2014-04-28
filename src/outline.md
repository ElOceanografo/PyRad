

- class RadarConsole (QtGui application)
	- Attributes:
		- A RadarScope object, connected to the PS3405
		- a path to save files in
		- display settings: range, thresholds, colormaps, etc.
	- Methods:
		- 

- class RadarPropertiesDialog

There is a file-selector dialog built into QtGui:

def selectFile():
    lineEdit.setText(QFileDialog.getOpenFileName())

pushButton.clicked.connect(selectFile)

- class RadarScope
	- getSweep()

