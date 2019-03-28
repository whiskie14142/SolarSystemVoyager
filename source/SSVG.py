# -*- coding: utf-8 -*-
"""SSVG (Solar System Voyager) (c) 2016-2019 Shushi Uetsuki (whiskie14142)

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
from PyQt5.QtGui import QTextDocument
from PyQt5.QtGui import QDesktopServices as qds

import sys
import os
import json
import shutil

import common
import probe
import target
from twobodypred import TwoBodyPred
from spktype21 import SPKType21

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
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
        super().__init__(parent)
        self.setGeometry(10, 40, 640, 700)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.manplans.setColumnWidth(0,60)
        self.ui.manplans.setColumnWidth(1,300)
        self.ui.manplans.setColumnWidth(2,80)
        self.ui.manplans.setCornerButtonEnabled(False)              # Disable table selection by clicking corner button
        self.ui.manplans.horizontalHeader().setSectionsClickable(False)     # Disable colomn selection by clicking
        self.ui.manplans.verticalHeader().setSectionsClickable(False)       # Disable row selection by clicking
        self.ui.selectedman.setColumnWidth(0,139)
        self.ui.selectedman.setColumnWidth(1,100)
        self.ui.actionOpen.triggered.connect(self.openmanplan)
        self.ui.actionNew.triggered.connect(self.newmanplan)
        self.ui.actionQuit.triggered.connect(self.appquit)
        self.ui.actionSave.triggered.connect(self.savemanplan)
        self.ui.actionSave_as.triggered.connect(self.saveasmanplan)
        
        self.ui.action_SPK_import.triggered.connect(self.import_SPK)
        self.ui.action_Flight_Plan_import.triggered.connect(self.import_Flight_Plan)
        self.ui.action_Flight_Plan_Export.triggered.connect(self.export_Flight_Plan)
        
        self.ui.actionProbe.triggered.connect(self.editprobe)
        self.ui.actionTarget.triggered.connect(self.edittarget)
        self.ui.actionCreate.triggered.connect(self.createcheckpoint)
        self.ui.actionResume.triggered.connect(self.resumecheckpointAction)
        self.ui.actionAbout_SSVG.triggered.connect(self.aboutselected)
        self.ui.action_UsersGuide.triggered.connect(self.openUsersGuide)
        self.ui.action_HomePage.triggered.connect(self.openHomePage)
        self.ui.execNext.clicked.connect(self.execnextclicked)
        self.ui.reviewthroughout.clicked.connect(self.reviewthroughout)
        self.ui.flightreview.clicked.connect(self.showflightreview)
        self.ui.showOrbit.clicked.connect(self.showorbitclicked)
        self.ui.editnext.clicked.connect(self.editnext)
        self.ui.initexec.clicked.connect(self.initexec)
        self.ui.manplans.currentCellChanged.connect(self.manplanscellchanged)
        self.ui.manplans.cellDoubleClicked.connect(self.editman)
        self.ui.execto.clicked.connect(self.execto)
        self.ui.editMan.clicked.connect(self.editman)
        self.ui.insertMan.clicked.connect(self.insertman)
        self.ui.deleteMan.clicked.connect(self.deleteman)

        self.ui.manplans.verticalHeader().setFixedWidth(30)     # Qt document has no information about this method.
        self.ui.manplans.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
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

        self._translate = QtCore.QCoreApplication.translate

        self.paramdesc = [
            self._translate('SSVG.py', 'time (ISOT)'),
            self._translate('SSVG.py', 'dv (m/s)'),
            self._translate('SSVG.py', 'dvpd (m/s/day)'),
            self._translate('SSVG.py', 'phi (deg)'),
            self._translate('SSVG.py', 'elv (deg)'),
            self._translate('SSVG.py', 'aria (m**2)'),
            self._translate('SSVG.py', 'theta (deg)'),
            self._translate('SSVG.py', 'tvmode (L|E)'),
            self._translate('SSVG.py', 'inter (days)')
            ]
        
        self.initConstants()
        self.initMessage()
        self.initselectedman()
        self.eraseselectedman()
        self.initSSV()
        
        # Suppress all RuntimeWarnings from Numpy
        np.warnings.filterwarnings('ignore')
        
    def initMessage(self):
        # i18n messages
        self.sysMes01 = self._translate('SSVG.py', 'Saved: {}')
        self.sysMes02 = self._translate('SSVG.py', 'Edited: Line {}')
        self.sysMes03 = self._translate('SSVG.py', 'Executed: {0}, Line {1}')
        self.sysMes04 = self._translate('SSVG.py', 'Cleared: Execution State')
        self.sysMes05 = self._translate('SSVG.py', 'Created: Flight Plan')
        self.sysMes06 = self._translate('SSVG.py', 'Opened: {}')
        self.sysMes07 = self._translate('SSVG.py', 'Edited: Probe, of {}')
        self.sysMes08 = self._translate('SSVG.py', 'Edited: Target, of {}')
        self.sysMes09 = self._translate('SSVG.py', 'Created: Checkpoint')
        self.sysMes10 = self._translate('SSVG.py', 'Resumed: Checkpoint')
        self.sysMes11 = self._translate('SSVG.py', 'Erased: Checkpoint')
        self.sysMes12 = self._translate('SSVG.py', 'Inserted: Line {}')
        self.sysMes13 = self._translate('SSVG.py', 'Deleted: Line {}')
        self.sysMes14 = self._translate('SSVG.py', 'Sent: Orbit, to Show Orbit')
        self.sysMes15 = self._translate('SSVG.py', 'Sent: FLYTO Record, to Flight Review')
        self.sysMes16 = self._translate('SSVG.py', 'Sent: Flight Records, to Review Throughout')
        
        self.mbTtl01 = self._translate('SSVG.py', 'Confirmation')
        self.mbMes01 = self._translate('SSVG.py', 'Current Flight Plan has not been saved.\nDo you want to save?')
        self.mbTtl02 = self._translate('SSVG.py', 'SPK File not Found')
        self.mbMes02 = self._translate('SSVG.py', "Target's SPK file {0} is not found.  Store it in 'SSVG_data' folder")
        self.mbTtl03 = self._translate('SSVG.py', 'Out of Range: Flight Plan')
        self.mbMes03 = self._translate('SSVG.py', "The Flight Plan file contains Maneuver(s) OUTSIDE of Target's time span.\nYou could encounter trouble(s) in running and/or editing the Flight Plan")
        self.mbTtl04 = self._translate('SSVG.py', 'Permission Error')
        self.mbMes04 = self._translate('SSVG.py', 'The File cannot be overwrite')
        self.mbTtl05 = self._translate('SSVG.py', 'Invalid Maneuver')
        self.mbMes05 = self._translate('SSVG.py', 'You do not have valid Maneuver')
        self.mbTtl06 = self._translate('SSVG.py', 'Execution Failed')
        self.mbMes06 = self._translate('SSVG.py', 'SSVG failed to execute the Maneuver.\n\n{}')
        self.mbTtl07 = self._translate('SSVG.py', 'Invalid Command')
        self.mbMes07 = self._translate('SSVG.py', 'To execute Maneuvers in a row, select a Line below the Next Line and click [EXECUTE *]')
        self.mbTtl09 = self._translate('SSVG.py', 'Invalid Date & Time')
        self.mbMes09 = self._translate('SSVG.py', "The date and time specified in the Maneuver is OUTSIDE of the valid time span of the Target.\nTry again.")
        self.mbTtl10 = self._translate('SSVG.py', 'Confirmation to Delete')
        self.mbMes10 = self._translate('SSVG.py', 'Line {} will be deleted. OK?')
        self.mbMes11 = self._translate('SSVG.py', "The Flight Plan file containes Maneuver(s) OUTSIDE of Target's time span.\nYou could encounter trouble(s) in running and/or editing this Flight Plan.\nIt is recommended that you select another SPK file.")

        self.mbTtl12 = self._translate('SSVG.py', 'Import Completed')
        self.mbMes12 = self._translate('SSVG.py', 'The SPK file was imported as "{0}".')
        self.mbMes13 = self._translate('SSVG.py', 'The Flight Plan file was imported as "{0}".\n\nOpen it now?')
        self.mbTtl14 = self._translate('SSVG.py', 'Export Completed')
        self.mbMes14 = self._translate('SSVG.py', 'Current Flight Plan was exported to:\n\n"{0}".')
        self.mbTtl15 = self._translate('SSVG.py', 'New Flight Plan')
        self.mbMes15 = self._translate('SSVG.py', 'New Flight Plan was created.  Click [Edit Next] button to start editing.')
        

    def initConstants(self):
        self.defaultFileName = 'newplan'
        
        # i18n planet names and its indices
        g.i_planetnames = [
            [self._translate('SSVG.py', 'Mercury'), 0],
            [self._translate('SSVG.py', 'Venus'), 1],
            [self._translate('SSVG.py', 'Mars'), 3],
            [self._translate('SSVG.py', 'Jupiter'), 4],
            [self._translate('SSVG.py', 'Saturn'), 5],
            [self._translate('SSVG.py', 'Uranus'), 6],
            [self._translate('SSVG.py', 'Neptune'), 7],
            [self._translate('SSVG.py', 'Pluto'), 8],
            [self._translate('SSVG.py', 'Moon'), 10],
            [self._translate('SSVG.py', 'Earth'), 11]
        ]
        
        # i18n space base names
        g.i_spacebases = [
            self._translate('SSVG.py', 'Earth L1'),
            self._translate('SSVG.py', 'Earth L2'),
            self._translate('SSVG.py', 'Mercury L1'),
            self._translate('SSVG.py', 'Mercury L2'),
            self._translate('SSVG.py', 'Venus L1'),
            self._translate('SSVG.py', 'Venus L2'),
            self._translate('SSVG.py', 'Mars L1'),
            self._translate('SSVG.py', 'Mars L2'),
            self._translate('SSVG.py', 'Jupiter L1'),
            self._translate('SSVG.py', 'Jupiter L2'),
            self._translate('SSVG.py', 'Saturn L1'),
            self._translate('SSVG.py', 'Saturn L2'),
            self._translate('SSVG.py', 'Uranus L1'),
            self._translate('SSVG.py', 'Uranus L2'),
            self._translate('SSVG.py', 'Neptune L1'),
            self._translate('SSVG.py', 'Neptune L2')
        ]
        
        self.winTtl_3D = self._translate('SSVG.py', '3D Orbit')
        self.winTtl_SFP = self._translate('SSVG.py', 'Select Flight Plan File')
        self.winTtl_OFP = self._translate('SSVG.py', 'Define Output Flight Plan File')
        self.procMes = self._translate('SSVG.py', 'Processing:  {0} {1}')

        self.winTtl_ISPK = self._translate('SSVG.py', 'Select SPK file to import')
        self.winTtl_IFP = self._translate('SSVG.py', 'Select Flight Plan file to import')
        self.winTtl_EFP = self._translate('SSVG.py', 'Define destination file to export')


    def initSSV(self):
        g.version = 'v1.3.2'
        g.options = {}
        g.options['log'] = True
        g.clipboard = QApplication.clipboard()
        g.currentdir = os.path.join(common.plandir)
        g.manfilename = self.defaultFileName
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
    
        matplotlib.rcParams['toolbar'] = 'none'
        matplotlib.rcParams['grid.linewidth'] = 0.25
        
        # Font for matplotlib
        fontDicFilePath = os.path.join(common.i18ndir, '3DOrbitFont.json')
        fontDicFile = open(fontDicFilePath, 'r')
        fontDic = json.load(fontDicFile)
        fontDicFile.close()
        langCode = self._translate('Language', 'en')
        try:
            familyName = fontDic[langCode]
        except KeyError:
            mbTitle = 'Error in font setup for 3D Orbit window'
            mbMessage = 'Language Code "{}" is not contained in 3DOrbitFont.json.  \nFont family "sans-serif" will be used for 3D Orbit window'.format(langCode)
            QMessageBox.critical(self, mbTitle, mbMessage, QMessageBox.Ok)
            familyName = 'sans-serif'
        matplotlib.rcParams['font.family'] = familyName

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
            g.logfile.flush()

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
        mngr.window.setGeometry(left+650, top, 700, 700)
        g.fig.canvas.set_window_title(self.winTtl_3D)
        self.figcid = g.fig.canvas.mpl_connect('close_event', 
                                               self.handle_3Dclose)
        
    def handle_3Dclose(self, event):
        g.fig.canvas.mpl_disconnect(self.figcid)
        g.fig = None

    def closeEvent(self, event):
        if g.manplan_saved:
           pass
        else:
            ans = QMessageBox.question(self, self.mbTtl01, self.mbMes01, 
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

    def openmanplan(self, checked=True, filepath=''):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, self.mbTtl01, self.mbMes01, 
               QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, 
                QMessageBox.Cancel)
            if ans == QMessageBox.Save :
                self.savemanplan()
            elif ans == QMessageBox.Discard :
                pass
            else:
                return
        
        if filepath == '':
            #   activated from menu
            ans = QFileDialog.getOpenFileName(parent=self, caption=self.winTtl_SFP,
                directory=g.currentdir, filter='JSON files (*.json)')
            ans = ans[0]
            if ans == '': return
        else:
            #   activated from import_Flight_Plan()
            ans = filepath

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
        fname = os.path.basename(temppath)
        if temppath != '':
            if os.path.isabs(temppath):
                try:
                    tempk = SPKType21.open(temppath)
                except FileNotFoundError:
                    try:
                        tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                    except FileNotFoundError:
                        QMessageBox.critical(self, self.mbTtl02, 
                            self.mbMes02.format(fname), QMessageBox.Ok)
                        return
            else:
                temppath = os.path.join(common.bspdir, temppath)
                try:
                    tempk = SPKType21.open(temppath)
                except FileNotFoundError:
                    try:
                        tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                    except FileNotFoundError:
                        QMessageBox.critical(self, self.mbTtl02, 
                            self.mbMes02.format(fname), QMessageBox.Ok)
                        return

            g.data_type = tempk.segments[0].data_type
            tempk.close()
        else:
            g.data_type = 0
        
        if g.mytarget is not None:
            g.mytarget.closesbkernel()
        g.mytarget = target.Target(**g.manplan['target'])
        
        g.maneuvers = g.manplan['maneuvers']

        # for old manplan data        
        for maneuver in g.maneuvers:
            if maneuver is not None:
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
        tname = g.manplan['target']['name']
        for i in range(10):
            if common.planets_id[g.i_planetnames[i][1]][1] == tname:
                tname = g.i_planetnames[i][0]
                break
        self.ui.targetname.setText(tname)
        bname = g.manplan['probe']['base']
        for i in range(16):
            if common.bases[i][0] == bname:
                bname = g.i_spacebases[i]
                break
        self.ui.spacebase.setText(bname)
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menu_Export.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.erasecheckpoint()
        self.dispmanfilename()
        self.dispSysMes(self.sysMes06.format(os.path.splitext(os.path.basename(g.manfilename))[0]))

        # Check Time of Maneuver with time range of Target
        tsjd, tejd = g.mytarget.getsejd()
        outofrange = False
        for man in g.manplan['maneuvers']:
            if man is not None:
                if man['type'] == 'START' or man['type'] == 'FLYTO':
                    if man['time'] < tsjd or man['time'] >= tejd:
                        outofrange = True
        if outofrange:
            QMessageBox.warning(self, self.mbTtl03, self.mbMes03, QMessageBox.Ok)
        
        if g.options['log']:
            logstring = []
            logstring.append('open flight plan: ' + nowtimestr() + '\n')
            logstring.append('    file name: ' + g.manfilename + '\n')
            if outofrange:
                logstring.append('    *** Warning *** ' + self.mbMes03 + '\n')
            g.logfile.writelines(logstring)
            g.logfile.flush()

    def newmanplan(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, self.mbTtl01, self.mbMes01,
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
        g.manfilename = self.defaultFileName
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
        tname = g.manplan['target']['name']
        for i in range(10):
            if common.planets_id[g.i_planetnames[i][1]][1] == tname:
                tname = g.i_planetnames[i][0]
                break
        self.ui.targetname.setText(tname)
        bname = g.manplan['probe']['base']
        for i in range(16):
            if common.bases[i][0] == bname:
                bname = g.i_spacebases[i]
                break
        self.ui.spacebase.setText(bname)
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menu_Export.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.ui.menuEdit.setEnabled(True)
        self.erasecheckpoint()
        self.dispmanfilename()
        self.dispSysMes(self.sysMes05)

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
            g.logfile.flush()
        self.dispmanfilename()
        QMessageBox.information(self, self.mbTtl15, 
                                self.mbMes15, QMessageBox.Ok)



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
            g.reviewthroughoutcontrol.drawmanFromSSVG()
        
        self.dispSysMes(self.sysMes16)


    def savemanplan(self):
        if g.manfilename == self.defaultFileName:
            self.saveasmanplan()
            return
        try:
            manfile = open(g.manfilename, 'w')
        except PermissionError:
            QMessageBox.critical(self, self.mbTtl04, self.mbMes04, 
                                 QMessageBox.Ok)
            return
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        manfile.close()
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)
            g.logfile.flush()
        self.dispmanfilename()
        self.dispSysMes(self.sysMes01.format(os.path.splitext(os.path.basename(g.manfilename))[0]))
        
    def saveasmanplan(self):
        if g.manfilename == self.defaultFileName:
            dr = os.path.join(g.currentdir, self.defaultFileName)
        else:
            dr = g.manfilename
        ans = QFileDialog.getSaveFileName(self, self.winTtl_OFP, dr, 
                                          'JSON files (*.json)')
        ans = ans[0]
        if ans == '': return

        g.currentdir = os.path.split(ans)[0]
        
        g.manfilename = ans
        try:
            manfile = open(g.manfilename, 'w')
        except PermissionError:
            QMessageBox.critical(self, self.mbTtl04, self.mbMes04, QMessageBox.Ok)
            return
            
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        manfile.close()
        self.dispmanfilename()
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)
            g.logfile.flush()
        self.dispmanfilename()
        self.dispSysMes(self.sysMes01.format(os.path.splitext(os.path.basename(g.manfilename))[0]))

    def import_SPK(self):
        ans = QFileDialog.getOpenFileName(parent=self, caption=self.winTtl_ISPK,
            directory=os.path.join('../'), filter='SPK files (*.bsp)')
        ans = ans[0]
        if ans == '': return
        
        filename = os.path.splitext(os.path.basename(ans))
        count = 1
        extention = ''
        while True:
            destname = os.path.join(common.bspdir, filename[0]+extention+filename[1])
            if not os.path.isfile(destname):
                break
            count += 1
            extention = '({})'.format(count)
        shutil.copyfile(ans, destname)
        name = os.path.basename(destname)
        QMessageBox.information(self, self.mbTtl12, 
                                self.mbMes12.format(name), QMessageBox.Ok)
    
    def import_Flight_Plan(self):
        ans = QFileDialog.getOpenFileName(parent=self, caption=self.winTtl_IFP,
            directory=os.path.join('../'), filter='JSON files (*.json)')
        ans = ans[0]
        if ans == '': return
        
        filename = os.path.splitext(os.path.basename(ans))
        count = 1
        extention = ''
        while True:
            destname = os.path.join(common.plandir, filename[0]+extention+filename[1])
            if not os.path.isfile(destname):
                break
            count += 1
            extention = '({})'.format(count)
        shutil.copyfile(ans, destname)
        name = os.path.basename(destname)
        ans = QMessageBox.question(self, self.mbTtl12, self.mbMes13.format(name),
           QMessageBox.Open | QMessageBox.Cancel, QMessageBox.Cancel)
        if ans == QMessageBox.Open:
            self.openmanplan(filepath=destname)
    
    def export_Flight_Plan(self):
        dr = os.path.join('../', os.path.basename(g.manfilename))
        ans = QFileDialog.getSaveFileName(self, self.winTtl_EFP, dr, 
                                          'JSON files (*.json)')
        ans = ans[0]
        if ans == '': return

        try:
            destfile = open(ans, 'w')
        except PermissionError:
            QMessageBox.critical(self, self.mbTtl04, self.mbMes04, QMessageBox.Ok)
            return
            
        json.dump(g.manplan, destfile, indent=4)
        destfile.close()
        QMessageBox.information(self, self.mbTtl14, 
                                self.mbMes14.format(ans), QMessageBox.Ok)

    def dispmanplan(self):
        self.ui.manplans.clearContents()  # clear previous table
        self.ui.manplans.setRowCount(len(g.maneuvers)+1)
        for i in range(len(g.maneuvers)):
            if g.maneuvers[i] is None: continue
            mtype = g.maneuvers[i]['type']
            anitem = QTableWidgetItem(mtype)
            anitem.setTextAlignment(Qt.AlignCenter)
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

    def execnextclicked(self):
        self.execnext()

    def execnext(self):
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    QMessageBox.Ok)
            return False
        if len(g.maneuvers) <= g.nextman:
            QMessageBox.information(self, self.mbTtl05, self.mbMes05, QMessageBox.Ok)
            return False
        if g.maneuvers[g.nextman] is None:
            QMessageBox.information(self, self.mbTtl05, self.mbMes05, QMessageBox.Ok)
            return False
        
        # prepare progress bar
        ptext = self.procMes.format(str(g.nextman + 1), g.maneuvers[g.nextman]['type'])
#
        success, emes = g.myprobe.exec_man(g.maneuvers[g.nextman], 
            g.mytarget, pbar=self.pbar, plabel=self.plabel, ptext=ptext)
        if success:
            self.dispSysMes(self.sysMes03.format(g.maneuvers[g.nextman]['type'], g.nextman+1))
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
            self.ui.showOrbit.setEnabled(True)
            if g.showorbitcontrol is None:
                self.showorbit()
            else:
                self.dispSysMes(self.sysMes14)
                g.showorbitcontrol.ssvgReset()
        else:
            QMessageBox.information(self, self.mbTtl06, 
                                self.mbMes06.format(emes), QMessageBox.Ok)
            return False
        
        self.dispcurrentstatus()
        self.ui.menuCheckpoint.setEnabled(True)
        return True

    def execto(self):
        start = g.nextman
        stop = self.currentrow
        if start > stop:
            QMessageBox.information(self, self.mbTtl07, self.mbMes07, QMessageBox.Ok)
            return
        for i in range(start, stop + 1):
            result = self.execnext()
            if not result:
                break

    def execinitialize(self):
        if not g.myprobe.onflight:
            return
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
        self.dispSysMes(self.sysMes04)


    def showorbitclicked(self):
        self.showorbit()

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
        self.dispSysMes(self.sysMes14)
        g.showorbitcontrol.ssvgRedraw()
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
            g.logfile.flush()
        
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
        
        if ans == QDialog.Rejected:
            if g.myprobe.onflight:
                self.showorbit()
            return

        # Check time
        if g.editedman['type']  == 'START' or g.editedman['type'] == 'FLYTO':
            tsjd, tejd = g.mytarget.getsejd()
            if g.editedman['time'] < tsjd or g.editedman['time'] >= tejd:
                QMessageBox.critical(self, self.mbTtl09, self.mbMes09, QMessageBox.Ok)
                return

        self.dispSysMes(self.sysMes02.format(self.currentrow+1))
        if g.nextman > 0:
            self.ui.showOrbit.setEnabled(True)

        g.manplan_saved = False
        if self.currentrow < len(g.maneuvers):
            g.maneuvers[self.currentrow] = g.editedman
            if self.currentrow < g.nextman:

                # resume if checkpoint is available
                if self.checkpoint:
                    if self.checkpointdata['checkrow'] < self.currentrow:
                        self.resumecheckpoint()
                    else:
                        self.execinitialize()
                else:
                    self.execinitialize()

            self.dispmanplan()
        else:
            g.maneuvers.append(g.editedman)
            self.dispmanplan()
        
        self.eraseselectedman()
        self.dispselectedman()
            
        if ans == g.finish_exec:
            if (not self.execnext()) and g.nextman > 0:
                self.showorbit()
        else:
            if g.nextman > 0:
                self.showorbit()
        self.dispmanfilename()
            
    def insertman(self):
        if self.currentrow < len(g.maneuvers):
            g.maneuvers.insert(self.currentrow, None)
        else:
            g.maneuvers.append(None)
        self.dispSysMes(self.sysMes12.format(self.currentrow+1))
        if self.currentrow < g.nextman:
            # resume if checkpoint is available
            if self.checkpoint:
                if self.checkpointdata['checkrow'] < self.currentrow:
                    self.resumecheckpoint()
                else:
                    self.execinitialize()
            else:
                self.execinitialize()
        g.manplan_saved = False
        self.dispmanplan()
        self.dispmanfilename()
        
        if g.options['log']:
            logstring = []
            logstring.append('insert BLANK maneuver: ' + nowtimestr() + '\n')
            logstring.append('    line: ' + str(self.currentrow + 1) + '\n')
            g.logfile.writelines(logstring)
            g.logfile.flush()
            
    def deleteman(self):
        if self.currentrow == len(g.maneuvers):
            return
        if g.maneuvers[self.currentrow] is not None:
            mes = self.mbMes10.format(str(self.currentrow + 1))
            ans = QMessageBox.question(self, self.mbTtl10, mes, QMessageBox.Ok | \
                    QMessageBox.Cancel, QMessageBox.Cancel)
            if ans == QMessageBox.Cancel : return
        if self.currentrow < len(g.maneuvers):
            if g.maneuvers[self.currentrow] is None:
                deltype = 'BLANK'
            else:
                deltype = g.maneuvers[self.currentrow]['type']
            del g.maneuvers[self.currentrow]
            self.dispSysMes(self.sysMes13.format(self.currentrow+1))

            if self.currentrow < g.nextman:
                # resume if checkpoint is available
                if self.checkpoint:
                    if self.checkpointdata['checkrow'] < self.currentrow:
                        self.resumecheckpoint()
                    else:
                        self.execinitialize()
                else:
                    self.execinitialize()
            g.manplan_saved = False
            self.dispmanplan()
            self.dispmanfilename()
            
            if g.options['log']:
                logstring = []
                logstring.append('delete maneuver: ' + nowtimestr() + '\n')
                logstring.append('    line: ' +
                                str(self.currentrow + 1) + '\n')
                logstring.append('    maneuver type: ' + deltype + '\n')
                g.logfile.writelines(logstring)
                g.logfile.flush()

    def dispmanfilename(self):
        filename = os.path.basename(g.manfilename)
        filename, ext = os.path.splitext(filename)
        if not g.manplan_saved:
            filename = filename + '*'
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
        
        self.dispSysMes(self.sysMes15)

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
        self.ui.label_SMA.setText('{:.0f}'.format(kepl['a'] / 1000.0))
        self.ui.label_SMAAU.setText('{:.8f}'.format(kepl['a'] / common.au))
        self.ui.label_Ecc.setText('{:.8f}'.format(kepl['e']))
        self.ui.label_Inc.setText('{:.6f}'.format(kepl['i']))
        self.ui.label_LAN.setText('{:.6f}'.format(kepl['LoAN']))
        self.ui.label_APH.setText('{:.6f}'.format(kepl['AoP']))
        try:
            self.ui.label_PPT.setText('{0}'.format(common.jd2isot(kepl['T'])))
        except ValueError:
            self.ui.label_PPT.setText('------------------------')
        self.ui.label_PPTJD.setText('{:.8f}'.format(kepl['T']))
        if kepl['e'] < 1.0:
            self.ui.label_MA.setText('{:.6f}'.format(kepl['MA']))
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
        self.ui.label_range.setText('{:.0f}'.format(rangekm))
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
        for i in range(1, 9):
            row = i - 1
            self.ui.selectedman.setItem(row, 0, QTableWidgetItem(self.paramdesc[i]))

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
            self.erasecheckpoint()
        self.checkpoint = True
        self.checkpointdata = {}
        self.checkpointdata['nextman'] = g.nextman
        self.checkpointdata['checkrow'] = g.nextman - 1
        self.checkpointdata['probe_trj'] = g.probe_trj.copy()
        g.myprobe.createCheckpoint()
        self.ui.actionResume.setEnabled(True)
        self.dispcheckpoint()
        self.dispSysMes(self.sysMes09)

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
            self.dispSysMes(self.sysMes11)
        self.checkpoint = False

    def resumecheckpointAction(self):
        self.resumecheckpoint()
        self.showorbit()
    
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
        
        self.dispSysMes(self.sysMes10)
        self.dispcurrentstatus()

    def editprobe(self):
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
        bname = g.manplan['probe']['base']
        for i in range(16):
            if common.bases[i][0] == bname:
                bname = g.i_spacebases[i]
                break
        self.ui.spacebase.setText(bname)
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menu_Export.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.dispSysMes(self.sysMes07.format(os.path.splitext(os.path.basename(g.manfilename))[0]))
        self.dispmanfilename()

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
            g.logfile.flush()
    
    def edittarget(self):
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
        tname = g.manplan['target']['name']
        for i in range(10):
            if common.planets_id[g.i_planetnames[i][1]][1] == tname:
                tname = g.i_planetnames[i][0]
                break
        self.ui.targetname.setText(tname)
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)
        self.ui.menu_Export.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuCheckpoint.setEnabled(False)
        self.dispSysMes(self.sysMes08.format(os.path.splitext(os.path.basename(g.manfilename))[0]))
        self.dispmanfilename()
        
        # Check Time of Maneuver with time range of Target
        tsjd, tejd = g.mytarget.getsejd()
        outofrange = False
        for man in g.manplan['maneuvers']:
            if man['type'] == 'START' or man['type'] == 'FLYTO':
                if man['time'] < tsjd or man['time'] >= tejd:
                    outofrange = True
        if outofrange:
            QMessageBox.warning(self, self.mbTtl03, self.mbMes11, QMessageBox.Ok)
    
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
                logstring.append('    *** Warning *** ' + self.mbMes11 + '\n')
            g.logfile.writelines(logstring)
            g.logfile.flush()
            
    def openUsersGuide(self):
        langCode = self._translate('Language', 'en')
        urltext = 'file:///' + os.path.abspath('SSVG_UsersGuide-' + langCode + '.pdf')
        url = QUrl(urltext, QUrl.TolerantMode)
        if not qds.openUrl(url):
            urltext = 'file:///' + os.path.abspath('SSVG_UsersGuide-en.pdf')
            url = QUrl(urltext, QUrl.TolerantMode)
            qds.openUrl(url)
            
    def openHomePage(self):
        langCode = self._translate('Language', 'en')
        if langCode == 'ja':
            urltext = 'http://whsk.sakura.ne.jp/ssvg/index.html'
        else:
            urltext = 'http://whsk.sakura.ne.jp/ssvg/index-en.html'
        url = QUrl(urltext, QUrl.TolerantMode)
        qds.openUrl(url)
    
    def dispSysMes(self, message):
        self.ui.sysMessage.appendPlainText(message)
        self.ui.sysMessage.centerCursor()
        

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
    
def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('ssvgicon.ico')))
    
    # Translations of QMessageBox buttons
    i18ndir = os.path.join(common.i18ndir)
    qtTranslator = QTranslator()
    qtTranslator.load(QLocale.system(), 'qt', '_', directory=i18ndir)
    app.installTranslator(qtTranslator)
    qtBaseTranslator = QTranslator()
    qtBaseTranslator.load(QLocale.system(), 'qtbase', '_', directory=i18ndir)
    app.installTranslator(qtBaseTranslator)
    
    # Translate SSVG
    ssvgTranslator = QTranslator()
    ssvgTranslator.load(QLocale.system(), 'ssvg', '_', directory=i18ndir)
    app.installTranslator(ssvgTranslator)
    
    
    
    g.mainform = MainForm()
    g.mainform.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
