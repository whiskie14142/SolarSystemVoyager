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
import math

class _Gdata:
    """Container of global data
    """
    __slots__ = [
        'version',                  # version no. of this program
        'options',                  # runtime options
        'ax',                       # axes of matplotlib
        'currentdir',               # current directory of application
        'clipboard',                # system clipboard object
        'editedman',                # edited maneuver : output of EditManDialog
        'fig',                      # figure of matplotlib
        'logfile',                  # file object of the SSVG LOG
        'mainform',                 # mainform of this application
        'maneuvers',                # list of maneuvers
        'manfilename',              # file name of maneuver plan
        'manplan',                  # maneuver plan
        'manplan_saved',            # flag for saved or not saved
        'myprobe',                  # instance of space probe
        'mytarget',                 # instance of Target (destination of the probe)
        'ndata',                    # number of points to draw orbit
        'nextman',                  # index of next maneuver
        'probe_trj',                # list of probe trajectories of each FLYTO
        'probe_Kepler',             # points of Kepler orbit of probe
        'target_Kepler',            # points of Kepler orbit of target
        'artist_Ptrj',              # list of artists of matplotlib for probe trajectories
        'artist_PKepler',           # artist of matplotlib for probe orbit
        'artist_TKepler',           # artist of matplotlib for target orbit
        'artist_mark_of_planets',   # artist of matplotlib for planet marks
        'artist_name_of_planets',   # artist of matplotlib for planet names
        'artist_of_time',           # artist of matplotlib for time and its type
        'showorbitcontrol',         # instance of ShowOrbitDialog
        'showorbitsettings',        # current settings of ShowOrbitDialog
        'flightreviewcontrol',      # instance of FlightReviewControl
        'reviewthroughoutcontrol',  # instance of ReviewThroughoutControl
        'finish_exec',              # return code of EditManDialog for finish and execute (== 2)
        'fta_parameters'            # return parameters from FTAsettingDialog
        ]
    
# global data container instance    
g = _Gdata()
    
def erase_Ptrj():
    for artist in g.artist_Ptrj:
        artist[0].remove()
    g.artist_Ptrj = []
    
def draw_Ptrj():
    g.artist_Ptrj = []
    for trj in g.probe_trj:
        g.artist_Ptrj.append(g.ax.plot(*trj[2:5], color='blue', lw=0.75))
    
def erase_PKepler():
    if g.artist_PKepler != None:
        g.artist_PKepler[0].remove()
    g.artist_PKepler = None
    
def draw_PKepler():
    if g.probe_Kepler != None:
        g.artist_PKepler = g.ax.plot(*g.probe_Kepler, color='red', lw=0.75)
    
def erase_TKepler():
    if g.artist_TKepler != None:
        g.artist_TKepler[0].remove()
    g.artist_TKepler = None
    
def draw_TKepler():
    if g.target_Kepler != None:
        g.artist_TKepler = g.ax.plot(*g.target_Kepler, color='green', lw=0.75)

def remove_planets():
    if g.artist_mark_of_planets != None:
        g.artist_mark_of_planets.remove()
        g.artist_mark_of_planets = None
    for art in g.artist_name_of_planets:
        art.remove()
    g.artist_name_of_planets = []
    
def replot_planets(jd):
    markx = []
    marky = []
    markz = []
    names = []
    id_of_target = g.mytarget.getID()
    id_of_EMB = 3
    id_of_Moon = 301
    id_of_Sun = 10
    
    for i in range(12):
        if common.planets_id[i][0] == id_of_target: continue
        if common.planets_id[i][0] == id_of_EMB: continue
        if common.planets_id[i][0] == id_of_Sun: continue
        pos, vel = common.SPKposvel(common.planets_id[i][0], jd)
        markx.append(pos[0])
        marky.append(pos[1])
        markz.append(pos[2])
        if common.planets_id[i][0] == id_of_Moon:
            names.append('')
        else:
            names.append(common.planets_id[i][1])
    
    g.artist_mark_of_planets = g.ax.scatter(markx, marky, markz, marker='+', 
                                           s=20, c='c', depthshade=False)
    g.artist_name_of_planets = []
    for i in range(len(names)):
        g.artist_name_of_planets.append(g.ax.text(markx[i], marky[i], markz[i],
                                      ' '+names[i], color='c', fontsize=9))

def remove_time():
    if g.artist_of_time != None:
        g.artist_of_time.remove()
        g.artist_of_time = None

def replot_time(jd, ttype=''):
    s = common.jd2isot(jd) + ' (' + ttype + ')'
    g.artist_of_time = g.ax.text2D(0.02, 0.96, s, transform=g.ax.transAxes)

def nowtimestr():
    # returns "YYYY-MM-DDTHH:MM:SS"
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
def nowtimestrf():
    # returns "YYYYMMDD_HHMMSS" (this string can be used as a file name)
    return datetime.now().strftime('%Y%m%d_%H%M%S')


from aboutSSVG import *

class AboutSSVG(QtGui.QDialog):
    """class for 'About SSVG' dialog
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_aboutSSVG()
        self.ui.setupUi(self)
        abouttext = """SSVG (Solar System Voyager) (c) 2016-2018 Shushi Uetsuki (whiskie14142)

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
  PyQt4 : https://www.riverbankcomputing.com/news/
  jplephem : https://github.com/brandon-rhodes/python-jplephem/
  julian : https://github.com/dannyzed/julian/
    Copyright (c) 2016 Daniel Zawada
  pytwobodyorbit : https://github.com/whiskie14142/pytwobodyorbit/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  spktype01 : https://github.com/whiskie14142/spktype01/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  PyInstaller : http://www.pyinstaller.org/"""

        self.ui.versionlabel.setText(g.version)        
        self.ui.licensetext.setPlainText(abouttext)
        self.connect(self.ui.okButton, SIGNAL('clicked()'), self.accept)
                


from newflightplandialog import *

class NewFlightPlanDialog(QtGui.QDialog):
    """class for 'New Flight Plan' dialog
    """
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_NewFlightPlanDialog()
        self.ui.setupUi(self)
        
        spacebaselist = []
        for baseitem in common.bases:
            spacebaselist.append(baseitem[0])
        self.ui.spacebase.addItems(spacebaselist)
        self.ui.spacebase.setCurrentIndex(1)
        
        for planet_id in common.planets_id:
            if planet_id[1] == 'EMB': continue
            if planet_id[1] == 'Sun': continue
            self.ui.planets.addItem(planet_id[1])
        self.ui.planets.setCurrentIndex(0)
        
        self.connect(self.ui.planetbutton, SIGNAL('clicked()'), 
                     self.planetbuttonclicked)
        self.connect(self.ui.smallbodybutton, SIGNAL('clicked()'), 
                     self.planetbuttonclicked)
        self.connect(self.ui.spkfileselect, SIGNAL('clicked()'), 
                     self.spkfileselectclicked)
        self.connect(self.ui.okbutton, SIGNAL('clicked()'), self.ok_clicked)
        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), self.reject)
            
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

    def ok_clicked(self):
        newplan = {}
        
        probe = {}
        probe['name'] = self.ui.probename.text()
        probe['base'] = self.ui.spacebase.currentText()
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 
                            'Probe mass should be a float number.', 0, 1, 0)
            return
        if mass <= 0.0:
            QMessageBox.information(self, 'Info', 'Invalid Probe mass.', 
                                    0, 1, 0)
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
            if target['name'].strip() == '':
                QMessageBox.information(self, 'Info', 
                                    'Specify target name.', 0, 1, 0)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.information(self, 'Info', 
                                    'Specify SPK file of the target.', 0, 1, 0)
                return
