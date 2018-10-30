# -*- coding: utf-8 -*-
"""SSVG (Solar System Voyager) (c) 2016-2018 Shushi Uetsuki (whiskie14142)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Source code and license terms will be retrieved from:
<https://github.com/whiskie14142/SolarSystemVoyager/>
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

import sys
import os
import json

import common
import probe
import target
from twobodypred import TwoBodyPred
from spktype21 import SPKType21

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from flightplan import NewFlightPlanDialog
from flightplan import EditProbeDialog
from flightplan import EditTargetDialog
from about import AboutSSVG
from editmaneuver import EditManDialog
from flightreview import FlightReviewControl
from showorbit import ShowOrbitDialog
from reviewthrough import ReviewThroughoutControl

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



from ui.mainwindow import *

class MainForm(QMainWindow):
    """class for the main window (SSVG window)
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 40, 640, 700)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.manplans.setColumnWidth(0,60)
        self.ui.manplans.setColumnWidth(1,330)
        self.ui.manplans.setColumnWidth(2,80)
        self.ui.manplans.setCornerButtonEnabled(False)              # Disable table selection by clicking corner button
        self.ui.manplans.horizontalHeader().setSectionsClickable(False)     # Disable colomn selection by clicking
        self.ui.manplans.verticalHeader().setSectionsClickable(False)       # Disable row selection by clicking
        self.ui.selectedman.setColumnWidth(0,100)
        self.ui.selectedman.setColumnWidth(1,139)
#        self.connect(self.ui.actionOpen, SIGNAL('triggered()'), 
#                                             self.openmanplan)
        self.ui.actionOpen.triggered.connect(self.openmanplan)
#        self.connect(self.ui.actionNew, SIGNAL('triggered()'), 
#                                             self.newmanplan)
        self.ui.actionNew.triggered.connect(self.newmanplan)
#        self.connect(self.ui.actionQuit, SIGNAL('triggered()'), 
#                                             self.appquit)
        self.ui.actionQuit.triggered.connect(self.appquit)
#        self.connect(self.ui.actionSave, SIGNAL('triggered()'), 
#                                             self.savemanplan)
        self.ui.actionSave.triggered.connect(self.savemanplan)
#        self.connect(self.ui.actionSave_as, SIGNAL('triggered()'), 
#                                             self.saveasmanplan)
        self.ui.actionSave_as.triggered.connect(self.saveasmanplan)
#        self.connect(self.ui.actionProbe, SIGNAL('triggered()'), 
#                                             self.editprobe)
        self.ui.actionProbe.triggered.connect(self.editprobe)
#        self.connect(self.ui.actionTarget, SIGNAL('triggered()'), 
#                                             self.edittarget)
        self.ui.actionTarget.triggered.connect(self.edittarget)
#        self.connect(self.ui.actionCreate, SIGNAL('triggered()'), 
#                                             self.createcheckpoint)
        self.ui.actionCreate.triggered.connect(self.createcheckpoint)
#        self.connect(self.ui.actionResume, SIGNAL('triggered()'), 
#                                             self.resumecheckpoint)
        self.ui.actionResume.triggered.connect(self.resumecheckpoint)
#        self.connect(self.ui.actionAbout_SSVG, SIGNAL('triggered()'), 
#                                            self.aboutselected)
        self.ui.actionAbout_SSVG.triggered.connect(self.aboutselected)
#        self.connect(self.ui.execNext, SIGNAL('clicked()'), self.execnext)
        self.ui.execNext.clicked.connect(self.execnext)
#        self.connect(self.ui.reviewthroughout, SIGNAL('clicked()'), 
#                                             self.reviewthroughout)
        self.ui.reviewthroughout.clicked.connect(self.reviewthroughout)
#        self.connect(self.ui.flightreview, SIGNAL('clicked()'), 
#                                             self.showflightreview)
        self.ui.flightreview.clicked.connect(self.showflightreview)
#        self.connect(self.ui.showOrbit, SIGNAL('clicked()'), self.showorbit)
        self.ui.showOrbit.clicked.connect(self.showorbit)
#        self.connect(self.ui.editnext, SIGNAL('clicked()'), self.editnext)
        self.ui.editnext.clicked.connect(self.editnext)
#        self.connect(self.ui.initexec, SIGNAL('clicked()'), self.initexec)
        self.ui.initexec.clicked.connect(self.initexec)
#        self.connect(self.ui.manplans, 
#                     SIGNAL('currentCellChanged(int,int,int,int)'), 
#                     self.manplanscellchanged)
        self.ui.manplans.currentCellChanged.connect(self.manplanscellchanged)
