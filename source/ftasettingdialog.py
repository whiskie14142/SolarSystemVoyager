# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ftasettingdialog.ui'
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

class Ui_ftasettingdialog(object):
    def setupUi(self, ftasettingdialog):
        ftasettingdialog.setObjectName(_fromUtf8("ftasettingdialog"))
        ftasettingdialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ftasettingdialog.resize(480, 320)
        ftasettingdialog.setModal(True)
        self.groupBox = QtGui.QGroupBox(ftasettingdialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 441, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.fromshoworbit = QtGui.QRadioButton(self.groupBox)
        self.fromshoworbit.setGeometry(QtCore.QRect(30, 20, 391, 16))
        self.fromshoworbit.setChecked(True)
        self.fromshoworbit.setObjectName(_fromUtf8("fromshoworbit"))
        self.directinput = QtGui.QRadioButton(self.groupBox)
        self.directinput.setGeometry(QtCore.QRect(30, 40, 391, 16))
        self.directinput.setObjectName(_fromUtf8("directinput"))
        self.timetoarrival = QtGui.QLineEdit(self.groupBox)
        self.timetoarrival.setEnabled(False)
        self.timetoarrival.setGeometry(QtCore.QRect(310, 70, 113, 20))
        self.timetoarrival.setCursorPosition(0)
        self.timetoarrival.setObjectName(_fromUtf8("timetoarrival"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(190, 70, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_2 = QtGui.QGroupBox(ftasettingdialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 150, 441, 111))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 181, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 181, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 181, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.rangeedit = QtGui.QLineEdit(self.groupBox_2)
        self.rangeedit.setGeometry(QtCore.QRect(230, 20, 91, 19))
        self.rangeedit.setObjectName(_fromUtf8("rangeedit"))
        self.phiedit = QtGui.QLineEdit(self.groupBox_2)
        self.phiedit.setGeometry(QtCore.QRect(230, 40, 91, 19))
        self.phiedit.setObjectName(_fromUtf8("phiedit"))
        self.elvedit = QtGui.QLineEdit(self.groupBox_2)
        self.elvedit.setGeometry(QtCore.QRect(230, 60, 91, 19))
        self.elvedit.setObjectName(_fromUtf8("elvedit"))
        self.cancel_button = QtGui.QPushButton(ftasettingdialog)
        self.cancel_button.setGeometry(QtCore.QRect(380, 280, 75, 23))
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.ok_button = QtGui.QPushButton(ftasettingdialog)
        self.ok_button.setGeometry(QtCore.QRect(290, 280, 75, 23))
        self.ok_button.setAutoDefault(False)
        self.ok_button.setObjectName(_fromUtf8("ok_button"))

        self.retranslateUi(ftasettingdialog)
        QtCore.QMetaObject.connectSlotsByName(ftasettingdialog)

    def retranslateUi(self, ftasettingdialog):
        ftasettingdialog.setWindowTitle(_translate("ftasettingdialog", "FTA Setting", None))
        self.groupBox.setTitle(_translate("ftasettingdialog", "Time to Arrival : ", None))
        self.fromshoworbit.setText(_translate("ftasettingdialog", "Get Prediction Time from Show Orbit Window", None))
        self.directinput.setText(_translate("ftasettingdialog", "Specify Time to Arrival", None))
        self.timetoarrival.setText(_translate("ftasettingdialog", "100.00000", None))
        self.label.setText(_translate("ftasettingdialog", "Time to Arrival (days)", None))
        self.groupBox_2.setTitle(_translate("ftasettingdialog", "Set Probe\'s Sights on : ", None))
        self.label_2.setText(_translate("ftasettingdialog", "Range from Target Center (km)", None))
        self.label_3.setText(_translate("ftasettingdialog", "Angle phi from Target Center (deg)", None))
        self.label_4.setText(_translate("ftasettingdialog", "Angle elv from Target Center (deg)", None))
        self.rangeedit.setText(_translate("ftasettingdialog", "0.0", None))
        self.phiedit.setToolTip(_translate("ftasettingdialog", "Leading position : phi=0, elv=0\n"
"Trailing position : phi=180, elv=0\n"
"Sunward lateral : phi=90, elv=0\n"
"Upward : elv=90", None))
        self.phiedit.setText(_translate("ftasettingdialog", "0.0", None))
        self.elvedit.setToolTip(_translate("ftasettingdialog", "Leading position : phi=0, elv=0\n"
"Trailing position : phi=180, elv=0\n"
"Sunward lateral : phi=90, elv=0\n"
"Upward : elv=90", None))
        self.elvedit.setText(_translate("ftasettingdialog", "0.0", None))
        self.cancel_button.setText(_translate("ftasettingdialog", "Cancel", None))
        self.ok_button.setText(_translate("ftasettingdialog", "OK", None))

