# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'descriptioneditor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DescriptionEditor(object):
    def setupUi(self, DescriptionEditor):
        DescriptionEditor.setObjectName("DescriptionEditor")
        DescriptionEditor.resize(600, 216)
        DescriptionEditor.setMinimumSize(QtCore.QSize(600, 216))
        DescriptionEditor.setMaximumSize(QtCore.QSize(600, 216))
        DescriptionEditor.setAcceptDrops(False)
        self.description = QtWidgets.QPlainTextEdit(DescriptionEditor)
        self.description.setGeometry(QtCore.QRect(10, 30, 581, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.description.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.description.setAcceptDrops(True)
        self.description.setToolTipDuration(1500)
        self.description.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.description.setDocumentTitle("")
        self.description.setUndoRedoEnabled(True)
        self.description.setReadOnly(False)
        self.description.setPlainText("")
        self.description.setObjectName("description")
        self.copyButton = QtWidgets.QPushButton(DescriptionEditor)
        self.copyButton.setGeometry(QtCore.QRect(0, 0, 70, 23))
        self.copyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.copyButton.setAutoDefault(False)
        self.copyButton.setObjectName("copyButton")
        self.cutButton = QtWidgets.QPushButton(DescriptionEditor)
        self.cutButton.setGeometry(QtCore.QRect(70, 0, 70, 23))
        self.cutButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cutButton.setAutoDefault(False)
        self.cutButton.setObjectName("cutButton")
        self.pasteButton = QtWidgets.QPushButton(DescriptionEditor)
        self.pasteButton.setGeometry(QtCore.QRect(140, 0, 70, 23))
        self.pasteButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pasteButton.setAutoDefault(False)
        self.pasteButton.setObjectName("pasteButton")
        self.undoButton = QtWidgets.QPushButton(DescriptionEditor)
        self.undoButton.setEnabled(False)
        self.undoButton.setGeometry(QtCore.QRect(230, 0, 70, 23))
        self.undoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.undoButton.setAutoDefault(False)
        self.undoButton.setObjectName("undoButton")
        self.redoButton = QtWidgets.QPushButton(DescriptionEditor)
        self.redoButton.setEnabled(False)
        self.redoButton.setGeometry(QtCore.QRect(300, 0, 70, 23))
        self.redoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.redoButton.setAutoDefault(False)
        self.redoButton.setObjectName("redoButton")

        self.retranslateUi(DescriptionEditor)
        self.copyButton.clicked.connect(self.description.copy)
        self.cutButton.clicked.connect(self.description.cut)
        self.pasteButton.clicked.connect(self.description.paste)
        self.undoButton.clicked.connect(self.description.undo)
        self.redoButton.clicked.connect(self.description.redo)
        QtCore.QMetaObject.connectSlotsByName(DescriptionEditor)

    def retranslateUi(self, DescriptionEditor):
        _translate = QtCore.QCoreApplication.translate
        DescriptionEditor.setWindowTitle(_translate("DescriptionEditor", "Maneuver Description Editor"))
        self.description.setToolTip(_translate("DescriptionEditor", "Edit the description"))
        self.description.setPlaceholderText(_translate("DescriptionEditor", "No description"))
        self.copyButton.setToolTip(_translate("DescriptionEditor", "Copy selected characters into clipboard"))
        self.copyButton.setText(_translate("DescriptionEditor", "Copy"))
        self.cutButton.setToolTip(_translate("DescriptionEditor", "Cut selected characters and store into clipboard"))
        self.cutButton.setText(_translate("DescriptionEditor", "Cut"))
        self.pasteButton.setToolTip(_translate("DescriptionEditor", "Paste characters from clipboard"))
        self.pasteButton.setText(_translate("DescriptionEditor", "Paste"))
        self.undoButton.setToolTip(_translate("DescriptionEditor", "Undo latest operation"))
        self.undoButton.setText(_translate("DescriptionEditor", "Undo"))
        self.redoButton.setToolTip(_translate("DescriptionEditor", "Redo latest undone operation"))
        self.redoButton.setText(_translate("DescriptionEditor", "Redo"))

