# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutSSVG.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_aboutSSVG(object):
    def setupUi(self, aboutSSVG):
        aboutSSVG.setObjectName("aboutSSVG")
        aboutSSVG.resize(480, 449)
        aboutSSVG.setMinimumSize(QtCore.QSize(480, 449))
        aboutSSVG.setMaximumSize(QtCore.QSize(480, 449))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        aboutSSVG.setFont(font)
        aboutSSVG.setAutoFillBackground(False)
        aboutSSVG.setModal(True)
        self.okButton = QtWidgets.QPushButton(aboutSSVG)
        self.okButton.setGeometry(QtCore.QRect(370, 410, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.okButton.setFont(font)
        self.okButton.setObjectName("okButton")
        self.groupBox = QtWidgets.QGroupBox(aboutSSVG)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 441, 51))
        self.groupBox.setObjectName("groupBox")
        self.versionlabel = QtWidgets.QLabel(self.groupBox)
        self.versionlabel.setGeometry(QtCore.QRect(50, 20, 341, 21))
        self.versionlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionlabel.setObjectName("versionlabel")
        self.groupBox_2 = QtWidgets.QGroupBox(aboutSSVG)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 100, 441, 291))
        self.groupBox_2.setObjectName("groupBox_2")
        self.licensetext = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.licensetext.setGeometry(QtCore.QRect(10, 30, 421, 231))
        self.licensetext.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.licensetext.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.licensetext.setAcceptDrops(False)
        self.licensetext.setAutoFillBackground(True)
        self.licensetext.setLineWidth(0)
        self.licensetext.setUndoRedoEnabled(False)
        self.licensetext.setReadOnly(True)
        self.licensetext.setObjectName("licensetext")

        self.retranslateUi(aboutSSVG)
        QtCore.QMetaObject.connectSlotsByName(aboutSSVG)

    def retranslateUi(self, aboutSSVG):
        _translate = QtCore.QCoreApplication.translate
        aboutSSVG.setWindowTitle(_translate("aboutSSVG", "about SSVG"))
        self.okButton.setText(_translate("aboutSSVG", "OK"))
        self.groupBox.setTitle(_translate("aboutSSVG", "Version"))
        self.versionlabel.setText(_translate("aboutSSVG", "0.1.0 Beta"))
        self.groupBox_2.setTitle(_translate("aboutSSVG", "Licese Terms"))

