# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flightreviewcontrol.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FlightReviewControl(object):
    def setupUi(self, FlightReviewControl):
        FlightReviewControl.setObjectName("FlightReviewControl")
        FlightReviewControl.resize(640, 216)
        FlightReviewControl.setMinimumSize(QtCore.QSize(640, 216))
        FlightReviewControl.setMaximumSize(QtCore.QSize(640, 216))
        FlightReviewControl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label = QtWidgets.QLabel(FlightReviewControl)
        self.label.setGeometry(QtCore.QRect(330, 50, 131, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.delta_t_edit = QtWidgets.QLineEdit(FlightReviewControl)
        self.delta_t_edit.setGeometry(QtCore.QRect(470, 50, 161, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.delta_t_edit.setFont(font)
        self.delta_t_edit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.delta_t_edit.setAcceptDrops(False)
        self.delta_t_edit.setToolTip("")
        self.delta_t_edit.setFrame(False)
        self.delta_t_edit.setReadOnly(True)
        self.delta_t_edit.setObjectName("delta_t_edit")
        self.fastbackward = QtWidgets.QPushButton(FlightReviewControl)
        self.fastbackward.setGeometry(QtCore.QRect(370, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastbackward.setFont(font)
        self.fastbackward.setAutoRepeat(True)
        self.fastbackward.setAutoDefault(False)
        self.fastbackward.setObjectName("fastbackward")
        self.backward = QtWidgets.QPushButton(FlightReviewControl)
        self.backward.setGeometry(QtCore.QRect(420, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.backward.setFont(font)
        self.backward.setAutoRepeat(True)
        self.backward.setAutoDefault(False)
        self.backward.setObjectName("backward")
        self.forward = QtWidgets.QPushButton(FlightReviewControl)
        self.forward.setGeometry(QtCore.QRect(470, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.forward.setFont(font)
        self.forward.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.forward.setAutoRepeat(True)
        self.forward.setAutoDefault(False)
        self.forward.setObjectName("forward")
        self.fastforward = QtWidgets.QPushButton(FlightReviewControl)
        self.fastforward.setGeometry(QtCore.QRect(520, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastforward.setFont(font)
        self.fastforward.setAutoRepeat(True)
        self.fastforward.setAutoDefault(False)
        self.fastforward.setObjectName("fastforward")
        self.timescale = QtWidgets.QSpinBox(FlightReviewControl)
        self.timescale.setGeometry(QtCore.QRect(580, 90, 51, 31))
        self.timescale.setMinimum(2)
        self.timescale.setMaximum(100)
        self.timescale.setSingleStep(1)
        self.timescale.setProperty("value", 10)
        self.timescale.setObjectName("timescale")
        self.label_2 = QtWidgets.QLabel(FlightReviewControl)
        self.label_2.setGeometry(QtCore.QRect(570, 72, 71, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(FlightReviewControl)
        self.label_6.setGeometry(QtCore.QRect(330, 10, 91, 16))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(FlightReviewControl)
        self.label_4.setGeometry(QtCore.QRect(330, 30, 91, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(FlightReviewControl)
        self.label_3.setGeometry(QtCore.QRect(50, 130, 201, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(FlightReviewControl)
        self.label_9.setGeometry(QtCore.QRect(250, 130, 191, 16))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(FlightReviewControl)
        self.label_10.setGeometry(QtCore.QRect(4, 150, 81, 16))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(FlightReviewControl)
        self.label_11.setGeometry(QtCore.QRect(4, 170, 81, 16))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(FlightReviewControl)
        self.label_12.setGeometry(QtCore.QRect(4, 190, 81, 16))
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(FlightReviewControl)
        self.label_14.setGeometry(QtCore.QRect(224, 150, 71, 16))
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(FlightReviewControl)
        self.label_15.setGeometry(QtCore.QRect(414, 150, 71, 16))
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(FlightReviewControl)
        self.label_16.setGeometry(QtCore.QRect(224, 170, 71, 16))
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(FlightReviewControl)
        self.label_17.setGeometry(QtCore.QRect(224, 190, 71, 16))
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(FlightReviewControl)
        self.label_18.setGeometry(QtCore.QRect(460, 130, 161, 16))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setWordWrap(False)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(FlightReviewControl)
        self.label_19.setGeometry(QtCore.QRect(360, 72, 211, 20))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setWordWrap(False)
        self.label_19.setObjectName("label_19")
        self.currenttime = QtWidgets.QLineEdit(FlightReviewControl)
        self.currenttime.setGeometry(QtCore.QRect(430, 30, 201, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.currenttime.setFont(font)
        self.currenttime.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.currenttime.setAcceptDrops(False)
        self.currenttime.setToolTip("")
        self.currenttime.setFrame(False)
        self.currenttime.setReadOnly(True)
        self.currenttime.setObjectName("currenttime")
        self.RVTvel = QtWidgets.QLineEdit(FlightReviewControl)
        self.RVTvel.setGeometry(QtCore.QRect(300, 149, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTvel.setFont(font)
        self.RVTvel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTvel.setToolTip("")
        self.RVTvel.setFrame(False)
        self.RVTvel.setReadOnly(True)
        self.RVTvel.setObjectName("RVTvel")
        self.RVTphi = QtWidgets.QLineEdit(FlightReviewControl)
        self.RVTphi.setGeometry(QtCore.QRect(300, 169, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTphi.setFont(font)
        self.RVTphi.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTphi.setToolTip("")
        self.RVTphi.setFrame(False)
        self.RVTphi.setReadOnly(True)
        self.RVTphi.setObjectName("RVTphi")
        self.RVTelv = QtWidgets.QLineEdit(FlightReviewControl)
        self.RVTelv.setGeometry(QtCore.QRect(300, 189, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTelv.setFont(font)
        self.RVTelv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTelv.setToolTip("")
        self.RVTelv.setFrame(False)
        self.RVTelv.setReadOnly(True)
        self.RVTelv.setObjectName("RVTelv")
        self.groupBox = QtWidgets.QGroupBox(FlightReviewControl)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 91, 111))
        self.groupBox.setObjectName("groupBox")
        self.tobarycenter = QtWidgets.QRadioButton(self.groupBox)
        self.tobarycenter.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.tobarycenter.setChecked(False)
        self.tobarycenter.setObjectName("tobarycenter")
        self.toprobe = QtWidgets.QRadioButton(self.groupBox)
        self.toprobe.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.toprobe.setChecked(True)
        self.toprobe.setObjectName("toprobe")
        self.totarget = QtWidgets.QRadioButton(self.groupBox)
        self.totarget.setGeometry(QtCore.QRect(10, 60, 81, 16))
        self.totarget.setObjectName("totarget")
        self.groupBox_3 = QtWidgets.QGroupBox(FlightReviewControl)
        self.groupBox_3.setGeometry(QtCore.QRect(110, 10, 131, 111))
        self.groupBox_3.setObjectName("groupBox_3")
        self.check_Ptrj = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_Ptrj.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.check_Ptrj.setChecked(True)
        self.check_Ptrj.setObjectName("check_Ptrj")
        self.showplanets = QtWidgets.QCheckBox(self.groupBox_3)
        self.showplanets.setGeometry(QtCore.QRect(10, 80, 121, 16))
        self.showplanets.setChecked(True)
        self.showplanets.setObjectName("showplanets")
        self.check_PKepler = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_PKepler.setGeometry(QtCore.QRect(10, 40, 121, 16))
        self.check_PKepler.setChecked(True)
        self.check_PKepler.setObjectName("check_PKepler")
        self.check_TKepler = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_TKepler.setGeometry(QtCore.QRect(10, 60, 121, 16))
        self.check_TKepler.setChecked(True)
        self.check_TKepler.setObjectName("check_TKepler")
        self.starttime = QtWidgets.QLineEdit(FlightReviewControl)
        self.starttime.setGeometry(QtCore.QRect(430, 10, 201, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.starttime.setFont(font)
        self.starttime.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.starttime.setAcceptDrops(False)
        self.starttime.setToolTip("")
        self.starttime.setFrame(False)
        self.starttime.setReadOnly(True)
        self.starttime.setObjectName("starttime")
        self.RPTrange = QtWidgets.QLineEdit(FlightReviewControl)
        self.RPTrange.setGeometry(QtCore.QRect(90, 149, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTrange.setFont(font)
        self.RPTrange.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTrange.setToolTip("")
        self.RPTrange.setFrame(False)
        self.RPTrange.setReadOnly(True)
        self.RPTrange.setObjectName("RPTrange")
        self.RPTphi = QtWidgets.QLineEdit(FlightReviewControl)
        self.RPTphi.setGeometry(QtCore.QRect(90, 169, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTphi.setFont(font)
        self.RPTphi.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTphi.setToolTip("")
        self.RPTphi.setFrame(False)
        self.RPTphi.setReadOnly(True)
        self.RPTphi.setObjectName("RPTphi")
        self.RPTelv = QtWidgets.QLineEdit(FlightReviewControl)
        self.RPTelv.setGeometry(QtCore.QRect(90, 189, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTelv.setFont(font)
        self.RPTelv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTelv.setToolTip("")
        self.RPTelv.setFrame(False)
        self.RPTelv.setReadOnly(True)
        self.RPTelv.setObjectName("RPTelv")
        self.LoSVvel = QtWidgets.QLineEdit(FlightReviewControl)
        self.LoSVvel.setGeometry(QtCore.QRect(490, 149, 101, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.LoSVvel.setFont(font)
        self.LoSVvel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LoSVvel.setToolTip("")
        self.LoSVvel.setFrame(False)
        self.LoSVvel.setReadOnly(True)
        self.LoSVvel.setObjectName("LoSVvel")
        self.sysMessage = QtWidgets.QPlainTextEdit(FlightReviewControl)
        self.sysMessage.setGeometry(QtCore.QRect(400, 176, 237, 37))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.sysMessage.setFont(font)
        self.sysMessage.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.sysMessage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sysMessage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sysMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.sysMessage.setLineWidth(0)
        self.sysMessage.setUndoRedoEnabled(False)
        self.sysMessage.setReadOnly(True)
        self.sysMessage.setMaximumBlockCount(20)
        self.sysMessage.setObjectName("sysMessage")
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
        self.sysMessage.raise_()

        self.retranslateUi(FlightReviewControl)
        QtCore.QMetaObject.connectSlotsByName(FlightReviewControl)
        FlightReviewControl.setTabOrder(self.tobarycenter, self.toprobe)
        FlightReviewControl.setTabOrder(self.toprobe, self.totarget)
        FlightReviewControl.setTabOrder(self.totarget, self.check_Ptrj)
        FlightReviewControl.setTabOrder(self.check_Ptrj, self.check_PKepler)
        FlightReviewControl.setTabOrder(self.check_PKepler, self.check_TKepler)
        FlightReviewControl.setTabOrder(self.check_TKepler, self.showplanets)
        FlightReviewControl.setTabOrder(self.showplanets, self.fastbackward)
        FlightReviewControl.setTabOrder(self.fastbackward, self.backward)
        FlightReviewControl.setTabOrder(self.backward, self.forward)
        FlightReviewControl.setTabOrder(self.forward, self.fastforward)
        FlightReviewControl.setTabOrder(self.fastforward, self.timescale)

    def retranslateUi(self, FlightReviewControl):
        _translate = QtCore.QCoreApplication.translate
        FlightReviewControl.setWindowTitle(_translate("FlightReviewControl", "Flight Review"))
        self.label.setText(_translate("FlightReviewControl", "Elapsed Time (days)"))
        self.fastbackward.setToolTip(_translate("FlightReviewControl", "Fast Backword"))
        self.fastbackward.setText(_translate("FlightReviewControl", "<<"))
        self.backward.setToolTip(_translate("FlightReviewControl", "Backward"))
        self.backward.setText(_translate("FlightReviewControl", "<"))
        self.forward.setToolTip(_translate("FlightReviewControl", "Forward"))
        self.forward.setText(_translate("FlightReviewControl", ">"))
        self.fastforward.setToolTip(_translate("FlightReviewControl", "Fast Forward"))
        self.fastforward.setText(_translate("FlightReviewControl", ">>"))
        self.timescale.setToolTip(_translate("FlightReviewControl", "Steps for FF and FB"))
        self.label_2.setText(_translate("FlightReviewControl", "Quickness"))
        self.label_6.setText(_translate("FlightReviewControl", "Start Time"))
        self.label_4.setText(_translate("FlightReviewControl", "Watching Time"))
        self.label_3.setText(_translate("FlightReviewControl", "Relative Position of Target"))
        self.label_9.setText(_translate("FlightReviewControl", "Relative Velocity of Target"))
        self.label_10.setText(_translate("FlightReviewControl", "distance (km)"))
        self.label_11.setText(_translate("FlightReviewControl", "phi (deg)"))
        self.label_12.setText(_translate("FlightReviewControl", "elv (deg)"))
        self.label_14.setText(_translate("FlightReviewControl", "vel (m/s)"))
        self.label_15.setText(_translate("FlightReviewControl", "vel (m/s)"))
        self.label_16.setText(_translate("FlightReviewControl", "phi (deg)"))
        self.label_17.setText(_translate("FlightReviewControl", "elv (deg)"))
        self.label_18.setText(_translate("FlightReviewControl", "Line of Sight Velocity"))
        self.label_19.setText(_translate("FlightReviewControl", "bkwd<<   Review Manipulator   >>fwd"))
        self.groupBox.setTitle(_translate("FlightReviewControl", "Look at"))
        self.tobarycenter.setToolTip(_translate("FlightReviewControl", "Solar System Barycenter"))
        self.tobarycenter.setText(_translate("FlightReviewControl", "SSB"))
        self.toprobe.setText(_translate("FlightReviewControl", "Probe"))
        self.totarget.setText(_translate("FlightReviewControl", "Target"))
        self.groupBox_3.setTitle(_translate("FlightReviewControl", "Show"))
        self.check_Ptrj.setText(_translate("FlightReviewControl", "Probe Trajectory"))
        self.showplanets.setText(_translate("FlightReviewControl", "Planets"))
        self.check_PKepler.setText(_translate("FlightReviewControl", "Probe Kepler Orbit"))
        self.check_TKepler.setText(_translate("FlightReviewControl", "Target Kepler Orbit"))
        self.sysMessage.setToolTip(_translate("FlightReviewControl", "System Messages"))

