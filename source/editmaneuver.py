# -*- coding: utf-8 -*-
"""
editmaneuver module for SSVG (Solar System Voyager)
(c) 2016-2018 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import math
from datetime import datetime
import julian

import common
from ftasetting import FTAsettingDialog
from optimize import StartOptimizeDialog
from optimize import CpOptimizeDialog

from ui.editmandialog import *
from showorbit import ShowOrbitDialog
from showorbit import ShowStartOrbitDialog

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


class EditManDialog(QDialog):
    """class for 'Edit Maneuver' dialog
    """
    
    def __init__(self, parent=None, editman=None, currentrow=0):
        super().__init__(parent)
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+380, 640, 320)
        self.ui = Ui_editmandialog()
        self.ui.setupUi(self)
        self.ui.applymantype.clicked.connect(self.applymantype)
        self.ui.isotedit.editingFinished.connect(self.isotedited)
        self.ui.jdedit.editingFinished.connect(self.jdedited)
        self.ui.parameters.cellChanged.connect(self.parameterchanged)
        self.ui.finish_exec.clicked.connect(self.finish_exec)
        self.ui.finishbutton.clicked.connect(self.finishbutton)
        self.ui.cancelbutton.clicked.connect(self.cancelbutton)
        self.ui.showorbit.clicked.connect(self.showorbit)
        self.ui.computeFTA.clicked.connect(self.computefta)
        self.ui.optimize.clicked.connect(self.optimize)
        self.ui.applyduration.clicked.connect(self.applyduration)
        
        self.types = ['START', 'CP', 'EP_ON', 'EP_OFF', 'SS_ON', 'SS_OFF', 
                      'FLYTO']
        self.typedict = {}
        for i in range(7):
            self.typedict[self.types[i]] = i
        self.paramname = ['time', 'dv', 'dvpd', 'phi', 'elv', 'aria', 'theta', 
                          'tvmode', 'inter']
        self.paramflag = [
            # 0:time, 1:dv, 2:dvpd, 3:phi, 4:elv, 5:aria, 6:theta, 7:tvmode, 8:inter
            [1, 1, 0, 1, 1, 0, 0, 0, 0], # for START
            [0, 1, 0, 1, 1, 0, 0, 0, 0], # for CP
            [0, 0, 1, 1, 1, 0, 0, 1, 0], # for EP_ON
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # for EP_OFF
            [0, 0, 0, 0, 1, 1, 1, 1, 0], # for SS_ON
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # for SS_OFF
            [1, 0, 0, 0, 0, 0, 0, 0, 1]  # for FLYTO
            ]
        paramdesc = [
            'time  : Maneuver Time (JD)',
            'dv      : magnitude of delta-V (m/s)',
            'dvpd  : magnitude of delta-V per day (m/s/day)',
            'phi     : angle phi (deg)',
            'elv     : angle elv (deg)',
            'aria    : area of solar sail (m**2)',
            'theta : angle theta (deg)',
            'tvmode : thrust vector mode (L|E)',
            'inter : integration interval (days)'
            ]
        self.timedesc = ['Start Time', '', '', '', '', '', 'End Time']
        self.fmttbl = [
            '{:.8f}',
            '{:.3f}',
            '{:.3f}',
            '{:.2f}',
            '{:.2f}',
            '{:.1f}',
            '{:.2f}',
            '{}',
            '{:.5f}'
            ]
        self.stringitems = []
        
        self.mes1 = 'You requested to apply parameters optimized for the time\n'
        self.mes2 = '  to the editing Maneuver.\n\n' \
            'Applied Maneuver should be executed at that time.  ' \
            'You need to adjust preceding Maneuver(s) before execution of '   \
            'this Maneuver.\n\n' \
            'The time has been copied to system clipboard.'
        
        for item in paramdesc:
            self.stringitems.append(QTableWidgetItem(item))
        
        for item in self.types:
            self.ui.mantype.addItem(item)
        self.ui.parameters.setColumnWidth(0,277)
        self.ui.parameters.setColumnWidth(1,237)
        for i in range(1, 9):
            row = i - 1
            self.ui.parameters.setItem(row, 0, self.stringitems[i])
            self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
        
        self.currentrow = currentrow
        if editman is None:
            self.editman = None
            self.dispman()
        else:
            self.editman = editman.copy()
            self.dispman()
        self.setenable()

    def setenable(self):
        self.ui.computeFTA.setEnabled(False)
        self.ui.optimize.setEnabled(False)
        self.ui.showorbit.setEnabled(False)
        self.ui.finish_exec.setEnabled(False)
        self.ui.duration.setEnabled(False)
        self.ui.applyduration.setEnabled(False)
        self.ui.label_duration.setEnabled(False)
        self.ui.finishbutton.setEnabled(False)
        if self.editman is None: return
            
        self.ui.finishbutton.setEnabled(True)
        
        ftaandopt = (self.typeID == 0 and self.currentrow == 0) or \
            (self.typeID == 1 and self.currentrow == g.nextman and 
            g.myprobe.onflight)
        if ftaandopt:
            self.ui.computeFTA.setEnabled(True)
            self.ui.optimize.setEnabled(True)

        buttons = (self.typeID == 0 and self.currentrow == 0) or \
            (self.currentrow == g.nextman and g.myprobe.onflight)
        if buttons:
            self.ui.showorbit.setEnabled(True)
            self.ui.finish_exec.setEnabled(True)
            
        duration = self.typeID == 6 and self.currentrow == g.nextman and \
            g.myprobe.onflight
        if duration:
            self.ui.duration.setEnabled(True)
            self.ui.applyduration.setEnabled(True)
            self.ui.label_duration.setEnabled(True)
        
        if buttons:
            self.showorbit()
        
    def initman(self, typeID):
        dt = datetime.now()
        jdtoday = julian.to_jd(dt, fmt='jd')
        jdtoday = int(jdtoday + 0.5) - 0.5
        ival = [jdtoday, 0.0, 0.0, 0.0, 0.0, 10000.0, 35.26, 'L', 1.0]
        if g.myprobe is not None:
            if g.myprobe.onflight:
                ival[0] = g.myprobe.jd
        self.editman = {}
        self.editman['type'] = self.types[typeID]
        for i in range(9):
            if self.paramflag[typeID][i] == 1:
                self.editman[self.paramname[i]] = ival[i]
        
    def dispman(self):
        if self.editman is None:
            self.ui.mantype.setCurrentIndex(-1)
            self.ui.mantypedisp.setText('Not Defined')
            self.ui.isotedit.setEnabled(False)
            self.ui.jdedit.setEnabled(False)
            for i in range(1, 9):
                row = i - 1
                self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
        else:
            self.typeID = self.typedict[self.editman['type']]
            self.ui.mantype.setCurrentIndex(self.typeID)
            self.ui.mantypedisp.setText(self.editman['type'])
            self.ui.label_time.setText(self.timedesc[self.typeID])
            if self.paramflag[self.typeID][0] == 1:
                jd = self.editman[self.paramname[0]]
                self.ui.jdedit.setText(self.fmttbl[0].format(jd))
                self.ui.jdedit.setEnabled(True)
                self.ui.isotedit.setText(common.jd2isot(jd))
                self.ui.isotedit.setEnabled(True)
                if self.typeID == 6 and self.currentrow == g.nextman and \
                        g.myprobe.onflight:
                    self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
            else:
                self.ui.jdedit.setEnabled(False)
                self.ui.isotedit.setEnabled(False)

            self.ui.parameters.cellChanged.disconnect()
            
            for i in range(1, 9):
                row = i - 1
                if self.paramflag[self.typeID][i] == 1:
                    anitem = QTableWidgetItem(self.fmttbl[i].format(
                        self.editman[self.paramname[i]]))
                    self.ui.parameters.setItem(row, 1, anitem)
                    self.ui.parameters.item(row, 1).setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEditable | 
                        Qt.ItemIsEnabled)
                    self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
                else:
                    anitem = QTableWidgetItem('')
                    self.ui.parameters.setItem(row, 1, anitem)
                    self.ui.parameters.item(row, 1).setFlags(Qt.NoItemFlags)
                    self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
    
            self.ui.parameters.cellChanged.connect(self.parameterchanged)
                
    def applymantype(self):
        newID = self.ui.mantype.currentIndex()
        if self.editman is None:
            self.initman(newID)
            self.dispman()
            if g.showorbitcontrol is not None:
                g.showorbitcontrol.close()
            self.setenable()
            
        if self.typeID == newID:
            return
        ans = QMessageBox.question(self, 
            'Mantype changed', 'Parameters will be lost. OK?', 
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if ans == QMessageBox.Ok :
            self.initman(newID)
            self.dispman()
            if g.showorbitcontrol is not None:
                g.showorbitcontrol.close()
            self.setenable()
        else:
            self.ui.mantype.setCurrentIndex(self.typeID)
        
    def isotedited(self):
        try:
            jd = common.isot2jd(self.ui.isotedit.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid ISOT', 
                                    QMessageBox.Ok)
            self.ui.isotedit.setText(common.jd2isot(
                float(self.ui.jdedit.text())))
            return
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        if self.ui.duration.isEnabled():
            self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
        self.editman[self.paramname[0]] = jd
        
    def jdedited(self):
        try:
            jd = float(self.ui.jdedit.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid JD', QMessageBox.Ok)
            self.ui.jdedit.setText('{:.8f}'.format(
                common.isot2jd(self.ui.isotedit.text())))
            return
        self.ui.isotedit.setText(common.jd2isot(jd))
        if self.ui.duration.isEnabled():
            self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
        self.editman[self.paramname[0]] = jd
        
    def parameterchanged(self, row, colmn):
        if colmn != 1: return
        prevval = self.editman[self.paramname[row+1]]
        if self.paramname[row+1] == 'tvmode':
            newval = self.ui.parameters.item(row, colmn).text().upper()
            if newval != 'L' and newval != 'E':
                self.ui.parameters.item(row, colmn).setText(
                    self.fmttbl[row+1].format(prevval))
                QMessageBox.critical(self, 
                    'Error', 'Enter L or E for tvmode', QMessageBox.Ok)
                return
        else:
            try:
                newval = float(self.ui.parameters.item(row, colmn).text())
            except ValueError:
                self.ui.parameters.item(row, colmn).setText(
                    self.fmttbl[row+1].format(prevval))
                QMessageBox.critical(self, 
                    'Error', 'Enter a floating number', QMessageBox.Ok)
                return
        self.editman[self.paramname[row+1]] = newval

    def finish_exec(self):
        g.editedman = self.editman
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.done(g.finish_exec)
        
    def finishbutton(self):
        g.editedman = self.editman
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.accept()
        
    def cancelbutton(self):
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.reject()

    def writeloglines(self):
        if not g.options['log']:
            return
        logstring = []
        logstring.append('finish maneuver editing: ' + nowtimestr() + '\n')
        logstring.append('    type: ' + self.editman['type'] + '\n')
        ix = self.typedict[self.editman['type']]
        if self.paramflag[ix][0] == 1:
            isot = common.jd2isot(self.editman['time'])
            logstring.append('    time: ' + isot + '\n')
        for i in range(1, 9):
            if self.paramflag[ix][i] == 1:
                pname = self.paramname[i]
                datastr =self.fmttbl[i].format(self.editman[pname])
                logstring.append('    ' + pname + ': ' + datastr + '\n')
        g.logfile.writelines(logstring)
        
    def closeEvent(self, event):
        ans = QMessageBox.question(self, 'Exit Editor', 'Discard changes?', 
            QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        if ans == QMessageBox.Cancel :
            event.ignore()
            return
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        event.accept()

    def showorbit(self):
        g.mainform.init3Dfigure()
        if self.typeID == 1:
            self.showorbitCP()
        elif self.typeID == 0:
            self.showorbitSTART()
        elif self.typeID == 6:
            self.showorbitFLYTO()
        else:
            self.showorbitOTHER()
    
    def showorbitCP(self):
        dv = self.editman['dv']
        phi = self.editman['phi']
        elv = self.editman['elv']
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_pred_dv(dv, phi, elv)
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.set_affect_parent(False)
    
    def showorbitSTART(self):
        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if self.editman['time'] < tsjd or self.editman['time'] >= tejd:
            if g.showorbitcontrol is not None:
                g.showorbitcontrol.close()
            QMessageBox.critical(self, 'Error', 
                'Invalid Start Time\nStart Time is OUTSIDE of ' +
                "Target's time span", QMessageBox.Ok)
            return
    
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowStartOrbitDialog(self, self.editman)
            g.showorbitcontrol.show()
        else:
            g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_affect_parent(False)

    def showorbitFLYTO(self):
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_DT(self.editman['time'])
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(True)
            
    def showorbitOTHER(self):
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_dv(0.0, 0.0, 0.0)
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(False)
        
            
    def computefta(self):
        norm = lambda x : x / np.sqrt(np.dot(x,x))
        if g.showorbitcontrol is None:
            QMessageBox.information(self, 
                'Info', 'To use FTA, open Show Orbit window and\n' 
                + 'try again', QMessageBox.Ok)
            return

        ftadialog = FTAsettingDialog(self)
        ans = ftadialog.exec_()
        if ans == QDialog.Rejected:
            return

        jd = g.fta_parameters[0]
        tpos, tvel = g.mytarget.posvel(jd)
        sunpos, sunvel = common.SPKposvel(10, jd)
        
        if g.fta_parameters[1] == 'OL':
            sr = g.fta_parameters[2][1]
            sphi = g.fta_parameters[2][2]
            selv = g.fta_parameters[2][3]
            vect = common.polar2rect(sr, sphi, selv)
            delta_pos = common.ldv2ecldv(vect, tpos, tvel, sunpos, sunvel)
            tepos = tpos + delta_pos
            try:
                dv, phi, elv = g.showorbitcontrol.tbpred.fta(jd, tepos)
            except ValueError:
                QMessageBox.information(self, 'Info', 
                    'Error occured during FTA computation.\n' 
                    + 'Try different parameters', QMessageBox.Ok)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = 'FTA Results are as follows. Apply them?\n' + \
                'dv = ' + str(dv) + '\n' + \
                'phi = ' + str(phi) + '\n' + \
                'elv = ' + str(elv)
            ans = QMessageBox.question(self, 'FTA Results', mes, 
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ans == QMessageBox.Ok :
                self.editman['dv'] = dv
                self.editman['phi'] = phi
                self.editman['elv'] = elv
                self.dispman()
                self.showorbit()
                
                if g.options['log']:
                    logstring = []
                    logstring.append('apply FTA result: ' + nowtimestr() + '\n')
                    logstring.append('    target: ' + g.mytarget.name + '\n')
                    logstring.append('    time to arrival: ' + 
                                    str(g.fta_parameters[2][0]) + '\n')
                    logstring.append('    Type of Precise Targeting: ' + 
                                    'OL coordinates or Center' + '\n')
                    logstring.append('    offset distance: ' + 
                                    str(g.fta_parameters[2][1]) + '\n')
                    logstring.append('    phi: ' + 
                                    str(g.fta_parameters[2][2]) + '\n')
                    logstring.append('    elv: ' + 
                                    str(g.fta_parameters[2][3]) + '\n')
                    logstring.append('    result dv: ' + str(dv) + '\n')
                    logstring.append('    result phi: ' + str(phi) + '\n')
                    logstring.append('    result elv: ' + str(elv) + '\n')
                    g.logfile.writelines(logstring)

        elif g.fta_parameters[1] == 'BP':
            # compute terminal velocity at Target
            tepos = tpos + np.zeros(3)
            try:
                dv, phi, elv, bc_ivel, bc_tvel              \
                    = g.showorbitcontrol.tbpred.ftavel(jd, tepos)
            except ValueError:
                QMessageBox.information(self, 'Info', 
                    'Error occured during FTA computation.\n' 
                    + 'Try different parameters', QMessageBox.Ok)
                return
            
            # compute B-Plane Unit Vectors
            uSvec = norm(bc_tvel - tvel)
            ss_tpos = tpos - sunpos
            ss_tvel = tvel - sunvel
            hvec = np.cross(ss_tpos, ss_tvel)
            uTvec = norm(np.cross(uSvec, hvec))
            uRvec = norm(np.cross(uSvec, uTvec))
            
            # get Precise Targeting Parameters
            sr = g.fta_parameters[2][1]
            sbeta = g.fta_parameters[2][2]
            rbeta = math.radians(sbeta)
            
            # compute delta_pos
            delta_pos = sr * (np.cos(rbeta) * uTvec + np.sin(rbeta) * uRvec)
            
            # FTA computing
            tepos = tpos + delta_pos
            try:
                dv, phi, elv = g.showorbitcontrol.tbpred.fta(jd, tepos)
            except ValueError:
                QMessageBox.information(self, 'Info', 
                    'Error occured during FTA computation.\n' 
                    + 'Try different parameters', QMessageBox.Ok)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = 'FTA Results are as follows. Apply them?\n' + \
                'dv = ' + str(dv) + '\n' + \
                'phi = ' + str(phi) + '\n' + \
                'elv = ' + str(elv)
            ans = QMessageBox.question(self, 'FTA Results', mes,
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ans == QMessageBox.Ok :
                self.editman['dv'] = dv
                self.editman['phi'] = phi
                self.editman['elv'] = elv
                self.dispman()
                self.showorbit()
                
                if g.options['log']:
                    logstring = []
                    logstring.append('apply FTA result: ' + nowtimestr() + '\n')
                    logstring.append('    target: ' + g.mytarget.name + '\n')
                    logstring.append('    time to arrival: ' + 
                                    str(g.fta_parameters[2][0]) + '\n')
                    logstring.append('    Type of Precise Targeting: ' + 
                                    'BP (B-plane coordinates)' + '\n')
                    logstring.append('    offset distance: ' + 
                                    str(g.fta_parameters[2][1]) + '\n')
                    logstring.append('    beta: ' + 
                                    str(g.fta_parameters[2][2]) + '\n')
                    logstring.append('    result dv: ' + str(dv) + '\n')
                    logstring.append('    result phi: ' + str(phi) + '\n')
                    logstring.append('    result elv: ' + str(elv) + '\n')
                    g.logfile.writelines(logstring)
        
    def optimize(self):
        g.mainform.init3Dfigure()
        if self.typeID == 0:
            self.start_optimize()
        elif self.typeID == 1:
            self.cp_optimize()
            
    def start_optimize(self):
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
            
        orgjd = float(self.ui.jdedit.text())
        dialog = StartOptimizeDialog(orgjd, self)
        ans = dialog.exec_()
        if ans == QDialog.Rejected:
            self.showorbit()
            return
        self.editman['time'] = dialog.result_it
        self.editman['dv'] = dialog.result_dv
        self.editman['phi'] = dialog.result_phi
        self.editman['elv'] = dialog.result_elv
        self.dispman()
        self.showorbit()
        
        if g.options['log']:
            logstring = []
            logstring.append('apply start optimize: ' + nowtimestr() + '\n')
            logstring.append('    start time: ' +
                            common.jd2isot(dialog.result_it) + '\n')
            logstring.append('    target: ' + g.mytarget.name + '\n')
            logstring.append('    dv: ' + str(dialog.result_dv) + '\n')
            logstring.append('    phi: ' + str(dialog.result_phi) + '\n')
            logstring.append('    elv: ' + str(dialog.result_elv) + '\n')
            logstring.append('    arrival time: ' +
                            common.jd2isot(dialog.result_tt) + '\n')
            logstring.append('    flight duration: ' +
                            str(dialog.result_tt - dialog.result_it) + '\n')
            g.logfile.writelines(logstring)
        
    
    def cp_optimize(self):
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
            
        orgjd = g.myprobe.jd
        dialog = CpOptimizeDialog(orgjd, self)
        ans = dialog.exec_()
        if ans == QDialog.Rejected:
            self.showorbit()
            return
        if orgjd != dialog.result_it:
            mantime = common.jd2isot(dialog.result_it)
            g.clipboard.setText(mantime)
            mes = self.mes1 + mantime + self.mes2
            QMessageBox.warning(self, 'Urgent!', mes, QMessageBox.Ok)

        self.editman['dv'] = dialog.result_dv
        self.editman['phi'] = dialog.result_phi
        self.editman['elv'] = dialog.result_elv
        self.dispman()
        self.showorbit()

        if g.options['log']:
            logstring = []
            logstring.append('apply CP optimize: ' + nowtimestr() + '\n')
            logstring.append('    fix maneuver time to current time: ' +
                            str(dialog.fixed_to_ct) + '\n')
            logstring.append('    maneuver time: ' +
                            common.jd2isot(dialog.result_it) + '\n')
            logstring.append('    target: ' + g.mytarget.name + '\n')
            logstring.append('    dv: ' + str(dialog.result_dv) + '\n')
            logstring.append('    phi: ' + str(dialog.result_phi) + '\n')
            logstring.append('    elv: ' + str(dialog.result_elv) + '\n')
            logstring.append('    arrival time: ' +
                            common.jd2isot(dialog.result_tt) + '\n')
            logstring.append('    flight duration: ' +
                            str(dialog.result_tt - dialog.result_it) + '\n')
            g.logfile.writelines(logstring)

    def gettime(self, jd):
        # this method is called from Show Orbit
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        self.jdedited()
        dt = jd - g.myprobe.jd
        self.ui.duration.setText('{:.8f}'.format(dt))

    def applyduration(self):
        try:
            dt = float(self.ui.duration.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid Duration days', 
                                    QMessageBox.Ok)
            self.ui.duration.setText('{:.8f}'.format(
                self.editman[self.paramname[0]] - g.myprobe.jd))
            return
        jd = g.myprobe.jd + dt
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        self.jdedited()
        
