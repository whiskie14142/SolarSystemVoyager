# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 700)
        MainWindow.setMinimumSize(QtCore.QSize(640, 700))
        MainWindow.setMaximumSize(QtCore.QSize(640, 700))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setIconSize(QtCore.QSize(64, 64))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.manplans = QtWidgets.QTableWidget(self.centralwidget)
        self.manplans.setEnabled(False)
        self.manplans.setGeometry(QtCore.QRect(20, 70, 489, 251))
        self.manplans.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.manplans.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.manplans.setTabKeyNavigation(False)
        self.manplans.setProperty("showDropIndicator", False)
        self.manplans.setDragDropOverwriteMode(False)
        self.manplans.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.manplans.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.manplans.setCornerButtonEnabled(False)
        self.manplans.setRowCount(10)
        self.manplans.setColumnCount(3)
        self.manplans.setObjectName("manplans")
        item = QtWidgets.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.manplans.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.manplans.setItem(0, 0, item)
        self.manplans.horizontalHeader().setVisible(True)
        self.manplans.horizontalHeader().setCascadingSectionResizes(True)
        self.manplans.horizontalHeader().setDefaultSectionSize(100)
        self.manplans.horizontalHeader().setHighlightSections(False)
        self.manplans.verticalHeader().setVisible(True)
        self.manplans.verticalHeader().setDefaultSectionSize(20)
        self.manplans.verticalHeader().setHighlightSections(False)
        self.manplans.verticalHeader().setMinimumSectionSize(20)
        self.execNext = QtWidgets.QPushButton(self.centralwidget)
        self.execNext.setEnabled(False)
        self.execNext.setGeometry(QtCore.QRect(520, 220, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.execNext.setFont(font)
        self.execNext.setObjectName("execNext")
        self.insertMan = QtWidgets.QPushButton(self.centralwidget)
        self.insertMan.setEnabled(False)
        self.insertMan.setGeometry(QtCore.QRect(540, 140, 81, 23))
        self.insertMan.setStatusTip("")
        self.insertMan.setWhatsThis("")
        self.insertMan.setObjectName("insertMan")
        self.showOrbit = QtWidgets.QPushButton(self.centralwidget)
        self.showOrbit.setEnabled(False)
        self.showOrbit.setGeometry(QtCore.QRect(514, 10, 111, 23))
        self.showOrbit.setObjectName("showOrbit")
        self.editMan = QtWidgets.QPushButton(self.centralwidget)
        self.editMan.setEnabled(False)
        self.editMan.setGeometry(QtCore.QRect(540, 110, 81, 23))
        self.editMan.setObjectName("editMan")
        self.execto = QtWidgets.QPushButton(self.centralwidget)
        self.execto.setEnabled(False)
        self.execto.setGeometry(QtCore.QRect(540, 260, 81, 23))
        self.execto.setObjectName("execto")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 81, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 81, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.probename = QtWidgets.QLabel(self.centralwidget)
        self.probename.setGeometry(QtCore.QRect(90, 10, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.probename.setFont(font)
        self.probename.setText("")
        self.probename.setObjectName("probename")
        self.targetname = QtWidgets.QLabel(self.centralwidget)
        self.targetname.setGeometry(QtCore.QRect(90, 30, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.targetname.setFont(font)
        self.targetname.setText("")
        self.targetname.setObjectName("targetname")
        self.deleteMan = QtWidgets.QPushButton(self.centralwidget)
        self.deleteMan.setEnabled(False)
        self.deleteMan.setGeometry(QtCore.QRect(540, 170, 81, 23))
        self.deleteMan.setStatusTip("")
        self.deleteMan.setObjectName("deleteMan")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 50, 91, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.manfilename = QtWidgets.QLabel(self.centralwidget)
        self.manfilename.setGeometry(QtCore.QRect(342, 50, 281, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.manfilename.setFont(font)
        self.manfilename.setText("")
        self.manfilename.setObjectName("manfilename")
        self.editnext = QtWidgets.QPushButton(self.centralwidget)
        self.editnext.setEnabled(False)
        self.editnext.setGeometry(QtCore.QRect(520, 70, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.editnext.setFont(font)
        self.editnext.setObjectName("editnext")
        self.initexec = QtWidgets.QPushButton(self.centralwidget)
        self.initexec.setEnabled(False)
        self.initexec.setGeometry(QtCore.QRect(540, 290, 81, 23))
        self.initexec.setObjectName("initexec")
        self.reviewthroughout = QtWidgets.QPushButton(self.centralwidget)
        self.reviewthroughout.setEnabled(False)
        self.reviewthroughout.setGeometry(QtCore.QRect(260, 10, 111, 23))
        self.reviewthroughout.setObjectName("reviewthroughout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 370, 151, 16))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 390, 151, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 350, 151, 16))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 450, 151, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 490, 151, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 510, 151, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(20, 530, 151, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(20, 550, 151, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(20, 610, 151, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(20, 630, 151, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(20, 570, 151, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(20, 590, 151, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(20, 470, 151, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(20, 410, 151, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(20, 430, 151, 16))
        self.label_18.setObjectName("label_18")
        self.flightreview = QtWidgets.QPushButton(self.centralwidget)
        self.flightreview.setEnabled(False)
        self.flightreview.setGeometry(QtCore.QRect(387, 10, 111, 23))
        self.flightreview.setObjectName("flightreview")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(20, 327, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(380, 327, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_mantime_h = QtWidgets.QLabel(self.centralwidget)
        self.label_mantime_h.setEnabled(False)
        self.label_mantime_h.setGeometry(QtCore.QRect(380, 348, 61, 16))
        self.label_mantime_h.setObjectName("label_mantime_h")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(380, 368, 121, 16))
        self.label_22.setObjectName("label_22")
        self.selectedman = QtWidgets.QTableWidget(self.centralwidget)
        self.selectedman.setEnabled(True)
        self.selectedman.setGeometry(QtCore.QRect(380, 388, 241, 162))
        self.selectedman.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.selectedman.setRowCount(8)
        self.selectedman.setColumnCount(2)
        self.selectedman.setObjectName("selectedman")
        self.selectedman.horizontalHeader().setVisible(False)
        self.selectedman.verticalHeader().setVisible(False)
        self.selectedman.verticalHeader().setDefaultSectionSize(20)
        self.selectedman.verticalHeader().setMinimumSectionSize(20)
        self.label_progress = QtWidgets.QLabel(self.centralwidget)
        self.label_progress.setGeometry(QtCore.QRect(380, 553, 241, 16))
        self.label_progress.setText("")
        self.label_progress.setObjectName("label_progress")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(390, 569, 241, 15))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_cman = QtWidgets.QLabel(self.centralwidget)
        self.label_cman.setGeometry(QtCore.QRect(540, 327, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_cman.setFont(font)
        self.label_cman.setObjectName("label_cman")
        self.label_ISOT = QtWidgets.QLineEdit(self.centralwidget)
        self.label_ISOT.setGeometry(QtCore.QRect(180, 370, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_ISOT.setFont(font)
        self.label_ISOT.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_ISOT.setToolTip("")
        self.label_ISOT.setFrame(False)
        self.label_ISOT.setReadOnly(True)
        self.label_ISOT.setObjectName("label_ISOT")
        self.label_JD = QtWidgets.QLineEdit(self.centralwidget)
        self.label_JD.setGeometry(QtCore.QRect(180, 390, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_JD.setFont(font)
        self.label_JD.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_JD.setToolTip("")
        self.label_JD.setFrame(False)
        self.label_JD.setReadOnly(True)
        self.label_JD.setObjectName("label_JD")
        self.label_range = QtWidgets.QLineEdit(self.centralwidget)
        self.label_range.setGeometry(QtCore.QRect(180, 410, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_range.setFont(font)
        self.label_range.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_range.setToolTip("")
        self.label_range.setFrame(False)
        self.label_range.setReadOnly(True)
        self.label_range.setObjectName("label_range")
        self.label_velocity = QtWidgets.QLineEdit(self.centralwidget)
        self.label_velocity.setGeometry(QtCore.QRect(180, 430, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_velocity.setFont(font)
        self.label_velocity.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_velocity.setToolTip("")
        self.label_velocity.setFrame(False)
        self.label_velocity.setReadOnly(True)
        self.label_velocity.setObjectName("label_velocity")
        self.label_SMA = QtWidgets.QLineEdit(self.centralwidget)
        self.label_SMA.setGeometry(QtCore.QRect(180, 450, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_SMA.setFont(font)
        self.label_SMA.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_SMA.setToolTip("")
        self.label_SMA.setFrame(False)
        self.label_SMA.setReadOnly(True)
        self.label_SMA.setObjectName("label_SMA")
        self.label_SMAAU = QtWidgets.QLineEdit(self.centralwidget)
        self.label_SMAAU.setGeometry(QtCore.QRect(180, 470, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_SMAAU.setFont(font)
        self.label_SMAAU.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_SMAAU.setToolTip("")
        self.label_SMAAU.setFrame(False)
        self.label_SMAAU.setReadOnly(True)
        self.label_SMAAU.setObjectName("label_SMAAU")
        self.label_Ecc = QtWidgets.QLineEdit(self.centralwidget)
        self.label_Ecc.setGeometry(QtCore.QRect(180, 490, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_Ecc.setFont(font)
        self.label_Ecc.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_Ecc.setToolTip("")
        self.label_Ecc.setFrame(False)
        self.label_Ecc.setReadOnly(True)
        self.label_Ecc.setObjectName("label_Ecc")
        self.label_Inc = QtWidgets.QLineEdit(self.centralwidget)
        self.label_Inc.setGeometry(QtCore.QRect(180, 510, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_Inc.setFont(font)
        self.label_Inc.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_Inc.setToolTip("")
        self.label_Inc.setFrame(False)
        self.label_Inc.setReadOnly(True)
        self.label_Inc.setObjectName("label_Inc")
        self.label_LAN = QtWidgets.QLineEdit(self.centralwidget)
        self.label_LAN.setGeometry(QtCore.QRect(180, 530, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_LAN.setFont(font)
        self.label_LAN.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_LAN.setToolTip("")
        self.label_LAN.setFrame(False)
        self.label_LAN.setReadOnly(True)
        self.label_LAN.setObjectName("label_LAN")
        self.label_APH = QtWidgets.QLineEdit(self.centralwidget)
        self.label_APH.setGeometry(QtCore.QRect(180, 550, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_APH.setFont(font)
        self.label_APH.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_APH.setToolTip("")
        self.label_APH.setFrame(False)
        self.label_APH.setReadOnly(True)
        self.label_APH.setObjectName("label_APH")
        self.label_PPT = QtWidgets.QLineEdit(self.centralwidget)
        self.label_PPT.setGeometry(QtCore.QRect(180, 570, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_PPT.setFont(font)
        self.label_PPT.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_PPT.setToolTip("")
        self.label_PPT.setFrame(False)
        self.label_PPT.setReadOnly(True)
        self.label_PPT.setObjectName("label_PPT")
        self.label_PPTJD = QtWidgets.QLineEdit(self.centralwidget)
        self.label_PPTJD.setGeometry(QtCore.QRect(180, 590, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_PPTJD.setFont(font)
        self.label_PPTJD.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_PPTJD.setToolTip("")
        self.label_PPTJD.setFrame(False)
        self.label_PPTJD.setReadOnly(True)
        self.label_PPTJD.setObjectName("label_PPTJD")
        self.label_MA = QtWidgets.QLineEdit(self.centralwidget)
        self.label_MA.setGeometry(QtCore.QRect(180, 610, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_MA.setFont(font)
        self.label_MA.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_MA.setToolTip("")
        self.label_MA.setFrame(False)
        self.label_MA.setReadOnly(True)
        self.label_MA.setObjectName("label_MA")
        self.label_OP = QtWidgets.QLineEdit(self.centralwidget)
        self.label_OP.setGeometry(QtCore.QRect(180, 630, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_OP.setFont(font)
        self.label_OP.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_OP.setToolTip("")
        self.label_OP.setFrame(False)
        self.label_OP.setReadOnly(True)
        self.label_OP.setObjectName("label_OP")
        self.label_mantime = QtWidgets.QLineEdit(self.centralwidget)
        self.label_mantime.setGeometry(QtCore.QRect(445, 348, 182, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_mantime.setFont(font)
        self.label_mantime.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_mantime.setToolTip("")
        self.label_mantime.setFrame(False)
        self.label_mantime.setReadOnly(True)
        self.label_mantime.setObjectName("label_mantime")
        self.label_ELM = QtWidgets.QLabel(self.centralwidget)
        self.label_ELM.setGeometry(QtCore.QRect(180, 350, 187, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_ELM.setFont(font)
        self.label_ELM.setText("")
        self.label_ELM.setObjectName("label_ELM")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(20, 650, 151, 16))
        self.label_21.setObjectName("label_21")
        self.label_ADV = QtWidgets.QLineEdit(self.centralwidget)
        self.label_ADV.setGeometry(QtCore.QRect(180, 650, 187, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.label_ADV.setFont(font)
        self.label_ADV.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.label_ADV.setToolTip("")
        self.label_ADV.setFrame(False)
        self.label_ADV.setReadOnly(True)
        self.label_ADV.setObjectName("label_ADV")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(0, 50, 81, 16))
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.spacebase = QtWidgets.QLabel(self.centralwidget)
        self.spacebase.setGeometry(QtCore.QRect(90, 50, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.spacebase.setFont(font)
        self.spacebase.setText("")
        self.spacebase.setObjectName("spacebase")
        self.sysMessage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.sysMessage.setEnabled(True)
        self.sysMessage.setGeometry(QtCore.QRect(380, 601, 248, 67))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.sysMessage.setFont(font)
        self.sysMessage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sysMessage.setAcceptDrops(False)
        self.sysMessage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sysMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.sysMessage.setLineWidth(0)
        self.sysMessage.setUndoRedoEnabled(False)
        self.sysMessage.setReadOnly(True)
        self.sysMessage.setMaximumBlockCount(20)
        self.sysMessage.setObjectName("sysMessage")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(380, 583, 131, 16))
        self.label_24.setObjectName("label_24")
        self.label_24.raise_()
        self.sysMessage.raise_()
        self.manplans.raise_()
        self.execNext.raise_()
        self.insertMan.raise_()
        self.showOrbit.raise_()
        self.editMan.raise_()
        self.execto.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.probename.raise_()
        self.targetname.raise_()
        self.deleteMan.raise_()
        self.label_3.raise_()
        self.manfilename.raise_()
        self.editnext.raise_()
        self.initexec.raise_()
        self.reviewthroughout.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.flightreview.raise_()
        self.label_19.raise_()
        self.label_20.raise_()
        self.label_mantime_h.raise_()
        self.label_22.raise_()
        self.selectedman.raise_()
        self.label_progress.raise_()
        self.progressBar.raise_()
        self.label_cman.raise_()
        self.label_ISOT.raise_()
        self.label_JD.raise_()
        self.label_range.raise_()
        self.label_velocity.raise_()
        self.label_SMA.raise_()
        self.label_SMAAU.raise_()
        self.label_Ecc.raise_()
        self.label_Inc.raise_()
        self.label_LAN.raise_()
        self.label_APH.raise_()
        self.label_PPT.raise_()
        self.label_PPTJD.raise_()
        self.label_MA.raise_()
        self.label_OP.raise_()
        self.label_mantime.raise_()
        self.label_ELM.raise_()
        self.label_21.raise_()
        self.label_ADV.raise_()
        self.label_23.raise_()
        self.spacebase.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuCheckpoint = QtWidgets.QMenu(self.menubar)
        self.menuCheckpoint.setEnabled(False)
        self.menuCheckpoint.setObjectName("menuCheckpoint")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setEnabled(False)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setEnabled(False)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNew_from_current_status = QtWidgets.QAction(MainWindow)
        self.actionNew_from_current_status.setEnabled(False)
        self.actionNew_from_current_status.setObjectName("actionNew_from_current_status")
        self.actionAbout_SSVG = QtWidgets.QAction(MainWindow)
        self.actionAbout_SSVG.setObjectName("actionAbout_SSVG")
        self.actionCreate = QtWidgets.QAction(MainWindow)
        self.actionCreate.setObjectName("actionCreate")
        self.actionResume = QtWidgets.QAction(MainWindow)
        self.actionResume.setEnabled(False)
        self.actionResume.setObjectName("actionResume")
        self.actionProbe = QtWidgets.QAction(MainWindow)
        self.actionProbe.setObjectName("actionProbe")
        self.actionTarget = QtWidgets.QAction(MainWindow)
        self.actionTarget.setObjectName("actionTarget")
        self.action_UsersGuide = QtWidgets.QAction(MainWindow)
        self.action_UsersGuide.setObjectName("action_UsersGuide")
        self.action_HomePage = QtWidgets.QAction(MainWindow)
        self.action_HomePage.setObjectName("action_HomePage")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.action_UsersGuide)
        self.menuHelp.addAction(self.action_HomePage)
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
        MainWindow.setTabOrder(self.reviewthroughout, self.flightreview)
        MainWindow.setTabOrder(self.flightreview, self.showOrbit)
        MainWindow.setTabOrder(self.showOrbit, self.editnext)
        MainWindow.setTabOrder(self.editnext, self.editMan)
        MainWindow.setTabOrder(self.editMan, self.insertMan)
        MainWindow.setTabOrder(self.insertMan, self.deleteMan)
        MainWindow.setTabOrder(self.deleteMan, self.execNext)
        MainWindow.setTabOrder(self.execNext, self.execto)
        MainWindow.setTabOrder(self.execto, self.initexec)
        MainWindow.setTabOrder(self.initexec, self.manplans)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SSVG"))
        self.manplans.setToolTip(_translate("MainWindow", "Maneuver Table"))
        item = self.manplans.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.manplans.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Parameters"))
        item = self.manplans.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        __sortingEnabled = self.manplans.isSortingEnabled()
        self.manplans.setSortingEnabled(False)
        self.manplans.setSortingEnabled(__sortingEnabled)
        self.execNext.setToolTip(_translate("MainWindow", "Execute \'Next\' Maneuver"))
        self.execNext.setText(_translate("MainWindow", "EXECUTE"))
        self.insertMan.setToolTip(_translate("MainWindow", "Insert an empty Maneuver"))
        self.insertMan.setText(_translate("MainWindow", "INS *"))
        self.showOrbit.setToolTip(_translate("MainWindow", "Show current Orbits"))
        self.showOrbit.setText(_translate("MainWindow", "SHOW Orbit"))
        self.editMan.setToolTip(_translate("MainWindow", "Edit selected Maneuver"))
        self.editMan.setText(_translate("MainWindow", "EDIT *"))
        self.execto.setToolTip(_translate("MainWindow", "Execute multiple Maneuvers"))
        self.execto.setText(_translate("MainWindow", "EXECUTE *"))
        self.label.setText(_translate("MainWindow", "Probe"))
        self.label_2.setText(_translate("MainWindow", "Target"))
        self.deleteMan.setToolTip(_translate("MainWindow", "Delete selected Maneuver"))
        self.deleteMan.setText(_translate("MainWindow", "DEL *"))
        self.label_3.setText(_translate("MainWindow", "Flight Plan"))
        self.editnext.setToolTip(_translate("MainWindow", "Edit \'Next\' Maneuver"))
        self.editnext.setText(_translate("MainWindow", "EDIT Next"))
        self.initexec.setToolTip(_translate("MainWindow", "Clear Execution State"))
        self.initexec.setText(_translate("MainWindow", "CLEAR"))
        self.reviewthroughout.setToolTip(_translate("MainWindow", "Review throughout the Flight"))
        self.reviewthroughout.setText(_translate("MainWindow", "REVIEW Through"))
        self.label_4.setText(_translate("MainWindow", "Current Time"))
        self.label_5.setText(_translate("MainWindow", "Current Time (JD)"))
        self.label_6.setText(_translate("MainWindow", "Executed Last Maneuver"))
        self.label_7.setText(_translate("MainWindow", "Semi-major Axis (km)"))
        self.label_8.setText(_translate("MainWindow", "Eccentricity"))
        self.label_9.setText(_translate("MainWindow", "Inclination (deg)"))
        self.label_10.setText(_translate("MainWindow", "Long. of Asc. Node (deg)"))
        self.label_11.setText(_translate("MainWindow", "Arg. of Perihelion (deg)"))
        self.label_12.setText(_translate("MainWindow", "Mean Anomaly (deg)"))
        self.label_13.setText(_translate("MainWindow", "Orbital Period (days)"))
        self.label_14.setText(_translate("MainWindow", "Perihelion Passage"))
        self.label_15.setText(_translate("MainWindow", "Perihelion Passage (JD)"))
        self.label_16.setText(_translate("MainWindow", "Semi-major Axis (AU)"))
        self.label_17.setText(_translate("MainWindow", "Distance from Sun (km)"))
        self.label_18.setText(_translate("MainWindow", "Velocity rel. to Sun (m/s)"))
        self.flightreview.setToolTip(_translate("MainWindow", "Review recent FLYTO Maneuver"))
        self.flightreview.setText(_translate("MainWindow", "REVIEW Recent"))
        self.label_19.setText(_translate("MainWindow", "Current Status"))
        self.label_20.setText(_translate("MainWindow", "Selected Maneuver"))
        self.label_mantime_h.setText(_translate("MainWindow", "Date&Time"))
        self.label_22.setText(_translate("MainWindow", "Parameters"))
        self.label_cman.setText(_translate("MainWindow", "1 START"))
        self.label_21.setText(_translate("MainWindow", "Accum. DV (m/s) CP, EP, SS"))
        self.label_23.setText(_translate("MainWindow", "Space Base"))
        self.sysMessage.setToolTip(_translate("MainWindow", "System Messages"))
        self.label_24.setText(_translate("MainWindow", "Messages"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuCheckpoint.setTitle(_translate("MainWindow", "Checkpoint"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a Flight Plan"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionNew.setToolTip(_translate("MainWindow", "Create a Flight Plan"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save the Flight Plan"))
        self.actionSave_as.setText(_translate("MainWindow", "Save &as"))
        self.actionSave_as.setToolTip(_translate("MainWindow", "Save the Flight Plan with new Name"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit SSVG"))
        self.actionNew_from_current_status.setText(_translate("MainWindow", "New from current status"))
        self.actionAbout_SSVG.setText(_translate("MainWindow", "&about SSVG"))
        self.actionCreate.setText(_translate("MainWindow", "&Create"))
        self.actionResume.setText(_translate("MainWindow", "&Resume"))
        self.actionProbe.setText(_translate("MainWindow", "&Probe"))
        self.actionTarget.setText(_translate("MainWindow", "&Target"))
        self.action_UsersGuide.setText(_translate("MainWindow", "&User\'s Guide"))
        self.action_HomePage.setText(_translate("MainWindow", "&Home Page"))

