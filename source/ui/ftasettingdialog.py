# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ftasettingdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ftasettingdialog(object):
    def setupUi(self, ftasettingdialog):
        ftasettingdialog.setObjectName("ftasettingdialog")
        ftasettingdialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ftasettingdialog.resize(480, 520)
        ftasettingdialog.setMinimumSize(QtCore.QSize(480, 520))
        ftasettingdialog.setMaximumSize(QtCore.QSize(480, 520))
        ftasettingdialog.setModal(True)
        self.groupBox = QtWidgets.QGroupBox(ftasettingdialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 60, 441, 91))
        self.groupBox.setObjectName("groupBox")
        self.fromshoworbit = QtWidgets.QRadioButton(self.groupBox)
        self.fromshoworbit.setGeometry(QtCore.QRect(30, 20, 391, 16))
        self.fromshoworbit.setChecked(True)
        self.fromshoworbit.setObjectName("fromshoworbit")
        self.directinput = QtWidgets.QRadioButton(self.groupBox)
        self.directinput.setGeometry(QtCore.QRect(30, 40, 391, 16))
        self.directinput.setObjectName("directinput")
        self.timetoarrival = QtWidgets.QLineEdit(self.groupBox)
        self.timetoarrival.setEnabled(False)
        self.timetoarrival.setGeometry(QtCore.QRect(280, 60, 113, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.timetoarrival.setFont(font)
        self.timetoarrival.setCursorPosition(0)
        self.timetoarrival.setObjectName("timetoarrival")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(80, 60, 191, 18))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.cancel_button = QtWidgets.QPushButton(ftasettingdialog)
        self.cancel_button.setGeometry(QtCore.QRect(380, 480, 75, 23))
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.setObjectName("cancel_button")
        self.ok_button = QtWidgets.QPushButton(ftasettingdialog)
        self.ok_button.setGeometry(QtCore.QRect(290, 480, 75, 23))
        self.ok_button.setAutoDefault(False)
        self.ok_button.setObjectName("ok_button")
        self.groupBox_3 = QtWidgets.QGroupBox(ftasettingdialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 170, 441, 291))
        self.groupBox_3.setObjectName("groupBox_3")
        self.selTargetcenter = QtWidgets.QRadioButton(self.groupBox_3)
        self.selTargetcenter.setGeometry(QtCore.QRect(30, 20, 391, 16))
        self.selTargetcenter.setChecked(True)
        self.selTargetcenter.setObjectName("selTargetcenter")
        self.selBplanecoord = QtWidgets.QRadioButton(self.groupBox_3)
        self.selBplanecoord.setGeometry(QtCore.QRect(30, 60, 391, 16))
        self.selBplanecoord.setObjectName("selBplanecoord")
        self.selOLcoord = QtWidgets.QRadioButton(self.groupBox_3)
        self.selOLcoord.setGeometry(QtCore.QRect(30, 170, 391, 16))
        self.selOLcoord.setObjectName("selOLcoord")
        self.Bplanecoords = QtWidgets.QGroupBox(self.groupBox_3)
        self.Bplanecoords.setEnabled(False)
        self.Bplanecoords.setGeometry(QtCore.QRect(130, 80, 261, 61))
        self.Bplanecoords.setTitle("")
        self.Bplanecoords.setObjectName("Bplanecoords")
        self.label_5 = QtWidgets.QLabel(self.Bplanecoords)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 121, 16))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.Brangeedit = QtWidgets.QLineEdit(self.Bplanecoords)
        self.Brangeedit.setGeometry(QtCore.QRect(150, 10, 91, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.Brangeedit.setFont(font)
        self.Brangeedit.setObjectName("Brangeedit")
        self.label_6 = QtWidgets.QLabel(self.Bplanecoords)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.betaedit = QtWidgets.QLineEdit(self.Bplanecoords)
        self.betaedit.setGeometry(QtCore.QRect(150, 30, 91, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.betaedit.setFont(font)
        self.betaedit.setObjectName("betaedit")
        self.OLcoords = QtWidgets.QGroupBox(self.groupBox_3)
        self.OLcoords.setEnabled(False)
        self.OLcoords.setGeometry(QtCore.QRect(130, 190, 261, 81))
        self.OLcoords.setTitle("")
        self.OLcoords.setObjectName("OLcoords")
        self.label_2 = QtWidgets.QLabel(self.OLcoords)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 121, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.OLcoords)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.OLcoords)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 121, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.rangeedit = QtWidgets.QLineEdit(self.OLcoords)
        self.rangeedit.setGeometry(QtCore.QRect(150, 10, 91, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.rangeedit.setFont(font)
        self.rangeedit.setObjectName("rangeedit")
        self.phiedit = QtWidgets.QLineEdit(self.OLcoords)
        self.phiedit.setGeometry(QtCore.QRect(150, 30, 91, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.phiedit.setFont(font)
        self.phiedit.setObjectName("phiedit")
        self.elvedit = QtWidgets.QLineEdit(self.OLcoords)
        self.elvedit.setGeometry(QtCore.QRect(150, 50, 91, 19))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.elvedit.setFont(font)
        self.elvedit.setObjectName("elvedit")
        self.label_7 = QtWidgets.QLabel(ftasettingdialog)
        self.label_7.setGeometry(QtCore.QRect(20, 20, 441, 16))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(ftasettingdialog)
        QtCore.QMetaObject.connectSlotsByName(ftasettingdialog)
        ftasettingdialog.setTabOrder(self.fromshoworbit, self.directinput)
        ftasettingdialog.setTabOrder(self.directinput, self.timetoarrival)
        ftasettingdialog.setTabOrder(self.timetoarrival, self.selTargetcenter)
        ftasettingdialog.setTabOrder(self.selTargetcenter, self.selBplanecoord)
        ftasettingdialog.setTabOrder(self.selBplanecoord, self.Brangeedit)
        ftasettingdialog.setTabOrder(self.Brangeedit, self.betaedit)
        ftasettingdialog.setTabOrder(self.betaedit, self.selOLcoord)
        ftasettingdialog.setTabOrder(self.selOLcoord, self.rangeedit)
        ftasettingdialog.setTabOrder(self.rangeedit, self.phiedit)
        ftasettingdialog.setTabOrder(self.phiedit, self.elvedit)
        ftasettingdialog.setTabOrder(self.elvedit, self.ok_button)
        ftasettingdialog.setTabOrder(self.ok_button, self.cancel_button)

    def retranslateUi(self, ftasettingdialog):
        _translate = QtCore.QCoreApplication.translate
        ftasettingdialog.setWindowTitle(_translate("ftasettingdialog", "FTA Setting"))
        self.groupBox.setTitle(_translate("ftasettingdialog", "Time to Arrival"))
        self.fromshoworbit.setText(_translate("ftasettingdialog", "Use Elapsed Time of Show Orbit Window"))
        self.directinput.setText(_translate("ftasettingdialog", "Specify Now"))
        self.timetoarrival.setText(_translate("ftasettingdialog", "100.00000"))
        self.label.setText(_translate("ftasettingdialog", "Time to Arrival (days)"))
        self.cancel_button.setText(_translate("ftasettingdialog", "Cancel"))
        self.ok_button.setText(_translate("ftasettingdialog", "OK"))
        self.groupBox_3.setTitle(_translate("ftasettingdialog", "Precise Targeting"))
        self.selTargetcenter.setText(_translate("ftasettingdialog", "Center of Target"))
        self.selBplanecoord.setText(_translate("ftasettingdialog", "B-plane Coordinates"))
        self.selOLcoord.setText(_translate("ftasettingdialog", "Orbit Local Coordinates"))
        self.label_5.setText(_translate("ftasettingdialog", "offset distance (km)"))
        self.Brangeedit.setText(_translate("ftasettingdialog", "0.0"))
        self.label_6.setText(_translate("ftasettingdialog", "beta (deg)"))
        self.betaedit.setToolTip(_translate("ftasettingdialog", "Angle beta on B-plane"))
        self.betaedit.setText(_translate("ftasettingdialog", "0.0"))
        self.label_2.setText(_translate("ftasettingdialog", "offset distance (km)"))
        self.label_3.setText(_translate("ftasettingdialog", "phi (deg)"))
        self.label_4.setText(_translate("ftasettingdialog", "elv (deg)"))
        self.rangeedit.setText(_translate("ftasettingdialog", "0.0"))
        self.phiedit.setToolTip(_translate("ftasettingdialog", "Angle phi on Orbit Local coordinate"))
        self.phiedit.setText(_translate("ftasettingdialog", "0.0"))
        self.elvedit.setToolTip(_translate("ftasettingdialog", "Angle elv on Orbit Local coordinate"))
        self.elvedit.setText(_translate("ftasettingdialog", "0.0"))
        self.label_7.setText(_translate("ftasettingdialog", "FTA computes delta-V for a Maneuver that brings the Probe to the Target."))

