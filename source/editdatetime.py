# -*- coding: utf-8 -*-
"""
editdatetime module for editmaneuver module of SSVG (Solar System Voyager)
(c) 2016-2018 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import common

from ui.edittimedialog import *

from globaldata import *
# Import followings
#     g : container of global data
#     erase_Ptrj()
#     draw_Ptrj()
#     erase_PKepler()
#     draw_PKepler()
#     erase_TKepler()
#     draw_TKepler()
#     remove_planets()
#     replot_planets(jd)
#     remove_time()
#     replot_time(jd, ttype='')
#     nowtimestr()
#     nowtimestrf()


class EditDateTimeDialog(QDialog):
    """class for the dialog to specity parameters for FTA
    """
    
    def __init__(self, parent=None, orgjd=0.0, fromjd=0.0, tojd=0.0, duration=False):
        super().__init__(parent)
        self.ui = Ui_edittimedialog()
        self.ui.setupUi(self)
        self.ui.radioISOT.clicked.connect(self.radioclicked)
        self.ui.radioJD.clicked.connect(self.radioclicked)
        self.ui.radioDuration.clicked.connect(self.radioclicked)
        self.ui.finishbutton.clicked.connect(self.finish_clicked)
        self.ui.cancelbutton.clicked.connect(self.reject)
        
        self.orgjd = orgjd
        self.fromjd = fromjd
        self.tojd = tojd
        self.activateDuration = duration
        self.maneuverEditor = parent

        self.ui.lineEditISOT.setText(common.jd2isot(self.orgjd))
        self.ui.lineEditJD.setText('{:.8f}'.format(self.orgjd))
        if self.activateDuration:
            self.ui.radioDuration.setEnabled(True)
            dt = self.orgjd - g.myprobe.jd
            self.ui.lineEditDuration.setText('{:.8f}'.format(dt))
        
    def radioclicked(self):
        if self.ui.radioISOT.isChecked():
            self.ui.lineEditISOT.setEnabled(True)
            self.ui.labelISOT.setEnabled(True)
            self.ui.lineEditJD.setEnabled(False)
            self.ui.lineEditDuration.setEnabled(False)
        elif self.ui.radioJD.isChecked():
            self.ui.lineEditISOT.setEnabled(False)
            self.ui.labelISOT.setEnabled(False)
            self.ui.lineEditJD.setEnabled(True)
            self.ui.lineEditDuration.setEnabled(False)
        elif self.ui.radioDuration.isChecked():
            self.ui.lineEditISOT.setEnabled(False)
            self.ui.labelISOT.setEnabled(False)
            self.ui.lineEditJD.setEnabled(False)
            self.ui.lineEditDuration.setEnabled(True)

    
    def finish_clicked(self):
        if self.ui.radioISOT.isChecked():
            try:
                jd = common.isot2jd(self.ui.lineEditISOT.text())
            except ValueError:
                QMessageBox.critical(self, 'Error', 'Invalid ISOT', 
                                        QMessageBox.Ok)
                return
            
            if jd < self.fromjd or jd >= self.tojd:
                mes = ('ISOT is out of range.\nIn this Flight Plan, ' + 
                       'ISOT should be in following range:\n from {0}\n' +
                       ' to   {1}').format(
                        common.jd2isot(self.fromjd), common.jd2isot(self.tojd))
                QMessageBox.critical(self, 'Error', mes, QMessageBox.Ok)
                return

        elif self.ui.radioJD.isChecked():
            try:
                jd = float(self.ui.lineEditJD.text())
            except ValueError:
                QMessageBox.critical(self, 'Error', 'Invalid JD', 
                                     QMessageBox.Ok)
                return
            if jd < self.fromjd or jd >= self.tojd:
                mes = ('JD is out of range.\nIn this Flight Plan, ' + 
                       'JD should be in following range:\n from {0:.2f}\n' +
                       ' to   {1:.2f}').format(self.fromjd, self.tojd)
                QMessageBox.critical(self, 'Error', mes, QMessageBox.Ok)
                return
            
        elif self.ui.radioDuration.isChecked():
            try:
                dt = float(self.ui.lineEditDuration.text())
            except ValueError:
                QMessageBox.critical(self, 'Error', 'Invalid Duration', 
                                     QMessageBox.Ok)
                return
            if dt < 0.0:
                QMessageBox.critical(self, 'Error', 'Duration should be positive', 
                                     QMessageBox.Ok)
                return
            jd = dt + g.myprobe.jd
            if jd >= self.tojd:
                mes = 'Duration is too large.\nIn this case, Duration ' + \
                    'should less than {:.2f}'.format(self.tojd - g.myprobe.jd)
                QMessageBox.critical(self, 'Error', mes, QMessageBox.Ok)
                return

        self.maneuverEditor.editedjd = jd
        self.accept()
