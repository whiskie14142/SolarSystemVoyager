# -*- coding: utf-8 -*-
"""SSVG (Solar System Voyager) (c) 2016 Shushi Uetsuki (whiskie14142)

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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import json

import common
import julian
from datetime import datetime
import probe
import target
from twobodypred import TwoBodyPred

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class _Gdata:
    """Container of global data
    """
    __slots__ = [
        'ax',                       # axes of matplotlib
        'currentdir',               # current directory of application
        'editedman',                # edited maneuver : output of EditManDialog
        'fig',                      # figure of matplotlib
        'mainform',                 # mainform of this application
        'maneuvers',                # list of maneuvers
        'manfilename',              # file name of maneuver plan
        'manplan',                  # maneuver plan
        'manplan_saved',            # flag for saved or not saved
        'myprobe',                  # instance of space probe
        'mytarget',                 # instance of Target (destination of the probe)
        'ndata',                    # number of points to draw orbit
        'nextman',                  # index of next maneuver
        'saved_artist_of_probe',    # list of artists of matplotlib for probe trajectories
        'saved_artist_of_target',   # artist of matplotlib for target orbit
        'saved_mark_of_planets',    # artist of matplotlib for planet marks
        'saved_name_of_planets',    # artist of matplotlib for planet names
        'saved_artist_of_time',     # artist of matplotlib for time and its type
        'showorbitcontrol',         # instance of ShowOrbitDialog
        'showorbitsettings',        # current settings of ShowOrbitDialog
        'flightreviewcontrol',      # instance of FlightReviewControl
        'reviewthroughoutcontrol',  # instance of ReviewThroughoutControl
        'finish_exec',              # return code of EditManDialog for finish and execute (== 2)
        'fta_parameters'            # return parameters from FTAsettingDialog
        ]
    
# global data container instance    
g = _Gdata()
    

def plot_2b_orbit_of_target(ndata, jd):
    xs, ys, zs, ts = g.mytarget.points(jd, ndata)
    artist = g.ax.plot(xs, ys, zs, color='green', lw=0.75)
    plt.draw()
    return artist

def plot_trj_of_probe():
    xs = g.myprobe.trj_record[-1][2]
    ys = g.myprobe.trj_record[-1][3]
    zs = g.myprobe.trj_record[-1][4]
    artist = g.ax.plot(xs, ys, zs, color='blue', lw=0.75)
    plt.draw()
    return artist

def remove_planets():
    if g.saved_mark_of_planets != None:
        g.saved_mark_of_planets.remove()
        g.saved_mark_of_planets = None
    for art in g.saved_name_of_planets:
        art.remove()
    g.saved_name_of_planets = []
    
def replot_planets(jd):
    markx = []
    marky = []
    markz = []
    names = []
    id_of_target = g.mytarget.getID()
    id_of_EMB = 3
    id_of_Moon = 301
    
    for i in range(12):
        if common.planets_id[i][0] == id_of_target: continue
        if common.planets_id[i][0] == id_of_EMB: continue
        pos, vel = common.SPKposvel(common.planets_id[i][0], jd)
        markx.append(pos[0])
        marky.append(pos[1])
        markz.append(pos[2])
        if common.planets_id[i][0] == id_of_Moon:
            names.append('')
        else:
            names.append(common.planets_id[i][1])
    
    g.saved_mark_of_planets = g.ax.scatter(markx, marky, markz, marker='+', 
                                           s=20, c='c', depthshade=False)
    g.saved_name_of_planets = []
    for i in range(len(names)):
        g.saved_name_of_planets.append(g.ax.text(markx[i], marky[i], markz[i],
                                      ' '+names[i], color='c', fontsize=9))
    plt.draw()

def remove_time():
    if g.saved_artist_of_time != None:
        g.saved_artist_of_time.remove()
        g.saved_artist_of_time = None

def replot_time(jd, ttype=''):
    s = common.jd2isot(jd) + ' (' + ttype + ')'
    g.saved_artist_of_time = g.ax.text2D(0.02, 0.96, s, transform=g.ax.transAxes)



from aboutSSVG import *

class AboutSSVG(QtGui.QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_aboutSSVG()
        self.ui.setupUi(self)
        version = '0.2.0 beta'
        abouttext = """SSVG (Solar System Voyager) (c) 2016 Shushi Uetsuki (whiskie14142)

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

This program uses following programs and modules:
  Numpy : http://www.numpy.org/
    Copyright (c) 2005-2016, NumPy Developers.
    All rights reserved.
  Scipy : http://scipy.org/
    Copyright (c) 2001, 2002 Enthought, Inc.
    All rights reserved.
    Copyright (c) 2003-2013 SciPy Developers.
    All rights reserved.
  matplotlib : http://matplotlib.org/
    Copyright (c) 2012-2013 Matplotlib Development Team;
    All Rights Reserved
  jplephem : https://github.com/brandon-rhodes/python-jplephem/
  PyQt4 : https://www.riverbankcomputing.com/news/
  julian : https://github.com/dannyzed/julian/
    Copyright (c) 2016 Daniel Zawada
  pytwobodyorbit : https://github.com/whiskie14142/pytwobodyorbit/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  spktype01 : https://github.com/whiskie14142/spktype01/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  PyInstaller : http://www.pyinstaller.org/"""

        self.ui.versionlabel.setText(version)        
        self.ui.licensetext.setPlainText(abouttext)
        self.connect(self.ui.okButton, SIGNAL('clicked()'), self.accept)
                


from newflightplandialog import *

class NewFlightPlanDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_NewFlightPlanDialog()
        self.ui.setupUi(self)
        
        spacebaselist = ['EarthL2']
        self.ui.spacebase.addItems(spacebaselist)
        self.ui.spacebase.setCurrentIndex(0)
        
        for planet_id in common.planets_id:
            if planet_id[1] == 'EMB': continue
            if planet_id[1] == 'Sun': continue
            self.ui.planets.addItem(planet_id[1])
        self.ui.planets.setCurrentIndex(0)
        
        self.connect(self.ui.startfromspacebase, SIGNAL('clicked()'), self.startfromspacebaseclicked)
        self.connect(self.ui.planetbutton, SIGNAL('clicked()'), self.planetbuttonclicked)
        self.connect(self.ui.smallbodybutton, SIGNAL('clicked()'), self.planetbuttonclicked)
        self.connect(self.ui.spkfileselect, SIGNAL('clicked()'), self.spkfileselectclicked)
