# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editmandialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_editmandialog(object):
    def setupUi(self, editmandialog):
        editmandialog.setObjectName("editmandialog")
        editmandialog.setWindowModality(QtCore.Qt.WindowModal)
        editmandialog.resize(640, 320)
        editmandialog.setMinimumSize(QtCore.QSize(640, 320))
        editmandialog.setMaximumSize(QtCore.QSize(640, 320))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        editmandialog.setFont(font)
        editmandialog.setModal(True)
        self.label = QtWidgets.QLabel(editmandialog)
        self.label.setGeometry(QtCore.QRect(390, 4, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.mantype = QtWidgets.QComboBox(editmandialog)
        self.mantype.setGeometry(QtCore.QRect(390, 24, 111, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mantype.setFont(font)
        self.mantype.setMaxVisibleItems(7)
        self.mantype.setFrame(True)
        self.mantype.setObjectName("mantype")
        self.label_time = QtWidgets.QLabel(editmandialog)
        self.label_time.setGeometry(QtCore.QRect(20, 8, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_time.setFont(font)
        self.label_time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_time.setObjectName("label_time")
        self.label_5 = QtWidgets.QLabel(editmandialog)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.parameters = QtWidgets.QTableWidget(editmandialog)
        self.parameters.setGeometry(QtCore.QRect(20, 120, 352, 162))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameters.setFont(font)
        self.parameters.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.parameters.setCornerButtonEnabled(False)
        self.parameters.setRowCount(8)
        self.parameters.setColumnCount(2)
        self.parameters.setObjectName("parameters")
        self.parameters.horizontalHeader().setVisible(False)
        self.parameters.verticalHeader().setVisible(False)
        self.parameters.verticalHeader().setDefaultSectionSize(20)
        self.parameters.verticalHeader().setMinimumSectionSize(20)
        self.finishbutton = QtWidgets.QPushButton(editmandialog)
        self.finishbutton.setGeometry(QtCore.QRect(330, 290, 101, 23))
        self.finishbutton.setAutoDefault(False)
        self.finishbutton.setObjectName("finishbutton")
        self.cancelbutton = QtWidgets.QPushButton(editmandialog)
        self.cancelbutton.setGeometry(QtCore.QRect(530, 290, 91, 23))
        self.cancelbutton.setAutoDefault(False)
        self.cancelbutton.setObjectName("cancelbutton")
        self.showorbit = QtWidgets.QPushButton(editmandialog)
        self.showorbit.setEnabled(False)
        self.showorbit.setGeometry(QtCore.QRect(530, 80, 91, 23))
        self.showorbit.setAutoDefault(False)
        self.showorbit.setObjectName("showorbit")
        self.computeFTA = QtWidgets.QPushButton(editmandialog)
        self.computeFTA.setEnabled(False)
        self.computeFTA.setGeometry(QtCore.QRect(530, 120, 91, 23))
        self.computeFTA.setAutoDefault(False)
        self.computeFTA.setObjectName("computeFTA")
        self.finish_exec = QtWidgets.QPushButton(editmandialog)
        self.finish_exec.setEnabled(False)
        self.finish_exec.setGeometry(QtCore.QRect(200, 290, 101, 23))
        self.finish_exec.setAutoDefault(False)
        self.finish_exec.setObjectName("finish_exec")
        self.optimize = QtWidgets.QPushButton(editmandialog)
        self.optimize.setEnabled(False)
        self.optimize.setGeometry(QtCore.QRect(530, 160, 91, 23))
        self.optimize.setAutoDefault(False)
        self.optimize.setObjectName("optimize")
        self.label_Click = QtWidgets.QLabel(editmandialog)
        self.label_Click.setGeometry(QtCore.QRect(506, 24, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_Click.setFont(font)
        self.label_Click.setObjectName("label_Click")
        self.sysMessage = QtWidgets.QPlainTextEdit(editmandialog)
        self.sysMessage.setGeometry(QtCore.QRect(388, 210, 239, 71))
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
        self.frameDT = QtWidgets.QFrame(editmandialog)
        self.frameDT.setGeometry(QtCore.QRect(20, 24, 351, 71))
        self.frameDT.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameDT.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameDT.setLineWidth(1)
        self.frameDT.setObjectName("frameDT")
        self.EditDateTime = QtWidgets.QPushButton(self.frameDT)
        self.EditDateTime.setEnabled(True)
        self.EditDateTime.setGeometry(QtCore.QRect(250, 40, 91, 23))
        self.EditDateTime.setAutoDefault(False)
        self.EditDateTime.setObjectName("EditDateTime")
        self.label_4 = QtWidgets.QLabel(self.frameDT)
        self.label_4.setGeometry(QtCore.QRect(20, 28, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.duration = QtWidgets.QLineEdit(self.frameDT)
        self.duration.setEnabled(True)
        self.duration.setGeometry(QtCore.QRect(110, 48, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.duration.setFont(font)
        self.duration.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.duration.setToolTip("")
        self.duration.setFrame(False)
        self.duration.setReadOnly(True)
        self.duration.setObjectName("duration")
        self.label_duration = QtWidgets.QLabel(self.frameDT)
        self.label_duration.setEnabled(True)
        self.label_duration.setGeometry(QtCore.QRect(10, 48, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_duration.setFont(font)
        self.label_duration.setTextFormat(QtCore.Qt.PlainText)
        self.label_duration.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_duration.setObjectName("label_duration")
        self.isotedit = QtWidgets.QLineEdit(self.frameDT)
        self.isotedit.setGeometry(QtCore.QRect(110, 8, 191, 17))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(9)
        self.isotedit.setFont(font)
        self.isotedit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.isotedit.setToolTip("")
        self.isotedit.setFrame(False)
        self.isotedit.setReadOnly(True)
        self.isotedit.setObjectName("isotedit")
        self.jdedit = QtWidgets.QLineEdit(self.frameDT)
        self.jdedit.setGeometry(QtCore.QRect(110, 28, 121, 17))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.jdedit.setFont(font)
        self.jdedit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.jdedit.setToolTip("")
        self.jdedit.setFrame(False)
        self.jdedit.setReadOnly(True)
        self.jdedit.setObjectName("jdedit")
        self.label_3 = QtWidgets.QLabel(self.frameDT)
        self.label_3.setGeometry(QtCore.QRect(20, 8, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_24 = QtWidgets.QLabel(editmandialog)
        self.label_24.setGeometry(QtCore.QRect(390, 192, 131, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.manTypeDesc = QtWidgets.QPlainTextEdit(editmandialog)
        self.manTypeDesc.setGeometry(QtCore.QRect(390, 54, 121, 121))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.manTypeDesc.setPalette(palette)
        self.manTypeDesc.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.manTypeDesc.setFocusPolicy(QtCore.Qt.NoFocus)
        self.manTypeDesc.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.manTypeDesc.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.manTypeDesc.setUndoRedoEnabled(False)
        self.manTypeDesc.setReadOnly(True)
        self.manTypeDesc.setPlaceholderText("")
        self.manTypeDesc.setObjectName("manTypeDesc")

        self.retranslateUi(editmandialog)
        QtCore.QMetaObject.connectSlotsByName(editmandialog)
        editmandialog.setTabOrder(self.mantype, self.showorbit)
        editmandialog.setTabOrder(self.showorbit, self.computeFTA)
        editmandialog.setTabOrder(self.computeFTA, self.optimize)
        editmandialog.setTabOrder(self.optimize, self.EditDateTime)
        editmandialog.setTabOrder(self.EditDateTime, self.finish_exec)
        editmandialog.setTabOrder(self.finish_exec, self.finishbutton)
        editmandialog.setTabOrder(self.finishbutton, self.cancelbutton)

    def retranslateUi(self, editmandialog):
        _translate = QtCore.QCoreApplication.translate
        editmandialog.setWindowTitle(_translate("editmandialog", "Maneuver Editor"))
        self.label.setText(_translate("editmandialog", "Maneuver Type"))
        self.mantype.setToolTip(_translate("editmandialog", "Click and Select a Maneuver type"))
        self.label_time.setText(_translate("editmandialog", "Date & Time"))
        self.label_5.setText(_translate("editmandialog", "Parameters"))
        self.parameters.setToolTip(_translate("editmandialog", "Click a Cell to Edit"))
        self.finishbutton.setToolTip(_translate("editmandialog", "Finish editing the Maneuver"))
        self.finishbutton.setText(_translate("editmandialog", "Finish"))
        self.cancelbutton.setToolTip(_translate("editmandialog", "Discard Changes and Quit Editing"))
        self.cancelbutton.setText(_translate("editmandialog", "Cancel"))
        self.showorbit.setToolTip(_translate("editmandialog", "Apply current Parameters"))
        self.showorbit.setText(_translate("editmandialog", "SHOW Orbit"))
        self.computeFTA.setToolTip(_translate("editmandialog", "Invoke FTA Function"))
        self.computeFTA.setText(_translate("editmandialog", "FTA"))
        self.finish_exec.setToolTip(_translate("editmandialog", "Finish Editing and Execute the Maneuver"))
        self.finish_exec.setText(_translate("editmandialog", "Finish and Exec"))
        self.optimize.setToolTip(_translate("editmandialog", "Invoke Optimize Assistant"))
        self.optimize.setText(_translate("editmandialog", "OPTIMIZE"))
        self.label_Click.setText(_translate("editmandialog", "Click & Select"))
        self.sysMessage.setToolTip(_translate("editmandialog", "System Messages"))
        self.EditDateTime.setToolTip(_translate("editmandialog", "Edit Date & Time"))
        self.EditDateTime.setText(_translate("editmandialog", "Edit Time"))
        self.label_4.setText(_translate("editmandialog", "JD"))
        self.label_duration.setText(_translate("editmandialog", "Duration (days)"))
        self.label_3.setText(_translate("editmandialog", "ISOT"))
        self.label_24.setText(_translate("editmandialog", "Messages"))