#
#       From May 2017, NASA-JPL HORIZONS produces barycentric SPK files 
#       for small bodies
#
            target['SPKID1A'] = 0
            target['SPKID2A'] = 0
            target['SPKID2B'] = 0
            try:
                spkid = int(self.ui.spkid_edit.text())
            except ValueError:
                QMessageBox.information(self, 'Info', 
                                    'SPKID should be an Integer.', 0, 1, 0)
                return
            if spkid <= 10000:
                QMessageBox.information(self, 'Info', 
                                    'Invalid SPKID.', 0, 1, 0)
                return
            target['SPKID1B'] = spkid
                
            
        newplan['probe'] = probe
        newplan['target'] = target
        newplan['maneuvers'] = []
        g.manplan = newplan
        self.accept()



class EditProbeDialog(NewFlightPlanDialog):
    """class for the dialog to edit probe information of a flight plan
    """

    def __init__(self, parent=None, manplan=None):
        super().__init__(parent)
        self.manplan = manplan
        probe = self.manplan['probe']
        target = self.manplan['target']
        self.ui.probename.setText(probe['name'])
        self.ui.probemass.setText('{:.3f}'.format(probe['pmass']))
        index = self.ui.spacebase.findText(probe['base'])
        self.ui.spacebase.setCurrentIndex(index)
        
        if target['file'] != '':
            self.ui.planetbutton.setChecked(False)
            self.ui.smallbodybutton.setChecked(True)
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            self.ui.targetname.setText(target['name'])
            self.ui.spkfilepath.setText(target['file'])
            self.ui.spkid_edit.setText(str(target['SPKID1B']))
        else:
            index = self.ui.planets.findText(target['name'])
            self.ui.planets.setCurrentIndex(index)
        
        self.initdialog()
        
    def initdialog(self):
        self.setWindowTitle('Edit Probe Properties')
        self.ui.target_box.setEnabled(False)
        
    def ok_clicked(self):
        probe = {}
        probe['name'] = self.ui.probename.text()
        probe['base'] = self.ui.spacebase.currentText()
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 
                            'Probe mass should be a float number.', 0, 1, 0)
            return
        if mass <= 0.0:
            QMessageBox.information(self, 'Info', 'Invalid Probe mass.', 
                                    0, 1, 0)
            return
        probe['pmass'] = mass
        
        self.manplan['probe'] = probe
        self.accept()
    
        
class EditTargetDialog(EditProbeDialog):
    """class for the dialog to edit target information of the flight plan
    """
    def initdialog(self):
        self.setWindowTitle('Select New Target')
        self.ui.probe_box.setEnabled(False)
        
    def ok_clicked(self):
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
            if target['name'].strip() == '':
                QMessageBox.information(self, 'Info', 
                                    'Specify target name.', 0, 1, 0)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.information(self, 'Info', 
                                    'Specify SPK file of the target.', 0, 1, 0)
                return
#
#       From May 2017, NASA-JPL HORIZONS produces barycentric SPK files 
#       for small bodies
#
            target['SPKID1A'] = 0
            target['SPKID2A'] = 0
            target['SPKID2B'] = 0
            try:
                spkid = int(self.ui.spkid_edit.text())
            except ValueError:
                QMessageBox.information(self, 'Info', 
                                    'SPKID should be an Integer.', 0, 1, 0)
                return
            if spkid <= 10000:
                QMessageBox.information(self, 'Info', 
                                    'Invalid SPKID.', 0, 1, 0)
                return
            target['SPKID1B'] = spkid
            
        self.manplan['target'] = target
        self.accept()
        



from ftasettingdialog import *

class FTAsettingDialog(QtGui.QDialog):
    """class for the dialog to specity parameters for FTA
    """
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ftasettingdialog()
        self.ui.setupUi(self)
        self.connect(self.ui.fromshoworbit, SIGNAL('clicked()'), 
                                                 self.ta_radioclicked)
        self.connect(self.ui.directinput, SIGNAL('clicked()'), 
                                                 self.ta_radioclicked)
        self.connect(self.ui.selTargetcenter, SIGNAL('clicked()'), 
                                                 self.pt_radioclicked)
        self.connect(self.ui.selBplanecoord, SIGNAL('clicked()'), 
                                                 self.pt_radioclicked)
        self.connect(self.ui.selOLcoord, SIGNAL('clicked()'), 
                                                 self.pt_radioclicked)

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
            QMessageBox.information(self, 'Info', 
                'Enter a floating point number for Time to Arrival.', 0, 1, 0)
            return
        if delta_jd < 1.0:
            QMessageBox.information(self, 'Info', 
                'To use FTA, Time to Arrival shall be\n' \
                + 'greater than 1.0 day', 0, 1, 0)
            return
        param[0] = g.showorbitcontrol.jd + delta_jd
        
        if self.ui.selBplanecoord.isChecked():
            try:        
                r = float(self.ui.Brangeedit.text()) * 1000.0
                beta = float(self.ui.betaedit.text())
            except ValueError:
                QMessageBox.information(self, 'Info', 
                                'Parameter should be floating numbers.', 0, 1, 0)
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
                    QMessageBox.information(self, 'Info', 
                                    'Parameter should be floating numbers.', 0, 1, 0)
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

from orbitoptimizedialog import *