#        self.connect(self.ui.isot_edit, SIGNAL('editingFinished()'), self.isotedited)
#        self.connect(self.ui.jd_edit, SIGNAL('editingFinished()'), self.jdedited)
        self.connect(self.ui.okbutton, SIGNAL('clicked()'), self.ok_clicked)
        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), self.reject)

    def startfromspacebaseclicked(self):
        if self.ui.startfromspacebase.isChecked():
            self.ui.spacebase.setEnabled(True)
            self.ui.startparametersgroupbox.setEnabled(False)
        else:
            self.ui.spacebase.setEnabled(False)
            self.ui.startparametersgroupbox.setEnabled(True)
            
    def planetbuttonclicked(self):
        if self.ui.planetbutton.isChecked():
            self.ui.planets.setEnabled(True)
            self.ui.targetgroupbox.setEnabled(False)
        if self.ui.smallbodybutton.isChecked():
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            
    def spkfileselectclicked(self):
        ans = QFileDialog.getOpenFileName(parent=self,
            caption='Select SPK file', directory=g.currentdir)
        if ans == '': return
        self.ui.spkfilepath.setText(ans)

    def isotedited(self):
        try:
            jd = common.isot2jd(self.ui.isot_edit.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Invalid ISOT.', 0, 1, 0)
            return
        self.ui.jd_edit.setText('{:8f}'.format(jd))
    
    def jdedited(self):
        try:
            isot = common.jd2isot(float(self.ui.jd_edit.text()))
        except ValueError:
            QMessageBox.information(self, 'Info', 'Invalid JD.', 0, 1, 0)
            return
        self.ui.jd_edit.setText(isot)
    

    def ok_clicked(self):
        newplan = {}
        
        probe = {}
        probe['name'] = self.ui.probename.text()
        probe['base'] = self.ui.spacebase.currentText()
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Probe mass should be a float number.', 0, 1, 0)
            return
        if mass <= 0.0:
            QMessageBox.information(self, 'Info', 'Invalid Probe mass.', 0, 1, 0)
            return
        probe['pmass'] = mass
        
        target = {}
        if self.ui.planetbutton.isChecked():
            target['name'] = self.ui.planets.currentText()
            target['file'] = ''
            target['SPKID1A'] = 0
            for planet in common.planets_id:
                if planet[1] != target['name']: continue
                if planet[1] == 'Moon' or planet[1] == 'Earth':
                    target['SPKID1B'] = 3
                    target['SPKID2A'] = 3
                    target['SPKID2B'] = planet[0]
                else:
                    target['SPKID1B'] = planet[0]
                    target['SPKID2A'] = 0
                    target['SPKID2B'] = 0
        if self.ui.smallbodybutton.isChecked():
            target['name'] = self.ui.targetname.text()
            target['file'] = self.ui.spkfilepath.text()
            target['SPKID1A'] = 0
            target['SPKID1B'] = 10
            target['SPKID2A'] = 10
            try:
                spkid = int(self.ui.spkid_edit.text())
            except ValueError:
                QMessageBox.information(self, 'Info', 'SPKID should be an Integer.', 0, 1, 0)
                return
            target['SPKID2B'] = spkid
            
        newplan['probe'] = probe
        newplan['target'] = target
        newplan['maneuvers'] = []
        g.manplan = newplan
        self.accept()


from ftasettingdialog import *

class FTAsettingDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ftasettingdialog()
        self.ui.setupUi(self)
        self.connect(self.ui.fromshoworbit, SIGNAL('clicked()'), self.ta_radioclicked)
        self.connect(self.ui.directinput, SIGNAL('clicked()'), self.ta_radioclicked)
        self.connect(self.ui.ok_button, SIGNAL('clicked()'), self.ok_clicked)
        self.connect(self.ui.cancel_button, SIGNAL('clicked()'), self.reject)
        
        self.ta_radioclicked()
        
    def ta_radioclicked(self):
        if self.ui.fromshoworbit.isChecked():
            ta = g.showorbitcontrol.get_pred_jd() - g.showorbitcontrol.jd
            self.ui.timetoarrival.setText('{:5f}'.format(ta))
            self.ui.timetoarrival.setEnabled(False)
        if self.ui.directinput.isChecked():
            self.ui.timetoarrival.setEnabled(True)
    
    def ok_clicked(self):
        param = [0.0, np.zeros(3)]      # JD(days), X, Y, Z(meters)
        try:        
            delta_jd = float(self.ui.timetoarrival.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Enter a floating point number for Time to Arrival.', 0, 1, 0)
            return
        if delta_jd < 1.0:
            QMessageBox.information(self, 'Info', 'To use FTA, Time to Arrival shall be\n' \
                + 'greater than 1.0 day', 0, 1, 0)
            return
        param[0] = g.showorbitcontrol.jd + delta_jd
        
        jd = param[0]
        tpos, tvel = g.mytarget.posvel(jd)
        sunpos, sunvel = common.SPKposvel(10, jd)
#        sunpos, sunvel = common.SPKkernel[0,10].compute_and_differentiate(jd)
#        sunpos = common.eqn2ecl(sunpos) * 1000.0
#        sunvel = common.eqn2ecl(sunvel) / common.secofday * 1000.0

        try:        
            r = float(self.ui.rangeedit.text()) * 1000.0
            phi = float(self.ui.phiedit.text())
            elv = float(self.ui.elvedit.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Parameter should be floating numbers.', 0, 1, 0)
            return
        vect = common.polar2rect(r, phi, elv)
        
        delta_pos = common.ldv2ecldv(vect, tpos, tvel, sunpos, sunvel)
        param[1] = tpos + delta_pos
        
        g.fta_parameters = param
        self.accept()



from editmandialog import *

class EditManDialog(QtGui.QDialog):
    
    def __init__(self, parent=None, editman=None, currentrow=0):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 420, 640, 320)
        self.ui = Ui_editmandialog()
        self.ui.setupUi(self)
        self.connect(self.ui.applymantype, SIGNAL('clicked()'), self.applymantype)
        self.connect(self.ui.isotedit, SIGNAL('editingFinished()'), self.isotedited)
        self.connect(self.ui.jdedit, SIGNAL('editingFinished()'), self.jdedited)
        self.connect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), self.parameterchanged)
        self.connect(self.ui.finish_exec, SIGNAL('clicked()'), self.finish_exec)
        self.connect(self.ui.finishbutton, SIGNAL('clicked()'), self.finishbutton)
        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), self.cancelbutton)
        self.connect(self.ui.showorbit, SIGNAL('clicked()'), self.showorbit)
        self.connect(self.ui.computeFTA, SIGNAL('clicked()'), self.computefta)
        self.connect(self.ui.gettime, SIGNAL('clicked()'), self.gettime)
        self.connect(self.ui.applyduration, SIGNAL('clicked()'), self.applyduration)
        
        self.types = ['START', 'CP', 'EP_ON', 'EP_OFF', 'SS_ON', 'SS_OFF', 'FLYTO']
        self.typedict = {}
        for i in range(7):
            self.typedict[self.types[i]] = i
        self.paramname = ['time', 'dv', 'dvpd', 'phi', 'elv', 'aria', 'theta', 'inter']
        self.paramflag = [
            # 0:time, 1:dv, 2:dvpd, 3:phi, 4:elv, 5:aria, 6:theta, 7:inter
            [1, 1, 0, 1, 1, 0, 0, 0], # for START
            [0, 1, 0, 1, 1, 0, 0, 0], # for CP
            [0, 0, 1, 1, 1, 0, 0, 0], # for EP_ON
            [0, 0, 0, 0, 0, 0, 0, 0], # for EP_OFF
            [0, 0, 0, 0, 1, 1, 1, 0], # for SS_ON
            [0, 0, 0, 0, 0, 0, 0, 0], # for SS_OFF
            [1, 0, 0, 0, 0, 0, 0, 1]  # for FLYTO
            ]
        paramdesc = [
            'time  : Maneuver Time (JD)',
            'dv    : Delta-V absolute value (m/s)',
            'dvpd  : Delta-V per day for EP (m/s/day)',
            'phi   : Angle (deg) for START, CP and EP',
            'elv   : Angle (deg) for all prop.',
            'aria  : Aria of Solar Sail (m**2)',
            'theta : Angle (deg) for SS',
            'inter : Integration Interval (days)'
            ]
        self.fmttbl = [
            '{:.8f}',
            '{:.3f}',
            '{:.3f}',
            '{:.2f}',
            '{:.2f}',
            '{:.1f}',
            '{:.2f}',
            '{:.5f}'
            ]
        self.stringitems = []
        for item in paramdesc:
            self.stringitems.append(QTableWidgetItem(item))
        
        for item in self.types:
            self.ui.mantype.addItem(item)
        self.ui.parameters.setColumnWidth(0,350)
        self.ui.parameters.setColumnWidth(1,160)
        for i in range(1, 8):
            row = i - 1
            self.ui.parameters.setItem(row, 0, self.stringitems[i])
            self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
        
        self.currentrow = currentrow
        if editman == None:
            self.editman = None
            self.dispman()
        else:
            self.editman = editman.copy()
            self.dispman()
        self.setenable()

    def setenable(self):
        self.ui.computeFTA.setEnabled(False)
        self.ui.showorbit.setEnabled(False)
        self.ui.finish_exec.setEnabled(False)
        self.ui.gettime.setEnabled(False)
        self.ui.duration.setEnabled(False)
        self.ui.applyduration.setEnabled(False)
        self.ui.label_duration.setEnabled(False)
        self.ui.finishbutton.setEnabled(False)
        if self.editman == None: return
            
        self.ui.finishbutton.setEnabled(True)
        
        fta = (self.typeID == 0 and self.currentrow == 0) or \
            (self.typeID == 1 and self.currentrow == g.nextman and 
            g.myprobe.onflight)
        if fta:
            self.ui.computeFTA.setEnabled(True)

        buttons = (self.typeID == 0 and self.currentrow == 0) or \
            (self.currentrow == g.nextman and g.myprobe.onflight)
        if buttons:
            self.ui.showorbit.setEnabled(True)
            self.ui.finish_exec.setEnabled(True)
            
        gettime = (self.typeID == 0 and self.currentrow == 0) or \
            (self.typeID == 6 and self.currentrow == g.nextman and \
            g.myprobe.onflight)
        if gettime:
            self.ui.gettime.setEnabled(True)
        
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
        ival = [jdtoday, 0.0, 0.0, 0.0, 0.0, 10000.0, 45.0, 1.0]
        if g.myprobe != None:
            if g.myprobe.onflight:
                ival[0] = g.myprobe.jd
        self.editman = {}
        self.editman['type'] = self.types[typeID]
        for i in range(8):
            if self.paramflag[typeID][i] == 1:
                self.editman[self.paramname[i]] = ival[i]
        
    def dispman(self):
        if self.editman == None:
            self.ui.mantype.setCurrentIndex(-1)
            self.ui.mantypedisp.setText('Not Defined')
            self.ui.isotedit.setEnabled(False)
            self.ui.jdedit.setEnabled(False)
            for i in range(1, 8):
                row = i - 1
                self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
        else:
            self.typeID = self.typedict[self.editman['type']]
            self.ui.mantype.setCurrentIndex(self.typeID)
            self.ui.mantypedisp.setText(self.editman['type'])
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

            self.disconnect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), self.parameterchanged)
            
            for i in range(1, 8):
                row = i - 1
                if self.paramflag[self.typeID][i] == 1:
                    anitem = QTableWidgetItem(self.fmttbl[i].format(self.editman[self.paramname[i]]))
                    self.ui.parameters.setItem(row, 1, anitem)
                    self.ui.parameters.item(row, 1).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                    self.ui.parameters.item(row, 0).setFlags(Qt.ItemIsEnabled)
                else:
                    anitem = QTableWidgetItem('')
                    self.ui.parameters.setItem(row, 1, anitem)
                    self.ui.parameters.item(row, 1).setFlags(Qt.NoItemFlags)
                    self.ui.parameters.item(row, 0).setFlags(Qt.NoItemFlags)
    
            self.connect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), self.parameterchanged)
                
    def applymantype(self):
        newID = self.ui.mantype.currentIndex()
        if self.editman == None:
            self.initman(newID)
            self.dispman()
            if g.showorbitcontrol != None:
                g.showorbitcontrol.close()
            self.setenable()
            
        if self.typeID == newID:
            return
        ans = QMessageBox.question(self, 'Mantype changed', 'Parameters will be lost. OK?', 0, button1=1, button2=2)
        if ans == 1:
            self.initman(newID)
            self.dispman()
            if g.showorbitcontrol != None:
                g.showorbitcontrol.close()
            self.setenable()
        else:
            self.ui.mantype.setCurrentIndex(self.typeID)
        
    def isotedited(self):
        try:
            jd = common.isot2jd(self.ui.isotedit.text())
        except ValueError:
            self.ui.isotedit.setText(common.jd2isot(float(self.ui.jdedit.text())))
            QMessageBox.information(self, 'Time Error', 'Invalid ISOT', 0, 1, 0)
            return
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        if self.ui.duration.isEnabled():
            self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
        self.editman[self.paramname[0]] = jd
        
    def jdedited(self):
        try:
            jd = float(self.ui.jdedit.text())
        except ValueError:
            self.ui.jdedit.setText('{:.8f}'.format(common.isot2jd(self.ui.isotedit.text())))
            QMessageBox.information(self, 'Time Error', 'Invalid JD', 0, 1, 0)
            return
        self.ui.isotedit.setText(common.jd2isot(jd))
        if self.ui.duration.isEnabled():
            self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
        self.editman[self.paramname[0]] = jd
        
    def parameterchanged(self, row, colmn):
        if colmn != 1: return
        prevval = self.editman[self.paramname[row+1]]
        try:
            newval = float(self.ui.parameters.item(row, colmn).text())
        except ValueError:
            self.ui.parameters.item(row, colmn).setText(self.fmttbl[row+1].format(prevval))
            QMessageBox.information(self, 'Parameter Error', 'Enter a floating number', 0, 1, 0)
            return
        self.editman[self.paramname[row+1]] = newval

    def finish_exec(self):
        g.editedman = self.editman
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        self.done(g.finish_exec)
        
    def finishbutton(self):
        g.editedman = self.editman
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        self.accept()
        
    def cancelbutton(self):
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        self.reject()
        
    def closeEvent(self, event):
        ans = QMessageBox.question(self, 'Exit Editor', 'Discard changes?', 0, button1=1, button2=2)
        if ans == 2:
            event.ignore()
            return
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        event.accept()

    def showorbit(self):
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
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_dv(dv, phi, elv)
        g.showorbitcontrol.redraw()
    
    def showorbitSTART(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowStartOrbitDialog(self, self.editman)
            g.showorbitcontrol.show()
        else:
            g.showorbitcontrol.redraw()

    def showorbitFLYTO(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_DT(self.editman['time'])
        g.showorbitcontrol.redraw()
            
    def showorbitOTHER(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_dv(0.0, 0.0, 0.0)
        g.showorbitcontrol.redraw()
        
            
    def computefta(self):
        if g.showorbitcontrol == None:
            QMessageBox.information(self, 'Info', 'To use FTA, open Show Orbit and\n' \
                + 'specify Delta-T (DT)', 0, 1, 0)
            return

        ftadialog = FTAsettingDialog(self)
        ans = ftadialog.exec_()
        if ans == QDialog.Rejected:
            return
        
        jd = g.fta_parameters[0]
        tepos = g.fta_parameters[1]
        
        try:
            dv, phi, elv = g.showorbitcontrol.tbpred.fta(jd, tepos)
        except ValueError:
            QMessageBox.information(self, 'Info', 'Error occured during FTA computation.\n' \
                + 'Try different parameters', 0, 1, 0)
            return

        dv = round(dv, 3)
        phi = round(phi, 2)
        elv = round(elv, 2)
            
        mes = 'FTA Results are as follows. Apply them?\n' + \
            'dv = ' + str(dv) + '\n' + \
            'phi = ' + str(phi) + '\n' + \
            'elv = ' + str(elv)
        ans = QMessageBox.question(self, 'FTA Results', mes, 0, button1=1, button2=2)
        if ans == 1:
            self.editman['dv'] = dv
            self.editman['phi'] = phi
            self.editman['elv'] = elv
            self.dispman()
            self.showorbit()

    def gettime(self):
        if g.showorbitcontrol != None:
            jd = g.showorbitcontrol.get_pred_jd()
            self.ui.jdedit.setText('{:.8f}'.format(jd))
            self.jdedited()
            self.showorbit()
            if self.typeID == 0:    # case of START
                g.showorbitcontrol.reset()
            if self.typeID == 6:    # case of FLYTO
                dt = jd - g.myprobe.jd
                self.ui.duration.setText('{:.5f}'.format(dt))

    def applyduration(self):
        try:
            dt = float(self.ui.duration.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Invalid Duration days', 0, 1, 0)
            return
        jd = g.myprobe.jd + dt
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        self.jdedited()
        


from showorbitcontrol import *

class ShowOrbitDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 780, 640, 211)
        self.ui = Ui_ShowOrbitControl()
        self.ui.setupUi(self)
        
        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), self.fastbackward)
        self.connect(self.ui.showprobe, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.showtarget, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.timescale, SIGNAL('valueChanged(int)'), self._valuechanged)
        self.connect(self.ui.dtApply, SIGNAL('clicked()'), self.dtapply)

        self.artist_of_orbit = None
        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        
        self.tbpred = None
        self.reset()

    def reset(self):
        self.dv = 0.0
        self.phi = 0.0
        self.elv = 0.0
        self.delta_jd = 0.0
        self.redraw()
        
    def redraw(self):
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 'Your probe has no valid orbit.', 0, 1, 0)
            return

        self.jd = g.myprobe.jd
        self.ui.currentdate.setText(common.jd2isot(self.jd))

        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        
        self.ppos = g.myprobe.pos
        self.pvel = g.myprobe.vel
        if self.tbpred == None:
            self.tbpred = TwoBodyPred(g.myprobe.name)

        self.tbpred.fix_state(self.jd, self.ppos, self.pvel)
        self.tbpred.set_pred_dv(self.dv, self.phi, self.elv)
        x, y, z, t = self.tbpred.points(g.ndata)
        self.artist_of_orbit = g.ax.plot(x, y, z, color='red', lw=0.75)
        
        self.ui.man_dv.setText('{:.3f}'.format(self.dv))
        self.ui.man_phi.setText('{:.2f}'.format(self.phi))
        self.ui.man_elv.setText('{:.2f}'.format(self.elv))

        self.restore_settings()
        self._redrawmark()

    def _redrawmark(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        tempjd = self.jd + self.delta_jd
        self.ui.preddate.setText(common.jd2isot(tempjd))
        
        probe_pos, probe_vel = self.tbpred.posvelatt(tempjd)
        self.target_pos, target_vel = g.mytarget.posvel(tempjd)
        
        sunpos = common.SPKkernel[0, 10].compute(tempjd)
        self.sun_pos = common.eqn2ecl(sunpos) * 1000.0

        xlim = g.ax.get_xlim()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = probe_pos
        else:
            cent = self.target_pos
        
        g.ax.set_xlim(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim(cent[2]-hw, cent[2]+hw)

        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.ui.showprobe.isChecked():
            self.artist_of_probe = g.ax.scatter(*probe_pos, s=50, c='r',depthshade=False, marker='x')
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        if self.ui.showtarget.isChecked():
            self.artist_of_target = g.ax.scatter(*self.target_pos, s=40, c='g',depthshade=False, marker='+')
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*self.sun_pos, s=50, c='w',depthshade=False, marker='o')

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(tempjd)

        remove_time()
        if self.delta_jd == 0.0:
            replot_time(tempjd, 'Real')
        else:
            replot_time(tempjd, 'Prediction')

        plt.draw()
        
        # display relative position and velocity
        rel_pos = self.target_pos - probe_pos
        rel_pos = common.eclv2lv(rel_pos, probe_pos, probe_vel, self.tbpred.sunpos, self.tbpred.sunvel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - probe_vel
        rel_vel = common.eclv2lv(rel_vel, probe_pos, probe_vel, self.tbpred.sunpos, self.tbpred.sunvel)
        relabsvel, tvphi, tvelv = common.rect2polar(rel_vel)
        losvel = np.dot(rel_vel, rel_pos) / trange
        self.ui.RPTrange.setText('{:.3f}'.format(trange / 1000.0))
        self.ui.RPTphi.setText('{:.2f}'.format(tphi))
        self.ui.RPTelv.setText('{:.2f}'.format(telv))
        self.ui.RVTvel.setText('{:.3f}'.format(relabsvel))
        self.ui.RVTphi.setText('{:.2f}'.format(tvphi))
        self.ui.RVTelv.setText('{:.2f}'.format(tvelv))
        self.ui.LoSVvel.setText('{:.3f}'.format(losvel))

    def set_pred_dv(self, dv, phi, elv):
        self.dv = dv
        self.phi = phi
        self.elv = elv
        self.redraw()

    def set_pred_DT(self, jd):
        dt = jd - self.jd
        self.ui.delta_t_edit.setText('{:.8f}'.format(dt))
        self.dtapply()

    def get_pred_jd(self):
        return self.jd + self.delta_jd
        
    def forward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value()
        self.delta_jd += 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        
    def backward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value()
        self.delta_jd -= 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        
    def fastforward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value() + 1
        self.delta_jd += 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()

    def fastbackward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value() + 1
        self.delta_jd -= 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        
    def _statuschanged(self):
        self.save_settings()
        self._redrawmark()
        
    def _valuechanged(self):
        self.save_settings()
    
    def dtapply(self):
        text = self.ui.delta_t_edit.text()
        try:
            value = float(text)
        except ValueError:
            self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
            QMessageBox.information(self, 'Info', 'Enter a floating point number.', 0, 1, 0)
            return
        self.delta_jd = value
        self._redrawmark()

    def closeEvent(self, event):
        g.showorbitcontrol = None
        self.save_settings()
        event.accept()
        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        remove_planets()
        remove_time()

    def save_settings(self):
        settings = {}
        settings['Show Probe'] = self.ui.showprobe.checkState()
        settings['Show Target'] = self.ui.showtarget.checkState()
        settings['Show Planets'] = self.ui.showplanets.checkState()
        settings['SSB'] = self.ui.tobarycenter.isChecked()
        settings['Probe'] = self.ui.toprobe.isChecked()
        settings['Target'] = self.ui.totarget.isChecked()
        settings['Scale'] = self.ui.timescale.value()
        g.showorbitsettings = settings
        
    def restore_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.showprobe.setCheckState(s['Show Probe'])
            self.ui.showtarget.setCheckState(s['Show Target'])
            self.ui.showplanets.setCheckState(s['Show Planets'])
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])
            self.ui.timescale.setValue(s['Scale'])



