# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orbitoptimizedialog.ui'
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

class Ui_OrbitOptimizeDialog(object):
    def setupUi(self, OrbitOptimizeDialog):
        OrbitOptimizeDialog.setObjectName(_fromUtf8("OrbitOptimizeDialog"))
        OrbitOptimizeDialog.setWindowModality(QtCore.Qt.WindowModal)
        OrbitOptimizeDialog.resize(600, 628)
        OrbitOptimizeDialog.setModal(True)
        self.starttime = QtGui.QLabel(OrbitOptimizeDialog)
        self.starttime.setGeometry(QtCore.QRect(432, 10, 201, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.starttime.setFont(font)
        self.starttime.setText(_fromUtf8(""))
        self.starttime.setObjectName(_fromUtf8("starttime"))
        self.label_3 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_3.setGeometry(QtCore.QRect(60, 450, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_9 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_9.setGeometry(QtCore.QRect(220, 450, 181, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_14 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_14.setGeometry(QtCore.QRect(230, 470, 41, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_16 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_16.setGeometry(QtCore.QRect(230, 490, 41, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_17.setGeometry(QtCore.QRect(230, 510, 41, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.terminalRV_cur = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.terminalRV_cur.setGeometry(QtCore.QRect(280, 470, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.terminalRV_cur.setFont(font)
        self.terminalRV_cur.setToolTip(_fromUtf8(""))
        self.terminalRV_cur.setFrame(False)
        self.terminalRV_cur.setReadOnly(True)
        self.terminalRV_cur.setObjectName(_fromUtf8("terminalRV_cur"))
        self.terminalRV_min = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.terminalRV_min.setGeometry(QtCore.QRect(280, 490, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.terminalRV_min.setFont(font)
        self.terminalRV_min.setToolTip(_fromUtf8(""))
        self.terminalRV_min.setFrame(False)
        self.terminalRV_min.setReadOnly(True)
        self.terminalRV_min.setObjectName(_fromUtf8("terminalRV_min"))
        self.terminalRV_max = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.terminalRV_max.setGeometry(QtCore.QRect(280, 510, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.terminalRV_max.setFont(font)
        self.terminalRV_max.setToolTip(_fromUtf8(""))
        self.terminalRV_max.setFrame(False)
        self.terminalRV_max.setReadOnly(True)
        self.terminalRV_max.setObjectName(_fromUtf8("terminalRV_max"))
        self.groupBox = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 91, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.tobarycenter = QtGui.QRadioButton(self.groupBox)
        self.tobarycenter.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.tobarycenter.setChecked(True)
        self.tobarycenter.setObjectName(_fromUtf8("tobarycenter"))
        self.toprobe = QtGui.QRadioButton(self.groupBox)
        self.toprobe.setEnabled(False)
        self.toprobe.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.toprobe.setChecked(False)
        self.toprobe.setObjectName(_fromUtf8("toprobe"))
        self.totarget = QtGui.QRadioButton(self.groupBox)
        self.totarget.setEnabled(False)
        self.totarget.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.totarget.setObjectName(_fromUtf8("totarget"))
        self.groupBox_3 = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(120, 10, 151, 111))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.check_Ptrj = QtGui.QCheckBox(self.groupBox_3)
        self.check_Ptrj.setEnabled(True)
        self.check_Ptrj.setGeometry(QtCore.QRect(10, 80, 131, 16))
        self.check_Ptrj.setChecked(False)
        self.check_Ptrj.setObjectName(_fromUtf8("check_Ptrj"))
        self.check_Ppred = QtGui.QCheckBox(self.groupBox_3)
        self.check_Ppred.setGeometry(QtCore.QRect(10, 60, 131, 16))
        self.check_Ppred.setChecked(True)
        self.check_Ppred.setObjectName(_fromUtf8("check_Ppred"))
        self.check_TKepler = QtGui.QCheckBox(self.groupBox_3)
        self.check_TKepler.setGeometry(QtCore.QRect(10, 40, 131, 16))
        self.check_TKepler.setChecked(True)
        self.check_TKepler.setObjectName(_fromUtf8("check_TKepler"))
        self.check_orgorb = QtGui.QCheckBox(self.groupBox_3)
        self.check_orgorb.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.check_orgorb.setChecked(True)
        self.check_orgorb.setObjectName(_fromUtf8("check_orgorb"))
        self.label_18 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_18.setGeometry(QtCore.QRect(40, 490, 41, 16))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.initialDV_min = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.initialDV_min.setGeometry(QtCore.QRect(90, 490, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.initialDV_min.setFont(font)
        self.initialDV_min.setToolTip(_fromUtf8(""))
        self.initialDV_min.setFrame(False)
        self.initialDV_min.setReadOnly(True)
        self.initialDV_min.setObjectName(_fromUtf8("initialDV_min"))
        self.initialDV_cur = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.initialDV_cur.setGeometry(QtCore.QRect(90, 470, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.initialDV_cur.setFont(font)
        self.initialDV_cur.setToolTip(_fromUtf8(""))
        self.initialDV_cur.setFrame(False)
        self.initialDV_cur.setReadOnly(True)
        self.initialDV_cur.setObjectName(_fromUtf8("initialDV_cur"))
        self.label_15 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_15.setGeometry(QtCore.QRect(40, 470, 41, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_19 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_19.setGeometry(QtCore.QRect(40, 510, 41, 16))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.initialDV_max = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.initialDV_max.setGeometry(QtCore.QRect(90, 510, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.initialDV_max.setFont(font)
        self.initialDV_max.setToolTip(_fromUtf8(""))
        self.initialDV_max.setFrame(False)
        self.initialDV_max.setReadOnly(True)
        self.initialDV_max.setObjectName(_fromUtf8("initialDV_max"))
        self.finishbutton = QtGui.QPushButton(OrbitOptimizeDialog)
        self.finishbutton.setGeometry(QtCore.QRect(330, 590, 121, 23))
        self.finishbutton.setAutoDefault(False)
        self.finishbutton.setObjectName(_fromUtf8("finishbutton"))
        self.cancelbutton = QtGui.QPushButton(OrbitOptimizeDialog)
        self.cancelbutton.setGeometry(QtCore.QRect(480, 590, 91, 23))
        self.cancelbutton.setAutoDefault(False)
        self.cancelbutton.setObjectName(_fromUtf8("cancelbutton"))
        self.groupBox_2 = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 10, 291, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.radio_fd = QtGui.QRadioButton(self.groupBox_2)
        self.radio_fd.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.radio_fd.setChecked(True)
        self.radio_fd.setObjectName(_fromUtf8("radio_fd"))
        self.radio_tt = QtGui.QRadioButton(self.groupBox_2)
        self.radio_tt.setGeometry(QtCore.QRect(140, 20, 101, 16))
        self.radio_tt.setChecked(False)
        self.radio_tt.setObjectName(_fromUtf8("radio_tt"))
        self.box_initialfix = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.box_initialfix.setEnabled(True)
        self.box_initialfix.setGeometry(QtCore.QRect(300, 70, 291, 51))
        self.box_initialfix.setObjectName(_fromUtf8("box_initialfix"))
        self.fixed_to_ct = QtGui.QCheckBox(self.box_initialfix)
        self.fixed_to_ct.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.fixed_to_ct.setChecked(False)
        self.fixed_to_ct.setObjectName(_fromUtf8("fixed_to_ct"))
        self.box_initialtime = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.box_initialtime.setGeometry(QtCore.QRect(10, 150, 581, 121))
        self.box_initialtime.setObjectName(_fromUtf8("box_initialtime"))
        self.label_6 = QtGui.QLabel(self.box_initialtime)
        self.label_6.setGeometry(QtCore.QRect(220, 13, 41, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.sl_inittime = QtGui.QSlider(self.box_initialtime)
        self.sl_inittime.setGeometry(QtCore.QRect(30, 60, 511, 22))
        self.sl_inittime.setMinimum(0)
        self.sl_inittime.setMaximum(500)
        self.sl_inittime.setOrientation(QtCore.Qt.Horizontal)
        self.sl_inittime.setObjectName(_fromUtf8("sl_inittime"))
        self.label_it = QtGui.QLabel(self.box_initialtime)
        self.label_it.setGeometry(QtCore.QRect(280, 90, 81, 20))
        self.label_it.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_it.setObjectName(_fromUtf8("label_it"))
        self.initialtime = QtGui.QLineEdit(self.box_initialtime)
        self.initialtime.setGeometry(QtCore.QRect(370, 90, 191, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.initialtime.setFont(font)
        self.initialtime.setAcceptDrops(False)
        self.initialtime.setToolTip(_fromUtf8(""))
        self.initialtime.setFrame(False)
        self.initialtime.setReadOnly(True)
        self.initialtime.setObjectName(_fromUtf8("initialtime"))
        self.itdeviation = QtGui.QLineEdit(self.box_initialtime)
        self.itdeviation.setGeometry(QtCore.QRect(180, 90, 81, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.itdeviation.setFont(font)
        self.itdeviation.setAcceptDrops(False)
        self.itdeviation.setToolTip(_fromUtf8(""))
        self.itdeviation.setFrame(False)
        self.itdeviation.setReadOnly(True)
        self.itdeviation.setObjectName(_fromUtf8("itdeviation"))
        self.label_10 = QtGui.QLabel(self.box_initialtime)
        self.label_10.setGeometry(QtCore.QRect(120, 90, 51, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.it_fb = QtGui.QPushButton(self.box_initialtime)
        self.it_fb.setGeometry(QtCore.QRect(120, 28, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.it_fb.setFont(font)
        self.it_fb.setAutoRepeat(True)
        self.it_fb.setAutoDefault(False)
        self.it_fb.setObjectName(_fromUtf8("it_fb"))
        self.it_ff = QtGui.QPushButton(self.box_initialtime)
        self.it_ff.setGeometry(QtCore.QRect(330, 28, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.it_ff.setFont(font)
        self.it_ff.setAutoRepeat(True)
        self.it_ff.setAutoDefault(False)
        self.it_ff.setObjectName(_fromUtf8("it_ff"))
        self.it_wide = QtGui.QRadioButton(self.box_initialtime)
        self.it_wide.setGeometry(QtCore.QRect(410, 20, 71, 16))
        self.it_wide.setChecked(True)
        self.it_wide.setObjectName(_fromUtf8("it_wide"))
        self.it_narrow = QtGui.QRadioButton(self.box_initialtime)
        self.it_narrow.setGeometry(QtCore.QRect(410, 40, 71, 16))
        self.it_narrow.setChecked(False)
        self.it_narrow.setObjectName(_fromUtf8("it_narrow"))
        self.label_itfrom = QtGui.QLabel(self.box_initialtime)
        self.label_itfrom.setGeometry(QtCore.QRect(20, 40, 31, 16))
        self.label_itfrom.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_itfrom.setObjectName(_fromUtf8("label_itfrom"))
        self.label_itto = QtGui.QLabel(self.box_initialtime)
        self.label_itto.setGeometry(QtCore.QRect(525, 40, 31, 16))
        self.label_itto.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_itto.setObjectName(_fromUtf8("label_itto"))
        self.it_center = QtGui.QLabel(self.box_initialtime)
        self.it_center.setGeometry(QtCore.QRect(160, 30, 161, 21))
        self.it_center.setFrameShape(QtGui.QFrame.NoFrame)
        self.it_center.setText(_fromUtf8(""))
        self.it_center.setAlignment(QtCore.Qt.AlignCenter)
        self.it_center.setObjectName(_fromUtf8("it_center"))
        self.groupBox_6 = QtGui.QGroupBox(OrbitOptimizeDialog)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 300, 581, 121))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.sl_duration = QtGui.QSlider(self.groupBox_6)
        self.sl_duration.setGeometry(QtCore.QRect(30, 60, 511, 22))
        self.sl_duration.setMinimum(0)
        self.sl_duration.setMaximum(500)
        self.sl_duration.setOrientation(QtCore.Qt.Horizontal)
        self.sl_duration.setObjectName(_fromUtf8("sl_duration"))
        self.label_7 = QtGui.QLabel(self.groupBox_6)
        self.label_7.setGeometry(QtCore.QRect(60, 90, 121, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.duration = QtGui.QLineEdit(self.groupBox_6)
        self.duration.setGeometry(QtCore.QRect(180, 90, 81, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.duration.setFont(font)
        self.duration.setAcceptDrops(False)
        self.duration.setToolTip(_fromUtf8(""))
        self.duration.setFrame(False)
        self.duration.setReadOnly(True)
        self.duration.setObjectName(_fromUtf8("duration"))
        self.label_8 = QtGui.QLabel(self.groupBox_6)
        self.label_8.setGeometry(QtCore.QRect(300, 90, 71, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.terminaltime = QtGui.QLineEdit(self.groupBox_6)
        self.terminaltime.setGeometry(QtCore.QRect(370, 90, 191, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.terminaltime.setFont(font)
        self.terminaltime.setAcceptDrops(False)
        self.terminaltime.setToolTip(_fromUtf8(""))
        self.terminaltime.setFrame(False)
        self.terminaltime.setReadOnly(True)
        self.terminaltime.setObjectName(_fromUtf8("terminaltime"))
        self.tt_fb = QtGui.QPushButton(self.groupBox_6)
        self.tt_fb.setGeometry(QtCore.QRect(120, 28, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tt_fb.setFont(font)
        self.tt_fb.setAutoRepeat(True)
        self.tt_fb.setAutoDefault(False)
        self.tt_fb.setObjectName(_fromUtf8("tt_fb"))
        self.tt_narrow = QtGui.QRadioButton(self.groupBox_6)
        self.tt_narrow.setGeometry(QtCore.QRect(410, 40, 71, 16))
        self.tt_narrow.setChecked(False)
        self.tt_narrow.setObjectName(_fromUtf8("tt_narrow"))
        self.label_ttto = QtGui.QLabel(self.groupBox_6)
        self.label_ttto.setGeometry(QtCore.QRect(525, 40, 31, 16))
        self.label_ttto.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_ttto.setObjectName(_fromUtf8("label_ttto"))
        self.tt_ff = QtGui.QPushButton(self.groupBox_6)
        self.tt_ff.setGeometry(QtCore.QRect(330, 28, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tt_ff.setFont(font)
        self.tt_ff.setAutoRepeat(True)
        self.tt_ff.setAutoDefault(False)
        self.tt_ff.setObjectName(_fromUtf8("tt_ff"))
        self.tt_wide = QtGui.QRadioButton(self.groupBox_6)
        self.tt_wide.setGeometry(QtCore.QRect(410, 20, 71, 16))
        self.tt_wide.setChecked(True)
        self.tt_wide.setObjectName(_fromUtf8("tt_wide"))
        self.label_11 = QtGui.QLabel(self.groupBox_6)
        self.label_11.setGeometry(QtCore.QRect(220, 13, 41, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_ttfrom = QtGui.QLabel(self.groupBox_6)
        self.label_ttfrom.setGeometry(QtCore.QRect(20, 40, 31, 16))
        self.label_ttfrom.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_ttfrom.setObjectName(_fromUtf8("label_ttfrom"))
        self.tt_center = QtGui.QLabel(self.groupBox_6)
        self.tt_center.setGeometry(QtCore.QRect(160, 30, 161, 21))
        self.tt_center.setFrameShape(QtGui.QFrame.NoFrame)
        self.tt_center.setText(_fromUtf8(""))
        self.tt_center.setAlignment(QtCore.Qt.AlignCenter)
        self.tt_center.setObjectName(_fromUtf8("tt_center"))
        self.label = QtGui.QLabel(OrbitOptimizeDialog)
        self.label.setGeometry(QtCore.QRect(430, 450, 121, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_20 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_20.setGeometry(QtCore.QRect(420, 490, 41, 16))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.totalDV_min = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.totalDV_min.setGeometry(QtCore.QRect(470, 489, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.totalDV_min.setFont(font)
        self.totalDV_min.setToolTip(_fromUtf8(""))
        self.totalDV_min.setFrame(False)
        self.totalDV_min.setReadOnly(True)
        self.totalDV_min.setObjectName(_fromUtf8("totalDV_min"))
        self.totalDV_max = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.totalDV_max.setGeometry(QtCore.QRect(470, 509, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.totalDV_max.setFont(font)
        self.totalDV_max.setToolTip(_fromUtf8(""))
        self.totalDV_max.setFrame(False)
        self.totalDV_max.setReadOnly(True)
        self.totalDV_max.setObjectName(_fromUtf8("totalDV_max"))
        self.label_21 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_21.setGeometry(QtCore.QRect(420, 510, 41, 16))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.totalDV_cur = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.totalDV_cur.setGeometry(QtCore.QRect(470, 469, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.totalDV_cur.setFont(font)
        self.totalDV_cur.setToolTip(_fromUtf8(""))
        self.totalDV_cur.setFrame(False)
        self.totalDV_cur.setReadOnly(True)
        self.totalDV_cur.setObjectName(_fromUtf8("totalDV_cur"))
        self.label_22 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_22.setGeometry(QtCore.QRect(420, 470, 41, 16))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.clearstat = QtGui.QPushButton(OrbitOptimizeDialog)
        self.clearstat.setGeometry(QtCore.QRect(480, 540, 91, 23))
        self.clearstat.setAutoDefault(False)
        self.clearstat.setObjectName(_fromUtf8("clearstat"))
        self.idv_phi = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.idv_phi.setGeometry(QtCore.QRect(90, 540, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.idv_phi.setFont(font)
        self.idv_phi.setToolTip(_fromUtf8(""))
        self.idv_phi.setFrame(False)
        self.idv_phi.setReadOnly(True)
        self.idv_phi.setObjectName(_fromUtf8("idv_phi"))
        self.idv_elv = QtGui.QLineEdit(OrbitOptimizeDialog)
        self.idv_elv.setGeometry(QtCore.QRect(90, 560, 91, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.idv_elv.setFont(font)
        self.idv_elv.setToolTip(_fromUtf8(""))
        self.idv_elv.setFrame(False)
        self.idv_elv.setReadOnly(True)
        self.idv_elv.setObjectName(_fromUtf8("idv_elv"))
        self.label_23 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_23.setGeometry(QtCore.QRect(40, 540, 51, 16))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(OrbitOptimizeDialog)
        self.label_24.setGeometry(QtCore.QRect(40, 560, 51, 16))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.reopenbutton = QtGui.QPushButton(OrbitOptimizeDialog)
        self.reopenbutton.setGeometry(QtCore.QRect(30, 590, 91, 23))
        self.reopenbutton.setAutoDefault(False)
        self.reopenbutton.setObjectName(_fromUtf8("reopenbutton"))
        self.box_initialtime.raise_()
        self.starttime.raise_()
        self.label_3.raise_()
        self.label_9.raise_()
        self.label_14.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.terminalRV_cur.raise_()
        self.terminalRV_min.raise_()
        self.terminalRV_max.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.label_18.raise_()
        self.initialDV_min.raise_()
        self.initialDV_cur.raise_()
        self.label_15.raise_()
        self.label_19.raise_()
        self.initialDV_max.raise_()
        self.finishbutton.raise_()
        self.cancelbutton.raise_()
        self.groupBox_2.raise_()
        self.box_initialfix.raise_()
        self.groupBox_6.raise_()
        self.label.raise_()
        self.label_20.raise_()
        self.totalDV_min.raise_()
        self.totalDV_max.raise_()
        self.label_21.raise_()
        self.totalDV_cur.raise_()
        self.label_22.raise_()
        self.clearstat.raise_()
        self.idv_phi.raise_()
        self.idv_elv.raise_()
        self.label_23.raise_()
        self.label_24.raise_()
        self.reopenbutton.raise_()

        self.retranslateUi(OrbitOptimizeDialog)
        QtCore.QMetaObject.connectSlotsByName(OrbitOptimizeDialog)
        OrbitOptimizeDialog.setTabOrder(self.tobarycenter, self.toprobe)
        OrbitOptimizeDialog.setTabOrder(self.toprobe, self.totarget)

    def retranslateUi(self, OrbitOptimizeDialog):
        OrbitOptimizeDialog.setWindowTitle(_translate("OrbitOptimizeDialog", "Start Optimize Assistant", None))
        self.starttime.setToolTip(_translate("OrbitOptimizeDialog", "Start time", None))
        self.label_3.setText(_translate("OrbitOptimizeDialog", "Initial Delta-V (m/s)", None))
        self.label_9.setText(_translate("OrbitOptimizeDialog", "Terminal Relative Velocity (m/s)", None))
        self.label_14.setText(_translate("OrbitOptimizeDialog", "Current", None))
        self.label_16.setText(_translate("OrbitOptimizeDialog", "Min.", None))
        self.label_17.setText(_translate("OrbitOptimizeDialog", "Max.", None))
        self.groupBox.setTitle(_translate("OrbitOptimizeDialog", "Look at", None))
        self.tobarycenter.setToolTip(_translate("OrbitOptimizeDialog", "Solar System Barycenter", None))
        self.tobarycenter.setText(_translate("OrbitOptimizeDialog", "SSB", None))
        self.toprobe.setText(_translate("OrbitOptimizeDialog", "Probe", None))
        self.totarget.setText(_translate("OrbitOptimizeDialog", "Target", None))
        self.groupBox_3.setTitle(_translate("OrbitOptimizeDialog", "Show Orbit", None))
        self.check_Ptrj.setText(_translate("OrbitOptimizeDialog", "Probe Trajectory", None))
        self.check_Ppred.setText(_translate("OrbitOptimizeDialog", "Probe Predicted", None))
        self.check_TKepler.setText(_translate("OrbitOptimizeDialog", "Target", None))
        self.check_orgorb.setText(_translate("OrbitOptimizeDialog", "Space Base", None))
        self.label_18.setText(_translate("OrbitOptimizeDialog", "Min.", None))
        self.label_15.setText(_translate("OrbitOptimizeDialog", "Current", None))
        self.label_19.setText(_translate("OrbitOptimizeDialog", "Max.", None))
        self.finishbutton.setText(_translate("OrbitOptimizeDialog", "Finish and Apply", None))
        self.cancelbutton.setText(_translate("OrbitOptimizeDialog", "Cancel", None))
        self.groupBox_2.setTitle(_translate("OrbitOptimizeDialog", "Flight Duration is Arranged by", None))
        self.radio_fd.setText(_translate("OrbitOptimizeDialog", "Flight Duration", None))
        self.radio_tt.setText(_translate("OrbitOptimizeDialog", "Arrival Time", None))
        self.box_initialfix.setTitle(_translate("OrbitOptimizeDialog", "Maneuver Time is", None))
        self.fixed_to_ct.setText(_translate("OrbitOptimizeDialog", "Fixed to Current Time", None))
        self.box_initialtime.setTitle(_translate("OrbitOptimizeDialog", "Arrange Start Time", None))
        self.label_6.setText(_translate("OrbitOptimizeDialog", "Center", None))
        self.label_it.setText(_translate("OrbitOptimizeDialog", "Start Time:", None))
        self.label_10.setText(_translate("OrbitOptimizeDialog", "Deviation:", None))
        self.it_fb.setText(_translate("OrbitOptimizeDialog", "<<", None))
        self.it_ff.setText(_translate("OrbitOptimizeDialog", ">>", None))
        self.it_wide.setText(_translate("OrbitOptimizeDialog", "Wide ", None))
        self.it_narrow.setText(_translate("OrbitOptimizeDialog", "Narrow", None))
        self.label_itfrom.setText(_translate("OrbitOptimizeDialog", "-250", None))
        self.label_itto.setText(_translate("OrbitOptimizeDialog", "+250", None))
        self.groupBox_6.setTitle(_translate("OrbitOptimizeDialog", "Arrange Flight Duration", None))
        self.label_7.setText(_translate("OrbitOptimizeDialog", "Flight Duration (days):", None))
        self.label_8.setText(_translate("OrbitOptimizeDialog", "Arrival Time:", None))
        self.tt_fb.setText(_translate("OrbitOptimizeDialog", "<<", None))
        self.tt_narrow.setText(_translate("OrbitOptimizeDialog", "Narrow", None))
        self.label_ttto.setText(_translate("OrbitOptimizeDialog", "500", None))
        self.tt_ff.setText(_translate("OrbitOptimizeDialog", ">>", None))
        self.tt_wide.setText(_translate("OrbitOptimizeDialog", "Wide ", None))
        self.label_11.setText(_translate("OrbitOptimizeDialog", "Center", None))
        self.label_ttfrom.setText(_translate("OrbitOptimizeDialog", "0", None))
        self.label.setText(_translate("OrbitOptimizeDialog", "Total DV (IDV + TRV)", None))
        self.label_20.setText(_translate("OrbitOptimizeDialog", "Min.", None))
        self.label_21.setText(_translate("OrbitOptimizeDialog", "Max.", None))
        self.label_22.setText(_translate("OrbitOptimizeDialog", "Current", None))
        self.clearstat.setText(_translate("OrbitOptimizeDialog", "Clear Statistics", None))
        self.label_23.setText(_translate("OrbitOptimizeDialog", "phi (deg)", None))
        self.label_24.setText(_translate("OrbitOptimizeDialog", "elv (deg)", None))
        self.reopenbutton.setText(_translate("OrbitOptimizeDialog", "Show Orbit", None))

