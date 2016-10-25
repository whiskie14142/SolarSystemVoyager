# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutSSVG.ui'
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

class Ui_aboutSSVG(object):
    def setupUi(self, aboutSSVG):
        aboutSSVG.setObjectName(_fromUtf8("aboutSSVG"))
        aboutSSVG.resize(480, 449)
        aboutSSVG.setAutoFillBackground(False)
        self.okButton = QtGui.QPushButton(aboutSSVG)
        self.okButton.setGeometry(QtCore.QRect(370, 410, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.groupBox = QtGui.QGroupBox(aboutSSVG)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 441, 51))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.versionlabel = QtGui.QLabel(self.groupBox)
        self.versionlabel.setGeometry(QtCore.QRect(170, 20, 221, 16))
        self.versionlabel.setObjectName(_fromUtf8("versionlabel"))
        self.groupBox_2 = QtGui.QGroupBox(aboutSSVG)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 100, 441, 291))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.licensetext = QtGui.QPlainTextEdit(self.groupBox_2)
        self.licensetext.setGeometry(QtCore.QRect(10, 30, 421, 231))
        self.licensetext.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.licensetext.setAcceptDrops(False)
        self.licensetext.setAutoFillBackground(True)
        self.licensetext.setLineWidth(0)
        self.licensetext.setUndoRedoEnabled(False)
        self.licensetext.setReadOnly(True)
        self.licensetext.setObjectName(_fromUtf8("licensetext"))

        self.retranslateUi(aboutSSVG)
        QtCore.QMetaObject.connectSlotsByName(aboutSSVG)

    def retranslateUi(self, aboutSSVG):
        aboutSSVG.setWindowTitle(_translate("aboutSSVG", "about SSVG", None))
        self.okButton.setText(_translate("aboutSSVG", "OK", None))
        self.groupBox.setTitle(_translate("aboutSSVG", "Version", None))
        self.versionlabel.setText(_translate("aboutSSVG", "0.1.0 Beta", None))
        self.groupBox_2.setTitle(_translate("aboutSSVG", "Licese Terms", None))