#        self.connect(self.ui.manplans, SIGNAL('cellDoubleClicked(int,int)'), 
#                     self.editman)
        self.ui.manplans.cellDoubleClicked.connect(self.editman)
#        self.connect(self.ui.execto, SIGNAL('clicked()'), self.execto)
        self.ui.execto.clicked.connect(self.execto)
#        self.connect(self.ui.editMan, SIGNAL('clicked()'), self.editman)
        self.ui.editMan.clicked.connect(self.editman)
#        self.connect(self.ui.insertMan, SIGNAL('clicked()'), self.insertman)
        self.ui.insertMan.clicked.connect(self.insertman)
#        self.connect(self.ui.deleteMan, SIGNAL('clicked()'), self.deleteman)
        self.ui.deleteMan.clicked.connect(self.deleteman)

        self.ui.manplans.verticalHeader().setFixedWidth(30)     # Qt document has no information about this method.
        self.ui.progressBar.setVisible(False)
        
        self.pbar = self.ui.progressBar
        self.plabel = self.ui.label_progress
        
        self.erasecurrentstatus()
        self.currentrow = 0
        self.paramname = ['time', 'dv', 'dvpd', 'phi', 'elv', 'aria', 'theta', 
                          'tvmode', 'inter']
        self.typedict = {'START':0, 'CP':1, 'EP_ON':2, 'EP_OFF':3, 'SS_ON':4,
                         'SS_OFF':5, 'FLYTO':6}
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
        self.initselectedman()
        self.eraseselectedman()
        self.initSSV()

    def initSSV(self):
        g.version = '1.2.0'
        g.options = {}
        g.options['log'] = True
        g.clipboard = QApplication.clipboard()
        g.currentdir = os.path.join('')
        g.manfilename = None
        g.manplan = None
        g.maneuvers = None
        g.manplan_saved = True
        g.ndata = 1001
        g.ndata_s = 301
        g.myprobe = None
        
        g.mytarget = None
        g.artist_TKepler = None
        g.artist_Ptrj = []
        g.artist_PKepler = None
        g.artist_of_time = None
        g.artist_mark_of_planets = None
        g.artist_name_of_planets = []
        
        g.probe_trj = []
        g.probe_Kepler = None
        g.target_Kepler = None
    
        plt.ion()
        g.fig = None
        self.init3Dfigure()
        
        g.showorbitcontrol = None
        g.showorbitsettings = None
        g.flightreviewcontrol = None
        g.reviewthroughoutcontrol = None
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        
        self.checkpoint = False
        g.finish_exec = 2
        
        if g.options['log']:
            fpath = os.path.join(common.logdir, 'SSVGLOG_' + nowtimestrf() + '.log')
            g.logfile = open(fpath, 'w', encoding='utf-8')
            logstring = 'start ssvg ' + g.version + ': ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            

    def init3Dfigure(self):
        if g.fig is not None:
            return
        g.fig=plt.figure(figsize=(11,11))
        g.ax=g.fig.gca(projection='3d', aspect='equal')
    
        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)
        g.ax.set_xlabel('X')
        g.ax.set_ylabel('Y')
        g.ax.set_zlabel('Z')
        g.fig.tight_layout()
        
        left = self.geometry().left()
        top = self.geometry().top()
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(left+650, top, 960, 960)
        g.fig.canvas.set_window_title('3D Orbit')
        self.figcid = g.fig.canvas.mpl_connect('close_event', 
                                               self.handle_3Dclose)
        
    def handle_3Dclose(self, event):
