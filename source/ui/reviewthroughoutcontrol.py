# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reviewthroughoutcontrol.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReviewThroughoutControl(object):
    def setupUi(self, ReviewThroughoutControl):
        ReviewThroughoutControl.setObjectName("ReviewThroughoutControl")
        ReviewThroughoutControl.resize(640, 216)
        ReviewThroughoutControl.setMinimumSize(QtCore.QSize(640, 216))
        ReviewThroughoutControl.setMaximumSize(QtCore.QSize(640, 216))
        self.label = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label.setGeometry(QtCore.QRect(350, 50, 111, 16))
        self.label.setObjectName("label")
        self.delta_t_edit = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.delta_t_edit.setGeometry(QtCore.QRect(470, 50, 161, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.delta_t_edit.setFont(font)
        self.delta_t_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.delta_t_edit.setAcceptDrops(False)
        self.delta_t_edit.setToolTip("")
        self.delta_t_edit.setFrame(False)
        self.delta_t_edit.setReadOnly(True)
        self.delta_t_edit.setObjectName("delta_t_edit")
        self.fastbackward = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.fastbackward.setGeometry(QtCore.QRect(350, 100, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastbackward.setFont(font)
        self.fastbackward.setAutoRepeat(True)
        self.fastbackward.setAutoDefault(False)
        self.fastbackward.setObjectName("fastbackward")
        self.backward = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.backward.setGeometry(QtCore.QRect(390, 100, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.backward.setFont(font)
        self.backward.setAutoRepeat(True)
        self.backward.setAutoDefault(False)
        self.backward.setObjectName("backward")
        self.forward = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.forward.setGeometry(QtCore.QRect(430, 100, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.forward.setFont(font)
        self.forward.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.forward.setAutoRepeat(True)
        self.forward.setAutoDefault(False)
        self.forward.setObjectName("forward")
        self.fastforward = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.fastforward.setGeometry(QtCore.QRect(470, 100, 31, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastforward.setFont(font)
        self.fastforward.setAutoRepeat(True)
        self.fastforward.setAutoDefault(False)
        self.fastforward.setObjectName("fastforward")
        self.timescale = QtWidgets.QSpinBox(ReviewThroughoutControl)
        self.timescale.setGeometry(QtCore.QRect(580, 100, 51, 22))
        self.timescale.setMinimum(2)
        self.timescale.setMaximum(100)
        self.timescale.setSingleStep(1)
        self.timescale.setProperty("value", 10)
        self.timescale.setObjectName("timescale")
        self.label_2 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_2.setGeometry(QtCore.QRect(580, 80, 41, 20))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_6.setGeometry(QtCore.QRect(350, 10, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_4.setGeometry(QtCore.QRect(350, 30, 77, 16))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 161, 16))
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_9.setGeometry(QtCore.QRect(237, 130, 191, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_10.setGeometry(QtCore.QRect(10, 150, 71, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_11.setGeometry(QtCore.QRect(10, 170, 61, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_12.setGeometry(QtCore.QRect(10, 190, 61, 16))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_14.setGeometry(QtCore.QRect(237, 150, 51, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_15.setGeometry(QtCore.QRect(450, 150, 51, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_16.setGeometry(QtCore.QRect(237, 170, 51, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_17.setGeometry(QtCore.QRect(237, 190, 51, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_18.setGeometry(QtCore.QRect(450, 130, 181, 21))
        self.label_18.setWordWrap(False)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(ReviewThroughoutControl)
        self.label_19.setGeometry(QtCore.QRect(380, 80, 111, 20))
        self.label_19.setWordWrap(False)
        self.label_19.setObjectName("label_19")
        self.currenttime = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.currenttime.setGeometry(QtCore.QRect(430, 30, 201, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.currenttime.setFont(font)
        self.currenttime.setFocusPolicy(QtCore.Qt.NoFocus)
        self.currenttime.setAcceptDrops(False)
        self.currenttime.setToolTip("")
        self.currenttime.setFrame(False)
        self.currenttime.setReadOnly(True)
        self.currenttime.setObjectName("currenttime")
        self.RVTvel = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RVTvel.setGeometry(QtCore.QRect(292, 149, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTvel.setFont(font)
        self.RVTvel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RVTvel.setToolTip("")
        self.RVTvel.setFrame(False)
        self.RVTvel.setReadOnly(True)
        self.RVTvel.setObjectName("RVTvel")
        self.RVTphi = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RVTphi.setGeometry(QtCore.QRect(292, 169, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTphi.setFont(font)
        self.RVTphi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RVTphi.setToolTip("")
        self.RVTphi.setFrame(False)
        self.RVTphi.setReadOnly(True)
        self.RVTphi.setObjectName("RVTphi")
        self.RVTelv = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RVTelv.setGeometry(QtCore.QRect(292, 189, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTelv.setFont(font)
        self.RVTelv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RVTelv.setToolTip("")
        self.RVTelv.setFrame(False)
        self.RVTelv.setReadOnly(True)
        self.RVTelv.setObjectName("RVTelv")
        self.groupBox = QtWidgets.QGroupBox(ReviewThroughoutControl)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 71, 111))
        self.groupBox.setObjectName("groupBox")
        self.tobarycenter = QtWidgets.QRadioButton(self.groupBox)
        self.tobarycenter.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.tobarycenter.setChecked(False)
        self.tobarycenter.setObjectName("tobarycenter")
        self.toprobe = QtWidgets.QRadioButton(self.groupBox)
        self.toprobe.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.toprobe.setChecked(True)
        self.toprobe.setObjectName("toprobe")
        self.totarget = QtWidgets.QRadioButton(self.groupBox)
        self.totarget.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.totarget.setObjectName("totarget")
        self.previousman = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.previousman.setGeometry(QtCore.QRect(290, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.previousman.setFont(font)
        self.previousman.setAutoRepeat(True)
        self.previousman.setAutoDefault(False)
        self.previousman.setObjectName("previousman")
        self.nextman = QtWidgets.QPushButton(ReviewThroughoutControl)
        self.nextman.setGeometry(QtCore.QRect(520, 100, 41, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nextman.setFont(font)
        self.nextman.setAutoRepeat(True)
        self.nextman.setAutoDefault(False)
        self.nextman.setObjectName("nextman")
        self.groupBox_3 = QtWidgets.QGroupBox(ReviewThroughoutControl)
        self.groupBox_3.setGeometry(QtCore.QRect(90, 10, 141, 111))
        self.groupBox_3.setObjectName("groupBox_3")
        self.check_Ptrj = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_Ptrj.setGeometry(QtCore.QRect(10, 15, 121, 16))
        self.check_Ptrj.setChecked(True)
        self.check_Ptrj.setObjectName("check_Ptrj")
        self.showplanets = QtWidgets.QCheckBox(self.groupBox_3)
        self.showplanets.setGeometry(QtCore.QRect(10, 69, 121, 16))
        self.showplanets.setChecked(True)
        self.showplanets.setObjectName("showplanets")
        self.check_PKepler = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_PKepler.setGeometry(QtCore.QRect(10, 33, 121, 16))
        self.check_PKepler.setChecked(False)
        self.check_PKepler.setObjectName("check_PKepler")
        self.check_TKepler = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_TKepler.setGeometry(QtCore.QRect(10, 51, 121, 16))
        self.check_TKepler.setChecked(True)
        self.check_TKepler.setObjectName("check_TKepler")
        self.showmantype = QtWidgets.QCheckBox(self.groupBox_3)
        self.showmantype.setGeometry(QtCore.QRect(10, 87, 101, 16))
        self.showmantype.setChecked(True)
        self.showmantype.setObjectName("showmantype")
        self.starttime = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.starttime.setGeometry(QtCore.QRect(430, 10, 201, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.starttime.setFont(font)
        self.starttime.setFocusPolicy(QtCore.Qt.NoFocus)
        self.starttime.setAcceptDrops(False)
        self.starttime.setToolTip("")
        self.starttime.setFrame(False)
        self.starttime.setReadOnly(True)
        self.starttime.setObjectName("starttime")
        self.RPTrange = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RPTrange.setGeometry(QtCore.QRect(83, 149, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTrange.setFont(font)
        self.RPTrange.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RPTrange.setToolTip("")
        self.RPTrange.setFrame(False)
        self.RPTrange.setReadOnly(True)
        self.RPTrange.setObjectName("RPTrange")
        self.RPTphi = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RPTphi.setGeometry(QtCore.QRect(83, 169, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTphi.setFont(font)
        self.RPTphi.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RPTphi.setToolTip("")
        self.RPTphi.setFrame(False)
        self.RPTphi.setReadOnly(True)
        self.RPTphi.setObjectName("RPTphi")
        self.RPTelv = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.RPTelv.setGeometry(QtCore.QRect(83, 189, 141, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTelv.setFont(font)
        self.RPTelv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RPTelv.setToolTip("")
        self.RPTelv.setFrame(False)
        self.RPTelv.setReadOnly(True)
        self.RPTelv.setObjectName("RPTelv")
        self.LoSVvel = QtWidgets.QLineEdit(ReviewThroughoutControl)
        self.LoSVvel.setGeometry(QtCore.QRect(502, 149, 126, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.LoSVvel.setFont(font)
        self.LoSVvel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.LoSVvel.setToolTip("")
        self.LoSVvel.setFrame(False)
        self.LoSVvel.setReadOnly(True)
        self.LoSVvel.setObjectName("LoSVvel")
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
        self.previousman.raise_()
        self.nextman.raise_()
        self.groupBox_3.raise_()
        self.starttime.raise_()
        self.RPTrange.raise_()
        self.RPTphi.raise_()
        self.RPTelv.raise_()
        self.LoSVvel.raise_()

        self.retranslateUi(ReviewThroughoutControl)
        QtCore.QMetaObject.connectSlotsByName(ReviewThroughoutControl)
        ReviewThroughoutControl.setTabOrder(self.tobarycenter, self.toprobe)
        ReviewThroughoutControl.setTabOrder(self.toprobe, self.totarget)
        ReviewThroughoutControl.setTabOrder(self.totarget, self.check_Ptrj)
        ReviewThroughoutControl.setTabOrder(self.check_Ptrj, self.check_PKepler)
        ReviewThroughoutControl.setTabOrder(self.check_PKepler, self.check_TKepler)
        ReviewThroughoutControl.setTabOrder(self.check_TKepler, self.showplanets)
        ReviewThroughoutControl.setTabOrder(self.showplanets, self.showmantype)
        ReviewThroughoutControl.setTabOrder(self.showmantype, self.previousman)
        ReviewThroughoutControl.setTabOrder(self.previousman, self.fastbackward)
        ReviewThroughoutControl.setTabOrder(self.fastbackward, self.backward)
        ReviewThroughoutControl.setTabOrder(self.backward, self.forward)
        ReviewThroughoutControl.setTabOrder(self.forward, self.fastforward)
        ReviewThroughoutControl.setTabOrder(self.fastforward, self.nextman)
        ReviewThroughoutControl.setTabOrder(self.nextman, self.timescale)

    def retranslateUi(self, ReviewThroughoutControl):
        _translate = QtCore.QCoreApplication.translate
        ReviewThroughoutControl.setWindowTitle(_translate("ReviewThroughoutControl", "Review Throughout"))
        self.label.setText(_translate("ReviewThroughoutControl", "Elapsed Time (days)"))
        self.fastbackward.setToolTip(_translate("ReviewThroughoutControl", "Fast Backword"))
        self.fastbackward.setText(_translate("ReviewThroughoutControl", "<<"))
        self.backward.setToolTip(_translate("ReviewThroughoutControl", "Backward"))
        self.backward.setText(_translate("ReviewThroughoutControl", "<"))
        self.forward.setToolTip(_translate("ReviewThroughoutControl", "Forward"))
        self.forward.setText(_translate("ReviewThroughoutControl", ">"))
        self.fastforward.setToolTip(_translate("ReviewThroughoutControl", "Fast Forward"))
        self.fastforward.setText(_translate("ReviewThroughoutControl", ">>"))
        self.timescale.setToolTip(_translate("ReviewThroughoutControl", "Steps for FF and FB"))
        self.label_2.setText(_translate("ReviewThroughoutControl", "Hopping"))
        self.label_6.setText(_translate("ReviewThroughoutControl", "Start Time"))
        self.label_4.setText(_translate("ReviewThroughoutControl", "Watching Time"))
        self.label_3.setText(_translate("ReviewThroughoutControl", "Relative Position of Target"))
        self.label_9.setText(_translate("ReviewThroughoutControl", "Relative Velocity of Target"))
        self.label_10.setText(_translate("ReviewThroughoutControl", "distance (km)"))
        self.label_11.setText(_translate("ReviewThroughoutControl", "phi (deg)"))
        self.label_12.setText(_translate("ReviewThroughoutControl", "elv (deg)"))
        self.label_14.setText(_translate("ReviewThroughoutControl", "vel (m/s)"))
        self.label_15.setText(_translate("ReviewThroughoutControl", "vel (m/s)"))
        self.label_16.setText(_translate("ReviewThroughoutControl", "phi (deg)"))
        self.label_17.setText(_translate("ReviewThroughoutControl", "elv (deg)"))
        self.label_18.setText(_translate("ReviewThroughoutControl", "Line of Sight Velocity"))
        self.label_19.setText(_translate("ReviewThroughoutControl", "Review Manipulator"))
        self.groupBox.setTitle(_translate("ReviewThroughoutControl", "Look at"))
        self.tobarycenter.setToolTip(_translate("ReviewThroughoutControl", "Solar System Barycenter"))
        self.tobarycenter.setText(_translate("ReviewThroughoutControl", "SSB"))
        self.toprobe.setText(_translate("ReviewThroughoutControl", "Probe"))
        self.totarget.setText(_translate("ReviewThroughoutControl", "Target"))
        self.previousman.setToolTip(_translate("ReviewThroughoutControl", "Previous Maneuver"))
        self.previousman.setText(_translate("ReviewThroughoutControl", "|<"))
        self.nextman.setToolTip(_translate("ReviewThroughoutControl", "Next Maneuver"))
        self.nextman.setText(_translate("ReviewThroughoutControl", ">|"))
        self.groupBox_3.setTitle(_translate("ReviewThroughoutControl", "Show"))
        self.check_Ptrj.setText(_translate("ReviewThroughoutControl", "Probe Trajectory"))
        self.showplanets.setText(_translate("ReviewThroughoutControl", "Planets"))
        self.check_PKepler.setText(_translate("ReviewThroughoutControl", "Probe Kepler Orbit"))
        self.check_TKepler.setText(_translate("ReviewThroughoutControl", "Target Kepler Orbit"))
        self.showmantype.setText(_translate("ReviewThroughoutControl", "Maneuver Type"))

