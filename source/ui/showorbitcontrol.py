# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showorbitcontrol.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShowOrbitControl(object):
    def setupUi(self, ShowOrbitControl):
        ShowOrbitControl.setObjectName("ShowOrbitControl")
        ShowOrbitControl.resize(640, 216)
        ShowOrbitControl.setMinimumSize(QtCore.QSize(640, 216))
        ShowOrbitControl.setMaximumSize(QtCore.QSize(640, 216))
        self.label = QtWidgets.QLabel(ShowOrbitControl)
        self.label.setGeometry(QtCore.QRect(350, 52, 116, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.delta_t_edit = QtWidgets.QLineEdit(ShowOrbitControl)
        self.delta_t_edit.setGeometry(QtCore.QRect(472, 51, 111, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.delta_t_edit.setFont(font)
        self.delta_t_edit.setAcceptDrops(False)
        self.delta_t_edit.setToolTip("")
        self.delta_t_edit.setObjectName("delta_t_edit")
        self.fastbackward = QtWidgets.QPushButton(ShowOrbitControl)
        self.fastbackward.setGeometry(QtCore.QRect(360, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastbackward.setFont(font)
        self.fastbackward.setAutoRepeat(True)
        self.fastbackward.setAutoDefault(False)
        self.fastbackward.setObjectName("fastbackward")
        self.backward = QtWidgets.QPushButton(ShowOrbitControl)
        self.backward.setGeometry(QtCore.QRect(410, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.backward.setFont(font)
        self.backward.setAutoRepeat(True)
        self.backward.setAutoDefault(False)
        self.backward.setObjectName("backward")
        self.forward = QtWidgets.QPushButton(ShowOrbitControl)
        self.forward.setGeometry(QtCore.QRect(460, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.forward.setFont(font)
        self.forward.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.forward.setAutoRepeat(True)
        self.forward.setAutoDefault(False)
        self.forward.setObjectName("forward")
        self.fastforward = QtWidgets.QPushButton(ShowOrbitControl)
        self.fastforward.setGeometry(QtCore.QRect(510, 90, 41, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fastforward.setFont(font)
        self.fastforward.setAutoRepeat(True)
        self.fastforward.setAutoDefault(False)
        self.fastforward.setObjectName("fastforward")
        self.timescale = QtWidgets.QSpinBox(ShowOrbitControl)
        self.timescale.setGeometry(QtCore.QRect(580, 90, 42, 31))
        self.timescale.setMinimum(-8)
        self.timescale.setMaximum(5)
        self.timescale.setObjectName("timescale")
        self.label_2 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_2.setGeometry(QtCore.QRect(570, 72, 67, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.ctimeLabel = QtWidgets.QLabel(ShowOrbitControl)
        self.ctimeLabel.setGeometry(QtCore.QRect(350, 10, 81, 16))
        self.ctimeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ctimeLabel.setObjectName("ctimeLabel")
        self.label_4 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_4.setGeometry(QtCore.QRect(350, 30, 81, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.dtApply = QtWidgets.QPushButton(ShowOrbitControl)
        self.dtApply.setGeometry(QtCore.QRect(591, 50, 41, 21))
        self.dtApply.setAutoDefault(False)
        self.dtApply.setObjectName("dtApply")
        self.label_3 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_3.setGeometry(QtCore.QRect(50, 130, 201, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_9.setGeometry(QtCore.QRect(250, 130, 191, 16))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_10.setGeometry(QtCore.QRect(4, 150, 81, 16))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_11.setGeometry(QtCore.QRect(4, 170, 81, 16))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_12.setGeometry(QtCore.QRect(4, 190, 81, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_14.setGeometry(QtCore.QRect(224, 150, 71, 16))
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_15.setGeometry(QtCore.QRect(414, 150, 71, 16))
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_16.setGeometry(QtCore.QRect(224, 170, 71, 16))
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_17.setGeometry(QtCore.QRect(224, 190, 71, 16))
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_18.setGeometry(QtCore.QRect(460, 130, 161, 16))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setWordWrap(False)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(ShowOrbitControl)
        self.label_19.setGeometry(QtCore.QRect(351, 72, 211, 20))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setWordWrap(False)
        self.label_19.setObjectName("label_19")
        self.preddate = QtWidgets.QLineEdit(ShowOrbitControl)
        self.preddate.setGeometry(QtCore.QRect(440, 29, 191, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.preddate.setFont(font)
        self.preddate.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.preddate.setAcceptDrops(False)
        self.preddate.setToolTip("")
        self.preddate.setFrame(False)
        self.preddate.setReadOnly(True)
        self.preddate.setObjectName("preddate")
        self.RVTvel = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RVTvel.setGeometry(QtCore.QRect(300, 149, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTvel.setFont(font)
        self.RVTvel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTvel.setToolTip("")
        self.RVTvel.setFrame(False)
        self.RVTvel.setReadOnly(True)
        self.RVTvel.setObjectName("RVTvel")
        self.RVTphi = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RVTphi.setGeometry(QtCore.QRect(300, 169, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTphi.setFont(font)
        self.RVTphi.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTphi.setToolTip("")
        self.RVTphi.setFrame(False)
        self.RVTphi.setReadOnly(True)
        self.RVTphi.setObjectName("RVTphi")
        self.RVTelv = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RVTelv.setGeometry(QtCore.QRect(300, 189, 91, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RVTelv.setFont(font)
        self.RVTelv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RVTelv.setToolTip("")
        self.RVTelv.setFrame(False)
        self.RVTelv.setReadOnly(True)
        self.RVTelv.setObjectName("RVTelv")
        self.groupBox = QtWidgets.QGroupBox(ShowOrbitControl)
        self.groupBox.setGeometry(QtCore.QRect(250, 10, 91, 111))
        self.groupBox.setObjectName("groupBox")
        self.man_elv = QtWidgets.QLabel(self.groupBox)
        self.man_elv.setGeometry(QtCore.QRect(30, 60, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.man_elv.setFont(font)
        self.man_elv.setText("")
        self.man_elv.setObjectName("man_elv")
        self.man_dv = QtWidgets.QLabel(self.groupBox)
        self.man_dv.setGeometry(QtCore.QRect(30, 20, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.man_dv.setFont(font)
        self.man_dv.setText("")
        self.man_dv.setObjectName("man_dv")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 21, 16))
        self.label_8.setObjectName("label_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 40, 21, 16))
        self.label_7.setObjectName("label_7")
        self.man_phi = QtWidgets.QLabel(self.groupBox)
        self.man_phi.setGeometry(QtCore.QRect(30, 40, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.man_phi.setFont(font)
        self.man_phi.setText("")
        self.man_phi.setObjectName("man_phi")
        self.groupBox_2 = QtWidgets.QGroupBox(ShowOrbitControl)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 91, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.tobarycenter = QtWidgets.QRadioButton(self.groupBox_2)
        self.tobarycenter.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.tobarycenter.setChecked(True)
        self.tobarycenter.setObjectName("tobarycenter")
        self.toprobe = QtWidgets.QRadioButton(self.groupBox_2)
        self.toprobe.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.toprobe.setObjectName("toprobe")
        self.totarget = QtWidgets.QRadioButton(self.groupBox_2)
        self.totarget.setGeometry(QtCore.QRect(10, 60, 81, 16))
        self.totarget.setObjectName("totarget")
        self.groupBox_3 = QtWidgets.QGroupBox(ShowOrbitControl)
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
        self.currentdate = QtWidgets.QLineEdit(ShowOrbitControl)
        self.currentdate.setGeometry(QtCore.QRect(440, 9, 191, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.currentdate.setFont(font)
        self.currentdate.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.currentdate.setAcceptDrops(False)
        self.currentdate.setToolTip("")
        self.currentdate.setFrame(False)
        self.currentdate.setReadOnly(True)
        self.currentdate.setObjectName("currentdate")
        self.RPTrange = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RPTrange.setGeometry(QtCore.QRect(90, 149, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTrange.setFont(font)
        self.RPTrange.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTrange.setToolTip("")
        self.RPTrange.setFrame(False)
        self.RPTrange.setReadOnly(True)
        self.RPTrange.setObjectName("RPTrange")
        self.RPTphi = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RPTphi.setGeometry(QtCore.QRect(90, 169, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTphi.setFont(font)
        self.RPTphi.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTphi.setToolTip("")
        self.RPTphi.setFrame(False)
        self.RPTphi.setReadOnly(True)
        self.RPTphi.setObjectName("RPTphi")
        self.RPTelv = QtWidgets.QLineEdit(ShowOrbitControl)
        self.RPTelv.setGeometry(QtCore.QRect(90, 189, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.RPTelv.setFont(font)
        self.RPTelv.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.RPTelv.setToolTip("")
        self.RPTelv.setFrame(False)
        self.RPTelv.setReadOnly(True)
        self.RPTelv.setObjectName("RPTelv")
        self.LoSVvel = QtWidgets.QLineEdit(ShowOrbitControl)
        self.LoSVvel.setGeometry(QtCore.QRect(490, 149, 101, 18))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.LoSVvel.setFont(font)
        self.LoSVvel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LoSVvel.setToolTip("")
        self.LoSVvel.setFrame(False)
        self.LoSVvel.setReadOnly(True)
        self.LoSVvel.setObjectName("LoSVvel")
        self.sysMessage = QtWidgets.QPlainTextEdit(ShowOrbitControl)
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
        self.groupBox_3.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.delta_t_edit.raise_()
        self.fastbackward.raise_()
        self.forward.raise_()
        self.fastforward.raise_()
        self.timescale.raise_()
        self.ctimeLabel.raise_()
        self.label_4.raise_()
        self.dtApply.raise_()
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
        self.preddate.raise_()
        self.RVTvel.raise_()
        self.RVTphi.raise_()
        self.RVTelv.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.backward.raise_()
        self.currentdate.raise_()
        self.RPTrange.raise_()
        self.RPTphi.raise_()
        self.RPTelv.raise_()
        self.LoSVvel.raise_()
        self.sysMessage.raise_()

        self.retranslateUi(ShowOrbitControl)
        self.delta_t_edit.returnPressed.connect(self.dtApply.click)
        QtCore.QMetaObject.connectSlotsByName(ShowOrbitControl)
        ShowOrbitControl.setTabOrder(self.tobarycenter, self.toprobe)
        ShowOrbitControl.setTabOrder(self.toprobe, self.totarget)
        ShowOrbitControl.setTabOrder(self.totarget, self.check_Ptrj)
        ShowOrbitControl.setTabOrder(self.check_Ptrj, self.check_PKepler)
        ShowOrbitControl.setTabOrder(self.check_PKepler, self.check_TKepler)
        ShowOrbitControl.setTabOrder(self.check_TKepler, self.showplanets)
        ShowOrbitControl.setTabOrder(self.showplanets, self.delta_t_edit)
        ShowOrbitControl.setTabOrder(self.delta_t_edit, self.dtApply)
        ShowOrbitControl.setTabOrder(self.dtApply, self.fastbackward)
        ShowOrbitControl.setTabOrder(self.fastbackward, self.backward)
        ShowOrbitControl.setTabOrder(self.backward, self.forward)
        ShowOrbitControl.setTabOrder(self.forward, self.fastforward)
        ShowOrbitControl.setTabOrder(self.fastforward, self.timescale)

    def retranslateUi(self, ShowOrbitControl):
        _translate = QtCore.QCoreApplication.translate
        ShowOrbitControl.setWindowTitle(_translate("ShowOrbitControl", "Show Orbit"))
        self.label.setText(_translate("ShowOrbitControl", "Elapsed Time (days)"))
        self.fastbackward.setToolTip(_translate("ShowOrbitControl", "Fast Backword"))
        self.fastbackward.setText(_translate("ShowOrbitControl", "<<"))
        self.backward.setToolTip(_translate("ShowOrbitControl", "Backward"))
        self.backward.setText(_translate("ShowOrbitControl", "<"))
        self.forward.setToolTip(_translate("ShowOrbitControl", "Forward"))
        self.forward.setText(_translate("ShowOrbitControl", ">"))
        self.fastforward.setToolTip(_translate("ShowOrbitControl", "Fast Forward"))
        self.fastforward.setText(_translate("ShowOrbitControl", ">>"))
        self.timescale.setToolTip(_translate("ShowOrbitControl", "The value specifies coarseness (or fineness) of the Prediction Time.  Larger value makes time steps larger."))
        self.label_2.setText(_translate("ShowOrbitControl", "coarse/fine"))
        self.ctimeLabel.setText(_translate("ShowOrbitControl", "Current Time"))
        self.label_4.setText(_translate("ShowOrbitControl", "Predict. Time"))
        self.dtApply.setText(_translate("ShowOrbitControl", "Apply"))
        self.label_3.setText(_translate("ShowOrbitControl", "Relative Position of Target"))
        self.label_9.setText(_translate("ShowOrbitControl", "Relative Velocity of Target"))
        self.label_10.setText(_translate("ShowOrbitControl", "distance (km)"))
        self.label_11.setText(_translate("ShowOrbitControl", "phi (deg)"))
        self.label_12.setText(_translate("ShowOrbitControl", "elv (deg)"))
        self.label_14.setText(_translate("ShowOrbitControl", "vel (m/s)"))
        self.label_15.setText(_translate("ShowOrbitControl", "vel (m/s)"))
        self.label_16.setText(_translate("ShowOrbitControl", "phi (deg)"))
        self.label_17.setText(_translate("ShowOrbitControl", "elv (deg)"))
        self.label_18.setText(_translate("ShowOrbitControl", "Line of Sight Velocity"))
        self.label_19.setText(_translate("ShowOrbitControl", "bkwd<<    Time Manipulator    >>fwd"))
        self.groupBox.setTitle(_translate("ShowOrbitControl", "M. Parameters"))
        self.label_8.setText(_translate("ShowOrbitControl", "elv"))
        self.label_6.setText(_translate("ShowOrbitControl", "dv"))
        self.label_7.setText(_translate("ShowOrbitControl", "phi"))
        self.groupBox_2.setTitle(_translate("ShowOrbitControl", "Look at"))
        self.tobarycenter.setToolTip(_translate("ShowOrbitControl", "Solar System Barycenter"))
        self.tobarycenter.setText(_translate("ShowOrbitControl", "SSB"))
        self.toprobe.setText(_translate("ShowOrbitControl", "Probe"))
        self.totarget.setText(_translate("ShowOrbitControl", "Target"))
        self.groupBox_3.setTitle(_translate("ShowOrbitControl", "Show"))
        self.check_Ptrj.setText(_translate("ShowOrbitControl", "Probe Trajectory"))
        self.showplanets.setText(_translate("ShowOrbitControl", "Planets"))
        self.check_PKepler.setText(_translate("ShowOrbitControl", "Probe Kepler Orbit"))
        self.check_TKepler.setText(_translate("ShowOrbitControl", "Target Kepler Orbit"))
        self.sysMessage.setToolTip(_translate("ShowOrbitControl", "System Messages"))

