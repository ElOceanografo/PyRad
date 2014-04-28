import sys
from PyQt4.QtGui import QApplication, QMainWindow
from radar_console import Ui_MainWindow

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(window)
	window.show()
	sys.exit(app.exec_())