class ShowStartOrbitDialog(ShowOrbitDialog):
    def __init__(self, parent=None, editman=None):
        self.editman = editman
        super().__init__(parent)
        self.ui.ctimeLabel.setText('S. Time')
        
    def redraw(self):
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        self.jd = self.editman['time']
        self.ui.currentdate.setText(common.jd2isot(self.jd))

        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self.ui.timescale.setValue(0)
        
        self.ppos, self.pvel = g.myprobe.pseudostart(self.jd, 0.0, 0.0, 0.0)
        self.dv = self.editman['dv']
        self.phi = self.editman['phi']
        self.elv = self.editman['elv']

        if self.tbpred == None:
            self.tbpred = TwoBodyPred(g.myprobe.name)

        self.tbpred.fix_state(self.jd, self.ppos, self.pvel)
        self.tbpred.set_pred_dv(self.dv, self.phi, self.elv)
        x, y, z, t = self.tbpred.points(g.ndata)
        self.artist_of_orbit = g.ax.plot(x, y, z, color='red', lw=0.75)
        
        self.ui.man_dv.setText('{:.3f}'.format(self.dv))
        self.ui.man_phi.setText('{:.2f}'.format(self.phi))
        self.ui.man_elv.setText('{:.2f}'.format(self.elv))

        self._redrawmark()
        


