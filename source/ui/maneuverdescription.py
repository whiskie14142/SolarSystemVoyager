# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maneuverdescription.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ManeuverDescription(object):
    def setupUi(self, ManeuverDescription):
        ManeuverDescription.setObjectName("ManeuverDescription")
        ManeuverDescription.resize(600, 216)
        ManeuverDescription.setMinimumSize(QtCore.QSize(600, 216))
        ManeuverDescription.setMaximumSize(QtCore.QSize(600, 216))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        ManeuverDescription.setFont(font)
        self.type_and_line = QtWidgets.QLabel(ManeuverDescription)
        self.type_and_line.setGeometry(QtCore.QRect(10, 6, 341, 16))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(11)
        self.type_and_line.setFont(font)
        self.type_and_line.setText("Maneuver Type and Line Number")
        self.type_and_line.setObjectName("type_and_line")
        self.description = QtWidgets.QPlainTextEdit(ManeuverDescription)
        self.description.setGeometry(QtCore.QRect(10, 30, 581, 181))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.description.setAcceptDrops(False)
        self.description.setToolTip("")
        self.description.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.description.setDocumentTitle("")
        self.description.setUndoRedoEnabled(False)
        self.description.setReadOnly(True)
        self.description.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.description.setObjectName("description")
        self.editButton = QtWidgets.QPushButton(ManeuverDescription)
        self.editButton.setGeometry(QtCore.QRect(465, 3, 111, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.editButton.setFont(font)
        self.editButton.setAutoDefault(False)
        self.editButton.setObjectName("editButton")

        self.retranslateUi(ManeuverDescription)
        QtCore.QMetaObject.connectSlotsByName(ManeuverDescription)

    def retranslateUi(self, ManeuverDescription):
        _translate = QtCore.QCoreApplication.translate
        ManeuverDescription.setWindowTitle(_translate("ManeuverDescription", "Maneuver Description"))
        self.description.setPlaceholderText(_translate("ManeuverDescription", "No description"))
        self.editButton.setToolTip(_translate("ManeuverDescription", "Start editing of the description"))
        self.editButton.setText(_translate("ManeuverDescription", "Edit Description"))

