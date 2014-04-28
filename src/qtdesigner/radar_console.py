# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radar_console.ui'
#
# Created: Sun Apr 27 20:38:37 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(780, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 781, 551))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphicsView = QtGui.QGraphicsView(self.horizontalLayoutWidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.recordButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.recordButton.setObjectName(_fromUtf8("recordButton"))
        self.verticalLayout.addWidget(self.recordButton)
        self.snapshotButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.snapshotButton.setObjectName(_fromUtf8("snapshotButton"))
        self.verticalLayout.addWidget(self.snapshotButton)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scaleMaxSpinBoxLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.scaleMaxSpinBoxLabel.setObjectName(_fromUtf8("scaleMaxSpinBoxLabel"))
        self.gridLayout.addWidget(self.scaleMaxSpinBoxLabel, 2, 0, 1, 1)
        self.rangeSpinBox = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.rangeSpinBox.setMaximumSize(QtCore.QSize(188, 16777215))
        self.rangeSpinBox.setObjectName(_fromUtf8("rangeSpinBox"))
        self.gridLayout.addWidget(self.rangeSpinBox, 0, 1, 1, 1)
        self.rangeSpinBoxLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.rangeSpinBoxLabel.setObjectName(_fromUtf8("rangeSpinBoxLabel"))
        self.gridLayout.addWidget(self.rangeSpinBoxLabel, 0, 0, 1, 1)
        self.colorSchemeComboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.colorSchemeComboBox.setObjectName(_fromUtf8("colorSchemeComboBox"))
        self.colorSchemeComboBox.addItem(_fromUtf8(""))
        self.colorSchemeComboBox.addItem(_fromUtf8(""))
        self.colorSchemeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.colorSchemeComboBox, 6, 1, 1, 1)
        self.colorSchemeComboBoxLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.colorSchemeComboBoxLabel.setObjectName(_fromUtf8("colorSchemeComboBoxLabel"))
        self.gridLayout.addWidget(self.colorSchemeComboBoxLabel, 6, 0, 1, 1)
        self.scaleMinSpinBoxLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        self.scaleMinSpinBoxLabel.setObjectName(_fromUtf8("scaleMinSpinBoxLabel"))
        self.gridLayout.addWidget(self.scaleMinSpinBoxLabel, 2, 1, 1, 1)
        self.verticalSlider_2 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName(_fromUtf8("verticalSlider_2"))
        self.gridLayout.addWidget(self.verticalSlider_2, 4, 1, 1, 1)
        self.verticalSlider = QtGui.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.gridLayout.addWidget(self.verticalSlider, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionConfigure_radar = QtGui.QAction(MainWindow)
        self.actionConfigure_radar.setObjectName(_fromUtf8("actionConfigure_radar"))
        self.actionConfigure_scope = QtGui.QAction(MainWindow)
        self.actionConfigure_scope.setObjectName(_fromUtf8("actionConfigure_scope"))
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionChoose_storage_location = QtGui.QAction(MainWindow)
        self.actionChoose_storage_location.setObjectName(_fromUtf8("actionChoose_storage_location"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionChoose_storage_location)
        self.menuFile.addAction(self.actionQuit)
        self.menuSettings.addAction(self.actionConfigure_radar)
        self.menuSettings.addAction(self.actionConfigure_scope)
        self.menuSettings.addAction(self.actionConnect)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.recordButton.setText(_translate("MainWindow", "Record", None))
        self.snapshotButton.setText(_translate("MainWindow", "Snapshot", None))
        self.scaleMaxSpinBoxLabel.setText(_translate("MainWindow", "Scale max", None))
        self.rangeSpinBoxLabel.setText(_translate("MainWindow", "Range (km)", None))
        self.colorSchemeComboBox.setItemText(0, _translate("MainWindow", "Jet", None))
        self.colorSchemeComboBox.setItemText(1, _translate("MainWindow", "Copper", None))
        self.colorSchemeComboBox.setItemText(2, _translate("MainWindow", "Spectral", None))
        self.colorSchemeComboBoxLabel.setText(_translate("MainWindow", "Color scheme", None))
        self.scaleMinSpinBoxLabel.setText(_translate("MainWindow", "Scale min", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.actionConfigure_radar.setText(_translate("MainWindow", "Configure radar...", None))
        self.actionConfigure_scope.setText(_translate("MainWindow", "Configure scope...", None))
        self.actionConnect.setText(_translate("MainWindow", "Connect", None))
        self.actionChoose_storage_location.setText(_translate("MainWindow", "Choose storage", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

