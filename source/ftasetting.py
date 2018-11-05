# -*- coding: utf-8 -*-
"""
ftasetting module for SSVG (Solar System Voyager)
(c) 2016-2018 Shushi Uetsuki (whiskie14142)
"""

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import common

from ui.ftasettingdialog import *

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


class FTAsettingDialog(QDialog):
    """class for the dialog to specity parameters for FTA
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ftasettingdialog()
        self.ui.setupUi(self)
        self.ui.fromshoworbit.clicked.connect(self.ta_radioclicked)
        self.ui.directinput.clicked.connect(self.ta_radioclicked)
        self.ui.selTargetcenter.clicked.connect(self.pt_radioclicked)
        self.ui.selBplanecoord.clicked.connect(self.pt_radioclicked)
        self.ui.selOLcoord.clicked.connect(self.pt_radioclicked)

        self.ui.ok_button.clicked.connect(self.ok_clicked)
        self.ui.cancel_button.clicked.connect(self.reject)
        
        self.ta_radioclicked()
        
    def ta_radioclicked(self):
        if self.ui.fromshoworbit.isChecked():
            ta = g.showorbitcontrol.get_pred_jd() - g.showorbitcontrol.jd
            self.ui.timetoarrival.setText('{:5f}'.format(ta))
            self.ui.timetoarrival.setEnabled(False)
        if self.ui.directinput.isChecked():
            self.ui.timetoarrival.setEnabled(True)

    def pt_radioclicked(self):
        self.ui.Bplanecoords.setEnabled(False)
        self.ui.OLcoords.setEnabled(False)
        if self.ui.selTargetcenter.isChecked():
            return
        elif self.ui.selBplanecoord.isChecked():
            self.ui.Bplanecoords.setEnabled(True)
            return
        elif self.ui.selOLcoord.isChecked():
            self.ui.OLcoords.setEnabled(True)
    
    def ok_clicked(self):
        param = [0.0, '', np.zeros(4)]      # JD(days),Type, [dt, R, phi, elv]
        try:        
            delta_jd = float(self.ui.timetoarrival.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 
                'Enter a floating point number for Time to Arrival.', QMessageBox.Ok)
            return
        if delta_jd < common.minft:
            QMessageBox.critical(self, 'Error', 
                ('To use FTA, Time to Arrival shall be\n' 
                + 'greater than {0:.1f} day').format(common.minft), QMessageBox.Ok)
            return

        if g.showorbitcontrol.jd + delta_jd >= g.mytarget.getendjd():
            QMessageBox.critical(self, 'Error', 
                'Invalid Time to Arrival.\nArrival time is OUTSIDE of ' +
                "Target's time span", QMessageBox.Ok)
            return

        param[0] = g.showorbitcontrol.jd + delta_jd
        
        if self.ui.selBplanecoord.isChecked():
            try:        
                r = float(self.ui.Brangeedit.text()) * 1000.0
                beta = float(self.ui.betaedit.text())
            except ValueError:
                QMessageBox.critical(self, 'Error', 
                                'Parameter should be floating numbers.', QMessageBox.Ok)
                return
        
            param[1] = 'BP'
            param[2][0] = delta_jd
            param[2][1] = r
            param[2][2] = beta
            param[2][3] = 0.0
        
        else:
            if self.ui.selOLcoord.isChecked():
                try:        
                    r = float(self.ui.rangeedit.text()) * 1000.0
                    phi = float(self.ui.phiedit.text())
                    elv = float(self.ui.elvedit.text())
                except ValueError:
                    QMessageBox.critical(self, 'Error', 
                                    'Parameter should be floating numbers.', QMessageBox.Ok)
                    return
            else:
                r = 0.0
                phi = 0.0
                elv = 0.0
            param[1] = 'OL'
            param[2][0] = delta_jd
            param[2][1] = r
            param[2][2] = phi
            param[2][3] = elv
        
        g.fta_parameters = param
        self.accept()
