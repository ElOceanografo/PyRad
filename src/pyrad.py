#!/usr/bin/python

import sys
from PyQt4.QtGui import QApplication, QMainWindow
from radar_console import RadarConsole


def main():
    app = QApplication(sys.argv)
    form = RadarConsole()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
