# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orbitoptimizedialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OrbitOptimizeDialog(object):
    def setupUi(self, OrbitOptimizeDialog):
        OrbitOptimizeDialog.setObjectName("OrbitOptimizeDialog")
        OrbitOptimizeDialog.setWindowModality(QtCore.Qt.WindowModal)
        OrbitOptimizeDialog.resize(621, 664)
        OrbitOptimizeDialog.setMinimumSize(QtCore.QSize(621, 664))
        OrbitOptimizeDialog.setMaximumSize(QtCore.QSize(621, 664))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        OrbitOptimizeDialog.setFont(font)
        OrbitOptimizeDialog.setModal(True)
        self.label_3 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_3.setGeometry(QtCore.QRect(50, 490, 171, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_9.setGeometry(QtCore.QRect(230, 490, 191, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_14 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_14.setGeometry(QtCore.QRect(200, 513, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.label_16 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_16.setGeometry(QtCore.QRect(200, 533, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.terminalRV_cur = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.terminalRV_cur.setGeometry(QtCore.QRect(280, 515, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.terminalRV_cur.setFont(font)
        self.terminalRV_cur.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.terminalRV_cur.setToolTip("")
        self.terminalRV_cur.setFrame(False)
        self.terminalRV_cur.setReadOnly(True)
        self.terminalRV_cur.setObjectName("terminalRV_cur")
        self.terminalRV_min = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.terminalRV_min.setGeometry(QtCore.QRect(280, 535, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.terminalRV_min.setFont(font)
        self.terminalRV_min.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.terminalRV_min.setToolTip("")
        self.terminalRV_min.setFrame(False)
        self.terminalRV_min.setReadOnly(True)
        self.terminalRV_min.setObjectName("terminalRV_min")
        self.groupBox_3 = QtWidgets.QGroupBox(OrbitOptimizeDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 221, 91))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.check_Ptrj = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_Ptrj.setEnabled(True)
        self.check_Ptrj.setGeometry(QtCore.QRect(110, 40, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.check_Ptrj.setFont(font)
        self.check_Ptrj.setChecked(False)
        self.check_Ptrj.setObjectName("check_Ptrj")
        self.check_Ppred = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_Ppred.setGeometry(QtCore.QRect(110, 20, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.check_Ppred.setFont(font)
        self.check_Ppred.setChecked(True)
        self.check_Ppred.setObjectName("check_Ppred")
        self.check_TKepler = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_TKepler.setGeometry(QtCore.QRect(10, 40, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.check_TKepler.setFont(font)
        self.check_TKepler.setChecked(True)
        self.check_TKepler.setObjectName("check_TKepler")
        self.check_orgorb = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_orgorb.setGeometry(QtCore.QRect(10, 20, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.check_orgorb.setFont(font)
        self.check_orgorb.setChecked(True)
        self.check_orgorb.setObjectName("check_orgorb")
        self.label_18 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_18.setGeometry(QtCore.QRect(10, 533, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.initialDV_min = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.initialDV_min.setGeometry(QtCore.QRect(90, 535, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.initialDV_min.setFont(font)
        self.initialDV_min.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.initialDV_min.setToolTip("")
        self.initialDV_min.setFrame(False)
        self.initialDV_min.setReadOnly(True)
        self.initialDV_min.setObjectName("initialDV_min")
        self.initialDV_cur = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.initialDV_cur.setGeometry(QtCore.QRect(90, 515, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.initialDV_cur.setFont(font)
        self.initialDV_cur.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.initialDV_cur.setToolTip("")
        self.initialDV_cur.setFrame(False)
        self.initialDV_cur.setReadOnly(True)
        self.initialDV_cur.setObjectName("initialDV_cur")
        self.label_15 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_15.setGeometry(QtCore.QRect(10, 513, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.finishbutton = QtWidgets.QPushButton(OrbitOptimizeDialog)
        self.finishbutton.setGeometry(QtCore.QRect(260, 625, 121, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.finishbutton.setFont(font)
        self.finishbutton.setAutoDefault(False)
        self.finishbutton.setObjectName("finishbutton")
        self.cancelbutton = QtWidgets.QPushButton(OrbitOptimizeDialog)
        self.cancelbutton.setGeometry(QtCore.QRect(510, 625, 91, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.cancelbutton.setFont(font)
        self.cancelbutton.setAutoDefault(False)
        self.cancelbutton.setObjectName("cancelbutton")
        self.label = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label.setGeometry(QtCore.QRect(420, 490, 191, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_20 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_20.setGeometry(QtCore.QRect(390, 533, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.totalDV_min = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.totalDV_min.setGeometry(QtCore.QRect(470, 534, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.totalDV_min.setFont(font)
        self.totalDV_min.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.totalDV_min.setToolTip("")
        self.totalDV_min.setFrame(False)
        self.totalDV_min.setReadOnly(True)
        self.totalDV_min.setObjectName("totalDV_min")
        self.totalDV_cur = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.totalDV_cur.setGeometry(QtCore.QRect(470, 514, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.totalDV_cur.setFont(font)
        self.totalDV_cur.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.totalDV_cur.setToolTip("")
        self.totalDV_cur.setFrame(False)
        self.totalDV_cur.setReadOnly(True)
        self.totalDV_cur.setObjectName("totalDV_cur")
        self.label_22 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_22.setGeometry(QtCore.QRect(390, 513, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.clearstat = QtWidgets.QPushButton(OrbitOptimizeDialog)
        self.clearstat.setGeometry(QtCore.QRect(280, 570, 101, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.clearstat.setFont(font)
        self.clearstat.setAutoDefault(False)
        self.clearstat.setObjectName("clearstat")
        self.idv_phi = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.idv_phi.setGeometry(QtCore.QRect(90, 565, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.idv_phi.setFont(font)
        self.idv_phi.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.idv_phi.setToolTip("")
        self.idv_phi.setFrame(False)
        self.idv_phi.setReadOnly(True)
        self.idv_phi.setObjectName("idv_phi")
        self.idv_elv = QtWidgets.QLineEdit(OrbitOptimizeDialog)
        self.idv_elv.setGeometry(QtCore.QRect(90, 585, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.idv_elv.setFont(font)
        self.idv_elv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.idv_elv.setToolTip("")
        self.idv_elv.setFrame(False)
        self.idv_elv.setReadOnly(True)
        self.idv_elv.setObjectName("idv_elv")
        self.label_23 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_23.setGeometry(QtCore.QRect(10, 565, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_24.setGeometry(QtCore.QRect(10, 585, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.reopenbutton = QtWidgets.QPushButton(OrbitOptimizeDialog)
        self.reopenbutton.setGeometry(QtCore.QRect(20, 625, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.reopenbutton.setFont(font)
        self.reopenbutton.setAutoDefault(False)
        self.reopenbutton.setObjectName("reopenbutton")
        self.fixed_to_ct = QtWidgets.QCheckBox(OrbitOptimizeDialog)
        self.fixed_to_ct.setGeometry(QtCore.QRect(110, 152, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.fixed_to_ct.setFont(font)
        self.fixed_to_ct.setChecked(False)
        self.fixed_to_ct.setObjectName("fixed_to_ct")
        self.box_initialtime = QtWidgets.QFrame(OrbitOptimizeDialog)
        self.box_initialtime.setGeometry(QtCore.QRect(10, 140, 601, 141))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.box_initialtime.setFont(font)
        self.box_initialtime.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.box_initialtime.setFrameShadow(QtWidgets.QFrame.Plain)
        self.box_initialtime.setObjectName("box_initialtime")
        self.groupBox_itsr = QtWidgets.QGroupBox(self.box_initialtime)
        self.groupBox_itsr.setGeometry(QtCore.QRect(360, 70, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.groupBox_itsr.setFont(font)
        self.groupBox_itsr.setObjectName("groupBox_itsr")
        self.it_wide = QtWidgets.QRadioButton(self.groupBox_itsr)
        self.it_wide.setGeometry(QtCore.QRect(30, 17, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.it_wide.setFont(font)
        self.it_wide.setChecked(True)
        self.it_wide.setObjectName("it_wide")
        self.it_narrow = QtWidgets.QRadioButton(self.groupBox_itsr)
        self.it_narrow.setGeometry(QtCore.QRect(30, 37, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.it_narrow.setFont(font)
        self.it_narrow.setChecked(False)
        self.it_narrow.setObjectName("it_narrow")
        self.it_f = QtWidgets.QPushButton(self.box_initialtime)
        self.it_f.setGeometry(QtCore.QRect(305, 66, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.it_f.setFont(font)
        self.it_f.setAutoRepeat(True)
        self.it_f.setAutoDefault(False)
        self.it_f.setObjectName("it_f")
        self.it_fb = QtWidgets.QPushButton(self.box_initialtime)
        self.it_fb.setGeometry(QtCore.QRect(10, 40, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.it_fb.setFont(font)
        self.it_fb.setAutoRepeat(True)
        self.it_fb.setAutoDefault(False)
        self.it_fb.setObjectName("it_fb")
        self.label_10 = QtWidgets.QLabel(self.box_initialtime)
        self.label_10.setGeometry(QtCore.QRect(1, 70, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_it = QtWidgets.QLabel(self.box_initialtime)
        self.label_it.setGeometry(QtCore.QRect(250, 13, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_it.setFont(font)
        self.label_it.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_it.setObjectName("label_it")
        self.label_itto = QtWidgets.QLabel(self.box_initialtime)
        self.label_itto.setGeometry(QtCore.QRect(520, 20, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_itto.setFont(font)
        self.label_itto.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_itto.setObjectName("label_itto")
        self.label_6 = QtWidgets.QLabel(self.box_initialtime)
        self.label_6.setGeometry(QtCore.QRect(549, 70, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.it_b = QtWidgets.QPushButton(self.box_initialtime)
        self.it_b.setGeometry(QtCore.QRect(265, 66, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.it_b.setFont(font)
        self.it_b.setAutoRepeat(True)
        self.it_b.setAutoDefault(False)
        self.it_b.setObjectName("it_b")
        self.label_itfrom = QtWidgets.QLabel(self.box_initialtime)
        self.label_itfrom.setGeometry(QtCore.QRect(10, 20, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_itfrom.setFont(font)
        self.label_itfrom.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_itfrom.setObjectName("label_itfrom")
        self.initialtime = QtWidgets.QLineEdit(self.box_initialtime)
        self.initialtime.setGeometry(QtCore.QRect(340, 12, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.initialtime.setFont(font)
        self.initialtime.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.initialtime.setAcceptDrops(False)
        self.initialtime.setToolTip("")
        self.initialtime.setFrame(False)
        self.initialtime.setReadOnly(True)
        self.initialtime.setObjectName("initialtime")
        self.sl_inittime = QtWidgets.QSlider(self.box_initialtime)
        self.sl_inittime.setGeometry(QtCore.QRect(45, 40, 511, 22))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.sl_inittime.setFont(font)
        self.sl_inittime.setMinimum(0)
        self.sl_inittime.setMaximum(500)
        self.sl_inittime.setOrientation(QtCore.Qt.Horizontal)
        self.sl_inittime.setObjectName("sl_inittime")
        self.it_ff = QtWidgets.QPushButton(self.box_initialtime)
        self.it_ff.setGeometry(QtCore.QRect(560, 40, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.it_ff.setFont(font)
        self.it_ff.setAutoRepeat(True)
        self.it_ff.setAutoDefault(False)
        self.it_ff.setObjectName("it_ff")
        self.label_2 = QtWidgets.QLabel(self.box_initialtime)
        self.label_2.setGeometry(QtCore.QRect(256, 110, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_initialtime = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_initialtime.setGeometry(QtCore.QRect(18, 123, 131, 17))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_initialtime.setFont(font)
        self.label_initialtime.setObjectName("label_initialtime")
        self.frame = QtWidgets.QFrame(OrbitOptimizeDialog)
        self.frame.setGeometry(QtCore.QRect(10, 315, 601, 151))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setGeometry(QtCore.QRect(80, 80, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.radio_fd = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_fd.setGeometry(QtCore.QRect(40, 17, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.radio_fd.setFont(font)
        self.radio_fd.setChecked(True)
        self.radio_fd.setObjectName("radio_fd")
        self.radio_tt = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_tt.setGeometry(QtCore.QRect(40, 37, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.radio_tt.setFont(font)
        self.radio_tt.setChecked(False)
        self.radio_tt.setObjectName("radio_tt")
        self.duration = QtWidgets.QLineEdit(self.frame)
        self.duration.setGeometry(QtCore.QRect(152, 12, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.duration.setFont(font)
        self.duration.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.duration.setAcceptDrops(False)
        self.duration.setToolTip("")
        self.duration.setFrame(False)
        self.duration.setReadOnly(True)
        self.duration.setObjectName("duration")
        self.tt_fb = QtWidgets.QPushButton(self.frame)
        self.tt_fb.setGeometry(QtCore.QRect(12, 50, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tt_fb.setFont(font)
        self.tt_fb.setAutoRepeat(True)
        self.tt_fb.setAutoDefault(False)
        self.tt_fb.setObjectName("tt_fb")
        self.label_ttto = QtWidgets.QLabel(self.frame)
        self.label_ttto.setGeometry(QtCore.QRect(520, 30, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_ttto.setFont(font)
        self.label_ttto.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_ttto.setObjectName("label_ttto")
        self.tt_b = QtWidgets.QPushButton(self.frame)
        self.tt_b.setGeometry(QtCore.QRect(265, 76, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tt_b.setFont(font)
        self.tt_b.setAutoRepeat(True)
        self.tt_b.setAutoDefault(False)
        self.tt_b.setObjectName("tt_b")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(551, 80, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(32, 11, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.tt_ff = QtWidgets.QPushButton(self.frame)
        self.tt_ff.setGeometry(QtCore.QRect(562, 50, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tt_ff.setFont(font)
        self.tt_ff.setAutoRepeat(True)
        self.tt_ff.setAutoDefault(False)
        self.tt_ff.setObjectName("tt_ff")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(2, 80, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.terminaltime = QtWidgets.QLineEdit(self.frame)
        self.terminaltime.setGeometry(QtCore.QRect(342, 12, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.terminaltime.setFont(font)
        self.terminaltime.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.terminaltime.setAcceptDrops(False)
        self.terminaltime.setToolTip("")
        self.terminaltime.setFrame(False)
        self.terminaltime.setReadOnly(True)
        self.terminaltime.setObjectName("terminaltime")
        self.label_ttfrom = QtWidgets.QLabel(self.frame)
        self.label_ttfrom.setGeometry(QtCore.QRect(10, 30, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_ttfrom.setFont(font)
        self.label_ttfrom.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_ttfrom.setObjectName("label_ttfrom")
        self.sl_duration = QtWidgets.QSlider(self.frame)
        self.sl_duration.setGeometry(QtCore.QRect(47, 50, 511, 22))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.sl_duration.setFont(font)
        self.sl_duration.setMinimum(0)
        self.sl_duration.setMaximum(500)
        self.sl_duration.setOrientation(QtCore.Qt.Horizontal)
        self.sl_duration.setObjectName("sl_duration")
        self.tt_f = QtWidgets.QPushButton(self.frame)
        self.tt_f.setGeometry(QtCore.QRect(305, 76, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.tt_f.setFont(font)
        self.tt_f.setAutoRepeat(True)
        self.tt_f.setAutoDefault(False)
        self.tt_f.setObjectName("tt_f")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(256, 120, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(252, 11, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.groupBox_ttsr = QtWidgets.QGroupBox(self.frame)
        self.groupBox_ttsr.setGeometry(QtCore.QRect(362, 80, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.groupBox_ttsr.setFont(font)
        self.groupBox_ttsr.setObjectName("groupBox_ttsr")
        self.tt_wide = QtWidgets.QRadioButton(self.groupBox_ttsr)
        self.tt_wide.setGeometry(QtCore.QRect(30, 17, 131, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.tt_wide.setFont(font)
        self.tt_wide.setChecked(True)
        self.tt_wide.setObjectName("tt_wide")
        self.tt_narrow = QtWidgets.QRadioButton(self.groupBox_ttsr)
        self.tt_narrow.setGeometry(QtCore.QRect(30, 37, 131, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.tt_narrow.setFont(font)
        self.tt_narrow.setChecked(False)
        self.tt_narrow.setObjectName("tt_narrow")
        self.label_5 = QtWidgets.QLabel(OrbitOptimizeDialog)
        self.label_5.setGeometry(QtCore.QRect(18, 298, 131, 17))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.sysMessage = QtWidgets.QPlainTextEdit(OrbitOptimizeDialog)
        self.sysMessage.setGeometry(QtCore.QRect(398, 571, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.sysMessage.setFont(font)
        self.sysMessage.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.sysMessage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sysMessage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sysMessage.setMaximumBlockCount(20)
        self.sysMessage.setObjectName("sysMessage")
        self.whatIsOptimize = QtWidgets.QPlainTextEdit(OrbitOptimizeDialog)
        self.whatIsOptimize.setGeometry(QtCore.QRect(250, 10, 351, 121))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.whatIsOptimize.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.whatIsOptimize.setFont(font)
        self.whatIsOptimize.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.whatIsOptimize.setFocusPolicy(QtCore.Qt.NoFocus)
        self.whatIsOptimize.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.whatIsOptimize.setObjectName("whatIsOptimize")
        self.label_3.raise_()
        self.label_9.raise_()
        self.label_14.raise_()
        self.label_16.raise_()
        self.terminalRV_cur.raise_()
        self.terminalRV_min.raise_()
        self.groupBox_3.raise_()
        self.label_18.raise_()
        self.initialDV_min.raise_()
        self.initialDV_cur.raise_()
        self.label_15.raise_()
        self.finishbutton.raise_()
        self.cancelbutton.raise_()
        self.label.raise_()
        self.label_20.raise_()
        self.totalDV_min.raise_()
        self.totalDV_cur.raise_()
        self.label_22.raise_()
        self.clearstat.raise_()
        self.idv_phi.raise_()
        self.idv_elv.raise_()
        self.label_23.raise_()
        self.label_24.raise_()
        self.reopenbutton.raise_()
        self.box_initialtime.raise_()
        self.fixed_to_ct.raise_()
        self.label_initialtime.raise_()
        self.frame.raise_()
        self.label_5.raise_()
        self.sysMessage.raise_()
        self.whatIsOptimize.raise_()

        self.retranslateUi(OrbitOptimizeDialog)
        QtCore.QMetaObject.connectSlotsByName(OrbitOptimizeDialog)
        OrbitOptimizeDialog.setTabOrder(self.check_orgorb, self.check_Ppred)
        OrbitOptimizeDialog.setTabOrder(self.check_Ppred, self.check_TKepler)
        OrbitOptimizeDialog.setTabOrder(self.check_TKepler, self.check_Ptrj)
        OrbitOptimizeDialog.setTabOrder(self.check_Ptrj, self.reopenbutton)
        OrbitOptimizeDialog.setTabOrder(self.reopenbutton, self.fixed_to_ct)
        OrbitOptimizeDialog.setTabOrder(self.fixed_to_ct, self.it_fb)
        OrbitOptimizeDialog.setTabOrder(self.it_fb, self.sl_inittime)
        OrbitOptimizeDialog.setTabOrder(self.sl_inittime, self.it_ff)
        OrbitOptimizeDialog.setTabOrder(self.it_ff, self.it_b)
        OrbitOptimizeDialog.setTabOrder(self.it_b, self.it_f)
        OrbitOptimizeDialog.setTabOrder(self.it_f, self.it_wide)
        OrbitOptimizeDialog.setTabOrder(self.it_wide, self.it_narrow)
        OrbitOptimizeDialog.setTabOrder(self.it_narrow, self.tt_fb)
        OrbitOptimizeDialog.setTabOrder(self.tt_fb, self.sl_duration)
        OrbitOptimizeDialog.setTabOrder(self.sl_duration, self.tt_ff)
        OrbitOptimizeDialog.setTabOrder(self.tt_ff, self.tt_b)
        OrbitOptimizeDialog.setTabOrder(self.tt_b, self.tt_f)
        OrbitOptimizeDialog.setTabOrder(self.tt_f, self.radio_fd)
        OrbitOptimizeDialog.setTabOrder(self.radio_fd, self.radio_tt)
        OrbitOptimizeDialog.setTabOrder(self.radio_tt, self.tt_wide)
        OrbitOptimizeDialog.setTabOrder(self.tt_wide, self.tt_narrow)
        OrbitOptimizeDialog.setTabOrder(self.tt_narrow, self.clearstat)
        OrbitOptimizeDialog.setTabOrder(self.clearstat, self.finishbutton)
        OrbitOptimizeDialog.setTabOrder(self.finishbutton, self.cancelbutton)

    def retranslateUi(self, OrbitOptimizeDialog):
        _translate = QtCore.QCoreApplication.translate
        OrbitOptimizeDialog.setWindowTitle(_translate("OrbitOptimizeDialog", "START Optimize Assistant"))
        self.label_3.setText(_translate("OrbitOptimizeDialog", "Initial Delta-V (m/s)"))
        self.label_9.setText(_translate("OrbitOptimizeDialog", "Terminal Relative Velocity (m/s)"))
        self.label_14.setText(_translate("OrbitOptimizeDialog", "Current"))
        self.label_16.setText(_translate("OrbitOptimizeDialog", "Min."))
        self.groupBox_3.setTitle(_translate("OrbitOptimizeDialog", "Show Orbit"))
        self.check_Ptrj.setText(_translate("OrbitOptimizeDialog", "Trajectory"))
        self.check_Ppred.setText(_translate("OrbitOptimizeDialog", "Current"))
        self.check_TKepler.setText(_translate("OrbitOptimizeDialog", "Target"))
        self.check_orgorb.setText(_translate("OrbitOptimizeDialog", "Space Base"))
        self.label_18.setText(_translate("OrbitOptimizeDialog", "Min."))
        self.label_15.setText(_translate("OrbitOptimizeDialog", "Current"))
        self.finishbutton.setToolTip(_translate("OrbitOptimizeDialog", "Finish Optimize and Apply"))
        self.finishbutton.setText(_translate("OrbitOptimizeDialog", "Finish"))
        self.cancelbutton.setToolTip(_translate("OrbitOptimizeDialog", "Cancel Optimize"))
        self.cancelbutton.setText(_translate("OrbitOptimizeDialog", "Cancel"))
        self.label.setText(_translate("OrbitOptimizeDialog", "Total DV (IDV + TRV)"))
        self.label_20.setText(_translate("OrbitOptimizeDialog", "Min."))
        self.label_22.setText(_translate("OrbitOptimizeDialog", "Current"))
        self.clearstat.setToolTip(_translate("OrbitOptimizeDialog", "Clear all Minimum Values"))
        self.clearstat.setText(_translate("OrbitOptimizeDialog", "Clear Minimums"))
        self.label_23.setText(_translate("OrbitOptimizeDialog", "phi (deg)"))
        self.label_24.setText(_translate("OrbitOptimizeDialog", "elv (deg)"))
        self.reopenbutton.setToolTip(_translate("OrbitOptimizeDialog", "Show 3D Orbit Window"))
        self.reopenbutton.setText(_translate("OrbitOptimizeDialog", "Redisplay 3D Orbit"))
        self.fixed_to_ct.setText(_translate("OrbitOptimizeDialog", "Fix to SSVG\'s Time"))
        self.groupBox_itsr.setTitle(_translate("OrbitOptimizeDialog", "Slider Range"))
        self.it_wide.setText(_translate("OrbitOptimizeDialog", "Wide    (500 days)"))
        self.it_narrow.setText(_translate("OrbitOptimizeDialog", "Narrow (100 days)"))
        self.it_f.setToolTip(_translate("OrbitOptimizeDialog", "Move the Handle Right"))
        self.it_f.setText(_translate("OrbitOptimizeDialog", ">"))
        self.it_fb.setToolTip(_translate("OrbitOptimizeDialog", "Shift Range to Left"))
        self.it_fb.setText(_translate("OrbitOptimizeDialog", "<<<"))
        self.label_10.setText(_translate("OrbitOptimizeDialog", "Shift\n"
"Range"))
        self.label_it.setText(_translate("OrbitOptimizeDialog", "Start Time"))
        self.label_itto.setText(_translate("OrbitOptimizeDialog", "2000-00-00"))
        self.label_6.setText(_translate("OrbitOptimizeDialog", "Shift\n"
"Range"))
        self.it_b.setToolTip(_translate("OrbitOptimizeDialog", "Move the Handle Left"))
        self.it_b.setText(_translate("OrbitOptimizeDialog", "<"))
        self.label_itfrom.setText(_translate("OrbitOptimizeDialog", "2000-00-00"))
        self.it_ff.setToolTip(_translate("OrbitOptimizeDialog", "Shift Range to Right"))
        self.it_ff.setText(_translate("OrbitOptimizeDialog", ">>>"))
        self.label_2.setText(_translate("OrbitOptimizeDialog", "Tweak Handle"))
        self.label_initialtime.setText(_translate("OrbitOptimizeDialog", "Adjust Start Time"))
        self.groupBox_2.setTitle(_translate("OrbitOptimizeDialog", "Slider Defines"))
        self.radio_fd.setText(_translate("OrbitOptimizeDialog", "Flight Time"))
        self.radio_tt.setText(_translate("OrbitOptimizeDialog", "Arrival Time"))
        self.tt_fb.setToolTip(_translate("OrbitOptimizeDialog", "Shift Range to Left"))
        self.tt_fb.setText(_translate("OrbitOptimizeDialog", "<<<"))
        self.label_ttto.setText(_translate("OrbitOptimizeDialog", "500"))
        self.tt_b.setToolTip(_translate("OrbitOptimizeDialog", "Move the Handle Left"))
        self.tt_b.setText(_translate("OrbitOptimizeDialog", "<"))
        self.label_13.setText(_translate("OrbitOptimizeDialog", "Shift\n"
"Range"))
        self.label_7.setText(_translate("OrbitOptimizeDialog", "Flight Time (days)"))
        self.tt_ff.setToolTip(_translate("OrbitOptimizeDialog", "Sift Range to Right"))
        self.tt_ff.setText(_translate("OrbitOptimizeDialog", ">>>"))
        self.label_12.setText(_translate("OrbitOptimizeDialog", "Shift\n"
"Range"))
        self.label_ttfrom.setText(_translate("OrbitOptimizeDialog", "0"))
        self.tt_f.setToolTip(_translate("OrbitOptimizeDialog", "Move the Handle Right"))
        self.tt_f.setText(_translate("OrbitOptimizeDialog", ">"))
        self.label_4.setText(_translate("OrbitOptimizeDialog", "Tweak Handle"))
        self.label_8.setText(_translate("OrbitOptimizeDialog", "Arrival Time"))
        self.groupBox_ttsr.setTitle(_translate("OrbitOptimizeDialog", "Slider Range"))
        self.tt_wide.setText(_translate("OrbitOptimizeDialog", "Wide    (500 days)"))
        self.tt_narrow.setText(_translate("OrbitOptimizeDialog", "Narrow (100 days)"))
        self.label_5.setText(_translate("OrbitOptimizeDialog", "Adjust Flight Time"))
        self.sysMessage.setToolTip(_translate("OrbitOptimizeDialog", "System Messages"))
        self.whatIsOptimize.setPlaceholderText(_translate("OrbitOptimizeDialog", "whatIsOptimize"))