class StartOptimizeDialog(QtGui.QDialog):
    """class for the Start Optimize Assistant
    """
    def __init__(self, orgjd, parent=None):
        QWidget.__init__(self, parent)
        g.probe_Kepler = None
        g.target_Kepler = None
        
        self.ui = Ui_OrbitOptimizeDialog()
        self.ui.setupUi(self)
        self.orgjd = orgjd

        self.artist_PCpos = None
        self.artist_PEpos = None
        self.artist_TCpos = None
        self.artist_sol = None
        self.artist_Porbit = None
        self.clearstatistics()
        
        g.ax.set_xlim(-3.0e11, 3.0e11)
        g.ax.set_ylim(-3.0e11, 3.0e11)
        g.ax.set_zlim(-3.0e11, 3.0e11)
        
        self.initdialog()
        self.initforCPoptimize()
        self.predorbit = TwoBodyPred('optimize')
        self.drawfixedorbit()
        
        self.draworbit()
        
        self.connect(self.ui.check_Ptrj, SIGNAL('clicked()'), 
                     self.fixedorbitchanged)
        self.connect(self.ui.check_orgorb, SIGNAL('clicked()'), 
                                             self.fixedorbitchanged)
        self.connect(self.ui.check_Ppred, SIGNAL('clicked()'), self.draworbit)
        self.connect(self.ui.check_TKepler, SIGNAL('clicked()'), 
                                             self.fixedorbitchanged)
        self.connect(self.ui.radio_fd, SIGNAL('clicked()'), self.fdchanged)
        self.connect(self.ui.radio_tt, SIGNAL('clicked()'), self.fdchanged)
        self.connect(self.ui.fixed_to_ct, SIGNAL('clicked()'), 
                                             self.fixed_to_ct_changed)
        
        self.connect(self.ui.it_fb, SIGNAL('clicked()'), self.it_fb)
        self.connect(self.ui.it_ff, SIGNAL('clicked()'), self.it_ff)
        self.connect(self.ui.tt_fb, SIGNAL('clicked()'), self.tt_fb)
        self.connect(self.ui.tt_ff, SIGNAL('clicked()'), self.tt_ff)
        
        self.connect(self.ui.it_b, SIGNAL('clicked()'), self.it_b)
        self.connect(self.ui.it_f, SIGNAL('clicked()'), self.it_f)
        self.connect(self.ui.tt_b, SIGNAL('clicked()'), self.tt_b)
        self.connect(self.ui.tt_f, SIGNAL('clicked()'), self.tt_f)
        
        self.connect(self.ui.it_wide, SIGNAL('clicked()'), self.itwnchanged)
        self.connect(self.ui.it_narrow, SIGNAL('clicked()'), self.itwnchanged)
        self.connect(self.ui.tt_wide, SIGNAL('clicked()'), self.fdchanged)
        self.connect(self.ui.tt_narrow, SIGNAL('clicked()'), self.fdchanged)
        self.connect(self.ui.clearstat, SIGNAL('clicked()'), 
                                             self.clearstatistics)
        
        self.connect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                             self.itslchanged)
        self.connect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                                             self.ttslchanged)

        self.connect(self.ui.reopenbutton, SIGNAL('clicked()'),
                                             self.reopen3dorbit)
        self.connect(self.ui.finishbutton, SIGNAL('clicked()'), 
                                             self.finishbutton)
        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), 
                                             self.cancelbutton)
        
    
    def initdialog(self):
        self.sl_minval = 0
        self.sl_maxval = 500
        self.itcenter = self.orgjd
        self.itfrom = -250.0
        self.itto = 250.0
        self.itcurrent = self.orgjd
        self.dispit()
        self.ui.sl_inittime.setValue(self.sl_real2pos(self.itfrom, 
            self.itto, self.itcurrent - self.itcenter))
        
        self.ttcenter = 250.0
        self.ttfrom = 0.0
        self.ttto = 500.0
        self.cduration = 250.0
        self.ttcurrent = self.itcurrent + self.cduration
        self.disptt()
        self.ui.sl_duration.setValue(self.sl_real2pos(self.ttfrom,
            self.ttto, self.cduration))
    
    def drawfixedorbit(self):
        # Probe Kepler Orbit
        ndata = self.sl_maxval - self.sl_minval + 1
        x = np.zeros(ndata)
        y = np.zeros(ndata)
        z = np.zeros(ndata)
        for i in range(ndata):
            pos = i + self.sl_minval
            jd = self.sl_pos2real(self.itfrom, self.itto, pos) + self.itcenter
            ppos, pvel = self.orgorbposvel(jd)
            x[i] = ppos[0]
            y[i] = ppos[1]
            z[i] = ppos[2]
        g.probe_Kepler = [x, y, z]
        
        # Target Kepler Orbit
        x, y, z, t = g.mytarget.points(self.itcenter, g.ndata)
        g.target_Kepler = [x, y, z]
        
        self.fixedorbitchanged()
        
    def draworbit(self):
        ppos, pvel = self.orgorbposvel(self.itcurrent)
        
        # erase positions and orbit
        if self.artist_PCpos != None:
            self.artist_PCpos.remove()
            self.artist_PCpos = None
        if self.artist_PEpos != None:
            self.artist_PEpos.remove()
            self.artist_PEpos = None
        if self.artist_TCpos != None:
            self.artist_TCpos.remove()
            self.artist_TCpos = None
        if self.artist_sol != None:
            self.artist_sol.remove()
            self.artist_sol = None
        if self.artist_Porbit != None:
            self.artist_Porbit[0].remove()
            self.artist_Porbit = None
        
        # FTA
        ttpos, ttvel = g.mytarget.posvel(self.ttcurrent)
        self.predorbit.fix_state(self.itcurrent, ppos, pvel)
        if self.itcurrent >= self.ttcurrent:
            return
        try:
            dv, phi, elv, ivel, tvel = self.predorbit.ftavel(self.ttcurrent, 
                                                             ttpos)
        except ValueError:
            return
        self.predorbit.fix_state(self.itcurrent, ppos, ivel)
        
        # Draw
        targetpos, targetvel = g.mytarget.posvel(self.itcurrent)
        self.artist_PCpos = g.ax.scatter(*ppos, s=50, c='r',depthshade=False, 
                                         marker='x')
        self.artist_TCpos = g.ax.scatter(*targetpos, s=40, c='g',
                                         depthshade=False, marker='+')
        self.artist_PEpos = g.ax.scatter(*ttpos, s=50, c='b',depthshade=False, 
                                         marker='x')
        sunpos, sunvel = common.SPKposvel(10, self.itcurrent)
        self.artist_sol = g.ax.scatter(*sunpos, s=50, c='w',depthshade=False, 
                                       marker='o')
        if self.ui.check_Ppred.isChecked():
            x, y, z, t = self.predorbit.points(101)
            self.artist_Porbit = g.ax.plot(x, y, z,color='c', lw=0.75)

        if g.fig != None: plt.draw()
        
        # Print
        idv = ivel - pvel
        idvabs = np.sqrt(np.dot(idv, idv))
        if self.statIDVmin == None:
            self.statIDVmin = idvabs
        elif idvabs < self.statIDVmin:
            self.statIDVmin = idvabs
        if self.statIDVmax == None:
            self.statIDVmax = idvabs
        elif idvabs > self.statIDVmax:
            self.statIDVmax = idvabs
        self.ui.initialDV_cur.setText('{:.3f}'.format(idvabs))
        self.ui.initialDV_min.setText('{:.3f}'.format(self.statIDVmin))
        self.ui.initialDV_max.setText('{:.3f}'.format(self.statIDVmax))
        
        self.ui.idv_phi.setText('{:.2f}'.format(phi))
        self.ui.idv_elv.setText('{:.2f}'.format(elv))
        
        self.result_it = self.itcurrent
        self.result_dv = round(dv, 3)
        self.result_phi = round(phi, 2)
        self.result_elv = round(elv, 2)
        self.result_tt = self.ttcurrent
        
        trv = ttvel - tvel
        trvabs = np.sqrt(np.dot(trv, trv))
        if self.statTRVmin == None:
            self.statTRVmin = trvabs
        elif trvabs < self.statTRVmin:
            self.statTRVmin = trvabs
        if self.statTRVmax == None:
            self.statTRVmax = trvabs
        elif trvabs > self.statTRVmax:
            self.statTRVmax = trvabs
        self.ui.terminalRV_cur.setText('{:.3f}'.format(trvabs))
        self.ui.terminalRV_min.setText('{:.3f}'.format(self.statTRVmin))
        self.ui.terminalRV_max.setText('{:.3f}'.format(self.statTRVmax))
        
        tdv = idvabs + trvabs
        if self.statTDVmin == None:
            self.statTDVmin = tdv
        elif tdv < self.statTDVmin:
            self.statTDVmin = tdv
        if self.statTDVmax == None:
            self.statTDVmax = tdv
        elif tdv > self.statTDVmax:
            self.statTDVmax = tdv
        self.ui.totalDV_cur.setText('{:.3f}'.format(tdv))
        self.ui.totalDV_min.setText('{:.3f}'.format(self.statTDVmin))
        self.ui.totalDV_max.setText('{:.3f}'.format(self.statTDVmax))
        
        
    def sl_real2pos(self, rfrom, rto, rval):
        pos = int((rval - rfrom) / (rto - rfrom) * self.sl_maxval + 0.5) \
            + self.sl_minval
        return pos
    
    def sl_pos2real(self, rfrom, rto, pos):
        rval = (pos - self.sl_minval) * (rto - rfrom) /    \
            (self.sl_maxval - self.sl_minval) + rfrom
        return rval

    def dispit(self):
        fromjd = self.sl_pos2real(self.itfrom, self.itto, self.sl_minval)  \
            + self.itcenter
        fromdate = common.jd2isot(fromjd).split('T')[0]
        self.ui.label_itfrom.setText(fromdate)
        tojd = self.sl_pos2real(self.itfrom, self.itto, self.sl_maxval)  \
            + self.itcenter
        todate = common.jd2isot(tojd).split('T')[0]
        self.ui.label_itto.setText(todate)
        self.ui.initialtime.setText(common.jd2isot(self.itcurrent))

    def disptt(self):
        if self.ui.radio_fd.isChecked():
            self.ui.label_ttfrom.setText('{:.0f}'.format(self.ttfrom))
            self.ui.label_ttto.setText('{:.0f}'.format(self.ttto))
        else:
            fromjd = self.sl_pos2real(self.ttfrom, self.ttto, self.sl_minval)  \
                + self.ttcenter
            fromdate = common.jd2isot(fromjd).split('T')[0]
            self.ui.label_ttfrom.setText(fromdate)
            tojd = self.sl_pos2real(self.ttfrom, self.ttto, self.sl_maxval)  \
                + self.ttcenter
            todate = common.jd2isot(tojd).split('T')[0]
            self.ui.label_ttto.setText(todate)
        self.ui.duration.setText('{:.1f}'.format(self.cduration))
        self.ui.terminaltime.setText(common.jd2isot(self.ttcurrent))
        
    def itslchanged(self, pos):
        self.itcurrent = self.sl_pos2real(self.itfrom, self.itto, pos)  \
            + self.itcenter
        self.ui.initialtime.setText(common.jd2isot(self.itcurrent))
        if self.ui.radio_fd.isChecked():
            self.ttcurrent = self.itcurrent + self.cduration
            self.ui.terminaltime.setText(common.jd2isot(self.ttcurrent))
        else:
            self.cduration = self.ttcurrent - self.itcurrent
            self.ui.duration.setText('{:.1f}'.format(self.cduration))
        self.draworbit()

    def ttslchanged(self, pos):
        if self.ui.radio_fd.isChecked():
            self.cduration = self.sl_pos2real(self.ttfrom, self.ttto, pos)
            self.ttcurrent = self.cduration + self.itcurrent
            self.ui.duration.setText('{:.1f}'.format(self.cduration))
            self.ui.terminaltime.setText(common.jd2isot(self.ttcurrent))
        else:
            self.ttcurrent = self.sl_pos2real(self.ttfrom, self.ttto, pos)  \
                + self.ttcenter
            self.cduration = self.ttcurrent - self.itcurrent
            self.ui.duration.setText('{:.1f}'.format(self.cduration))
            self.ui.terminaltime.setText(common.jd2isot(self.ttcurrent))
        self.draworbit()
        
    def fixedorbitchanged(self):
        erase_PKepler()
        if self.ui.check_orgorb.isChecked():
            draw_PKepler()
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()
        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()

        if g.fig != None: plt.draw()
    
    def fdchanged(self):
        self.disconnect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                        self.ttslchanged)
        if self.ui.tt_wide.isChecked():
            dev = 250.0
        else:
            dev = 50.0
        
        if self.ui.radio_fd.isChecked():
            if self.cduration < 0.0:
                self.cduration = 0.0
            self.ttcenter = 250.0
            self.ttfrom = self.ttcenter - dev
            self.ttto = self.ttcenter + dev
            pos = self.sl_real2pos(self.ttfrom, self.ttto, self.cduration)
            while pos < self.sl_minval:
                self.ttfrom -= 100.0
                self.ttto -= 100.0
                self.ttcenter -= 100.0
                pos = self.sl_real2pos(self.ttfrom, self.ttto, self.cduration)
            while pos > self.sl_maxval:
                self.ttfrom += 100.0
                self.ttto += 100.0
                self.ttcenter += 100.0
                pos = self.sl_real2pos(self.ttfrom, self.ttto, self.cduration)
            self.ui.sl_duration.setValue(pos)
            
        else:
            self.ttcenter = self.ttcurrent
            self.ttfrom = 0.0 - dev
            self.ttto = 0.0 + dev
            pos = self.sl_real2pos(self.ttfrom, self.ttto, 0.0)
            self.ui.sl_duration.setValue(pos)
            
        self.disptt()
        self.connect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                     self.ttslchanged)

    def it_fb(self):
        if self.ui.it_wide.isChecked():
            self.itcenter -= 250.0
        else:
            self.itcenter -= 50.0

        rval = self.itcurrent - self.itcenter
        pos = self.sl_real2pos(self.itfrom, self.itto, rval)
        if pos > self.sl_maxval:
            pos = self.sl_maxval
        if pos < self.sl_minval:
            pos = self.sl_minval
        self.disconnect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                             self.itslchanged)
        self.ui.sl_inittime.setValue(pos)
        self.connect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                             self.itslchanged)
        self.drawfixedorbit()
        self.itslchanged(pos) 
        self.dispit()
    
    
    def it_ff(self):
        if self.ui.it_wide.isChecked():
            self.itcenter += 250.0
        else:
            self.itcenter += 50.0

        rval = self.itcurrent - self.itcenter
        pos = self.sl_real2pos(self.itfrom, self.itto, rval)
        if pos > self.sl_maxval:
            pos = self.sl_maxval
        if pos < self.sl_minval:
            pos = self.sl_minval
        self.disconnect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                             self.itslchanged)
        self.ui.sl_inittime.setValue(pos)
        self.connect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                             self.itslchanged)
        self.drawfixedorbit()
        self.itslchanged(pos) 
        self.dispit()
    
    def tt_fb(self):
        if self.ui.tt_wide.isChecked():
            self.ttcenter -= 250.0
            if self.ui.radio_fd.isChecked():
                if self.ttcenter < 250.0:
                    self.ttcenter = 250.0
                self.ttfrom = self.ttcenter - 250.0
                self.ttto = self.ttcenter + 250.0
        else:
            self.ttcenter -= 50.0
            if self.ui.radio_fd.isChecked():
                if self.ttcenter < 50.0:
                    self.ttcenter = 50.0
                self.ttfrom = self.ttcenter - 50.0
                self.ttto = self.ttcenter + 50.0

        if self.ui.radio_fd.isChecked():
            rval = self.cduration
        else:
            rval = self.ttcurrent - self.ttcenter
        pos = self.sl_real2pos(self.ttfrom, self.ttto, rval)
        if pos > self.sl_maxval:
            pos = self.sl_maxval
        if pos < self.sl_minval:
            pos = self.sl_minval
        self.disconnect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                                             self.ttslchanged)
        self.ui.sl_duration.setValue(pos)
        self.connect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                                             self.ttslchanged)
        self.ttslchanged(pos) 
        self.disptt()
    
    def tt_ff(self):
        if self.ui.tt_wide.isChecked():
            self.ttcenter += 250.0
            if self.ui.radio_fd.isChecked():
                self.ttfrom = self.ttcenter - 250.0
                self.ttto = self.ttcenter + 250.0
        else:
            self.ttcenter += 50.0
            if self.ui.radio_fd.isChecked():
                self.ttfrom = self.ttcenter - 50.0
                self.ttto = self.ttcenter + 50.0

        if self.ui.radio_fd.isChecked():
            rval = self.cduration
        else:
            rval = self.ttcurrent - self.ttcenter
        pos = self.sl_real2pos(self.ttfrom, self.ttto, rval)
        if pos > self.sl_maxval:
            pos = self.sl_maxval
        if pos < self.sl_minval:
            pos = self.sl_minval
        self.disconnect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                                             self.ttslchanged)
        self.ui.sl_duration.setValue(pos)
        self.connect(self.ui.sl_duration, SIGNAL('valueChanged(int)'), 
                                             self.ttslchanged)
        self.ttslchanged(pos) 
        self.disptt()
        
    def it_b(self):
        pos = self.ui.sl_inittime.value()
        if pos == self.sl_minval:
            return
        pos -= 1
        self.ui.sl_inittime.setValue(pos)
        
    def it_f(self):
        pos = self.ui.sl_inittime.value()
        if pos == self.sl_maxval:
            return
        pos += 1
        self.ui.sl_inittime.setValue(pos)
    
    def tt_b(self):
        pos = self.ui.sl_duration.value()
        if pos == self.sl_minval:
            return
        pos -= 1
        self.ui.sl_duration.setValue(pos)
    
    def tt_f(self):
        pos = self.ui.sl_duration.value()
        if pos == self.sl_maxval:
            return
        pos += 1
        self.ui.sl_duration.setValue(pos)
    
    def itwnchanged(self):
        if self.ui.it_wide.isChecked():
            dev = 250.0
        else:
            dev = 50.0
        self.itfrom = 0.0 - dev
        self.itto = 0.0 + dev
        self.itcenter = self.itcurrent
        pos = self.sl_real2pos(self.itfrom, self.itto, 0.0)
        self.disconnect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                        self.itslchanged)
        self.ui.sl_inittime.setValue(pos)
        self.dispit()
        self.connect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                     self.itslchanged)
        
        self.drawfixedorbit()
    
    def clearstatistics(self):
        self.statIDVmin = None
        self.statIDVmax = None
        self.statTRVmin = None
        self.statTRVmax = None
        self.statTDVmin = None
        self.statTDVmax = None
        self.ui.initialDV_min.setText('')
        self.ui.initialDV_max.setText('')
        self.ui.terminalRV_min.setText('')
        self.ui.terminalRV_max.setText('')
        self.ui.totalDV_min.setText('')
        self.ui.totalDV_max.setText('')
    
    def closeEvent(self, event):
        event.accept()
        self.eraseall()
    
    def eraseall(self):
        if self.artist_PCpos != None:
            self.artist_PCpos.remove()
            self.artist_PCpos = None
        if self.artist_PEpos != None:
            self.artist_PEpos.remove()
            self.artist_PEpos = None
        if self.artist_TCpos != None:
            self.artist_TCpos.remove()
            self.artist_TCpos = None
        if self.artist_sol != None:
            self.artist_sol.remove()
            self.artist_sol = None
        if self.artist_Porbit != None:
            self.artist_Porbit[0].remove()
            self.artist_Porbit = None
        erase_PKepler()
        erase_TKepler()
        erase_Ptrj()

    def reopen3dorbit(self):
        g.mainform.init3Dfigure()
        self.drawfixedorbit()
        self.draworbit()
        
    def finishbutton(self):
        self.eraseall()
        self.accept()
        
    def cancelbutton(self):
        self.eraseall()
        self.reject()

    def initforCPoptimize(self):
        # Place Holder for CPoptimize
        self.ui.fixed_to_ct.setVisible(False)
        self.ui.check_Ptrj.setVisible(False)
        
    def fixed_to_ct_changed(self):
        # Place Holder for CPoptimize
        pass

    def orgorbposvel(self, jd):
        return g.myprobe.pseudostart(jd, 0.0, 0.0, 0.0)



