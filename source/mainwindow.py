# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 700)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS UI Gothic"))
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.manplans = QtGui.QTableWidget(self.centralwidget)
        self.manplans.setEnabled(False)
        self.manplans.setGeometry(QtCore.QRect(10, 70, 521, 251))
        self.manplans.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.manplans.setTabKeyNavigation(False)
        self.manplans.setProperty("showDropIndicator", False)
        self.manplans.setDragDropOverwriteMode(False)
        self.manplans.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.manplans.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.manplans.setCornerButtonEnabled(False)
        self.manplans.setRowCount(10)
        self.manplans.setColumnCount(3)
        self.manplans.setObjectName(_fromUtf8("manplans"))
        item = QtGui.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.manplans.setItem(0, 0, item)
        self.manplans.horizontalHeader().setVisible(True)
        self.manplans.horizontalHeader().setCascadingSectionResizes(True)
        self.manplans.horizontalHeader().setDefaultSectionSize(100)
        self.manplans.horizontalHeader().setHighlightSections(False)
        self.manplans.verticalHeader().setVisible(True)
        self.manplans.verticalHeader().setDefaultSectionSize(20)
        self.manplans.verticalHeader().setHighlightSections(False)
        self.manplans.verticalHeader().setMinimumSectionSize(20)
        self.execNext = QtGui.QPushButton(self.centralwidget)
        self.execNext.setEnabled(False)
        self.execNext.setGeometry(QtCore.QRect(550, 70, 75, 23))
        self.execNext.setObjectName(_fromUtf8("execNext"))
        self.insertMan = QtGui.QPushButton(self.centralwidget)
        self.insertMan.setEnabled(False)
        self.insertMan.setGeometry(QtCore.QRect(550, 270, 75, 23))
        self.insertMan.setStatusTip(_fromUtf8(""))
        self.insertMan.setWhatsThis(_fromUtf8(""))
        self.insertMan.setObjectName(_fromUtf8("insertMan"))
        self.showOrbit = QtGui.QPushButton(self.centralwidget)
        self.showOrbit.setEnabled(False)
        self.showOrbit.setGeometry(QtCore.QRect(550, 10, 75, 23))
        self.showOrbit.setObjectName(_fromUtf8("showOrbit"))
        self.editMan = QtGui.QPushButton(self.centralwidget)
        self.editMan.setEnabled(False)
        self.editMan.setGeometry(QtCore.QRect(550, 240, 75, 23))
        self.editMan.setObjectName(_fromUtf8("editMan"))
        self.execto = QtGui.QPushButton(self.centralwidget)
        self.execto.setEnabled(False)
        self.execto.setGeometry(QtCore.QRect(550, 100, 75, 23))
        self.execto.setObjectName(_fromUtf8("execto"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.probename = QtGui.QLabel(self.centralwidget)
        self.probename.setGeometry(QtCore.QRect(90, 10, 131, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        font.setPointSize(9)
        self.probename.setFont(font)
        self.probename.setText(_fromUtf8(""))
        self.probename.setObjectName(_fromUtf8("probename"))
        self.targetname = QtGui.QLabel(self.centralwidget)
        self.targetname.setGeometry(QtCore.QRect(90, 30, 231, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        font.setPointSize(9)
        self.targetname.setFont(font)
        self.targetname.setText(_fromUtf8(""))
        self.targetname.setObjectName(_fromUtf8("targetname"))
        self.deleteMan = QtGui.QPushButton(self.centralwidget)
        self.deleteMan.setEnabled(False)
        self.deleteMan.setGeometry(QtCore.QRect(550, 300, 75, 23))
        self.deleteMan.setStatusTip(_fromUtf8(""))
        self.deleteMan.setObjectName(_fromUtf8("deleteMan"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.manfilename = QtGui.QLabel(self.centralwidget)
        self.manfilename.setGeometry(QtCore.QRect(90, 50, 231, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        font.setPointSize(9)
        self.manfilename.setFont(font)
        self.manfilename.setText(_fromUtf8(""))
        self.manfilename.setObjectName(_fromUtf8("manfilename"))
        self.editnext = QtGui.QPushButton(self.centralwidget)
        self.editnext.setEnabled(False)
        self.editnext.setGeometry(QtCore.QRect(550, 210, 75, 23))
        self.editnext.setObjectName(_fromUtf8("editnext"))
        self.initexec = QtGui.QPushButton(self.centralwidget)
        self.initexec.setEnabled(False)
        self.initexec.setGeometry(QtCore.QRect(550, 150, 75, 23))
        self.initexec.setObjectName(_fromUtf8("initexec"))
        self.reviewthroughout = QtGui.QPushButton(self.centralwidget)
        self.reviewthroughout.setEnabled(False)
        self.reviewthroughout.setGeometry(QtCore.QRect(230, 10, 141, 23))
        self.reviewthroughout.setObjectName(_fromUtf8("reviewthroughout"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 370, 131, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS UI Gothic"))
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 390, 131, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 350, 141, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS UI Gothic"))
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 450, 131, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 490, 131, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 510, 131, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(20, 530, 131, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(20, 550, 131, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(20, 610, 131, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(20, 630, 131, 16))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(20, 570, 131, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(20, 590, 131, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(20, 470, 131, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(20, 410, 141, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(20, 430, 151, 16))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.flightreview = QtGui.QPushButton(self.centralwidget)
        self.flightreview.setEnabled(False)
        self.flightreview.setGeometry(QtCore.QRect(390, 10, 141, 23))
        self.flightreview.setObjectName(_fromUtf8("flightreview"))
        self.label_19 = QtGui.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(20, 329, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtGui.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(380, 340, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_mantime_h = QtGui.QLabel(self.centralwidget)
        self.label_mantime_h.setEnabled(False)
        self.label_mantime_h.setGeometry(QtCore.QRect(380, 360, 61, 16))
        self.label_mantime_h.setObjectName(_fromUtf8("label_mantime_h"))
        self.label_22 = QtGui.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(380, 380, 61, 16))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.selectedman = QtGui.QTableWidget(self.centralwidget)
        self.selectedman.setEnabled(True)
        self.selectedman.setGeometry(QtCore.QRect(380, 400, 241, 164))
        self.selectedman.setRowCount(8)
        self.selectedman.setColumnCount(2)
        self.selectedman.setObjectName(_fromUtf8("selectedman"))
        self.selectedman.horizontalHeader().setVisible(False)
        self.selectedman.verticalHeader().setVisible(False)
        self.selectedman.verticalHeader().setDefaultSectionSize(20)
        self.selectedman.verticalHeader().setMinimumSectionSize(20)
        self.label_progress = QtGui.QLabel(self.centralwidget)
        self.label_progress.setGeometry(QtCore.QRect(380, 612, 241, 16))
        self.label_progress.setText(_fromUtf8(""))
        self.label_progress.setObjectName(_fromUtf8("label_progress"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(380, 630, 241, 15))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_cman = QtGui.QLabel(self.centralwidget)
        self.label_cman.setGeometry(QtCore.QRect(540, 342, 91, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_cman.setFont(font)
        self.label_cman.setObjectName(_fromUtf8("label_cman"))
        self.label_ISOT = QtGui.QLineEdit(self.centralwidget)
        self.label_ISOT.setGeometry(QtCore.QRect(180, 370, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_ISOT.setFont(font)
        self.label_ISOT.setToolTip(_fromUtf8(""))
        self.label_ISOT.setFrame(False)
        self.label_ISOT.setReadOnly(True)
        self.label_ISOT.setObjectName(_fromUtf8("label_ISOT"))
        self.label_JD = QtGui.QLineEdit(self.centralwidget)
        self.label_JD.setGeometry(QtCore.QRect(180, 390, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_JD.setFont(font)
        self.label_JD.setToolTip(_fromUtf8(""))
        self.label_JD.setFrame(False)
        self.label_JD.setReadOnly(True)
        self.label_JD.setObjectName(_fromUtf8("label_JD"))
        self.label_range = QtGui.QLineEdit(self.centralwidget)
        self.label_range.setGeometry(QtCore.QRect(180, 410, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_range.setFont(font)
        self.label_range.setToolTip(_fromUtf8(""))
        self.label_range.setFrame(False)
        self.label_range.setReadOnly(True)
        self.label_range.setObjectName(_fromUtf8("label_range"))
        self.label_velocity = QtGui.QLineEdit(self.centralwidget)
        self.label_velocity.setGeometry(QtCore.QRect(180, 430, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_velocity.setFont(font)
        self.label_velocity.setToolTip(_fromUtf8(""))
        self.label_velocity.setFrame(False)
        self.label_velocity.setReadOnly(True)
        self.label_velocity.setObjectName(_fromUtf8("label_velocity"))
        self.label_SMA = QtGui.QLineEdit(self.centralwidget)
        self.label_SMA.setGeometry(QtCore.QRect(180, 450, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_SMA.setFont(font)
        self.label_SMA.setToolTip(_fromUtf8(""))
        self.label_SMA.setFrame(False)
        self.label_SMA.setReadOnly(True)
        self.label_SMA.setObjectName(_fromUtf8("label_SMA"))
        self.label_SMAAU = QtGui.QLineEdit(self.centralwidget)
        self.label_SMAAU.setGeometry(QtCore.QRect(180, 470, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_SMAAU.setFont(font)
        self.label_SMAAU.setToolTip(_fromUtf8(""))
        self.label_SMAAU.setFrame(False)
        self.label_SMAAU.setReadOnly(True)
        self.label_SMAAU.setObjectName(_fromUtf8("label_SMAAU"))
        self.label_Ecc = QtGui.QLineEdit(self.centralwidget)
        self.label_Ecc.setGeometry(QtCore.QRect(180, 490, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_Ecc.setFont(font)
        self.label_Ecc.setToolTip(_fromUtf8(""))
        self.label_Ecc.setFrame(False)
        self.label_Ecc.setReadOnly(True)
        self.label_Ecc.setObjectName(_fromUtf8("label_Ecc"))
        self.label_Inc = QtGui.QLineEdit(self.centralwidget)
        self.label_Inc.setGeometry(QtCore.QRect(180, 510, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_Inc.setFont(font)
        self.label_Inc.setToolTip(_fromUtf8(""))
        self.label_Inc.setFrame(False)
        self.label_Inc.setReadOnly(True)
        self.label_Inc.setObjectName(_fromUtf8("label_Inc"))
        self.label_LAN = QtGui.QLineEdit(self.centralwidget)
        self.label_LAN.setGeometry(QtCore.QRect(180, 530, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_LAN.setFont(font)
        self.label_LAN.setToolTip(_fromUtf8(""))
        self.label_LAN.setFrame(False)
        self.label_LAN.setReadOnly(True)
        self.label_LAN.setObjectName(_fromUtf8("label_LAN"))
        self.label_APH = QtGui.QLineEdit(self.centralwidget)
        self.label_APH.setGeometry(QtCore.QRect(180, 550, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_APH.setFont(font)
        self.label_APH.setToolTip(_fromUtf8(""))
        self.label_APH.setFrame(False)
        self.label_APH.setReadOnly(True)
        self.label_APH.setObjectName(_fromUtf8("label_APH"))
        self.label_PPT = QtGui.QLineEdit(self.centralwidget)
        self.label_PPT.setGeometry(QtCore.QRect(180, 570, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_PPT.setFont(font)
        self.label_PPT.setToolTip(_fromUtf8(""))
        self.label_PPT.setFrame(False)
        self.label_PPT.setReadOnly(True)
        self.label_PPT.setObjectName(_fromUtf8("label_PPT"))
        self.label_PPTJD = QtGui.QLineEdit(self.centralwidget)
        self.label_PPTJD.setGeometry(QtCore.QRect(180, 590, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_PPTJD.setFont(font)
        self.label_PPTJD.setToolTip(_fromUtf8(""))
        self.label_PPTJD.setFrame(False)
        self.label_PPTJD.setReadOnly(True)
        self.label_PPTJD.setObjectName(_fromUtf8("label_PPTJD"))
        self.label_MA = QtGui.QLineEdit(self.centralwidget)
        self.label_MA.setGeometry(QtCore.QRect(180, 610, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_MA.setFont(font)
        self.label_MA.setToolTip(_fromUtf8(""))
        self.label_MA.setFrame(False)
        self.label_MA.setReadOnly(True)
        self.label_MA.setObjectName(_fromUtf8("label_MA"))
        self.label_OP = QtGui.QLineEdit(self.centralwidget)
        self.label_OP.setGeometry(QtCore.QRect(180, 630, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_OP.setFont(font)
        self.label_OP.setToolTip(_fromUtf8(""))
        self.label_OP.setFrame(False)
        self.label_OP.setReadOnly(True)
        self.label_OP.setObjectName(_fromUtf8("label_OP"))
        self.label_mantime = QtGui.QLineEdit(self.centralwidget)
        self.label_mantime.setGeometry(QtCore.QRect(445, 360, 185, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.label_mantime.setFont(font)
        self.label_mantime.setToolTip(_fromUtf8(""))
        self.label_mantime.setFrame(False)
        self.label_mantime.setReadOnly(True)
        self.label_mantime.setObjectName(_fromUtf8("label_mantime"))
        self.label_ELM = QtGui.QLabel(self.centralwidget)
        self.label_ELM.setGeometry(QtCore.QRect(180, 350, 181, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_ELM.setFont(font)
        self.label_ELM.setText(_fromUtf8(""))
        self.label_ELM.setObjectName(_fromUtf8("label_ELM"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuCheckpoint = QtGui.QMenu(self.menubar)
        self.menuCheckpoint.setEnabled(False)
        self.menuCheckpoint.setObjectName(_fromUtf8("menuCheckpoint"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setEnabled(False)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(MainWindow)
        self.actionSave_as.setEnabled(False)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew_from_current_status = QtGui.QAction(MainWindow)
        self.actionNew_from_current_status.setEnabled(False)
        self.actionNew_from_current_status.setObjectName(_fromUtf8("actionNew_from_current_status"))
        self.actionAbout_SSVG = QtGui.QAction(MainWindow)
        self.actionAbout_SSVG.setObjectName(_fromUtf8("actionAbout_SSVG"))
        self.actionCreate = QtGui.QAction(MainWindow)
        self.actionCreate.setObjectName(_fromUtf8("actionCreate"))
        self.actionResume = QtGui.QAction(MainWindow)
        self.actionResume.setEnabled(False)
        self.actionResume.setObjectName(_fromUtf8("actionResume"))
        self.actionProbe = QtGui.QAction(MainWindow)
        self.actionProbe.setObjectName(_fromUtf8("actionProbe"))
        self.actionTarget = QtGui.QAction(MainWindow)
        self.actionTarget.setObjectName(_fromUtf8("actionTarget"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout_SSVG)
        self.menuCheckpoint.addAction(self.actionCreate)
        self.menuCheckpoint.addAction(self.actionResume)
        self.menuEdit.addAction(self.actionProbe)
        self.menuEdit.addAction(self.actionTarget)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuCheckpoint.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.manplans, self.showOrbit)
        MainWindow.setTabOrder(self.showOrbit, self.execNext)
        MainWindow.setTabOrder(self.execNext, self.execto)
        MainWindow.setTabOrder(self.execto, self.editMan)
        MainWindow.setTabOrder(self.editMan, self.insertMan)
        MainWindow.setTabOrder(self.insertMan, self.deleteMan)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SSVG", None))
        item = self.manplans.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type", None))
        item = self.manplans.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Parameters", None))
        item = self.manplans.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Exec", None))
        __sortingEnabled = self.manplans.isSortingEnabled()
        self.manplans.setSortingEnabled(False)
        self.manplans.setSortingEnabled(__sortingEnabled)
        self.execNext.setToolTip(_translate("MainWindow", "Execute \'Next\' maneuver", None))
        self.execNext.setText(_translate("MainWindow", "Exec Next", None))
        self.insertMan.setToolTip(_translate("MainWindow", "Insert a blank maneuver", None))
        self.insertMan.setText(_translate("MainWindow", "Insert *", None))
        self.showOrbit.setToolTip(_translate("MainWindow", "Show Orbit", None))
        self.showOrbit.setText(_translate("MainWindow", "Show Orbit", None))
        self.editMan.setToolTip(_translate("MainWindow", "Edit selected maneuver", None))
        self.editMan.setText(_translate("MainWindow", "Edit *", None))
        self.execto.setToolTip(_translate("MainWindow", "Execute maneuvers to the selected line ", None))
        self.execto.setText(_translate("MainWindow", "Exec to *", None))
        self.label.setText(_translate("MainWindow", "Probe Name : ", None))
        self.label_2.setText(_translate("MainWindow", "Target        :", None))
        self.deleteMan.setToolTip(_translate("MainWindow", "Delete selected maneuver", None))
        self.deleteMan.setText(_translate("MainWindow", "Delete *", None))
        self.label_3.setText(_translate("MainWindow", "Plan File     :", None))
        self.editnext.setToolTip(_translate("MainWindow", "Edit \'Next\' maneuver", None))
        self.editnext.setText(_translate("MainWindow", "Edit Next", None))
        self.initexec.setToolTip(_translate("MainWindow", "Initialize execution of the flight plan", None))
        self.initexec.setText(_translate("MainWindow", "Ex Initialize", None))
        self.reviewthroughout.setToolTip(_translate("MainWindow", "Review throughout the flight", None))
        self.reviewthroughout.setText(_translate("MainWindow", "Review Throughout", None))
        self.label_4.setText(_translate("MainWindow", "Current Time", None))
        self.label_5.setText(_translate("MainWindow", "Current Time (JD)", None))
        self.label_6.setText(_translate("MainWindow", "Executed Last Maneuver", None))
        self.label_7.setText(_translate("MainWindow", "Semi-major Axis (km)", None))
        self.label_8.setText(_translate("MainWindow", "Eccentricity", None))
        self.label_9.setText(_translate("MainWindow", "Inclination (deg)", None))
        self.label_10.setText(_translate("MainWindow", "Long. of Asc. Node (deg)", None))
        self.label_11.setText(_translate("MainWindow", "Arg. of Perihelion (deg)", None))
        self.label_12.setText(_translate("MainWindow", "Mean Anomary (deg)", None))
        self.label_13.setText(_translate("MainWindow", "Orbital Period (days)", None))
        self.label_14.setText(_translate("MainWindow", "Perihelion Passage", None))
        self.label_15.setText(_translate("MainWindow", "Perihelion Passage (JD)", None))
        self.label_16.setText(_translate("MainWindow", "Semi-major Axis (AU)", None))
        self.label_17.setText(_translate("MainWindow", "Range from the Sun (km)", None))
        self.label_18.setText(_translate("MainWindow", "Velocity rel. to the Sun (m/s)", None))
        self.flightreview.setToolTip(_translate("MainWindow", "Review recent FLYTO maneuver", None))
        self.flightreview.setText(_translate("MainWindow", "Review Recent FLYTO", None))
        self.label_19.setText(_translate("MainWindow", "Current status", None))
        self.label_20.setText(_translate("MainWindow", "Selected maneuver:", None))
        self.label_mantime_h.setText(_translate("MainWindow", "Date&Time", None))
        self.label_22.setText(_translate("MainWindow", "Parameters", None))
        self.label_cman.setText(_translate("MainWindow", "1 START", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuCheckpoint.setTitle(_translate("MainWindow", "Checkpoint", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.actionOpen.setText(_translate("MainWindow", "&Open", None))
        self.actionNew.setText(_translate("MainWindow", "&New", None))
        self.actionSave.setText(_translate("MainWindow", "&Save", None))
        self.actionSave_as.setText(_translate("MainWindow", "Save &As...", None))
        self.actionQuit.setText(_translate("MainWindow", "&Quit", None))
        self.actionNew_from_current_status.setText(_translate("MainWindow", "New from current status", None))
        self.actionAbout_SSVG.setText(_translate("MainWindow", "about SSVG", None))
        self.actionCreate.setText(_translate("MainWindow", "Create", None))
        self.actionResume.setText(_translate("MainWindow", "Resume", None))
        self.actionProbe.setText(_translate("MainWindow", "Probe", None))
        self.actionTarget.setText(_translate("MainWindow", "Target", None))

