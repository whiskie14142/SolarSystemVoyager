# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flightreviewcontrol.ui'
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

class Ui_FlightReviewControl(object):
    def setupUi(self, FlightReviewControl):
        FlightReviewControl.setObjectName(_fromUtf8("FlightReviewControl"))
        FlightReviewControl.resize(640, 211)
        self.label = QtGui.QLabel(FlightReviewControl)
        self.label.setGeometry(QtCore.QRect(370, 50, 51, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.delta_t_edit = QtGui.QLineEdit(FlightReviewControl)
        self.delta_t_edit.setGeometry(QtCore.QRect(430, 50, 201, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.delta_t_edit.setFont(font)
        self.delta_t_edit.setAcceptDrops(False)
        self.delta_t_edit.setToolTip(_fromUtf8(""))
        self.delta_t_edit.setFrame(False)
        self.delta_t_edit.setReadOnly(True)
        self.delta_t_edit.setObjectName(_fromUtf8("delta_t_edit"))
        self.fastbackward = QtGui.QPushButton(FlightReviewControl)
        self.fastbackward.setGeometry(QtCore.QRect(370, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastbackward.setFont(font)
        self.fastbackward.setAutoRepeat(True)
        self.fastbackward.setAutoDefault(False)
        self.fastbackward.setObjectName(_fromUtf8("fastbackward"))
        self.backward = QtGui.QPushButton(FlightReviewControl)
        self.backward.setGeometry(QtCore.QRect(420, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.backward.setFont(font)
        self.backward.setAutoRepeat(True)
        self.backward.setAutoDefault(False)
        self.backward.setObjectName(_fromUtf8("backward"))
        self.forward = QtGui.QPushButton(FlightReviewControl)
        self.forward.setGeometry(QtCore.QRect(470, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.forward.setFont(font)
        self.forward.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.forward.setAutoRepeat(True)
        self.forward.setAutoDefault(False)
        self.forward.setObjectName(_fromUtf8("forward"))
        self.fastforward = QtGui.QPushButton(FlightReviewControl)
        self.fastforward.setGeometry(QtCore.QRect(520, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastforward.setFont(font)
        self.fastforward.setAutoRepeat(True)
        self.fastforward.setAutoDefault(False)
        self.fastforward.setObjectName(_fromUtf8("fastforward"))
        self.timescale = QtGui.QSpinBox(FlightReviewControl)
        self.timescale.setGeometry(QtCore.QRect(580, 100, 51, 22))
        self.timescale.setMinimum(2)
        self.timescale.setMaximum(100)
        self.timescale.setSingleStep(1)
        self.timescale.setProperty("value", 10)
        self.timescale.setObjectName(_fromUtf8("timescale"))
        self.label_2 = QtGui.QLabel(FlightReviewControl)
        self.label_2.setGeometry(QtCore.QRect(580, 80, 41, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_6 = QtGui.QLabel(FlightReviewControl)
        self.label_6.setGeometry(QtCore.QRect(370, 10, 51, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_4 = QtGui.QLabel(FlightReviewControl)
        self.label_4.setGeometry(QtCore.QRect(370, 30, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_3 = QtGui.QLabel(FlightReviewControl)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 161, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_9 = QtGui.QLabel(FlightReviewControl)
        self.label_9.setGeometry(QtCore.QRect(237, 130, 191, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(FlightReviewControl)
        self.label_10.setGeometry(QtCore.QRect(10, 150, 71, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(FlightReviewControl)
        self.label_11.setGeometry(QtCore.QRect(10, 170, 61, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(FlightReviewControl)
        self.label_12.setGeometry(QtCore.QRect(10, 190, 61, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_14 = QtGui.QLabel(FlightReviewControl)
        self.label_14.setGeometry(QtCore.QRect(237, 150, 51, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(FlightReviewControl)
        self.label_15.setGeometry(QtCore.QRect(450, 150, 51, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(FlightReviewControl)
        self.label_16.setGeometry(QtCore.QRect(237, 170, 51, 16))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(FlightReviewControl)
        self.label_17.setGeometry(QtCore.QRect(237, 190, 51, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(FlightReviewControl)
        self.label_18.setGeometry(QtCore.QRect(450, 130, 181, 21))
        self.label_18.setWordWrap(False)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_19 = QtGui.QLabel(FlightReviewControl)
        self.label_19.setGeometry(QtCore.QRect(420, 80, 101, 16))
        self.label_19.setWordWrap(False)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.currenttime = QtGui.QLineEdit(FlightReviewControl)
        self.currenttime.setGeometry(QtCore.QRect(430, 30, 201, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.currenttime.setFont(font)
        self.currenttime.setAcceptDrops(False)
        self.currenttime.setToolTip(_fromUtf8(""))
        self.currenttime.setFrame(False)
        self.currenttime.setReadOnly(True)
        self.currenttime.setObjectName(_fromUtf8("currenttime"))
        self.RVTvel = QtGui.QLineEdit(FlightReviewControl)
        self.RVTvel.setGeometry(QtCore.QRect(292, 149, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RVTvel.setFont(font)
        self.RVTvel.setToolTip(_fromUtf8(""))
        self.RVTvel.setFrame(False)
        self.RVTvel.setReadOnly(True)
        self.RVTvel.setObjectName(_fromUtf8("RVTvel"))
        self.RVTphi = QtGui.QLineEdit(FlightReviewControl)
        self.RVTphi.setGeometry(QtCore.QRect(292, 169, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RVTphi.setFont(font)
        self.RVTphi.setToolTip(_fromUtf8(""))
        self.RVTphi.setFrame(False)
        self.RVTphi.setReadOnly(True)
        self.RVTphi.setObjectName(_fromUtf8("RVTphi"))
        self.RVTelv = QtGui.QLineEdit(FlightReviewControl)
        self.RVTelv.setGeometry(QtCore.QRect(292, 189, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RVTelv.setFont(font)
        self.RVTelv.setToolTip(_fromUtf8(""))
        self.RVTelv.setFrame(False)
        self.RVTelv.setReadOnly(True)
        self.RVTelv.setObjectName(_fromUtf8("RVTelv"))
        self.groupBox = QtGui.QGroupBox(FlightReviewControl)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 71, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.tobarycenter = QtGui.QRadioButton(self.groupBox)
        self.tobarycenter.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.tobarycenter.setChecked(False)
        self.tobarycenter.setObjectName(_fromUtf8("tobarycenter"))
        self.toprobe = QtGui.QRadioButton(self.groupBox)
        self.toprobe.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.toprobe.setChecked(True)
        self.toprobe.setObjectName(_fromUtf8("toprobe"))
        self.totarget = QtGui.QRadioButton(self.groupBox)
        self.totarget.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.totarget.setObjectName(_fromUtf8("totarget"))
        self.groupBox_3 = QtGui.QGroupBox(FlightReviewControl)
        self.groupBox_3.setGeometry(QtCore.QRect(90, 10, 151, 111))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.check_Ptrj = QtGui.QCheckBox(self.groupBox_3)
        self.check_Ptrj.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.check_Ptrj.setChecked(True)
        self.check_Ptrj.setObjectName(_fromUtf8("check_Ptrj"))
        self.showplanets = QtGui.QCheckBox(self.groupBox_3)
        self.showplanets.setGeometry(QtCore.QRect(10, 80, 121, 16))
        self.showplanets.setChecked(True)
        self.showplanets.setObjectName(_fromUtf8("showplanets"))
        self.check_PKepler = QtGui.QCheckBox(self.groupBox_3)
        self.check_PKepler.setGeometry(QtCore.QRect(10, 40, 121, 16))
        self.check_PKepler.setChecked(False)
        self.check_PKepler.setObjectName(_fromUtf8("check_PKepler"))
        self.check_TKepler = QtGui.QCheckBox(self.groupBox_3)
        self.check_TKepler.setGeometry(QtCore.QRect(10, 60, 121, 16))
        self.check_TKepler.setChecked(True)
        self.check_TKepler.setObjectName(_fromUtf8("check_TKepler"))
        self.starttime = QtGui.QLineEdit(FlightReviewControl)
        self.starttime.setGeometry(QtCore.QRect(430, 10, 201, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.starttime.setFont(font)
        self.starttime.setAcceptDrops(False)
        self.starttime.setToolTip(_fromUtf8(""))
        self.starttime.setFrame(False)
        self.starttime.setReadOnly(True)
        self.starttime.setObjectName(_fromUtf8("starttime"))
        self.RPTrange = QtGui.QLineEdit(FlightReviewControl)
        self.RPTrange.setGeometry(QtCore.QRect(83, 149, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RPTrange.setFont(font)
        self.RPTrange.setToolTip(_fromUtf8(""))
        self.RPTrange.setFrame(False)
        self.RPTrange.setReadOnly(True)
        self.RPTrange.setObjectName(_fromUtf8("RPTrange"))
        self.RPTphi = QtGui.QLineEdit(FlightReviewControl)
        self.RPTphi.setGeometry(QtCore.QRect(83, 169, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RPTphi.setFont(font)
        self.RPTphi.setToolTip(_fromUtf8(""))
        self.RPTphi.setFrame(False)
        self.RPTphi.setReadOnly(True)
        self.RPTphi.setObjectName(_fromUtf8("RPTphi"))
        self.RPTelv = QtGui.QLineEdit(FlightReviewControl)
        self.RPTelv.setGeometry(QtCore.QRect(83, 189, 141, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.RPTelv.setFont(font)
        self.RPTelv.setToolTip(_fromUtf8(""))
        self.RPTelv.setFrame(False)
        self.RPTelv.setReadOnly(True)
        self.RPTelv.setObjectName(_fromUtf8("RPTelv"))
        self.LoSVvel = QtGui.QLineEdit(FlightReviewControl)
        self.LoSVvel.setGeometry(QtCore.QRect(505, 149, 126, 18))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.LoSVvel.setFont(font)
        self.LoSVvel.setToolTip(_fromUtf8(""))
        self.LoSVvel.setFrame(False)
        self.LoSVvel.setReadOnly(True)
        self.LoSVvel.setObjectName(_fromUtf8("LoSVvel"))
        self.label_2.raise_()
        self.label.raise_()
        self.delta_t_edit.raise_()
        self.fastbackward.raise_()
        self.backward.raise_()
        self.forward.raise_()
        self.fastforward.raise_()
        self.timescale.raise_()
        self.label_6.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.label_19.raise_()
        self.currenttime.raise_()
        self.RVTvel.raise_()
        self.RVTphi.raise_()
        self.RVTelv.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.starttime.raise_()
        self.RPTrange.raise_()
        self.RPTphi.raise_()
        self.RPTelv.raise_()
        self.LoSVvel.raise_()

        self.retranslateUi(FlightReviewControl)
        QtCore.QMetaObject.connectSlotsByName(FlightReviewControl)
        FlightReviewControl.setTabOrder(self.tobarycenter, self.toprobe)
        FlightReviewControl.setTabOrder(self.toprobe, self.totarget)
        FlightReviewControl.setTabOrder(self.totarget, self.fastbackward)
        FlightReviewControl.setTabOrder(self.fastbackward, self.backward)
        FlightReviewControl.setTabOrder(self.backward, self.forward)
        FlightReviewControl.setTabOrder(self.forward, self.fastforward)
        FlightReviewControl.setTabOrder(self.fastforward, self.currenttime)
        FlightReviewControl.setTabOrder(self.currenttime, self.delta_t_edit)
        FlightReviewControl.setTabOrder(self.delta_t_edit, self.timescale)

    def retranslateUi(self, FlightReviewControl):
        FlightReviewControl.setWindowTitle(_translate("FlightReviewControl", "Flight Review", None))
        self.label.setText(_translate("FlightReviewControl", "DT(days)", None))
        self.fastbackward.setToolTip(_translate("FlightReviewControl", "Fast Backword", None))
        self.fastbackward.setText(_translate("FlightReviewControl", "<<", None))
        self.backward.setToolTip(_translate("FlightReviewControl", "Backward", None))
        self.backward.setText(_translate("FlightReviewControl", "<", None))
        self.forward.setToolTip(_translate("FlightReviewControl", "Forward", None))
        self.forward.setText(_translate("FlightReviewControl", ">", None))
        self.fastforward.setToolTip(_translate("FlightReviewControl", "Fast Forward", None))
        self.fastforward.setText(_translate("FlightReviewControl", ">>", None))
        self.timescale.setToolTip(_translate("FlightReviewControl", "Steps for FF and FB", None))
        self.label_2.setText(_translate("FlightReviewControl", "Hopping", None))
        self.label_6.setText(_translate("FlightReviewControl", "Start", None))
        self.label_4.setText(_translate("FlightReviewControl", "Seeing", None))
        self.label_3.setText(_translate("FlightReviewControl", "Relative Position of Target", None))
        self.label_9.setText(_translate("FlightReviewControl", "Relative Velocity of Target", None))
        self.label_10.setText(_translate("FlightReviewControl", "distance (km)", None))
        self.label_11.setText(_translate("FlightReviewControl", "phi (deg)", None))
        self.label_12.setText(_translate("FlightReviewControl", "elv (deg)", None))
        self.label_14.setText(_translate("FlightReviewControl", "vel (m/s)", None))
        self.label_15.setText(_translate("FlightReviewControl", "vel (m/s)", None))
        self.label_16.setText(_translate("FlightReviewControl", "phi (deg)", None))
        self.label_17.setText(_translate("FlightReviewControl", "elv (deg)", None))
        self.label_18.setText(_translate("FlightReviewControl", "Line of Sight Velocity (departing)", None))
        self.label_19.setText(_translate("FlightReviewControl", "Review Manipulator", None))
        self.groupBox.setTitle(_translate("FlightReviewControl", "Look at", None))
        self.tobarycenter.setToolTip(_translate("FlightReviewControl", "Solar System Barycenter", None))
        self.tobarycenter.setText(_translate("FlightReviewControl", "SSB", None))
        self.toprobe.setText(_translate("FlightReviewControl", "Probe", None))
        self.totarget.setText(_translate("FlightReviewControl", "Target", None))
        self.groupBox_3.setTitle(_translate("FlightReviewControl", "Show", None))
        self.check_Ptrj.setText(_translate("FlightReviewControl", "Probe Trajectory", None))
        self.showplanets.setText(_translate("FlightReviewControl", "Planets", None))
        self.check_PKepler.setText(_translate("FlightReviewControl", "Probe Kepler Orbit", None))
        self.check_TKepler.setText(_translate("FlightReviewControl", "Target Kepler Orbit", None))