class CpOptimizeDialog(StartOptimizeDialog):
    """class for the CP Optimize Assistant
    """

    def initforCPoptimize(self):
        self.setWindowTitle('CP Optimize Assistant')
        self.ui.fixed_to_ct.setChecked(True)
        self.ui.box_initialtime.setEnabled(False)
        self.ui.check_orgorb.setText('Previous')
        self.ui.box_initialtime.setTitle('Maneuver Time')
        self.ui.label_it.setText('Maneuver Time')
        
        self.orgorb = TwoBodyPred('orgorb')
        self.orgorb.fix_state(g.myprobe.jd, g.myprobe.pos, g.myprobe.vel)
        self.fixed_to_ct = True
        
    def fixed_to_ct_changed(self):
        if self.ui.fixed_to_ct.isChecked():
            self.ui.box_initialtime.setEnabled(False)
            self.itcenter = self.orgjd
            self.itcurrent = self.orgjd
            self.dispit()
            self.disconnect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                                    self.itslchanged)
            self.ui.sl_inittime.setValue(self.sl_real2pos(self.itfrom, 
                self.itto, self.itcurrent - self.itcenter))
            self.connect(self.ui.sl_inittime, SIGNAL('valueChanged(int)'), 
                                                 self.itslchanged)
            self.draworbit()
            self.fixed_to_ct = True
        else:
            self.ui.box_initialtime.setEnabled(True)
            self.fixed_to_ct = False

    def orgorbposvel(self, jd):
        return self.orgorb.posvelatt(jd)