#        print('Closed: 3D Orbit')
        g.fig.canvas.mpl_disconnect(self.figcid)
        g.fig = None

    def closeEvent(self, event):
        if g.manplan_saved:
           pass
        else:
            ans = QMessageBox.question(self, 'Quit SSV', 
                'Flight Plan has not been saved.\nDo you want to save?', 
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, 
                QMessageBox.Cancel)
            if ans == QMessageBox.Save:
                self.savemanplan()
            elif ans == QMessageBox.Discard:
                pass
            else:
                event.ignore()
                return

        if g.options['log']:
            logstring = 'end ssvg: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            g.logfile.close()
        event.accept()
        plt.close('all')

    def openmanplan(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'Open Flight Plan File', 
               'Current Flight Plan has not been saved.\nDo you want to save?', 
               QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, 
                QMessageBox.Cancel)
            if ans == QMessageBox.Save :
                self.savemanplan()
            elif ans == QMessageBox.Discard :
                pass
            else:
                return
            
        ans = QFileDialog.getOpenFileName(parent=self,
            caption='Select Flight Plan File',
            directory=g.currentdir, filter='JSON files (*.json)')
        ans = ans[0]
        if ans == '': return

        g.currentdir = os.path.split(ans)[0]
        
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()
            
        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)

        self.erasecurrentstatus()
        self.eraseselectedman()
        self.currentrow = 0
        
        g.manfilename = ans
        manfile = open(g.manfilename, 'r')
        g.manplan = json.load(manfile)
        manfile.close()
        
        # Check SPK file, and set data_type
        temppath = g.manplan['target']['file']
        if temppath != '':
            try:
                tempk = SPKType21.open(temppath)
            except FileNotFoundError:
                try:
                    fname = os.path.basename(temppath)
                    tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                except FileNotFoundError:
                    QMessageBox.critical(self, 'File not Found',
                        "Target's SPK file {0} is not found.  Store it in 'data' folder".format(fname),
                        QMessageBox.Ok)
                    return
            g.data_type = tempk.segments[0].data_type
            tempk.close()
        else:
            g.data_type = 0
        
        if g.mytarget is not None:
            g.mytarget.closesbkernel()
        g.mytarget = target.Target(**g.manplan['target'])
        
        self.dispmanfilename()
        g.maneuvers = g.manplan['maneuvers']

        # for old manplan data        
        for maneuver in g.maneuvers:
            if maneuver['type'] == 'EP_ON' or maneuver['type'] == 'SS_ON':
                if not ('tvmode' in maneuver):
                    maneuver['tvmode'] = 'L'
        
        g.manplan_saved = True
        g.nextman = 0
        g.myprobe = probe.Probe(**g.manplan['probe'])
        
        erase_Ptrj()
        g.probe_trj = []
        erase_TKepler()
            
        self.enablewidgets()
        self.ui.probename.setText(g.manplan['probe']['name'])
        self.ui.targetname.setText(g.manplan['target']['name'])
        self.ui.spacebase.setText(g.manplan['probe']['base'])
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.erasecheckpoint()

        # Check Time of Maneuver with time range of Target
        tsjd, tejd = g.mytarget.getsejd()
        outofrange = False
        for man in g.manplan['maneuvers']:
            if man['type'] == 'START' or man['type'] == 'FLYTO':
                if man['time'] < tsjd or man['time'] >= tejd:
                    outofrange = True
        if outofrange:
            oormes = "The Flight Plan file containes Maneuver(s) that " + \
                "is OUTSIDE of Target's time span."
            oormes2 = "\nYou could encounter " + \
                "trouble(s) in running and/or editing this Flight Plan"
            QMessageBox.warning(self, 'Warning', oormes + oormes2)
        
        if g.options['log']:
            logstring = []
            logstring.append('open flight plan: ' + nowtimestr() + '\n')
            logstring.append('    file name: ' + g.manfilename + '\n')
            if outofrange:
                logstring.append('    *** Warning *** ' + oormes + '\n')
            g.logfile.writelines(logstring)
    def newmanplan(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'New Flight Plan', 
               'Current Flight Plan has not been saved.\nDo you want to save?', 
               QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, 
               QMessageBox.Cancel)
            if ans == QMessageBox.Save :
                self.savemanplan()
            elif ans == QMessageBox.Discard :
                pass
            else:
                return

        newdialog = NewFlightPlanDialog(self)
        ans = newdialog.exec_()
        if ans == QDialog.Rejected:
            return

        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()

        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)

        self.erasecurrentstatus()
        self.eraseselectedman()
        self.currentrow = 0
        g.manfilename = None
        self.dispmanfilename()
        g.maneuvers = g.manplan['maneuvers']
        g.manplan_saved = False
        g.nextman = 0
        g.myprobe = probe.Probe(**g.manplan['probe'])
        
        erase_Ptrj()
        g.probe_trj = []
        
        erase_TKepler()
        
        if g.mytarget is not None:
            g.mytarget.closesbkernel()
        g.mytarget = target.Target(**g.manplan['target'])
        
        self.enablewidgets()
        
        self.ui.probename.setText(g.manplan['probe']['name'])
        self.ui.targetname.setText(g.manplan['target']['name'])
        self.ui.spacebase.setText(g.manplan['probe']['base'])
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.ui.menuEdit.setEnabled(True)
        self.erasecheckpoint()

        if g.options['log']:
            logstring = []
            logstring.append('new flight plan: ' + nowtimestr() + '\n')
            logstring.append('    probe name: ' +
                            g.manplan['probe']['name'] + '\n')
            logstring.append('    probe mass: ' +
                            str(g.manplan['probe']['pmass']) + '\n')
            logstring.append('    space base: ' +
                            g.manplan['probe']['base'] + '\n')
            logstring.append('    target name: ' +
                            g.manplan['target']['name'] + '\n')
            if g.manplan['target']['SPKID2B'] > 10000:
                logstring.append('    target SPK file: ' +
                                g.manplan['target']['file'] + '\n')
                logstring.append('    target SPKID: ' +
                                str(g.manplan['target']['SPKID2B']) + '\n')
            g.logfile.writelines(logstring)


    def reviewthroughout(self):
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    QMessageBox.Ok)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe is not on flight.', QMessageBox.Ok)
            return
        
        self.init3Dfigure()
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        
        if g.reviewthroughoutcontrol is None:
            g.reviewthroughoutcontrol = ReviewThroughoutControl(self)
            g.reviewthroughoutcontrol.show()
        else:
            g.reviewthroughoutcontrol.drawman()


    def savemanplan(self):
        if g.manfilename is None:
            self.saveasmanplan()
            return
        manfile = open(g.manfilename, 'w')
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        QMessageBox.information(self, 'Info', 
                                'Flight Plan was saved.', QMessageBox.Ok)
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)
        
    def saveasmanplan(self):
        if g.manfilename is None:
            dr = g.currentdir
        else:
            dr = g.manfilename
        ans = QFileDialog.getSaveFileName(self, 
            'Define output maneuver file', dr, 'JSON files (*.json)')
        if ans == '': return

        g.currentdir = os.path.split(ans)[0]
        
        g.manfilename = ans
        manfile = open(g.manfilename, 'w')
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        self.dispmanfilename()
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)

    def dispmanplan(self):
        self.ui.manplans.clearContents()  # clear previous table
        self.ui.manplans.setRowCount(len(g.maneuvers)+1)
        for i in range(len(g.maneuvers)):
            if g.maneuvers[i] is None: continue
            mtype = g.maneuvers[i]['type']
            anitem = QTableWidgetItem(mtype)
            self.ui.manplans.setItem(i, 0, anitem)
            desc = ''
            for name in self.paramname:
                if name in g.maneuvers[i]:
                    if name == 'time':
                        desc = desc + 'Date=' + \
                            common.jd2datetime(g.maneuvers[i][name])[0] + ' '
                    elif name == 'tvmode':
                        desc = desc + name + '=' + g.maneuvers[i][name] + ' '
                    else:
                        desc = desc + name + '=' + \
                            '{:.2f}'.format(g.maneuvers[i][name]) + ' '
            anitem = QTableWidgetItem(desc)
            self.ui.manplans.setItem(i, 1, anitem)
        anitem = QTableWidgetItem('Next')
        anitem.setTextAlignment(Qt.AlignCenter)
        self.ui.manplans.setItem(g.nextman, 2, anitem)
        self.ui.manplans.selectRow(self.currentrow)
        self.dispcheckpoint()
        
    def appquit(self):        
        self.close()

    def execnext(self):
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    QMessageBox.Ok)
            return False
        if len(g.maneuvers) <= g.nextman:
            QMessageBox.information(self, 
                        'Info', "You don't have valid maneuver.", QMessageBox.Ok)
            return False
        if g.maneuvers[g.nextman] is None:
            QMessageBox.information(self, 'Info', 
                        "You don't have valid maneuver.", QMessageBox.Ok)
            return False
        
        # prepare progress bar
        ptext = 'Processing:  ' + str(g.nextman + 1) + ' ' + \
            g.maneuvers[g.nextman]['type']
