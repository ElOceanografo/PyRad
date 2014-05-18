import sys, os, random, time
import scipy as sp
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PyQt4'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm

from radar_scope import TestRadarScope, TestPs3000a
from radar_scope_threads import DataAcquisitionThread, DataProcessingThread

# Constants
CLOCK_FMT = "%Y%m%d-%H:%M:%S"
TIMESTAMP_FMT = "%Y%m%d_%H%M%S"

class RadarConsole(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("Radar Console")
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        # self.connect_scope()
        # self.update_ppi()
        self.radar_scope = None
        self.data = None
        self.timestamp = None
        self.cmap = cm.jet
        self.output_dir = os.getcwd()
        self.file_text.setText(self.output_dir)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.recording = False

    def on_about(self):
        msg = """
        WE'VE GOT A THING THAT'S CALLED RADAR LOVE\nWE'VE GOT A LINE IN THE SKY\nRADAR LOVE
        """
        QMessageBox.about(self, "ABOUT", msg.strip())

    def update_clock(self):
        self.time_text.setText(time.strftime(CLOCK_FMT))

    def update_ppi(self):
        """
        Redraws the figure
        """
        # if self.data is None:
        #     self.data = self.radar_scope.get_trimmed_sweep()
        theta = sp.linspace(0, 2 * sp.pi, self.data.shape[0])
        # theta = sp.hstack((theta[100:400], theta[0:100]))
        R = sp.arange(self.data.shape[1])
        sub_R = 1
        sub_theta = 5
        # clear the axes and redraw the plot
        self.axes.clear()        
        self.axes.pcolormesh(theta[::sub_theta], R[::sub_R], 
            self.data[::sub_theta, ::sub_R], vmin=self.vmin_spin_box.value(),
            vmax=self.vmax_spin_box.value(), cmap=self.cmap)
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
        self.recordBtn = QPushButton("&Record", self)
        self.recordBtn.setCheckable(True)
        self.recordBtn.clicked[bool].connect(self.setRecording)

        self.capture_button = QPushButton("&Capture")
        self.capture_button.setCheckable(True)
        self.capture_button.clicked[bool].connect(self.capture_sweep) 

        self.colormap_combo_box = QComboBox()
        for cmap in ["jet", "spectral", "copper"]:
            self.colormap_combo_box.addItem(cmap)
        self.connect(self.colormap_combo_box, SIGNAL("activated(QString)"), 
            self.set_cmap)

        self.vmin_spin_box = QDoubleSpinBox()
        self.vmax_spin_box = QDoubleSpinBox()
        for w in [self.vmin_spin_box, self.vmax_spin_box]:
            w.setMinimum(-10.0)
            w.setMaximum(10.0)
            self.connect(w, SIGNAL("valueChanged(double)"), self.set_cmap_range)
        self.vmin_spin_box.setValue(-2.0)
        self.vmax_spin_box.setValue(2.0)
        vmin_label = QLabel("Scale min")
        vmax_label = QLabel("Scale max")
        colormap_layout = QGridLayout()
        colormap_layout.addWidget(vmin_label, 0, 0)
        colormap_layout.addWidget(vmax_label, 0, 1)
        colormap_layout.addWidget(self.vmin_spin_box, 1, 0)
        colormap_layout.addWidget(self.vmax_spin_box, 1, 1)


        # Layout with box sizers
        controlbox = QVBoxLayout()
        for w in [self.recordBtn, self.capture_button, self.colormap_combo_box]:
            w.setFixedWidth(200)
            controlbox.addWidget(w)
        controlbox.addLayout(colormap_layout)
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
        self.status_text = QLabel("Not connected")
        self.file_text = QLabel("some file")
        self.time_text = QLabel(time.strftime(CLOCK_FMT))
        self.statusBar().addWidget(self.status_text, 0.5)
        self.statusBar().addWidget(self.file_text, 1)
        self.statusBar().addWidget(self.time_text)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        set_output_dir_action = self.create_action("&Set output directory",
            shortcut="Ctrl+S", slot=self.set_output_dir, 
            tip="Save the plot")
        connect_scope_action = self.create_action("&Connect scope",
            shortcut="Ctrl+c", slot=self.connect_scope, 
            tip="Connect to digitizing oscilloscope")
        disconnect_scope_action = self.create_action("&Disconnect scope",
            shortcut="Ctrl+d", slot=self.disconnect_scope, 
            tip="Connect to digitizing oscilloscope")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (set_output_dir_action, connect_scope_action, disconnect_scope_action,
             None, quit_action))
        
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

    def create_action(self, text, slot=None, shortcut=None, 
        icon=None, tip=None, checkable=False, signal="triggered()"):
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
        # choose configuration file
        try:
            self.config_file = QFileDialog.getOpenFileName(self, 
                "Choose config file")
            pico_serial_num, params_dict = read_config(self.config_file)
            file_found = True
        except:
            QMessageBox.about(self, "File error", "File not in expected format")
            return 0
        # Open picoscope
        try:
            picoscope = TestPs3000a(pico_serial_num) #ps3000a.PS3000a(pico_serial_num)
        except:
            msg = "Could not connect to PicoScope " + pico_serial_num
            QMessageBox.about(self, "Connection error", msg)
            return 0
        self.radar_scope = TestRadarScope(picoscope, **params_dict)
        self.data_q = Queue.Queue()
        self.acq_thread = DataAcquisitionThread(self.data_q, self.radar_scope)
        self.proc_thread = DataProcessingThread(self.data_q, self.radar_scope, self)
        self.acq_thread.setDaemon(True)
        self.proc_thread.setDaemon(True)
        self.acq_thread.start()
        self.proc_thread.start()
        self.status_text.setText("Connected")
        return 1

    def disconnect_scope(self):
        if self.acq_thread is not None:
            self.acq_thread.join(0.01)
            self.proc_thread.join(0.01)       
            self.acq_thread = None
            self.proc_thread = None
            self.stopRecording()
            self.status_text.setText("Not connected")
        self.radar_scope.disconnect()
        self.radar_scope = None

    def set_output_dir(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, 
            "Set output directory")
        self.file_text.setText(self.output_dir)

    def set_cmap(self):
        self.cmap = cm.get_cmap(str(self.colormap_combo_box.currentText()))

    def set_cmap_range(self):
        self.vmin_spin_box.setMaximum(self.vmax_spin_box.value())
        self.vmax_spin_box.setMinimum(self.vmin_spin_box.value())
        self.vmin = self.vmin_spin_box.value()
        self.vmax = self.vmax_spin_box.value()

    def save_file(self):
        filename = "sweep_" + self.timestamp + ".swp"
        filename = os.path.join(self.output_dir, filename)
        self.file_text.setText(filename)
        # output_file = open(filename, "wb")
        # # Should have more metadata in here
        # output_file.write(self.data)
        # output_file.close()

    def capture_sweep(self, on):
        if on:
            if self.radar_scope is None:
                connection_success = self.connect_scope()
                if not connection_success:
                    self.capture_button.setChecked(False)
                    return
            self.save_file()
            self.capture_button.setChecked(False)
        else:
            if self.recording:
                self.capture_button.setChecked(True)

    def setRecording(self, on):
        if on:
            self.startRecording()
        else:
            self.stopRecording()

    def startRecording(self):
        if self.radar_scope is None:
            connection_success = self.connect_scope()
            if not connection_success:
                self.recordBtn.setChecked(False)
                return
        self.recording = True
        self.capture_button.setChecked(True)
        self.status_text.setText("Recording")
        self.status_text.setStyleSheet('color: red')
        
    def stopRecording(self):
        self.status_text.setText("Ready")
        self.status_text.setStyleSheet('color: black')
        self.recording = False
        self.recordBtn.setChecked(False)
        self.capture_button.setChecked(False)