from editmandialog import *

class EditManDialog(QtGui.QDialog):
    """class for 'Edit Maneuver' dialog
    """
    
    def __init__(self, parent=None, editman=None, currentrow=0):
        QWidget.__init__(self, parent)
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+380, 640, 320)
        self.ui = Ui_editmandialog()
        self.ui.setupUi(self)
        self.connect(self.ui.applymantype, SIGNAL('clicked()'), 
                                             self.applymantype)
        self.connect(self.ui.isotedit, SIGNAL('editingFinished()'), 
                                             self.isotedited)
        self.connect(self.ui.jdedit, SIGNAL('editingFinished()'), 
                                             self.jdedited)
        self.connect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), 
                                             self.parameterchanged)
        self.connect(self.ui.finish_exec, SIGNAL('clicked()'), 
                                             self.finish_exec)
        self.connect(self.ui.finishbutton, SIGNAL('clicked()'), 
                                             self.finishbutton)
        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), 
                                             self.cancelbutton)
        self.connect(self.ui.showorbit, SIGNAL('clicked()'), self.showorbit)
        self.connect(self.ui.computeFTA, SIGNAL('clicked()'), self.computefta)
        self.connect(self.ui.optimize, SIGNAL('clicked()'), self.optimize)
        self.connect(self.ui.applyduration, SIGNAL('clicked()'), 
                                             self.applyduration)
        
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
        self.mes2 = '  to the editing maneuver.\n\n' \
            'Applied maneuver should be executed at that time.  ' \
            'You need to adjust preceding maneuver(s) before execution of '   \
            'this maneuver.\n\n' \
            'The time for which parameters are optimized has been copied ' \
            'to the system clipboard.'
        
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
        if editman == None:
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
        if self.editman == None: return
            
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
        if g.myprobe != None:
            if g.myprobe.onflight:
                ival[0] = g.myprobe.jd
        self.editman = {}
        self.editman['type'] = self.types[typeID]
        for i in range(9):
            if self.paramflag[typeID][i] == 1:
                self.editman[self.paramname[i]] = ival[i]
        
    def dispman(self):
        if self.editman == None:
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

            self.disconnect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), 
                            self.parameterchanged)
            
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
    
            self.connect(self.ui.parameters, SIGNAL('cellChanged(int,int)'), 
                         self.parameterchanged)
                
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
        ans = QMessageBox.question(self, 
            'Mantype changed', 'Parameters will be lost. OK?', 
            0, button1=1, button2=2)
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
            self.ui.isotedit.setText(common.jd2isot(
                float(self.ui.jdedit.text())))
            QMessageBox.information(self, 'Time Error', 'Invalid ISOT', 
                                    0, 1, 0)
            return
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        if self.ui.duration.isEnabled():
            self.ui.duration.setText('{:.8f}'.format(jd - g.myprobe.jd))
        self.editman[self.paramname[0]] = jd
        
    def jdedited(self):
        try:
            jd = float(self.ui.jdedit.text())
        except ValueError:
            self.ui.jdedit.setText('{:.8f}'.format(
                common.isot2jd(self.ui.isotedit.text())))
            QMessageBox.information(self, 'Time Error', 'Invalid JD', 0, 1, 0)
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
                QMessageBox.information(self, 
                    'Parameter Error', 'Enter L or E for tvmode', 0, 1, 0)
                return
        else:
            try:
                newval = float(self.ui.parameters.item(row, colmn).text())
            except ValueError:
                self.ui.parameters.item(row, colmn).setText(
                    self.fmttbl[row+1].format(prevval))
                QMessageBox.information(self, 
                    'Parameter Error', 'Enter a floating number', 0, 1, 0)
                return
        self.editman[self.paramname[row+1]] = newval

    def finish_exec(self):
        g.editedman = self.editman
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.done(g.finish_exec)
        
    def finishbutton(self):
        g.editedman = self.editman
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        self.writeloglines()
        self.accept()
        
    def cancelbutton(self):
        if g.showorbitcontrol != None:
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
                                   0, button1=1, button2=2)
        if ans == 2:
            event.ignore()
            return
        if g.showorbitcontrol != None:
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
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_pred_dv(dv, phi, elv)
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.set_affect_parent(False)
    
    def showorbitSTART(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowStartOrbitDialog(self, self.editman)
            g.showorbitcontrol.show()
        else:
            g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(True)
        g.showorbitcontrol.set_affect_parent(False)

    def showorbitFLYTO(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_DT(self.editman['time'])
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(True)
            
    def showorbitOTHER(self):
        if g.showorbitcontrol == None:
            g.showorbitcontrol = ShowOrbitDialog(self)
            g.showorbitcontrol.show()
        g.showorbitcontrol.set_pred_dv(0.0, 0.0, 0.0)
        g.showorbitcontrol.redraw()
        g.showorbitcontrol.ui.groupBox.setEnabled(False)
        g.showorbitcontrol.set_affect_parent(False)
        
            
    def computefta(self):
        norm = lambda x : x / np.sqrt(np.dot(x,x))
        if g.showorbitcontrol == None:
            QMessageBox.information(self, 
                'Info', 'To use FTA, open Show Orbit window and\n' 
                + 'try again', 0, 1, 0)
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
                    + 'Try different parameters', 0, 1, 0)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = 'FTA Results are as follows. Apply them?\n' + \
                'dv = ' + str(dv) + '\n' + \
                'phi = ' + str(phi) + '\n' + \
                'elv = ' + str(elv)
            ans = QMessageBox.question(self, 'FTA Results', mes, 0, button1=1, 
                                       button2=2)
            if ans == 1:
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
                    + 'Try different parameters', 0, 1, 0)
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
                    + 'Try different parameters', 0, 1, 0)
                return
    
            dv = round(dv, 3)
            phi = round(phi, 2)
            elv = round(elv, 2)
                
            mes = 'FTA Results are as follows. Apply them?\n' + \
                'dv = ' + str(dv) + '\n' + \
                'phi = ' + str(phi) + '\n' + \
                'elv = ' + str(elv)
            ans = QMessageBox.question(self, 'FTA Results', mes, 0, button1=1, 
                                       button2=2)
            if ans == 1:
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
        if g.showorbitcontrol != None:
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
        if g.showorbitcontrol != None:
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
            QMessageBox.information(self, 'Urgent!', 
                mes, 0, 1, 0)

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
        self.ui.duration.setText('{:.5f}'.format(dt))

    def applyduration(self):
        try:
            dt = float(self.ui.duration.text())
        except ValueError:
            QMessageBox.information(self, 'Info', 'Invalid Duration days', 
                                    0, 1, 0)
            return
        jd = g.myprobe.jd + dt
        self.ui.jdedit.setText('{:.8f}'.format(jd))
        self.jdedited()
        