#
        success, emes = g.myprobe.exec_man(g.maneuvers[g.nextman], 
            g.mytarget, pbar=self.pbar, plabel=self.plabel, ptext=ptext)
        if success:
            self.ui.reviewthroughout.setEnabled(True)
            if g.myprobe.trj_record[-1][0]['type'] == 'FLYTO':
                g.probe_trj.append(g.myprobe.trj_record[-1])
                self.ui.flightreview.setEnabled(True)
            else:
                self.ui.flightreview.setEnabled(False)
            anitem = QTableWidgetItem('')
            self.ui.manplans.setItem(g.nextman, 2, anitem)
            anitem = QTableWidgetItem('Next')
            anitem.setTextAlignment(Qt.AlignCenter)
            g.nextman += 1
            self.ui.manplans.setItem(g.nextman, 2, anitem)
            self.currentrow = g.nextman
            self.ui.manplans.selectRow(self.currentrow)
            
            self.init3Dfigure()
            if g.showorbitcontrol is None:
                self.showorbit()
                self.ui.showOrbit.setEnabled(True)
        else:
            QMessageBox.information(self, 'Info', 
                                "Cannot Execute this Maneuver.\n\n"    \
                                + emes, QMessageBox.Ok)
            return False

        g.showorbitcontrol.reset()
        self.dispcurrentstatus()
        self.ui.menuCheckpoint.setEnabled(True)
        return True

    def execto(self):
        start = g.nextman
        stop = self.currentrow
        if start > stop:
            QMessageBox.information(self, 'Info', 
                                "Select maneuver later than 'Next'", QMessageBox.Ok)
            return
        for i in range(start, stop + 1):
            result = self.execnext()
            if not result:
                break

    def execinitialize(self):
        erase_Ptrj()
        g.probe_trj = []
        
        g.myprobe.execinitialize()
        g.nextman = 0
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.erasecurrentstatus()
        self.erasecheckpoint()
        self.ui.menuCheckpoint.setEnabled(False)

    def showorbit(self):
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    QMessageBox.Ok)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe has no valid orbit.', QMessageBox.Ok)
            return
        self.init3Dfigure()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()
        if g.showorbitcontrol is None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        else:
            g.showorbitcontrol.redraw()
        g.showorbitcontrol.set_affect_parent(False)

    def manplanscellchanged(self, newrow, newcolm, prevrow, prevcolm):
        self.eraseselectedman()
        if newrow >= 0:
            self.currentrow = newrow
            self.dispselectedman()

    def editnext(self):
        self.currentrow = g.nextman
        self.ui.manplans.selectRow(self.currentrow)
        self.editman()

    def initexec(self):
        self.execinitialize()
        self.dispmanplan()
        
    def editman(self):
        if g.options['log']:
            logstring = []
            logstring.append('begin maneuver editing: ' + nowtimestr() + '\n')
            logstring.append('    line: ' + str(self.currentrow + 1) + '\n')
            g.logfile.writelines(logstring)
        
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()
        if self.currentrow < len(g.maneuvers):
            man = g.maneuvers[self.currentrow]
        else:
            man = None
        g.editedman = None
        editdialog = EditManDialog(self, man, self.currentrow)
        ans = editdialog.exec_()
        
        if g.nextman > 0:
            self.showorbit()
            self.ui.showOrbit.setEnabled(True)

        if ans == QDialog.Rejected:
            return
        if g.editedman['type'] == 'START' and self.currentrow != 0:
            QMessageBox.information(self, 'Info', 
                                'START shall be the 1st maneuver', QMessageBox.Ok)
            return
        if g.editedman['type'] != 'START' and self.currentrow == 0:
            QMessageBox.information(self, 'Info', 
                                'The 1st maneuver shall be START', QMessageBox.Ok)
            return

        # Check time
        if g.editedman['type']  == 'START' or g.editedman['type'] == 'FLYTO':
            tsjd, tejd = g.mytarget.getsejd()
            if g.editedman['time'] < tsjd or g.editedman['time'] >= tejd:
                oormes = "The time specified in the Maneuver is outside " + \
                "of the valid time span of the Target.\nTry again."
                QMessageBox.critical(self, 'Invalid Parameter', oormes,
                                     QMessageBox.Ok)
                return

        g.manplan_saved = False
        if self.currentrow < len(g.maneuvers):
            g.maneuvers[self.currentrow] = g.editedman
            if self.currentrow < g.nextman:
                self.execinitialize()
            self.dispmanplan()
        else:
            g.maneuvers.append(g.editedman)
            self.dispmanplan()
        
        self.eraseselectedman()
        self.dispselectedman()
            
        if ans == g.finish_exec:
            self.execnext()
            
    def insertman(self):
        if self.currentrow < len(g.maneuvers):
            g.maneuvers.insert(self.currentrow, None)
        else:
            g.maneuvers.append(None)
        if self.currentrow < g.nextman:
            self.execinitialize()
        g.manplan_saved = False
        self.dispmanplan()
        
        if g.options['log']:
            logstring = []
            logstring.append('insert BLANK maneuver: ' + nowtimestr() + '\n')
            logstring.append('    line: ' + str(self.currentrow + 1) + '\n')
            g.logfile.writelines(logstring)
            
    def deleteman(self):
        if self.currentrow == len(g.maneuvers):
            return
        mes = 'Line No. ' + str(self.currentrow + 1) + ' will be deleted. OK?'
        ans = QMessageBox.question(self, 'Delete Man.', mes, QMessageBox.Ok | \
                QMessageBox.Cancel, QMessageBox.Cancel)
        if ans == QMessageBox.Cancel : return
        if self.currentrow < len(g.maneuvers):
            if g.maneuvers[self.currentrow] is None:
                deltype = 'BLANK'
            else:
                deltype = g.maneuvers[self.currentrow]['type']
            del(g.maneuvers[self.currentrow])
            if self.currentrow < g.nextman:
                self.execinitialize()
            g.manplan_saved = False
            self.dispmanplan()
            
            if g.options['log']:
                logstring = []
                logstring.append('delete maneuver: ' + nowtimestr() + '\n')
                logstring.append('    line: ' +
                                str(self.currentrow + 1) + '\n')
                logstring.append('    maneuver type: ' + deltype + '\n')
                g.logfile.writelines(logstring)

    def dispmanfilename(self):
        if g.manfilename is None:
            filename = ''
        else:
            filename = os.path.basename(g.manfilename)
        self.ui.manfilename.setText(filename)

    def showflightreview(self):
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    QMessageBox.Ok)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe is not on flight.', QMessageBox.Ok)
            return
        if g.myprobe.trj_record[-1][0]['type'] != 'FLYTO':
            QMessageBox.information(self, 'Info', 
                                    'Latest maneuver was not FLYTO.', QMessageBox.Ok)
            return  
        
        self.init3Dfigure()
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()
        
        if g.flightreviewcontrol is None:
            g.flightreviewcontrol = FlightReviewControl(self)
            g.flightreviewcontrol.show()
        else:
            g.flightreviewcontrol.redraw()

    def dispcurrentstatus(self):
        if self.tbpred_formain is None:
            self.tbpred_formain = TwoBodyPred(g.myprobe.name)
        self.tbpred_formain.fix_state(g.myprobe.jd, g.myprobe.pos, 
                                      g.myprobe.vel)
        kepl = self.tbpred_formain.elmKepl()

        self.ui.label_ELM.setText('{0} {1}'.format(g.nextman, 
                                  g.maneuvers[g.nextman-1]['type']))
        self.ui.label_ISOT.setText('{0}'.format(common.jd2isot(g.myprobe.jd)))
        self.ui.label_JD.setText('{:.8f}'.format(g.myprobe.jd))
        self.ui.label_SMA.setText('{:,.0f}'.format(kepl['a'] / 1000.0))
        self.ui.label_SMAAU.setText('{:.8f}'.format(kepl['a'] / common.au))
        self.ui.label_Ecc.setText('{:.8f}'.format(kepl['e']))
        self.ui.label_Inc.setText('{:.6f}'.format(kepl['i']))
        self.ui.label_LAN.setText('{:.6f}'.format(kepl['Lomega']))
        self.ui.label_APH.setText('{:.6f}'.format(kepl['Somega']))
        self.ui.label_PPT.setText('{0}'.format(common.jd2isot(kepl['T'])))
        self.ui.label_PPTJD.setText('{:.8f}'.format(kepl['T']))
        if kepl['e'] < 1.0:
            self.ui.label_MA.setText('{:.6f}'.format(kepl['ma']))
            self.ui.label_OP.setText('{:.6f}'.format(kepl['P']))
        else:
            self.ui.label_MA.setText('N/A')
            self.ui.label_OP.setText('N/A')
        self.ui.label_ADV.setText('{0:.0f}, {1:.0f}, {2:.0f}'.format(
                                    g.myprobe.accumdv['CP'],
                                    g.myprobe.accumdv['EP'],
                                    g.myprobe.accumdv['SS']))
        
        sunpos, sunvel = common.SPKposvel(10, g.myprobe.jd)
        relpos = g.myprobe.pos - sunpos
        rangekm = np.sqrt(np.dot(relpos, relpos)) / 1000.0
        relvel = g.myprobe.vel - sunvel
        velmag = np.sqrt(np.dot(relvel, relvel))
        self.ui.label_range.setText('{:,.0f}'.format(rangekm))
        self.ui.label_velocity.setText('{:.3f}'.format(velmag))

    
    def erasecurrentstatus(self):
        self.tbpred_formain = None
        self.ui.label_ELM.setText('')
        self.ui.label_ISOT.setText('')
        self.ui.label_JD.setText('')
        self.ui.label_range.setText('')
        self.ui.label_velocity.setText('')
        self.ui.label_SMA.setText('')
        self.ui.label_SMAAU.setText('')
        self.ui.label_Ecc.setText('')
        self.ui.label_Inc.setText('')
        self.ui.label_LAN.setText('')
        self.ui.label_APH.setText('')
        self.ui.label_PPT.setText('')
        self.ui.label_PPTJD.setText('')
        self.ui.label_MA.setText('')
        self.ui.label_OP.setText('')
        self.ui.label_ADV.setText('')

    def enablewidgets(self):
        self.ui.execNext.setEnabled(True)
        self.ui.execto.setEnabled(True)
        self.ui.initexec.setEnabled(True)
        self.ui.editnext.setEnabled(True)
        self.ui.editMan.setEnabled(True)
        self.ui.insertMan.setEnabled(True)
        self.ui.deleteMan.setEnabled(True)
        self.ui.manplans.setEnabled(True)
        
    def aboutselected(self):
        aboutdialog = AboutSSVG(self)
        aboutdialog.exec_()

    def initselectedman(self):
        paramdesc = [
            'time (ISOT)',
            'dv (m/s)',
            'dvpd (m/s/day)',
            'phi (deg)',
            'elv (deg)',
            'aria (m**2)',
            'theta (deg)',
            'tvmode (L|E)',
            'inter (days)'
            ]

        for i in range(1, 9):
            row = i - 1
            self.ui.selectedman.setItem(row, 0, QTableWidgetItem(paramdesc[i]))

    def dispselectedman(self):
        lenman = len(g.manplan['maneuvers'])
        if lenman == 0:
            return
        if self.currentrow < 0 or self.currentrow >= lenman:
            return
        man = g.manplan['maneuvers'][self.currentrow]
        if man is None:
            return
        typeID = self.typedict[man['type']]
        
        cman = str(self.currentrow + 1) + ' ' + man['type']
        self.ui.label_cman.setText(cman)
        
        if self.paramflag[typeID][0] == 1:
            self.ui.label_mantime_h.setEnabled(True)
            self.ui.label_mantime.setText(common.jd2isot(man['time']))

        for i in range(1, 9):
            row = i - 1
            if self.paramflag[typeID][i] == 1:
                anitem = QTableWidgetItem(self.fmttbl[i].format(
                                                    man[self.paramname[i]]))
                self.ui.selectedman.setItem(row, 1, anitem)
                self.ui.selectedman.item(row, 1).setFlags(Qt.ItemIsEnabled)
                self.ui.selectedman.item(row, 0).setFlags(Qt.ItemIsEnabled)
            else:
                anitem = QTableWidgetItem('')
                self.ui.selectedman.setItem(row, 1, anitem)
                self.ui.selectedman.item(row, 1).setFlags(Qt.NoItemFlags)
                self.ui.selectedman.item(row, 0).setFlags(Qt.NoItemFlags)

    def eraseselectedman(self):
        self.ui.label_mantime_h.setEnabled(False)
        self.ui.label_mantime.setText('')
        self.ui.label_cman.setText('')
        for i in range(1, 9):
            row = i - 1
            anitem = QTableWidgetItem('')
            self.ui.selectedman.setItem(row, 1, anitem)
            self.ui.selectedman.item(row, 1).setFlags(Qt.NoItemFlags)
            self.ui.selectedman.item(row, 0).setFlags(Qt.NoItemFlags)

    def createcheckpoint(self):
        if not g.myprobe.onflight:
            return
        if self.checkpoint:
            ans = QMessageBox.question(self, 'Create New Checkpoint', 
                'Existing checkpoint will be lost.  OK?', QMessageBox.Ok | \
                QMessageBox.Cancel, QMessageBox.Cancel)
            if ans != QMessageBox.Ok :
                return
            self.erasecheckpoint()
        self.checkpoint = True
        self.checkpointdata = {}
        self.checkpointdata['nextman'] = g.nextman
        self.checkpointdata['checkrow'] = g.nextman - 1
        self.checkpointdata['probe_trj'] = g.probe_trj.copy()
        g.myprobe.createCheckpoint()
        self.ui.actionResume.setEnabled(True)
        self.dispcheckpoint()

    def dispcheckpoint(self):
        if self.checkpoint:
            anitem = QTableWidgetItem('checkpoint')
            anitem.setTextAlignment(Qt.AlignCenter)
            self.ui.manplans.setItem(self.checkpointdata['checkrow'], 2, anitem)

    def erasecheckpoint(self):
        if self.checkpoint:
            self.ui.actionResume.setEnabled(False)
            anitem = QTableWidgetItem('')
            self.ui.manplans.setItem(self.checkpointdata['checkrow'], 2, 
                                     anitem)
        self.checkpoint = False
    
    def resumecheckpoint(self):
        if not self.checkpoint:
            return
        if g.showorbitcontrol is not None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol is not None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol is not None:
            g.reviewthroughoutcontrol.close()

        g.myprobe.resumeCheckpoint()
        g.probe_trj = self.checkpointdata['probe_trj'].copy()

        anitem = QTableWidgetItem('')
        self.ui.manplans.setItem(g.nextman, 2, anitem)
        
        g.nextman = self.checkpointdata['nextman']
        self.currentrow = g.nextman
        self.dispmanplan()
        
        self.showorbit()
        self.dispcurrentstatus()

    def editprobe(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'Edit Probe Properties', 
               'Current Flight Plan has not been saved.\nDo you want to save?', 
               QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel, 
               QMessageBox.Cancel)
            if ans == QMessageBox.Save :
                self.savemanplan()
            elif ans == QMessageBox.Ignore :
                pass
            else:
                return

        manplan = g.manplan.copy()
        editdialog = EditProbeDialog(self, manplan)
        ans = editdialog.exec_()
        if ans == QDialog.Rejected:
            return
        
        self.execinitialize()
        g.manplan_saved = False
        g.manplan['probe'] = manplan['probe']
        g.myprobe = probe.Probe(**g.manplan['probe'])
        
        self.enablewidgets()
        self.ui.probename.setText(g.manplan['probe']['name'])
        self.ui.spacebase.setText(g.manplan['probe']['base'])
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)

        if g.options['log']:
            logstring = []
            logstring.append('edit probe: ' + nowtimestr() + '\n')
            logstring.append('    probe name: ' +
                            g.manplan['probe']['name'] + '\n')
            logstring.append('    probe mass: ' +
                            str(g.manplan['probe']['pmass']) + '\n')
            logstring.append('    space base: ' +
                            g.manplan['probe']['base'] + '\n')
            g.logfile.writelines(logstring)
    
    def edittarget(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'Edit Target', 
               'Current Flight Plan has not been saved.\nDo you want to save?', 
               QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel, 
               QMessageBox.Cancel)
            if ans == QMessageBox.Save :
                self.savemanplan()
            elif ans == QMessageBox.Ignore :
                pass
            else:
                return

        manplan = g.manplan.copy()
        editdialog = EditTargetDialog(self, manplan)
        ans = editdialog.exec_()
        if ans == QDialog.Rejected:
            return
        
        self.execinitialize()
        g.manplan_saved = False
        g.manplan['target'] = manplan['target']
        erase_TKepler()
        g.mytarget.closesbkernel()
        g.mytarget = target.Target(**g.manplan['target'])
        
        self.enablewidgets()
        self.ui.targetname.setText(g.manplan['target']['name'])
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)

        # Check Time of Maneuver with time range of Target
        tsjd, tejd = g.mytarget.getsejd()
        outofrange = False
        for man in g.manplan['maneuvers']:
            if man['type'] == 'START' or man['type'] == 'FLYTO':
                if man['time'] < tsjd or man['time'] >= tejd:
                    outofrange = True
        if outofrange:
            oormes = "The Flight Plan file containes Maneuver(s) that " + \
                "is OUTSIDE of Target's time span."
            oormes2 = "\nYou could encounter " + \
                "trouble(s) in running and/or editing this Flight Plan." + \
                "\nIt is recommended that you select another SPK file."
            QMessageBox.warning(self, 'Warning', oormes + oormes2)

    
        if g.options['log']:
            logstring = []
            logstring.append('edit target: ' + nowtimestr() + '\n')
            logstring.append('    target name: ' +
                            g.manplan['target']['name'] + '\n')
            if g.manplan['target']['file'] != '':
                logstring.append('    target SPK file: ' +
                    g.manplan['target']['file'] + '\n')
                logstring.append('    target SPKID: ' +
                    str(g.manplan['target']['SPKID1B']) + '\n')
            if outofrange:
                logstring.append('    *** Warning *** ' + oormes + '\n')
            g.logfile.writelines(logstring)

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
    
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('SSVG.ico')))
    #print(os.path.abspath(os.path.dirname(sys.argv[0])))
    g.mainform = MainForm()
    g.mainform.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