def read_config(filename):
    dict = eval(open(filename).read().replace('\n', ''))
    pico_serial = dict.pop("pico_serial")
    return pico_serial, dict

# class RadarScopeConfigDialog(QDialog):
#     """docstring for RadarScopeConfigDialog"""
#     def __init__(self, parent=None):
#         super(RadarScopeConfigDialog, self).__init__(parent)
#         layout = QVBoxLayout()

#         # set up form to configure picoscope
#         pico_form = QFormLayout()
#         serial_line_edit = QLineEdit()
#         video_chan_combo_box = QComboBox()
#         heading_chan_combo_box = QComboBox()
#         pico_form.addRow("Serial #", serial_line_edit)
#         pico_form.addRow("Video channel", video_chan_combo_box)
#         pico_form.addRow("Heading channel", heading_chan_combo_box)

#         #set up form to configure radar
#         radar_form = QFormLayout()
#         rotation_period_spin_box = QDoubleSpinBox()
#         max_range_spin_box = QSpinBox()
#         radar_form.addRow("Rotation period (s)", rotation_period_spin_box)
#         radar_form.addRow("Max range (m)", max_range_spin_box)

#         pico_box = QGroupBox("PicoScope")
#         radar_box = QGroupBox("Radar")
#         pico_box.setLayout(pico_form)
#         radar_box.setLayout(radar_form)

#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self)

#         layout.addWidget(pico_box)
#         layout.addWidget(radar_box)
#         layout.addWidget(self.buttons)