from showorbitcontrol import *

class ShowOrbitDialog(QtGui.QDialog):
    """class for 'Show Orbit' window
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.mother = parent
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+740, 640, 211)
        self.ui = Ui_ShowOrbitControl()
        self.ui.setupUi(self)
        
        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), 
                                             self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), 
                                             self.fastbackward)
        self.connect(self.ui.check_Ptrj, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_PKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_TKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.timescale, SIGNAL('valueChanged(int)'), 
                                             self._valuechanged)
        self.connect(self.ui.dtApply, SIGNAL('clicked()'), self.dtapply)

        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        
        self.tbpred = None
        self.reset()
        
        self.affect_parent = False

    def reset(self):
        self.dv = 0.0
        self.phi = 0.0
        self.elv = 0.0
        self.delta_jd = 0.0
        self.ui.groupBox.setEnabled(False)
        
        if g.myprobe.onflight:
            jd = g.myprobe.jd
        else:
            dt = datetime.now()
            jdtoday = julian.to_jd(dt, fmt='jd')
            jd = int(jdtoday + 0.5) - 0.5
        xs, ys, zs, ts = g.mytarget.points(jd, g.ndata)
        g.target_Kepler = [xs, ys, zs]
        
        self.redraw()
        
    def redraw(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 
                                    'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe has no valid orbit.', 0, 1, 0)
            return

        self.jd = g.myprobe.jd
        self.ui.currentdate.setText(common.jd2isot(self.jd))

        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        
        self.ppos = g.myprobe.pos
        self.pvel = g.myprobe.vel
        if self.tbpred == None:
            self.tbpred = TwoBodyPred(g.myprobe.name)

        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()
        
        self.tbpred.fix_state(self.jd, self.ppos, self.pvel)
        self.tbpred.set_pred_dv(self.dv, self.phi, self.elv)
        x, y, z, t = self.tbpred.points(g.ndata)
        g.probe_Kepler = [x, y, z]
        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            draw_PKepler()
        
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()
        
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
        self.artist_of_probe = g.ax.scatter(*probe_pos, s=50, c='r', 
                                            depthshade=False, marker='x')
        
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*self.target_pos, s=40, c='g', 
                                             depthshade=False, marker='+')
            
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*self.sun_pos, s=50, c='w',
                                          depthshade=False, marker='o')

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(tempjd)

        remove_time()
        if self.delta_jd == 0.0:
            replot_time(tempjd, 'Real')
        else:
            replot_time(tempjd, 'Prediction')

        if g.fig != None: plt.draw()
        
        # display relative position and velocity
        rel_pos = self.target_pos - probe_pos
        rel_pos = common.eclv2lv(rel_pos, probe_pos, probe_vel, 
                                 self.tbpred.sunpos, self.tbpred.sunvel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - probe_vel
        rel_vel = common.eclv2lv(rel_vel, probe_pos, probe_vel, 
                                 self.tbpred.sunpos, self.tbpred.sunvel)
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
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)
        
    def backward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value()
        self.delta_jd -= 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)
        
    def fastforward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value() + 1
        self.delta_jd += 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)

    def fastbackward(self):
        self.delta_jd = float(self.ui.delta_t_edit.text())
        exp = self.ui.timescale.value() + 1
        self.delta_jd -= 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)
        
    def _statuschanged(self):
        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()
        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            draw_PKepler()
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()

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
            QMessageBox.information(self, 'Info', 
                                    'Enter a floating point number.', 0, 1, 0)
            return
        self.delta_jd = value
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)

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
        erase_Ptrj()
        erase_PKepler()
        erase_TKepler()
        remove_planets()
        remove_time()

    def save_settings(self):
        settings = {}
        settings['SSB'] = self.ui.tobarycenter.isChecked()
        settings['Probe'] = self.ui.toprobe.isChecked()
        settings['Target'] = self.ui.totarget.isChecked()
        g.showorbitsettings = settings
        
    def restore_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])
    
    def set_affect_parent(self, flag=False):
        self.affect_parent = flag



class ShowStartOrbitDialog(ShowOrbitDialog):
    """class for 'Show Start Orbit' window
    """
    def __init__(self, parent=None, editman=None):
        self.editman = editman
        super().__init__(parent)
        self.ui.ctimeLabel.setText('Start Time')
        
    def redraw(self):
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
        g.probe_Kepler = [x, y, z]
        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            draw_PKepler()
        
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()
        
        self.ui.man_dv.setText('{:.3f}'.format(self.dv))
        self.ui.man_phi.setText('{:.2f}'.format(self.phi))
        self.ui.man_elv.setText('{:.2f}'.format(self.elv))

        self.restore_settings()
        self._redrawmark()
        


from flightreviewcontrol import *

class FlightReviewControl(QtGui.QDialog):
    """class for 'Flight Review' window
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+740, 640, 211)
        self.ui = Ui_FlightReviewControl()
        self.ui.setupUi(self)

        # Get Settings of 'Look at' from showorbitsettings
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])
        
        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), 
                                             self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), 
                                             self.fastbackward)
        self.connect(self.ui.check_Ptrj, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_PKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_TKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), 
                                             self._statuschanged)

        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        self.artist_of_epssinfo = None
        
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
            QMessageBox.information(self, 'Info', 
                                    'You have no valid probe.', 0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe has no valid orbit.', 0, 1, 0)
            return

        if g.myprobe.trj_record[-1][0]['type'] != 'FLYTO':
            QMessageBox.information(self, 'Info', 
                                    'Last maneuver was not FLYTO.', 0, 1, 0)
            return

        self.last_trj = g.probe_trj[-1][1:]
        self.maninfo = g.probe_trj[-1][0]
        self.start_time = self.last_trj[0][0]
#        self.end_time = self.last_trj[0][-1]  not used?
        self.ui.starttime.setText(common.jd2isot(self.start_time))
        
        xs, ys, zs, ts = g.mytarget.points(self.start_time, g.ndata)
        g.target_Kepler = [xs, ys, zs]

        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()
        
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()

        
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
        ssacc = self.last_trj[7][self.c_index]

        erase_PKepler()

        if self.ui.check_PKepler.isChecked():
            if self.tbpred == None:
                self.tbpred = TwoBodyPred(g.myprobe.name)
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata)
            g.probe_Kepler = [x, y, z]
            if self.ui.check_PKepler.isChecked():
                draw_PKepler()

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
        self.artist_of_probe = g.ax.scatter(*ppos, s=50, c='r',
                                            depthshade=False, marker='x')
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',
                                             depthshade=False, marker='+')
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',
                                          depthshade=False, marker='o')

        if self.artist_of_epssinfo != None:
            self.artist_of_epssinfo.remove()
            self.artist_of_epssinfo = None
        epsstext = ''
        if self.maninfo['epon']:
            epsstext = epsstext + '  EP(' + self.maninfo['epmode'] + ')'
        if self.maninfo['sson']:
            epsstext = epsstext + '  SS({0}) SSacc={1:.3f}'.format(
                self.maninfo['ssmode'], ssacc)
        self.artist_of_epssinfo = g.ax.text(*ppos, epsstext, color='r', 
                                            fontsize=11)

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(c_time)

        remove_time()
        replot_time(c_time, 'Real')
        
        if g.fig != None: plt.draw()
        
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
        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()
        
        self.save_settings()
        self._redrawmark()

    def save_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
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
        if self.artist_of_epssinfo != None:
            self.artist_of_epssinfo.remove()
            self.artist_of_epssinfo = None
        erase_Ptrj()
        erase_PKepler()
        erase_TKepler()
        remove_planets()
        remove_time()