from flightreviewcontrol import *

class FlightReviewControl(QtGui.QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 780, 640, 211)
        self.ui = Ui_FlightReviewControl()
        self.ui.setupUi(self)

        # Get Settings of 'Look at' from showorbitsettings
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])
            self.ui.showplanets.setChecked(s['Show Planets'])
        
        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), self.fastbackward)
        self.connect(self.ui.showkepler, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), self._statuschanged)

        self.artist_of_orbit = None
        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        
        self.tbpred = None
        self.reset()
        
    def reset(self):
        self.c_index = 0
        self.redraw()

    def redraw(self):
#        if self.artist_of_orbit != None:
#            self.artist_of_orbit[0].remove()
#            self.artist_of_orbit = None
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 'Your probe has no valid orbit.', 0, 1, 0)
            return

        if g.myprobe.trj_record[-1][0]['type'] != 'FLYTO':
            QMessageBox.information(self, 'Info', 'Last maneuver was not FLYTO.', 0, 1, 0)
            return

        self.last_trj = g.myprobe.trj_record[-1][1:]
        self.start_time = self.last_trj[0][0]
#        self.end_time = self.last_trj[0][-1]  not used?
        self.ui.starttime.setText(common.jd2isot(self.start_time))
        
        self._redrawmark()

    def _redrawmark(self):
        c_time = self.last_trj[0][self.c_index]
        delta_jd = c_time - self.start_time
        self.ui.currenttime.setText(common.jd2isot(c_time))
        self.ui.delta_t_edit.setText('{:.8f}'.format(delta_jd))

        ppos = np.zeros(3)
        pvel = np.zeros(3)
        ppos[0] = self.last_trj[1][self.c_index]
        ppos[1] = self.last_trj[2][self.c_index]
        ppos[2] = self.last_trj[3][self.c_index]
        pvel[0] = self.last_trj[4][self.c_index]
        pvel[1] = self.last_trj[5][self.c_index]
        pvel[2] = self.last_trj[6][self.c_index]

        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None

        if self.ui.showkepler.isChecked():
            if self.tbpred == None:
                self.tbpred = TwoBodyPred(g.myprobe.name)
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata)
            self.artist_of_orbit = g.ax.plot(x, y, z, color='red', lw=0.75)

        target_pos, target_vel = g.mytarget.posvel(c_time)
        sun_pos, sun_vel = common.SPKposvel(10, c_time)        

        xlim = g.ax.get_xlim()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = ppos
        else:
            cent = target_pos
        
        g.ax.set_xlim(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim(cent[2]-hw, cent[2]+hw)

        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*ppos, s=50, c='r',depthshade=False, marker='x')
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',depthshade=False, marker='+')
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',depthshade=False, marker='o')

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(c_time)

        remove_time()
        replot_time(c_time, 'Real')
        
        plt.draw()
        
        # display relative position and velocity
        rel_pos = target_pos - ppos
        rel_pos = common.eclv2lv(rel_pos, ppos, pvel, sun_pos, sun_vel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - pvel
        rel_vel = common.eclv2lv(rel_vel, ppos, pvel, sun_pos, sun_vel)
        relabsvel, tvphi, tvelv = common.rect2polar(rel_vel)
        losvel = np.dot(rel_vel, rel_pos) / trange
        self.ui.RPTrange.setText('{:.3f}'.format(trange / 1000.0))
        self.ui.RPTphi.setText('{:.2f}'.format(tphi))
        self.ui.RPTelv.setText('{:.2f}'.format(telv))
        self.ui.RVTvel.setText('{:.3f}'.format(relabsvel))
        self.ui.RVTphi.setText('{:.2f}'.format(tvphi))
        self.ui.RVTelv.setText('{:.2f}'.format(tvelv))
        self.ui.LoSVvel.setText('{:.3f}'.format(losvel))

    def forward(self):
        if self.c_index + 1 < len(self.last_trj[0]):
            self.c_index += 1
            self._redrawmark()
        
    def backward(self):
        if self.c_index > 0:
            self.c_index -= 1
            self._redrawmark()
        
    def fastforward(self):
        if self.c_index == len(self.last_trj[0]) - 1: return
        hopping = self.ui.timescale.value()
        self.c_index += hopping
        if self.c_index >= len(self.last_trj[0]):
            self.c_index = len(self.last_trj[0]) - 1
        self._redrawmark()

    def fastbackward(self):
        if self.c_index == 0: return
        hopping = self.ui.timescale.value()
        self.c_index -= hopping
        if self.c_index < 0:
            self.c_index = 0
        self._redrawmark()
        
    def _statuschanged(self):
        self.save_settings()
        self._redrawmark()

    def save_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            s['Show Planets'] = self.ui.showplanets.checkState()
            s['SSB'] = self.ui.tobarycenter.isChecked()
            s['Probe'] = self.ui.toprobe.isChecked()
            s['Target'] = self.ui.totarget.isChecked()
            g.showorbitsettings = s
        
    def closeEvent(self, event):
        g.flightreviewcontrol = None
        event.accept()
        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        remove_planets()
        remove_time()

from reviewthroughoutcontrol import *

class ReviewThroughoutControl(QtGui.QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 780, 640, 211)
        self.ui = Ui_ReviewThroughoutControl()
        self.ui.setupUi(self)

        # Get Settings of 'Look at' from showorbitsettings
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])
            self.ui.showplanets.setChecked(s['Show Planets'])

        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), self.fastbackward)
        self.connect(self.ui.previousman, SIGNAL('clicked()'), self.previousman)
        self.connect(self.ui.nextman, SIGNAL('clicked()'), self.nextman)
        self.connect(self.ui.showkepler, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.showmantype, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), self._statuschanged)

        self.mainwindow = parent
        self.artist_of_orbit = None
        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        self.artist_of_type = None
        
        self.tbpred = TwoBodyPred(g.myprobe.name)
        self.man_index = 0
        self.man_count = len(g.myprobe.trj_record)
        
        self.drawman()
        
    def drawman(self):
        record = g.myprobe.trj_record[self.man_index]
        mantype = record[0]['type']
        self.c_mantype = mantype
        self.mantext = '   ' + str(self.man_index + 1) + ' ' + mantype
        status = np.zeros(7)
        if mantype == 'FLYTO':
            status[0] = record[1][0]
            status[1] = record[2][0]
            status[2] = record[3][0]
            status[3] = record[4][0]
            status[4] = record[5][0]
            status[5] = record[6][0]
            status[6] = record[7][0]
            self.last_trj = record[1:]
            self.c_index = 0
            self.ui.fastbackward.setEnabled(True)
            self.ui.backward.setEnabled(True)
            self.ui.forward.setEnabled(True)
            self.ui.fastforward.setEnabled(True)
            self.ui.timescale.setEnabled(True)
        else:
            status = record[1]
            self.ui.fastbackward.setEnabled(False)
            self.ui.backward.setEnabled(False)
            self.ui.forward.setEnabled(False)
            self.ui.fastforward.setEnabled(False)
            self.ui.timescale.setEnabled(False)
        if mantype == 'START':
            self.ui.starttime.setText(common.jd2isot(record[1][0]))
            self.start_time = status[0]
        target_pos, target_vel = g.mytarget.posvel(status[0])
        
        # adjust center of image
        xlim = g.ax.get_xlim()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = status[1:4]
        else:
            cent = target_pos
        g.ax.set_xlim(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim(cent[2]-hw, cent[2]+hw)

        # Kepler Orbit of probe        
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        if self.ui.showkepler.isChecked():
            self.tbpred.fix_state(status[0], status[1:4], status[4:])
            x, y, z, t = self.tbpred.points(g.ndata)
            self.artist_of_orbit = g.ax.plot(x, y, z, color='red', lw=0.75)

        # Planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(status[0])
        
        # Kepler Orbit of target
        if g.saved_artist_of_target != None:
            g.saved_artist_of_target[0].remove()
        g.saved_artist_of_target = plot_2b_orbit_of_target(g.ndata, status[0])

        # Probe mark
        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*status[1:4], s=50, c='r',depthshade=False, marker='x')
        
        # Maneuver Type
        if self.artist_of_type != None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            if mantype == 'FLYTO':
                self.artist_of_type = g.ax.text(*status[1:4], self.mantext+'(start)', color='r', fontsize=11)
            else:
                self.artist_of_type = g.ax.text(*status[1:4], self.mantext, color='r', fontsize=11)
        
        # Target mark
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',depthshade=False, marker='+')
        
        # Sun mark
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        sun_pos, sun_vel = common.SPKposvel(10, status[0])
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',depthshade=False, marker='o')
        
        # time
        remove_time()
        replot_time(status[0], 'Real')
        
        # display relative position and velocity, and time
        rel_pos = target_pos - status[1:4]
        rel_pos = common.eclv2lv(rel_pos, status[1:4], status[4:], sun_pos, sun_vel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - status[4:]
        rel_vel = common.eclv2lv(rel_vel, status[1:4], status[4:], sun_pos, sun_vel)
        relabsvel, tvphi, tvelv = common.rect2polar(rel_vel)
        losvel = np.dot(rel_vel, rel_pos) / trange
        self.ui.RPTrange.setText('{:.3f}'.format(trange / 1000.0))
        self.ui.RPTphi.setText('{:.2f}'.format(tphi))
        self.ui.RPTelv.setText('{:.2f}'.format(telv))
        self.ui.RVTvel.setText('{:.3f}'.format(relabsvel))
        self.ui.RVTphi.setText('{:.2f}'.format(tvphi))
        self.ui.RVTelv.setText('{:.2f}'.format(tvelv))
        self.ui.LoSVvel.setText('{:.3f}'.format(losvel))
        delta_jd = status[0] - self.start_time
        self.ui.currenttime.setText(common.jd2isot(status[0]))
        self.ui.delta_t_edit.setText('{:.8f}'.format(delta_jd))

        self.mainwindow.ui.manplans.selectRow(self.man_index)
        
    def drawFLYTO(self):
        c_time = self.last_trj[0][self.c_index]
        delta_jd = c_time - self.start_time
        self.ui.currenttime.setText(common.jd2isot(c_time))
        self.ui.delta_t_edit.setText('{:.8f}'.format(delta_jd))
        
        ppos = np.zeros(3)
        pvel = np.zeros(3)

        ppos[0] = self.last_trj[1][self.c_index]
        ppos[1] = self.last_trj[2][self.c_index]
        ppos[2] = self.last_trj[3][self.c_index]
        pvel[0] = self.last_trj[4][self.c_index]
        pvel[1] = self.last_trj[5][self.c_index]
        pvel[2] = self.last_trj[6][self.c_index]

        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None

        if self.ui.showkepler.isChecked():
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata)
            self.artist_of_orbit = g.ax.plot(x, y, z, color='red', lw=0.75)

        target_pos, target_vel = g.mytarget.posvel(c_time)
        sun_pos, sun_vel = common.SPKposvel(10, c_time)        

        xlim = g.ax.get_xlim()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = ppos
        else:
            cent = target_pos
        
        g.ax.set_xlim(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim(cent[2]-hw, cent[2]+hw)

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(c_time)

        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*ppos, s=50, c='r',depthshade=False, marker='x')
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None

        # Maneuver Type
        if self.artist_of_type != None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            if self.c_index == 0:
                self.artist_of_type = g.ax.text(*ppos, self.mantext+'(start)', color='r', fontsize=11)
            elif self.c_index + 1 == len(self.last_trj[0]):
                self.artist_of_type = g.ax.text(*ppos, self.mantext+'(end)', color='r', fontsize=11)
            else:
                self.artist_of_type = g.ax.text(*ppos, self.mantext, color='r', fontsize=11)

        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',depthshade=False, marker='+')
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',depthshade=False, marker='o')

        remove_time()
        replot_time(c_time, 'Real')
        
        plt.draw()
        
        # display relative position and velocity
        rel_pos = target_pos - ppos
        rel_pos = common.eclv2lv(rel_pos, ppos, pvel, sun_pos, sun_vel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - pvel
        rel_vel = common.eclv2lv(rel_vel, ppos, pvel, sun_pos, sun_vel)
        relabsvel, tvphi, tvelv = common.rect2polar(rel_vel)
        losvel = np.dot(rel_vel, rel_pos) / trange
        self.ui.RPTrange.setText('{:.3f}'.format(trange / 1000.0))
        self.ui.RPTphi.setText('{:.2f}'.format(tphi))
        self.ui.RPTelv.setText('{:.2f}'.format(telv))
        self.ui.RVTvel.setText('{:.3f}'.format(relabsvel))
        self.ui.RVTphi.setText('{:.2f}'.format(tvphi))
        self.ui.RVTelv.setText('{:.2f}'.format(tvelv))
        self.ui.LoSVvel.setText('{:.3f}'.format(losvel))
    
    def forward(self):
        if self.c_index + 1 < len(self.last_trj[0]):
            self.c_index += 1
            self.drawFLYTO()
    
    def backward(self):
        if self.c_index > 0:
            self.c_index -= 1
            self.drawFLYTO()
        
    def fastforward(self):
        if self.c_index == len(self.last_trj[0]) - 1: return
        hopping = self.ui.timescale.value()
        self.c_index += hopping
        if self.c_index >= len(self.last_trj[0]):
            self.c_index = len(self.last_trj[0]) - 1
        self.drawFLYTO()

    def fastbackward(self):
        if self.c_index == 0: return
        hopping = self.ui.timescale.value()
        self.c_index -= hopping
        if self.c_index < 0:
            self.c_index = 0
        self.drawFLYTO()

    def previousman(self):
        if self.c_mantype == 'FLYTO':
            if self.c_index == 0:
                if self.man_index == 0:
                    return
                self.man_index -= 1
                self.drawman()
            else:
                self.c_index = 0
                self.drawFLYTO()
        else:
            if self.man_index == 0:
                return
            self.man_index -= 1
            self.drawman()
    
    def nextman(self):
        if self.c_mantype == 'FLYTO':
            length = len(self.last_trj[0])
            if self.c_index + 1 == length:
                if self.man_index + 1 == self.man_count:
                    return
                self.man_index += 1
                self.drawman()
            else:
                self.c_index = length - 1
                self.drawFLYTO()
        else:
            if self.man_index + 1 == self.man_count:
                return
            self.man_index += 1
            self.drawman()
        
    def _statuschanged(self):
        self.save_settings()
        if self.c_mantype == 'FLYTO':
            self.drawFLYTO()
        else:
            self.drawman()
    
    def save_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            s['Show Planets'] = self.ui.showplanets.checkState()
            s['SSB'] = self.ui.tobarycenter.isChecked()
            s['Probe'] = self.ui.toprobe.isChecked()
            s['Target'] = self.ui.totarget.isChecked()
            g.showorbitsettings = s
        
    def closeEvent(self, event):
        g.reviewthroughoutcontrol = None
        event.accept()
        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.artist_of_type != None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        if self.artist_of_orbit != None:
            self.artist_of_orbit[0].remove()
            self.artist_of_orbit = None
        remove_planets()
        remove_time()


from mainwindow import *

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(10, 40, 640, 700)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.manplans.setColumnWidth(0,60)
        self.ui.manplans.setColumnWidth(1,350)
        self.ui.manplans.setColumnWidth(2,60)
        self.ui.manplans.setCornerButtonEnabled(False)              # Disable table selection by clicking corner button
        self.ui.manplans.horizontalHeader().setClickable(False)     # Disable colomn selection by clicking
        self.ui.manplans.verticalHeader().setClickable(False)       # Disable row selection by clicking
        self.ui.selectedman.setColumnWidth(0,100)
        self.ui.selectedman.setColumnWidth(1,139)
        self.connect(self.ui.actionOpen, SIGNAL('triggered()'), self.openmanplan)
        self.connect(self.ui.actionNew, SIGNAL('triggered()'), self.newmanplan)
        self.connect(self.ui.actionQuit, SIGNAL('triggered()'), self.appquit)
        self.connect(self.ui.actionSave, SIGNAL('triggered()'), self.savemanplan)
        self.connect(self.ui.actionSave_as, SIGNAL('triggered()'), self.saveasmanplan)
        self.connect(self.ui.actionAbout_SSVG, SIGNAL('triggered()'), self.aboutselected)
        self.connect(self.ui.execNext, SIGNAL('clicked()'), self.execnext)
        self.connect(self.ui.reviewthroughout, SIGNAL('clicked()'), self.reviewthroughout)
        self.connect(self.ui.flightreview, SIGNAL('clicked()'), self.showflightreview)
        self.connect(self.ui.showOrbit, SIGNAL('clicked()'), self.showorbit)
        self.connect(self.ui.editnext, SIGNAL('clicked()'), self.editnext)
        self.connect(self.ui.initexec, SIGNAL('clicked()'), self.initexec)
        self.connect(self.ui.manplans, SIGNAL('currentCellChanged(int,int,int,int)'), self.manplanscellchanged)
        self.connect(self.ui.manplans, SIGNAL('cellDoubleClicked(int,int)'), self.editman)
        self.connect(self.ui.execto, SIGNAL('clicked()'), self.execto)
        self.connect(self.ui.editMan, SIGNAL('clicked()'), self.editman)
        self.connect(self.ui.insertMan, SIGNAL('clicked()'), self.insertman)
        self.connect(self.ui.deleteMan, SIGNAL('clicked()'), self.deleteman)

        self.ui.manplans.verticalHeader().setFixedWidth(30)     # Qt document has no information about this method.
        self.ui.progressBar.setVisible(False)
        
        self.pbar = self.ui.progressBar
        self.plabel = self.ui.label_progress
        
        self.erasecurrentstatus()
        self.currentrow = 0
        self.paramname = ['time', 'dv', 'dvpd', 'phi', 'elv', 'aria', 'theta', 'inter']
        self.typedict = {'START':0, 'CP':1, 'EP_ON':2, 'EP_OFF':3, 'SS_ON':4,
                         'SS_OFF':5, 'FLYTO':6}
        self.paramflag = [
            # 0:time, 1:dv, 2:dvpd, 3:phi, 4:elv, 5:aria, 6:theta, 7:inter
            [1, 1, 0, 1, 1, 0, 0, 0], # for START
            [0, 1, 0, 1, 1, 0, 0, 0], # for CP
            [0, 0, 1, 1, 1, 0, 0, 0], # for EP_ON
            [0, 0, 0, 0, 0, 0, 0, 0], # for EP_OFF
            [0, 0, 0, 0, 1, 1, 1, 0], # for SS_ON
            [0, 0, 0, 0, 0, 0, 0, 0], # for SS_OFF
            [1, 0, 0, 0, 0, 0, 0, 1]  # for FLYTO
            ]
        self.fmttbl = [
            '{:.8f}',
            '{:.3f}',
            '{:.3f}',
            '{:.2f}',
            '{:.2f}',
            '{:.1f}',
            '{:.2f}',
            '{:.5f}'
            ]
        self.initselectedman()
        self.eraseselectedman()
        self.initSSV()

    def initSSV(self):
        g.currentdir = ''
        g.manfilename = None
        g.manplan = None
        g.maneuvers = None
        g.manplan_saved = True
        g.ndata = 1001
        g.myprobe = None
        
        g.mytarget = None
        g.saved_artist_of_target = None
        g.saved_artist_of_probe = []
        g.saved_artist_of_time = None
        g.saved_mark_of_planets = None
        g.saved_name_of_planets = []
    
        plt.ion()
        g.fig=plt.figure(figsize=(11,11))
        g.ax=g.fig.gca(projection='3d', aspect='equal')
    
        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)
        g.ax.set_xlabel('X')
        g.ax.set_ylabel('Y')
        g.ax.set_zlabel('Z')
        g.fig.tight_layout()
        
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(660, 40, 960, 960)
        g.fig.canvas.set_window_title('3D Orbit')
        
        g.showorbitcontrol = None
        g.showorbitsettings = None
        g.flightreviewcontrol = None
        g.reviewthroughoutcontrol = None
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        
        g.finish_exec = 2

    def closeEvent(self, event):
