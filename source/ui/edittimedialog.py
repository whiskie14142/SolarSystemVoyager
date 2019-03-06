# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edittimedialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_edittimedialog(object):
    def setupUi(self, edittimedialog):
        edittimedialog.setObjectName("edittimedialog")
        edittimedialog.setWindowModality(QtCore.Qt.ApplicationModal)
        edittimedialog.resize(470, 150)
        edittimedialog.setMinimumSize(QtCore.QSize(470, 150))
        edittimedialog.setMaximumSize(QtCore.QSize(470, 150))
        edittimedialog.setModal(True)
        self.cancelbutton = QtWidgets.QPushButton(edittimedialog)
        self.cancelbutton.setGeometry(QtCore.QRect(370, 120, 75, 23))
        self.cancelbutton.setAutoDefault(False)
        self.cancelbutton.setObjectName("cancelbutton")
        self.finishbutton = QtWidgets.QPushButton(edittimedialog)
        self.finishbutton.setGeometry(QtCore.QRect(180, 120, 101, 23))
        self.finishbutton.setAutoDefault(False)
        self.finishbutton.setObjectName("finishbutton")
        self.radioISOT = QtWidgets.QRadioButton(edittimedialog)
        self.radioISOT.setGeometry(QtCore.QRect(40, 27, 111, 16))
        self.radioISOT.setChecked(True)
        self.radioISOT.setObjectName("radioISOT")
        self.radioJD = QtWidgets.QRadioButton(edittimedialog)
        self.radioJD.setGeometry(QtCore.QRect(40, 57, 111, 16))
        self.radioJD.setObjectName("radioJD")
        self.radioDuration = QtWidgets.QRadioButton(edittimedialog)
        self.radioDuration.setEnabled(False)
        self.radioDuration.setGeometry(QtCore.QRect(40, 87, 111, 16))
        self.radioDuration.setObjectName("radioDuration")
        self.lineEditISOT = QtWidgets.QLineEdit(edittimedialog)
        self.lineEditISOT.setGeometry(QtCore.QRect(150, 27, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.lineEditISOT.setFont(font)
        self.lineEditISOT.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEditISOT.setObjectName("lineEditISOT")
        self.lineEditJD = QtWidgets.QLineEdit(edittimedialog)
        self.lineEditJD.setEnabled(False)
        self.lineEditJD.setGeometry(QtCore.QRect(150, 57, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.lineEditJD.setFont(font)
        self.lineEditJD.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEditJD.setObjectName("lineEditJD")
        self.lineEditDuration = QtWidgets.QLineEdit(edittimedialog)
        self.lineEditDuration.setEnabled(False)
        self.lineEditDuration.setGeometry(QtCore.QRect(150, 87, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.lineEditDuration.setFont(font)
        self.lineEditDuration.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEditDuration.setObjectName("lineEditDuration")
        self.labelISOT = QtWidgets.QLabel(edittimedialog)
        self.labelISOT.setGeometry(QtCore.QRect(153, 11, 201, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.labelISOT.setFont(font)
        self.labelISOT.setObjectName("labelISOT")

        self.retranslateUi(edittimedialog)
        QtCore.QMetaObject.connectSlotsByName(edittimedialog)
        edittimedialog.setTabOrder(self.radioISOT, self.radioJD)
        edittimedialog.setTabOrder(self.radioJD, self.radioDuration)
        edittimedialog.setTabOrder(self.radioDuration, self.lineEditISOT)
        edittimedialog.setTabOrder(self.lineEditISOT, self.lineEditJD)
        edittimedialog.setTabOrder(self.lineEditJD, self.lineEditDuration)
        edittimedialog.setTabOrder(self.lineEditDuration, self.finishbutton)
        edittimedialog.setTabOrder(self.finishbutton, self.cancelbutton)

    def retranslateUi(self, edittimedialog):
        _translate = QtCore.QCoreApplication.translate
        edittimedialog.setWindowTitle(_translate("edittimedialog", "Date and Time Editor"))
        self.cancelbutton.setText(_translate("edittimedialog", "Cancel"))
        self.finishbutton.setText(_translate("edittimedialog", "Finish"))
        self.radioISOT.setText(_translate("edittimedialog", "Edit by ISOT"))
        self.radioJD.setText(_translate("edittimedialog", "Edit by JD"))
        self.radioDuration.setText(_translate("edittimedialog", "Edit by Duration"))
        self.labelISOT.setText(_translate("edittimedialog", "yyyy-mm-ddThh:mm:ss.ssss"))