from reviewthroughoutcontrol import *

class ReviewThroughoutControl(QtGui.QDialog):
    """class for 'Review Throughout' window
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+740, 640, 211)
        self.ui = Ui_ReviewThroughoutControl()
        self.ui.setupUi(self)

        # Get Settings of 'Look at' from showorbitsettings
        if g.showorbitsettings != None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])

        self.connect(self.ui.forward, SIGNAL('clicked()'), self.forward)
        self.connect(self.ui.backward, SIGNAL('clicked()'), self.backward)
        self.connect(self.ui.fastforward, SIGNAL('clicked()'), 
                                             self.fastforward)
        self.connect(self.ui.fastbackward, SIGNAL('clicked()'), 
                                             self.fastbackward)
        self.connect(self.ui.previousman, SIGNAL('clicked()'), 
                                             self.previousman)
        self.connect(self.ui.nextman, SIGNAL('clicked()'), self.nextman)
        self.connect(self.ui.check_Ptrj, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_PKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.check_TKepler, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.showplanets, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.showmantype, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.tobarycenter, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.toprobe, SIGNAL('clicked()'), 
                                             self._statuschanged)
        self.connect(self.ui.totarget, SIGNAL('clicked()'), 
                                             self._statuschanged)

        self.mainwindow = parent
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
        self.c_maninfo = record[0]
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
            ssacc = record[8][0]
            self.last_trj = record[1:]
            self.c_index = 0
            self.ui.fastbackward.setEnabled(True)
            self.ui.backward.setEnabled(True)
            self.ui.forward.setEnabled(True)
            self.ui.fastforward.setEnabled(True)
            self.ui.timescale.setEnabled(True)
            if self.c_maninfo['epon']:
                self.mantext = self.mantext + ' EP(' + \
                                self.c_maninfo['epmode'] + ')'
            if self.c_maninfo['sson']:
                self.mantext = self.mantext + ' SS(' + \
                                self.c_maninfo['ssmode'] + ')'
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

        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()

        # Kepler Orbit of probe        
        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            self.tbpred.fix_state(status[0], status[1:4], status[4:])
            x, y, z, t = self.tbpred.points(g.ndata)
            g.probe_Kepler = [x, y, z]
            if self.ui.check_PKepler.isChecked():
                draw_PKepler()

        # Planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(status[0])
        
        # Kepler Orbit of target
        xs, ys, zs, ts = g.mytarget.points(status[0], g.ndata)
        g.target_Kepler = [xs, ys, zs]
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()

        # Probe mark
        if self.artist_of_probe != None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*status[1:4], s=50, c='r',
                                            depthshade=False, marker='x')
        
        # Maneuver Type
        if self.artist_of_type != None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            if mantype == 'FLYTO':
                acctext = ''
                if self.c_maninfo['sson']:
                    acctext = ' SSacc={:.3f}'.format(ssacc)
                self.artist_of_type = g.ax.text(*status[1:4], 
                            self.mantext+acctext+' (start)', color='r', 
                            fontsize=11)
            else:
                self.artist_of_type = g.ax.text(*status[1:4], self.mantext, 
                                                color='r', fontsize=11)
        
        # Target mark
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',
                                             depthshade=False, marker='+')
        
        # Sun mark
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        sun_pos, sun_vel = common.SPKposvel(10, status[0])
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',
                                          depthshade=False, marker='o')
        
        # time
        remove_time()
        replot_time(status[0], 'Real')
        
        if g.fig != None: plt.draw()
        
        # display relative position and velocity, and time
        rel_pos = target_pos - status[1:4]
        rel_pos = common.eclv2lv(rel_pos, status[1:4], status[4:], sun_pos, 
                                 sun_vel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - status[4:]
        rel_vel = common.eclv2lv(rel_vel, status[1:4], status[4:], sun_pos, 
                                 sun_vel)
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
        ssacc = self.last_trj[7][self.c_index]

        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata)
            g.probe_Kepler = [x, y, z]
            if self.ui.check_PKepler.isChecked():
                draw_PKepler()

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
        self.artist_of_probe = g.ax.scatter(*ppos, s=50, c='r',
                                            depthshade=False, marker='x')
        if self.artist_of_target != None:
            self.artist_of_target.remove()
            self.artist_of_target = None

        # Maneuver Type
        if self.artist_of_type != None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            acctext = ''
            if self.c_maninfo['sson']:
                acctext = ' SSacc={:.3f}'.format(ssacc)
            if self.c_index == 0:
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext+
                    ' (start)', color='r', fontsize=11)
            elif self.c_index + 1 == len(self.last_trj[0]):
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext+
                    ' (end)', color='r', fontsize=11)
            else:
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext, 
                    color='r', fontsize=11)

        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',
                                             depthshade=False, marker='+')
        if self.artist_of_sun != None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',
                                          depthshade=False, marker='o')

        remove_time()
        replot_time(c_time, 'Real')
        
        if g.fig != None: plt.draw()
        
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
            erase_Ptrj()
            if self.ui.check_Ptrj.isChecked():
                draw_Ptrj()
            erase_TKepler()
            if self.ui.check_TKepler.isChecked():
                draw_TKepler()
            self.drawFLYTO()
        else:
            self.drawman()
    
    def save_settings(self):
        if g.showorbitsettings != None:
            s = g.showorbitsettings
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
        erase_Ptrj()
        erase_PKepler()
        erase_TKepler()
        remove_planets()
        remove_time()


from mainwindow import *

class MainForm(QtGui.QMainWindow):
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
        self.ui.manplans.horizontalHeader().setClickable(False)     # Disable colomn selection by clicking
        self.ui.manplans.verticalHeader().setClickable(False)       # Disable row selection by clicking
        self.ui.selectedman.setColumnWidth(0,100)
        self.ui.selectedman.setColumnWidth(1,139)
        self.connect(self.ui.actionOpen, SIGNAL('triggered()'), 
                                             self.openmanplan)
        self.connect(self.ui.actionNew, SIGNAL('triggered()'), 
                                             self.newmanplan)
        self.connect(self.ui.actionQuit, SIGNAL('triggered()'), 
                                             self.appquit)
        self.connect(self.ui.actionSave, SIGNAL('triggered()'), 
                                             self.savemanplan)
        self.connect(self.ui.actionSave_as, SIGNAL('triggered()'), 
                                             self.saveasmanplan)
        self.connect(self.ui.actionProbe, SIGNAL('triggered()'), 
                                             self.editprobe)
        self.connect(self.ui.actionTarget, SIGNAL('triggered()'), 
                                             self.edittarget)
        self.connect(self.ui.actionCreate, SIGNAL('triggered()'), 
                                             self.createcheckpoint)
        self.connect(self.ui.actionResume, SIGNAL('triggered()'), 
                                             self.resumecheckpoint)
        self.connect(self.ui.actionAbout_SSVG, SIGNAL('triggered()'), 
                                             self.aboutselected)
        self.connect(self.ui.execNext, SIGNAL('clicked()'), self.execnext)
        self.connect(self.ui.reviewthroughout, SIGNAL('clicked()'), 
                                             self.reviewthroughout)
        self.connect(self.ui.flightreview, SIGNAL('clicked()'), 
                                             self.showflightreview)
        self.connect(self.ui.showOrbit, SIGNAL('clicked()'), self.showorbit)
        self.connect(self.ui.editnext, SIGNAL('clicked()'), self.editnext)
        self.connect(self.ui.initexec, SIGNAL('clicked()'), self.initexec)
        self.connect(self.ui.manplans, 
                     SIGNAL('currentCellChanged(int,int,int,int)'), 
                     self.manplanscellchanged)
        self.connect(self.ui.manplans, SIGNAL('cellDoubleClicked(int,int)'), 
                     self.editman)
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
        g.currentdir = ''
        g.manfilename = None
        g.manplan = None
        g.maneuvers = None
        g.manplan_saved = True
        g.ndata = 1001
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
            fpath = common.logdir + 'SSVGLOG_' + nowtimestrf() + '.log'
            g.logfile = open(fpath, 'w', encoding='utf-8')
            logstring = 'start ssvg ' + g.version + ': ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            

    def init3Dfigure(self):
        if g.fig != None:
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
                ' Save and Quit ', ' Discard and Quit ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
            elif ans == 1:
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
        self.currentrow = 0
        
        g.manfilename = ans
        manfile = open(g.manfilename, 'r')
        g.manplan = json.load(manfile)
        manfile.close()
        
        try:
            g.mytarget = target.Target(**g.manplan['target'])
        except RuntimeError as e:
            QMessageBox.critical(self, 'File not Found', 
                str(e) + "\n\n"
                "Get appropriate SPK file, \n"
                "and store it in the 'data' folder.    ",
                0, 1, 0)
            return
        
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
        
        if g.options['log']:
            logstring = 'open flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)

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
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe is not on flight.', 0, 1, 0)
            return
        
        self.init3Dfigure()
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        
        if g.reviewthroughoutcontrol == None:
            g.reviewthroughoutcontrol = ReviewThroughoutControl(self)
            g.reviewthroughoutcontrol.show()
        else:
            g.reviewthroughoutcontrol.drawman()


    def savemanplan(self):
        if g.manfilename == None:
            self.saveasmanplan()
            return
        manfile = open(g.manfilename, 'w')
        json.dump(g.manplan, manfile, indent=4)
        g.manplan_saved = True
        QMessageBox.information(self, 'Info', 
                                'Flight Plan was saved.', 0, 1, 0)
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)
        
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
        
        if g.options['log']:
            logstring = 'save flight plan: ' + nowtimestr() + '\n'
            g.logfile.write(logstring)
            logstring = '    file name: ' + g.manfilename + '\n'
            g.logfile.write(logstring)

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
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    0, 1, 0)
            return False
        if len(g.maneuvers) <= g.nextman:
            QMessageBox.information(self, 
                        'Info', "You don't have valid maneuver.", 0, 1, 0)
            return False
        if g.maneuvers[g.nextman] == None:
            QMessageBox.information(self, 'Info', 
                        "You don't have valid maneuver.", 0, 1, 0)
            return False
        
        # prepare progress bar
        ptext = 'Processing:  ' + str(g.nextman + 1) + ' ' + \
            g.maneuvers[g.nextman]['type']
#
        success, emes = g.myprobe.exec_man(g.maneuvers[g.nextman],  
                             pbar=self.pbar, plabel=self.plabel, ptext=ptext)
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
            if g.showorbitcontrol == None:
                self.showorbit()
                self.ui.showOrbit.setEnabled(True)
        else:
            QMessageBox.information(self, 'Info', 
                                "Cannot Execute this Maneuver.\n\n"    \
                                + emes, 0, 1, 0)
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
                                "Select maneuver later than 'Next'", 0, 1, 0)
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
        self.erasecheckpoint()
        self.ui.menuCheckpoint.setEnabled(False)

    def showorbit(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe has no valid orbit.', 0, 1, 0)
            return
        self.init3Dfigure()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
            g.reviewthroughoutcontrol.close()
        if g.showorbitcontrol == None:
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
            QMessageBox.information(self, 'Info', 
                                'START shall be the 1st maneuver', 0, 1, 0)
            return
        if g.editedman['type'] != 'START' and self.currentrow == 0:
            QMessageBox.information(self, 'Info', 
                                'The 1st maneuver shall be START', 0, 1, 0)
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
        ans = QMessageBox.question(self, 'Delete Man.', mes, 0, button1=1, 
                                   button2=2)
        if ans == 2: return
        if self.currentrow < len(g.maneuvers):
            if g.maneuvers[self.currentrow] == None:
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
        if g.manfilename == None:
            filename = ''
        else:
            drs = g.manfilename.split('/')
            drs = drs[-1].split('.')
            filename = '.'.join(drs[0:-1])
        self.ui.manfilename.setText(filename)

    def showflightreview(self):
        if g.myprobe == None:
            QMessageBox.information(self, 'Info', 'You have no valid probe.', 
                                    0, 1, 0)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe is not on flight.', 0, 1, 0)
            return
        if g.myprobe.trj_record[-1][0]['type'] != 'FLYTO':
            QMessageBox.information(self, 'Info', 
                                    'Latest maneuver was not FLYTO.', 0, 1, 0)
            return  
        
        self.init3Dfigure()
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
        if man == None:
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
                'Existing checkpoint will be lost.  OK?', 0, button1=1, 
                button2=2)
            if ans != 1:
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
        if g.showorbitcontrol != None:
            g.showorbitcontrol.close()
        if g.flightreviewcontrol != None:
            g.flightreviewcontrol.close()
        if g.reviewthroughoutcontrol != None:
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
               ' Save and Proceed ', ' Proceed ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
            elif ans == 1:
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
               ' Save and Proceed ', ' Proceed ', ' Cancel ')
            if ans == 0:
                self.savemanplan()
            elif ans == 1:
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
    
        if g.options['log']:
            logstring = []
            logstring.append('edit target: ' + nowtimestr() + '\n')
            logstring.append('    target name: ' +
                            g.manplan['target']['name'] + '\n')
            if g.manplan['target']['SPKID2B'] > 10000:
                logstring.append('    target SPK file: ' +
                    g.manplan['target']['file'] + '\n')
                logstring.append('    target SPKID: ' +
                    str(g.manplan['target']['SPKID2B']) + '\n')
            g.logfile.writelines(logstring)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #print(os.path.abspath(os.path.dirname(sys.argv[0])))
    g.mainform = MainForm()
    g.mainform.show()
    sys.exit(app.exec_())
