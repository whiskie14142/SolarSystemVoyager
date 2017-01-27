# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newflightplandialog.ui'
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

class Ui_NewFlightPlanDialog(object):
    def setupUi(self, NewFlightPlanDialog):
        NewFlightPlanDialog.setObjectName(_fromUtf8("NewFlightPlanDialog"))
        NewFlightPlanDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NewFlightPlanDialog.resize(480, 360)
        NewFlightPlanDialog.setModal(True)
        self.probe_box = QtGui.QGroupBox(NewFlightPlanDialog)
        self.probe_box.setGeometry(QtCore.QRect(10, 20, 461, 91))
        self.probe_box.setObjectName(_fromUtf8("probe_box"))
        self.label = QtGui.QLabel(self.probe_box)
        self.label.setGeometry(QtCore.QRect(20, 20, 51, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.probe_box)
        self.label_2.setGeometry(QtCore.QRect(250, 50, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.probe_box)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.probename = QtGui.QLineEdit(self.probe_box)
        self.probename.setGeometry(QtCore.QRect(80, 20, 111, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.probename.setFont(font)
        self.probename.setObjectName(_fromUtf8("probename"))
        self.spacebase = QtGui.QComboBox(self.probe_box)
        self.spacebase.setGeometry(QtCore.QRect(320, 50, 111, 22))
        self.spacebase.setObjectName(_fromUtf8("spacebase"))
        self.probemass = QtGui.QLineEdit(self.probe_box)
        self.probemass.setGeometry(QtCore.QRect(80, 50, 113, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.probemass.setFont(font)
        self.probemass.setObjectName(_fromUtf8("probemass"))
        self.target_box = QtGui.QGroupBox(NewFlightPlanDialog)
        self.target_box.setEnabled(True)
        self.target_box.setGeometry(QtCore.QRect(10, 130, 461, 131))
        self.target_box.setFlat(False)
        self.target_box.setObjectName(_fromUtf8("target_box"))
        self.planetbutton = QtGui.QRadioButton(self.target_box)
        self.planetbutton.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.planetbutton.setChecked(True)
        self.planetbutton.setObjectName(_fromUtf8("planetbutton"))
        self.smallbodybutton = QtGui.QRadioButton(self.target_box)
        self.smallbodybutton.setGeometry(QtCore.QRect(20, 50, 91, 16))
        self.smallbodybutton.setObjectName(_fromUtf8("smallbodybutton"))
        self.planets = QtGui.QComboBox(self.target_box)
        self.planets.setGeometry(QtCore.QRect(20, 90, 111, 22))
        self.planets.setObjectName(_fromUtf8("planets"))
        self.targetgroupbox = QtGui.QGroupBox(self.target_box)
        self.targetgroupbox.setEnabled(False)
        self.targetgroupbox.setGeometry(QtCore.QRect(150, 20, 301, 101))
        self.targetgroupbox.setTitle(_fromUtf8(""))
        self.targetgroupbox.setFlat(False)
        self.targetgroupbox.setObjectName(_fromUtf8("targetgroupbox"))
        self.spkid_edit = QtGui.QLineEdit(self.targetgroupbox)
        self.spkid_edit.setGeometry(QtCore.QRect(60, 70, 113, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.spkid_edit.setFont(font)
        self.spkid_edit.setObjectName(_fromUtf8("spkid_edit"))
        self.label_5 = QtGui.QLabel(self.targetgroupbox)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 41, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.spkfileselect = QtGui.QPushButton(self.targetgroupbox)
        self.spkfileselect.setGeometry(QtCore.QRect(272, 38, 21, 23))
        self.spkfileselect.setAutoDefault(False)
        self.spkfileselect.setObjectName(_fromUtf8("spkfileselect"))
        self.targetname = QtGui.QLineEdit(self.targetgroupbox)
        self.targetname.setGeometry(QtCore.QRect(60, 10, 113, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.targetname.setFont(font)
        self.targetname.setObjectName(_fromUtf8("targetname"))
        self.label_6 = QtGui.QLabel(self.targetgroupbox)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 41, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.spkfilepath = QtGui.QLineEdit(self.targetgroupbox)
        self.spkfilepath.setGeometry(QtCore.QRect(60, 40, 211, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Console"))
        self.spkfilepath.setFont(font)
        self.spkfilepath.setObjectName(_fromUtf8("spkfilepath"))
        self.label_4 = QtGui.QLabel(self.targetgroupbox)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.cancelbutton = QtGui.QPushButton(NewFlightPlanDialog)
        self.cancelbutton.setGeometry(QtCore.QRect(380, 310, 75, 23))
        self.cancelbutton.setAutoDefault(False)
        self.cancelbutton.setObjectName(_fromUtf8("cancelbutton"))
        self.okbutton = QtGui.QPushButton(NewFlightPlanDialog)
        self.okbutton.setGeometry(QtCore.QRect(280, 310, 75, 23))
        self.okbutton.setObjectName(_fromUtf8("okbutton"))

        self.retranslateUi(NewFlightPlanDialog)
        self.spacebase.setCurrentIndex(-1)
        self.planets.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(NewFlightPlanDialog)

    def retranslateUi(self, NewFlightPlanDialog):
        NewFlightPlanDialog.setWindowTitle(_translate("NewFlightPlanDialog", "New Flight Plan", None))
        self.probe_box.setTitle(_translate("NewFlightPlanDialog", "Probe properties", None))
        self.label.setText(_translate("NewFlightPlanDialog", "Name", None))
        self.label_2.setText(_translate("NewFlightPlanDialog", "Space Base", None))
        self.label_3.setText(_translate("NewFlightPlanDialog", "Mass (kg)", None))
        self.probename.setText(_translate("NewFlightPlanDialog", "myprobe", None))
        self.probemass.setText(_translate("NewFlightPlanDialog", "500.0", None))
        self.target_box.setTitle(_translate("NewFlightPlanDialog", "Target", None))
        self.planetbutton.setText(_translate("NewFlightPlanDialog", "Planet/Moon", None))
        self.smallbodybutton.setText(_translate("NewFlightPlanDialog", "Small Body", None))
        self.spkid_edit.setText(_translate("NewFlightPlanDialog", "2000001", None))
        self.label_5.setText(_translate("NewFlightPlanDialog", "SPK file", None))
        self.spkfileselect.setText(_translate("NewFlightPlanDialog", "...", None))
        self.targetname.setText(_translate("NewFlightPlanDialog", "Ceres", None))
        self.label_6.setText(_translate("NewFlightPlanDialog", "SPKID", None))
        self.label_4.setText(_translate("NewFlightPlanDialog", "Name", None))
        self.cancelbutton.setText(_translate("NewFlightPlanDialog", "Cancel", None))
        self.okbutton.setText(_translate("NewFlightPlanDialog", "OK", None))

