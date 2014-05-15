import sys, os, random, time
import scipy as sp
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PyQt4'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from radar_scope import TestRadarScope


class RadarConsole(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Radar Console")
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.connect_scope()
        # self.on_draw()

    def save_plot(self):
        pass

    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:
        
         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        QMessageBox.about(self, "About the demo", msg.strip())
    
    
    def on_draw(self):
        """
        Redraws the figure
        """
        self.data = self.radar_scope.get_trimmed_sweep()
        theta = sp.linspace(0, 2 * sp.pi, self.data.shape[0])
        theta = sp.hstack((theta[100:400], theta[0:100]))
        R = sp.arange(self.data.shape[1])

        # clear the axes and redraw the plot anew
        self.axes.clear()        
        self.axes.pcolormesh(theta, R, self.data)
        self.canvas.draw()
    
    def create_main_frame(self):
        self.main_frame = QWidget()
        # Create the mpl Figure and FigCanvas objects. 
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111, polar=True)   
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        

        # control panel
        self.recordBtn = QPushButton("Record", self)
        self.recordBtn.setCheckable(True)
        self.recordBtn.clicked[bool].connect(self.setRecording)

        self.draw_button = QPushButton("&Draw")
        self.connect(self.draw_button, SIGNAL('clicked()'), self.on_draw)    

        # Layout with box sizers
        controlbox = QVBoxLayout()
        for w in [self.recordBtn, self.draw_button]:
            w.setFixedWidth(200)
            controlbox.addWidget(w)
        controlbox.addStretch(1)

        plotbox = QVBoxLayout()
        plotbox.addWidget(self.canvas)
        plotbox.addWidget(self.mpl_toolbar)

        hbox = QHBoxLayout()
        hbox.addLayout(plotbox)
        hbox.addLayout(controlbox)

        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)
    
    def create_status_bar(self):
        self.status_text = QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def connect_scope(self):
        msg = """
        Placeholder for the dialog box that will setup the scope
        """
        QMessageBox.about(self, "About the demo", msg.strip())
        self.status_text.setText("(Connecting to scope)")
        self.radar_scope = TestRadarScope()
        self.status_text.setText("Ready")


    def set_output_file(self):
        self.status_text.setText("(Choosing output file)")
        time.sleep(2)

    def setRecording(self, on):
        if on:
            self.startRecording()
        else:
            self.stopRecording()

    def startRecording(self):
        # if self.scope_monitor is not None: # i.e., if we're already recording
        #     return
        # self.recordBtn.setStyleSheet("color : black; background-color: red")
        # self.recording = True
        # self.radar_data_q = Queue.Queue()
        # self.scope_monitor = ScopeMonitorThread(self.radar_data_q)
        # self.status_text.setText("Starting data acquisition...")
        # self.scope_monitor.start()
        self.status_text.setText("Recording")
        self.status_text.setStyleSheet('color: red')
        
    def stopRecording(self):
        # if self is not None:
        #     self.scope_monitor.join()
        #     self.status_text.setText("Stopping data acquisition...")
        #     self.scope_monitor = None
        self.status_text.setText("Ready")
        self.status_text.setStyleSheet('color: black')
        # self.recordBtn.setStyleSheet("color : black; background-color: green")
        # self.recording = False