#
#        print(dir(g))  # check global data list
#
        if g.manplan_saved:
            event.accept()
            QApplication.closeAllWindows()
        else:
            ans = QMessageBox.question(self, 'Quit SSV', 
                'Flight Plan has not been saved.\nDo you want to save?', 
                ' Save and Quit ', ' Discard and Quit ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
                event.accept()
                QApplication.closeAllWindows()
            elif ans == 1:
                event.accept()
                QApplication.closeAllWindows()
            else:
                event.ignore()

    def openmanplan(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'Open Flight Plan File', 
                'Current Flight Plan has not been saved.\nDo you want to save?', 
                ' Save and Proceed ', ' Discard and Proceed ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
            elif ans == 1:
                pass
            else:
                return
            
        ans = QFileDialog.getOpenFileName(parent=self,
            caption='Select input maneuver file',
            directory=g.currentdir, filter='JSON files (*.json)')
        if ans == '': return

        dirs = ans.split('/')
        g.currentdir = '/'.join(dirs[0:-1])

        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()
            
        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)

        self.erasecurrentstatus()
        self.eraseselectedman()
        
        g.manfilename = ans
        manfile = open(g.manfilename, 'r')
        g.manplan = json.load(manfile)
        manfile.close()
        self.dispmanfilename()
        g.maneuvers = g.manplan['maneuvers']
        g.manplan_saved = True
        g.nextman = 0
        g.myprobe = probe.Probe(**g.manplan['probe'])
        for art in g.saved_artist_of_probe:
            art[0].remove()
        g.saved_artist_of_probe = []
        
        if g.saved_artist_of_target != None:
            g.saved_artist_of_target[0].remove()
        
        dt = datetime.now()
        jdtoday = julian.to_jd(dt, fmt='jd')
        cjd = int(jdtoday + 0.5) - 0.5
        g.mytarget = target.Target(**g.manplan['target'])
        g.saved_artist_of_target = plot_2b_orbit_of_target(g.ndata, cjd)
        
        plt.draw()
        
        if len(g.maneuvers) >= 1:
            if not ('onflight' in g.maneuvers[0]):
                g.maneuvers
        
        self.enablewidgets()

        self.ui.probename.setText(g.manplan['probe']['name'])
        self.ui.targetname.setText(g.manplan['target']['name'])
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)

    def newmanplan(self):
        if not g.manplan_saved:
            ans = QMessageBox.question(self, 'New Flight Plan', 
                'Current Flight Plan has not been saved.\nDo you want to save?', 
                ' Save and Proceed ', ' Discard and Proceed ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
            elif ans == 1:
                pass
            else:
                return

        newdialog = NewFlightPlanDialog(self)
        ans = newdialog.exec_()
        if ans == QDialog.Rejected:
            return

        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()

        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)

        self.erasecurrentstatus()
        self.eraseselectedman()
        g.manfilename = None
        self.dispmanfilename()
        g.maneuvers = g.manplan['maneuvers']
        g.manplan_saved = False
        g.nextman = 0
        g.myprobe = probe.Probe(**g.manplan['probe'])
        for art in g.saved_artist_of_probe:
            art[0].remove()
        g.saved_artist_of_probe = []
        
        if g.saved_artist_of_target != None:
            g.saved_artist_of_target[0].remove()
        
        dt = datetime.now()
        jdtoday = julian.to_jd(dt, fmt='jd')
        cjd = int(jdtoday + 0.5) - 0.5
        g.mytarget = target.Target(**g.manplan['target'])
        g.saved_artist_of_target = plot_2b_orbit_of_target(g.ndata, cjd)
        
        plt.draw()

        self.enablewidgets()
        
        self.ui.probename.setText(g.manplan['probe']['name'])
        self.ui.targetname.setText(g.manplan['target']['name'])
        
        g.showorbitsettings = None
        self.dispmanplan()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)

    def reviewthroughout(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 'Your probe is not on flight.', 0, 1, 0)
            return
        
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        
        if g.reviewthroughoutcontrol == None:
            g.reviewthroughoutcontrol = ReviewThroughoutControl(self)
            g.reviewthroughoutcontrol.show()
        else:
            g.reviewthroughoutcontrol.drawman()

    def redrawtargetorb(self):
        if g.myprobe == None:
            return
        if g.myprobe.onflight:
            if g.saved_artist_of_target != None:
                g.saved_artist_of_target[0].remove()
            jd = g.myprobe.jd
            g.saved_artist_of_target = plot_2b_orbit_of_target(g.ndata, jd)
            plt.draw()

    def savemanplan(self):
        if g.manfilename == None:
            self.saveasmanplan()
            return
        manfile = open(g.manfilename, 'w')
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        
    def saveasmanplan(self):
        if g.manfilename == None:
            dr = g.currentdir
        else:
            dr = g.manfilename
        ans = QFileDialog.getSaveFileName(self, 
            'Define output maneuver file', dr, 'JSON files (*.json)')
        if ans == '': return

        dirs = ans.split('/')
        g.currentdir = '/'.join(dirs[0:-1])
        
        g.manfilename = ans
        manfile = open(g.manfilename, 'w')
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        self.dispmanfilename()

    def dispmanplan(self):
        self.ui.manplans.clearContents()  # clear previous table
        self.ui.manplans.setRowCount(len(g.maneuvers)+1)
        for i in range(len(g.maneuvers)):
            if g.maneuvers[i] == None: continue
            mtype = g.maneuvers[i]['type']
            anitem = QTableWidgetItem(mtype)
            self.ui.manplans.setItem(i, 0, anitem)
            desc = ''
            for name in self.paramname:
                if name in g.maneuvers[i]:
                    if name == 'time':
                        desc = desc + 'Date=' + common.jd2datetime(g.maneuvers[i][name])[0] + ' '
                    else:
                        desc = desc + name + '=' + '{:.2f}'.format(g.maneuvers[i][name]) + ' '
            anitem = QTableWidgetItem(desc)
            self.ui.manplans.setItem(i, 1, anitem)
        anitem = QTableWidgetItem('Next')
        anitem.setTextAlignment(Qt.AlignCenter)
        self.ui.manplans.setItem(g.nextman, 2, anitem)
        self.ui.manplans.selectRow(self.currentrow)
        
    def appquit(self):        
        self.close()

    def execnext(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return False
        if len(g.maneuvers) <= g.nextman:
            QMessageBox.information(self, 'Info', "You don't have valid maneuver.", 0, 1, 0)
            return False
        if g.maneuvers[g.nextman] == None:
            QMessageBox.information(self, 'Info', "You don't have valid maneuver.", 0, 1, 0)
            return False
        
        # prepare progress bar
        ptext = 'Processing:  ' + str(g.nextman + 1) + ' ' + g.maneuvers[g.nextman]['type']
#
        if g.myprobe.exec_man(g.maneuvers[g.nextman], pbar=self.pbar, plabel=self.plabel, ptext=ptext):
            self.ui.reviewthroughout.setEnabled(True)
            if g.myprobe.trj_record[-1][0]['type'] == 'FLYTO':
                g.saved_artist_of_probe.append(plot_trj_of_probe())
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
            
            if g.showorbitcontrol == None:
                self.showorbit()
                self.ui.showOrbit.setEnabled(True)
        else:
            QMessageBox.information(self, 'Info', "Cannot Executhe the Flight Plan.", 0, 1, 0)
            return False

        self.redrawtargetorb()
        g.showorbitcontrol.reset()
        self.dispcurrentstatus()
        return True

    def execto(self):
        start = g.nextman
        stop = self.currentrow
        if start > stop:
            QMessageBox.information(self, 'Info', "Select maneuver later than 'Next'", 0, 1, 0)
            return
        for i in range(start, stop + 1):
            result = self.execnext()
            if not result:
                break

    def execinitialize(self):
        for art in g.saved_artist_of_probe:
            art[0].remove()
        g.saved_artist_of_probe = []
        g.myprobe.execinitialize()
        g.nextman = 0
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()
        self.ui.showOrbit.setEnabled(False)
        self.ui.flightreview.setEnabled(False)
        self.ui.reviewthroughout.setEnabled(False)
        self.erasecurrentstatus()

    def showorbit(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 'Your probe has no valid orbit.', 0, 1, 0)
            return
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        else:
            g.showorbitcontrol.redraw()

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
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
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
            QMessageBox.information(self, 'Info', 'START shall be the 1st maneuver', 0, 1, 0)
            return
        if g.editedman['type'] != 'START' and self.currentrow == 0:
            QMessageBox.information(self, 'Info', 'The 1st maneuver shall be START', 0, 1, 0)
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
            
    def deleteman(self):
        if self.currentrow == len(g.maneuvers):
            return
        mes = 'Line No. ' + str(self.currentrow + 1) + ' will be deleted. OK?'
        ans = QMessageBox.question(self, 'Delete Man.', mes, 0, button1=1, button2=2)
        if ans == 2: return
        if self.currentrow < len(g.maneuvers):
            del(g.maneuvers[self.currentrow])
            if self.currentrow < g.nextman:
                self.execinitialize()
            g.manplan_saved = False
            self.dispmanplan()

    def dispmanfilename(self):
        if g.manfilename == None:
            filename = ''
        else:
            drs = g.manfilename.split('/')
            drs = drs[-1].split('.')
            filename = '.'.join(drs[0:-1])
        self.ui.manfilename.setText(filename)

    def showflightreview(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 'Your probe is not on flight.', 0, 1, 0)
            return
        if g.myprobe.trj_record[-1][0]['type'] != 'FLYTO':
            QMessageBox.information(self, 'Info', 'Latest maneuver was not FLYTO.', 0, 1, 0)
            return  
        
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()
        
        if g.flightreviewcontrol == None:
            g.flightreviewcontrol = FlightReviewControl(self)
            g.flightreviewcontrol.show()
        else:
            g.flightreviewcontrol.redraw()

    def dispcurrentstatus(self):
        if self.tbpred_formain == None:
            self.tbpred_formain = TwoBodyPred(g.myprobe.name)
        self.tbpred_formain.fix_state(g.myprobe.jd, g.myprobe.pos, g.myprobe.vel)
        kepl = self.tbpred_formain.elmKepl()

        self.ui.label_ELM.setText('No.{0}  ({1})'.format(g.nextman, g.maneuvers[g.nextman-1]['type']))
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
            
        sunpos, sunvel = common.SPKposvel(10, g.myprobe.jd)
#        sunpos, sunvel = common.SPKkernel[0,10].compute_and_differentiate(g.myprobe.jd)
#        sunpos = common.eqn2ecl(sunpos) * 1000.0
#        sunvel = common.eqn2ecl(sunvel) / common.secofday * 1000.0
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
            'inter (days)'
            ]

        for i in range(1, 8):
            row = i - 1
            self.ui.selectedman.setItem(row, 0, QTableWidgetItem(paramdesc[i]))

    def dispselectedman(self):
        lenman = len(g.manplan['maneuvers'])
        if lenman == 0:
            return
        if self.currentrow < 0 or self.currentrow >= lenman:
            return
        man = g.manplan['maneuvers'][self.currentrow]
        typeID = self.typedict[man['type']]
        
        cman = str(self.currentrow + 1) + ' ' + man['type']
        self.ui.label_cman.setText(cman)
        
        if self.paramflag[typeID][0] == 1:
            self.ui.label_mantime_h.setEnabled(True)
            self.ui.label_mantime.setText(common.jd2isot(man['time']))

        for i in range(1, 8):
            row = i - 1
            if self.paramflag[typeID][i] == 1:
                anitem = QTableWidgetItem(self.fmttbl[i].format(man[self.paramname[i]]))
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
        for i in range(1, 8):
            row = i - 1
            anitem = QTableWidgetItem('')
            self.ui.selectedman.setItem(row, 1, anitem)
            self.ui.selectedman.item(row, 1).setFlags(Qt.NoItemFlags)
            self.ui.selectedman.item(row, 0).setFlags(Qt.NoItemFlags)
            
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #print(os.path.abspath(os.path.dirname(sys.argv[0])))
    g.mainform = MainForm()
    g.mainform.show()
    sys.exit(app.exec_())
