# -*- coding: utf-8 -*-
"""
editmaneuver module for SSVG (Solar System Voyager)
(c) 2016-2019 Shushi Uetsuki (whiskie14142)
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
from editdatetime import EditDateTimeDialog
from editmandesc import EditManDesc

from globaldata import g, nowtimestr
#     g : container of global data


class EditManDialog(QDialog):
    """class for 'Edit Maneuver' dialog
    """
    
    def __init__(self, parent=None, editman=None, currentrow=0):
        super().__init__(parent)
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+380, 640, 320)
        self.ui = Ui_editmandialog()
        self.ui.setupUi(self)
        self.ui.finish_exec.clicked.connect(self.finish_exec)
        self.ui.finishbutton.clicked.connect(self.finishbutton)
        self.ui.cancelbutton.clicked.connect(self.cancelbutton)
        self.ui.showorbit.clicked.connect(self.showorbitclicked)
        self.ui.computeFTA.clicked.connect(self.computefta)
        self.ui.optimize.clicked.connect(self.optimize)
        self.ui.EditDateTime.clicked.connect(self.editdatetime)
        self.ui.parameters.cellChanged.connect(self.cellChanged)
        
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
        self.roundParam = [     # digits parameters will be rounded to
            3,      # dv
            3,      # dvpd
            2,      # phi
            2,      # elv
            1,      # aria
            2,      # theta
            0,      # (place holder)
            5       # inter
            ]

        self._translate = QtCore.QCoreApplication.translate

        paramdesc = [
            self._translate('editmaneuver.py', 'time  : Maneuver Time (JD)'),
            self._translate('editmaneuver.py', 'dv      : magnitude of delta-V (m/s)'),
            self._translate('editmaneuver.py', 'dvpd  : magnitude of acceleration (m/s/day)'),
            self._translate('editmaneuver.py', 'phi     : angle phi (deg)'),
            self._translate('editmaneuver.py', 'elv     : angle elv (deg)'),
            self._translate('editmaneuver.py', 'aria    : area of solar sail (m**2)'),
            self._translate('editmaneuver.py', 'theta : angle theta (deg)'),
            self._translate('editmaneuver.py', 'tvmode : thrust vector mode (L|E)'),
            self._translate('editmaneuver.py', 'inter : integration interval (days)')
            ]
        self.timedesc = [
                self._translate('editmaneuver.py', 'Start Time'), 
                self._translate('editmaneuver.py', 'Date & Time'), 
                self._translate('editmaneuver.py', 'Date & Time'), 
                self._translate('editmaneuver.py', 'Date & Time'), 
                self._translate('editmaneuver.py', 'Date & Time'), 
                self._translate('editmaneuver.py', 'Date & Time'), 
                self._translate('editmaneuver.py', 'End Time')
                ]
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
        self.manTypeDesc = [
                self._translate('editmaneuver.py', 'that starts the Probe from the Space Base'),
                self._translate('editmaneuver.py', 'that makes orbit transition with Chemical Propulsion Engine'),
                self._translate('editmaneuver.py', 'that turns on the Electric Propulsion Engine'),
                self._translate('editmaneuver.py', 'that turns off the Electric Propulsion Engine'),
                self._translate('editmaneuver.py', 'that turns on the Solar Sail'),
                self._translate('editmaneuver.py', 'that turns off the Solar Sail'),
                self._translate('editmaneuver.py', 'that flies the Probe until specified End Time'),
                ''
            ]
        self.stringitems = []
        
        self.initMessages()

        for item in paramdesc:
            self.stringitems.append(QTableWidgetItem(item))
        
        for item in self.types:
            self.ui.mantype.addItem(item)
        self.ui.parameters.setColumnWidth(0,250)
        self.ui.parameters.setColumnWidth(1,100)
        
        self.ui.parameters.cellChanged.disconnect(self.cellChanged)
        for i in range(1, 9):
            row = i - 1
            self.ui.parameters.setItem(row, 0, self.stringitems[i])
            self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
        self.ui.parameters.cellChanged.connect(self.cellChanged)
        
        self.currentrow = currentrow

        if editman is None:
            if self.currentrow == 0:
                type = 0
                self.initman(type)
                self.ui.mantype.setCurrentIndex(type)
                self.ui.mantype.setEnabled(False)
                self.ui.label_Click.hide()
                self.dispman()
                self.setenable()
            else:
                self.editman = None
                self.ui.mantype.setCurrentIndex(-1)
                self.ui.mantype.setEnabled(True)
                self.ui.label_Click.show()
                self.dispman()
                self.setenable()
                self.ui.mantype.currentIndexChanged.connect(self.mantypeChanged)
        else:
            self.editman = editman.copy()
            self.ui.mantype.setEnabled(False)
            self.ui.label_Click.hide()
            self.dispman()
            self.setenable()

        self.desckeyname = 'description_' + g.i_languagecode
        self.editdescription()
        
    def initMessages(self):
        self.sysMes01 = self._translate('editmaneuver.py', 'Received: Date and Time, from Show Orbit')
        self.sysMes02 = self._translate('editmaneuver.py', 'Received: Results, from FTA')
        self.sysMes03 = self._translate('editmaneuver.py', 'Received: Results, from OPTIMIZE')
        self.sysMes04 = self._translate('editmaneuver.py', 'Edited: Date and Time')
        self.sysMes05 = self._translate('editmaneuver.py', 'Sent: Parameters, to Show Orbit')
        self.sysMes06 = self._translate('editmaneuver.py', 'Edited: Parameter {}')
        self.sysMes07 = self._translate('editmaneuver.py', 'Rounded: Parameter {}')
        
        self.mbTtl01 = self._translate('editmaneuver.py', 'Inappropriate Maneuver Type')
        self.mbMes01 = self._translate('editmaneuver.py', 'START can be used for the first Maneuver only.\n\nSelect another Maneuver Type.')
        self.mbTtl02 = self._translate('editmaneuver.py', 'Inappropriate Parameter')
        self.mbMes02 = self._translate('editmaneuver.py', 'tvmode should be L or E')
        self.mbMes03 = self._translate('editmaneuver.py', '{} should be a floating number')
        self.mbMes04 = self._translate('editmaneuver.py', '{} should be greater than or equal to 0.00001')
        self.mbMes05 = self._translate('editmaneuver.py', '{} should not be a negative value')
        self.mbTtl06 = self._translate('editmaneuver.py', 'Out of Range: Start Time')
        self.mbMes06 = self._translate('editmaneuver.py', "Inappropriate Start Time\nStart Time is OUTSIDE of Target's time span")
        self.mbTtl07 = self._translate('editmaneuver.py', 'Information')
        self.mbMes07 = self._translate('editmaneuver.py', 'To use FTA, open Show Orbit window and try again')
        self.mbMes08 = self._translate('editmaneuver.py', 'Error occured during FTA computation.\nTry different parameters')
        self.mbTtl09 = self._translate('editmaneuver.py', 'Confirm FTA Results')
        self.mbMes09 = self._translate('editmaneuver.py', 'FTA Results are as follows. Apply them?\ndv = {0}\nphi = {1}\nelv = {2}')
        self.mbTtl10 = self._translate('editmaneuver.py', 'Urgent!')
        self.mbMes10 = self._translate('editmaneuver.py', 'You requested to apply parameters optimized for the time\n{}\nto the Maneuver.\n\nApplied Maneuver should be executed at that time.  You need to adjust preceding Maneuver(s) before execution of the Maneuver.\n\nThe time (ISOT format) has been copied to system clipboard.')

    def setenable(self):
        self.ui.computeFTA.setEnabled(False)
        self.ui.optimize.setEnabled(False)
        self.ui.showorbit.setEnabled(False)
        self.ui.finish_exec.setEnabled(False)
        self.ui.finishbutton.setEnabled(False)
        if self.editman is None: return
            
        self.ui.finishbutton.setEnabled(True)
        
        ftaandopt = (self.typeID == 0 and self.currentrow == g.nextman) or \
            (self.typeID == 1 and self.currentrow == g.nextman and 
            g.myprobe.onflight)
        if ftaandopt:
            self.ui.computeFTA.setEnabled(True)
            self.ui.optimize.setEnabled(True)

        buttons = (self.currentrow == g.nextman) and \
                  (g.myprobe.onflight or self.typeID == 0)
        if buttons:
            self.ui.showorbit.setEnabled(True)
            self.ui.finish_exec.setEnabled(True)
            
        duration = self.typeID == 6 and self.currentrow == g.nextman and \
            g.myprobe.onflight
        if duration:
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
        self.ui.parameters.cellChanged.disconnect(self.cellChanged)
        
        if self.editman is None:
            self.typeID = -1
            self.disableDateTime()
            for row in range(8):
                self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
                self.ui.parameters.setItem(row, 1, QTableWidgetItem(''))
                self.ui.parameters.item(row, 1).setFlags(Qt.NoItemFlags)
        else:
            self.typeID = self.typedict[self.editman['type']]
            self.ui.mantype.setCurrentIndex(self.typeID)
            self.ui.label_time.setText(self.timedesc[self.typeID])
            if self.paramflag[self.typeID][0] == 1:
                jd = self.editman[self.paramname[0]]
                duration = False
                if self.typeID == 6 and self.currentrow == g.nextman and \
                        g.myprobe.onflight:
                    duration = True
                self.enableDateTime(jd, duration)
            else:
                self.disableDateTime()

            for row in range(8):
                i = row + 1
                if self.paramflag[self.typeID][i] == 1:
                    anitem = QTableWidgetItem(self.fmttbl[i].format(
                        self.editman[self.paramname[i]]))
                    self.ui.parameters.setItem(row, 1, anitem)
                    self.ui.parameters.item(row, 1).setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEditable | 
                        Qt.ItemIsEnabled)
                    self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
                else:
                    self.ui.parameters.setItem(row, 1, QTableWidgetItem(''))
                    self.ui.parameters.item(row, 1).setFlags(Qt.NoItemFlags)
                    self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
        self.ui.parameters.cellChanged.connect(self.cellChanged)
        self.ui.manTypeDesc.clear()
        self.ui.manTypeDesc.appendPlainText(self.manTypeDesc[self.typeID])
    
    def enableDateTime(self, jd, duration):
        self.ui.frameDT.setEnabled(True)
        self.ui.label_time.setEnabled(True)
        
        self.ui.isotedit.setText(common.jd2isot(jd))
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        
        if duration:
            self.ui.label_duration.setEnabled(True)
            dt = jd - g.myprobe.jd
            self.ui.duration.setText('{:.8f}'.format(dt))
        else:
            self.ui.label_duration.setEnabled(False)
            self.ui.duration.setText('')
    
    def disableDateTime(self):
        self.ui.frameDT.setEnabled(False)
        self.ui.label_time.setEnabled(False)
        
        self.ui.isotedit.setText('')
        self.ui.jdedit.setText('')
        self.ui.duration.setText('')

                
    def mantypeChanged(self, newID):
        if newID == 0:
            self.editman = None
            self.dispman()
            self.setenable()
            self.ui.label_Click.show()
            if g.showorbitcontrol is not None:
                g.showorbitcontrol.close()
            QMessageBox.information(self, self.mbTtl01, self.mbMes01, QMessageBox.Ok)
            return

        self.ui.label_Click.hide()
        
        self.initman(newID)
        self.dispman()
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.setenable()

    def editdatetime(self):
        jd = self.editman[self.paramname[0]]
        startjd, endjd = g.mytarget.getsejd()
        duration = False
        if self.typeID == 6 and self.currentrow == g.nextman and \
                g.myprobe.onflight:
            duration = True

        dialog = EditDateTimeDialog(self, jd, startjd, endjd, duration)
        ans = dialog.exec_()
        if ans == QDialog.Rejected:
            return

        self.dispSysMes(self.sysMes04)
        self.editman[self.paramname[0]] = self.editedjd
        self.enableDateTime(self.editedjd, duration)
        if self.currentrow == g.nextman:
            self.showorbit()

    def finish_exec(self):
        if not self.applyParameters():
            return

        if g.descriptioneditor is not None:
            self.editman[self.desckeyname] = g.descriptioneditor.getText()
        else:
            self.editman[self.desckeyname] = g.saveddescription
        if g.descriptioneditor is not None:
            g.descriptioneditor.close()
            
        g.editedman = self.editman
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.done(g.finish_exec)
        
    def finishbutton(self):
        if not self.applyParameters():
            return

        if g.descriptioneditor is not None:
            self.editman[self.desckeyname] = g.descriptioneditor.getText()
        else:
            self.editman[self.desckeyname] = g.saveddescription
        if g.descriptioneditor is not None:
            g.descriptioneditor.close()
            
        g.editedman = self.editman
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.accept()

    def applyParameters(self):
        inputError = 0
        self.ui.parameters.cellChanged.disconnect(self.cellChanged)
        for paramIdx in range(8):
            if self.paramflag[self.typeID][paramIdx+1] == 1:
                paramText = self.ui.parameters.item(paramIdx, 1).text().upper().strip()
                if self.paramname[paramIdx+1] == 'tvmode':
                    if paramText != 'L' and paramText != 'E':
                        inputError += 1
                        QMessageBox.critical(self, 
                            self.mbTtl02, self.mbMes02, QMessageBox.Ok)
                    else:
                        self.editman[self.paramname[paramIdx+1]] = paramText
                else:
                    try:
                        newval = float(paramText)
                    except ValueError:
                        inputError += 1
                        QMessageBox.critical(self, self.mbTtl02, 
                            self.mbMes03.format(self.paramname[paramIdx+1]), 
                            QMessageBox.Ok)
                        continue
                    # round entered parameters
                    rounded = round(newval, self.roundParam[paramIdx])
                    if rounded != newval:
                        newval = rounded
                        message = self.sysMes07.format(self.paramname[paramIdx+1])
                        self.dispSysMes(message)
                        anitem = QTableWidgetItem(self.fmttbl[paramIdx+1].format(newval))
                        self.ui.parameters.setItem(paramIdx, 1, anitem)

                    if self.paramname[paramIdx+1] == 'inter':
                        if newval < 0.00001:
                            inputError += 1
                            QMessageBox.critical(self, self.mbTtl02, 
                                self.mbMes04.format(self.paramname[paramIdx+1]), 
                                QMessageBox.Ok)
                            continue
                    elif self.paramname[paramIdx+1] == 'dv' or \
                         self.paramname[paramIdx+1] == 'dvpd' or \
                         self.paramname[paramIdx+1] == 'area' :
                        if newval < 0.0:
                            inputError += 1
                            QMessageBox.critical(self, self.mbTtl02, 
                                self.mbMes05.format(self.paramname[paramIdx+1]), 
                                QMessageBox.Ok)
                            continue
                    self.editman[self.paramname[paramIdx+1]] = newval
        
        self.ui.parameters.cellChanged.connect(self.cellChanged)
        if inputError == 0:
            return True
        return False
        
    def cancelbutton(self):
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.descriptioneditor is not None:
            g.descriptioneditor.close()
        self.reject()
    
    def cellChanged(self, row, column):
        self.dispSysMes(self.sysMes06.format(self.paramname[row+1]))

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
        g.logfile.flush()
        
    def closeEvent(self, event):
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.descriptioneditor is not None:
            g.descriptioneditor.close()
        event.accept()

    def showorbitclicked(self):
        self.showorbit()

    def showorbit(self):
        if not self.applyParameters():
            return
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
        self.dispSysMes(self.sysMes05)
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_pred_dv(dv, phi, elv)
        g.showorbitcontrol.editingRedraw()
        g.showorbitcontrol.set_affect_parent(False)
    
    def showorbitSTART(self):
        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if self.editman['time'] < tsjd or self.editman['time'] >= tejd:
            if g.showorbitcontrol is not None:
                g.showorbitcontrol.close()
            QMessageBox.critical(self, self.mbTtl06, self.mbMes06, QMessageBox.Ok)
            return
    
        self.dispSysMes(self.sysMes05)
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowStartOrbitDialog(self, self.editman)
            g.showorbitcontrol.show()
        g.showorbitcontrol.editingRedraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_affect_parent(False)

    def showorbitFLYTO(self):
        self.dispSysMes(self.sysMes05)
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_DT(self.editman['time'])
        g.showorbitcontrol.editingRedraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(True)
            
    def showorbitOTHER(self):
        self.dispSysMes(self.sysMes05)
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_dv(0.0, 0.0, 0.0)
        g.showorbitcontrol.editingRedraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(False)
        
            
    def computefta(self):
        norm = lambda x : x / np.sqrt(np.dot(x,x))
        if g.showorbitcontrol is None:
            QMessageBox.information(self, self.mbTtl07, self.mbMes07, QMessageBox.Ok)
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
                QMessageBox.information(self, self.mbTtl07, 
                    self.mbMes08, QMessageBox.Ok)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = self.mbMes09.format(str(dv), str(phi), str(elv))
            ans = QMessageBox.question(self, self.mbTtl09, mes, 
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ans == QMessageBox.Ok :
                self.editman['dv'] = dv
                self.editman['phi'] = phi
                self.editman['elv'] = elv
                self.dispman()
                self.dispSysMes(self.sysMes02)
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
                                    str(g.fta_parameters[2][1] / 1000.0) + '\n')
                    logstring.append('    phi: ' + 
                                    str(g.fta_parameters[2][2]) + '\n')
                    logstring.append('    elv: ' + 
                                    str(g.fta_parameters[2][3]) + '\n')
                    logstring.append('    result dv: ' + str(dv) + '\n')
                    logstring.append('    result phi: ' + str(phi) + '\n')
                    logstring.append('    result elv: ' + str(elv) + '\n')
                    g.logfile.writelines(logstring)
                    g.logfile.flush()

        elif g.fta_parameters[1] == 'BP':
            # compute terminal velocity at Target
            tepos = tpos + np.zeros(3)
            try:
                dv, phi, elv, bc_ivel, bc_tvel              \
                    = g.showorbitcontrol.tbpred.ftavel(jd, tepos)
            except ValueError:
                QMessageBox.information(self, self.mbTtl07, 
                    self.mbMes08, QMessageBox.Ok)
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
                QMessageBox.information(self, self.mbTtl07, 
                    self.mbMes08, QMessageBox.Ok)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = self.mbMes09.format(str(dv), str(phi), str(elv))
            ans = QMessageBox.question(self, self.mbTtl09, mes,
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ans == QMessageBox.Ok :
                self.editman['dv'] = dv
                self.editman['phi'] = phi
                self.editman['elv'] = elv
                self.dispman()
                self.dispSysMes(self.sysMes02)
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
                                    str(g.fta_parameters[2][1] / 1000.0) + '\n')
                    logstring.append('    beta: ' + 
                                    str(g.fta_parameters[2][2]) + '\n')
                    logstring.append('    result dv: ' + str(dv) + '\n')
                    logstring.append('    result phi: ' + str(phi) + '\n')
                    logstring.append('    result elv: ' + str(elv) + '\n')
                    g.logfile.writelines(logstring)
                    g.logfile.flush()
        
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
        self.dispSysMes(self.sysMes03)
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
            logstring.append('    flight time: ' +
                            str(dialog.result_tt - dialog.result_it) + '\n')
            g.logfile.writelines(logstring)
            g.logfile.flush()
        
    
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
            mes = self.mbMes10.format(mantime)
            QMessageBox.warning(self, self.mbTtl10, mes, QMessageBox.Ok)

        self.editman['dv'] = dialog.result_dv
        self.editman['phi'] = dialog.result_phi
        self.editman['elv'] = dialog.result_elv
        self.dispman()
        self.dispSysMes(self.sysMes03)
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
            logstring.append('    flight time: ' +
                            str(dialog.result_tt - dialog.result_it) + '\n')
            g.logfile.writelines(logstring)
            g.logfile.flush()

    def settime(self, jd):
        # this method is called from Show Orbit
        self.editman[self.paramname[0]] = jd
        self.ui.isotedit.setText(common.jd2isot(jd))
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        dt = jd - g.myprobe.jd
        self.ui.duration.setText('{:.8f}'.format(dt))
        self.dispSysMes(self.sysMes01)

    def dispSysMes(self, message):
        self.ui.sysMessage.appendPlainText(message)
        self.ui.sysMessage.centerCursor()
        
    def editdescription(self):
        if g.maneuverdescription is not None:
            g.maneuverdescription.close()
        if g.descriptioneditor is not None:
            g.descriptioneditor.close()
        
        if self.editman is None:
            initialtext = ''
        elif self.desckeyname in self.editman:
            initialtext = self.editman[self.desckeyname]
        else:
            initialtext =''
        g.descriptioneditor = EditManDesc(self, initialtext)
        g.descriptioneditor.show()
