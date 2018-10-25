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
import os
import json

import common
import julian
from datetime import datetime
import probe
import target
from twobodypred import TwoBodyPred
from spktype21 import SPKType21

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

import flightplan
from flightplan import NewFlightPlanDialog
from flightplan import EditProbeDialog
from flightplan import EditTargetDialog

import about
from about import AboutSSVG

import ftasetting
from ftasetting import FTAsettingDialog

import optimize
from optimize import StartOptimizeDialog
from optimize import CpOptimizeDialog

import editmaneuver
from editmaneuver import EditManDialog


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

# set global variables to modules
flightplan.g = g
about.g = g
ftasetting.g = g
optimize.g = g
optimize.erase_PKepler = erase_PKepler
optimize.draw_PKepler = draw_PKepler
optimize.erase_TKepler = erase_TKepler
optimize.draw_TKepler = draw_TKepler
optimize.erase_Ptrj = erase_Ptrj
optimize.draw_Ptrj = draw_Ptrj
editmaneuver.g = g
editmaneuver.nowtimestr = nowtimestr





from ui.showorbitcontrol import *

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
            tsjd, tejd = g.mytarget.getsejd()
            jd = (tsjd + tejd) * 0.5
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
        
        xs, ys, zs, ts = g.mytarget.points(self.jd, g.ndata)
        g.target_Kepler = [xs, ys, zs]
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

        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if tempjd < tsjd or tempjd >= tejd:
            return
        
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
            QMessageBox.critical(self, 'Error', 
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

# temp
editmaneuver.ShowOrbitDialog = ShowOrbitDialog

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

        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if self.jd < tsjd or self.jd >= tejd:
            oormes = "Start Time is OUTSIDE of Target's time span.\n" + \
                     "Enter approrpiate Start Time."
            QMessageBox.critical(self, 'Invalid Start Time', oormes)
            return

        if self.tbpred == None:
            self.tbpred = TwoBodyPred(g.myprobe.name)

        self.tbpred.fix_state(self.jd, self.ppos, self.pvel)
        self.tbpred.set_pred_dv(self.dv, self.phi, self.elv)
        x, y, z, t = self.tbpred.points(g.ndata)
        g.probe_Kepler = [x, y, z]
        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            draw_PKepler()
        
        xs, ys, zs, ts = g.mytarget.points(self.jd, g.ndata)
        g.target_Kepler = [xs, ys, zs]
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()
        
        self.ui.man_dv.setText('{:.3f}'.format(self.dv))
        self.ui.man_phi.setText('{:.2f}'.format(self.phi))
        self.ui.man_elv.setText('{:.2f}'.format(self.elv))

        self.restore_settings()
        self._redrawmark()

# temp        
editmaneuver.ShowStartOrbitDialog = ShowStartOrbitDialog

from ui.flightreviewcontrol import *

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

from ui.reviewthroughoutcontrol import *

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


from ui.mainwindow import *

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
        g.currentdir = os.path.join('')
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
            fpath = os.path.join(common.logdir, 'SSVGLOG_' + nowtimestrf() + '.log')
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
            caption='Select Flight Plan File',
            directory=g.currentdir, filter='JSON files (*.json)')
        if ans == '': return

        g.currentdir = os.path.split(ans)[0]
        
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
        
        # for old manplan data, check SPK file, and set data_type
        if not ('data_type' in g.manplan['target']):
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
                            0, 1, 0)
                        return
                g.manplan['target']['data_type'] = tempk.segments[0].data_type
                tempk.close()
            else:
                g.manplan['target']['data_type'] = 0
        
        if g.mytarget != None:
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
        
        if g.mytarget != None:
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

        # Check time
        if g.editedman['type']  == 'START' or g.editedman['type'] == 'FLYTO':
            tsjd, tejd = g.mytarget.getsejd()
            if g.editedman['time'] < tsjd or g.editedman['time'] >= tejd:
                oormes = "The time specified in the Maneuver is outside " + \
                "of the valid time span of the Target.\nTry again."
                QMessageBox.critical(self, 'Invalid Parameter', oormes)
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
            filename = os.path.basename(g.manfilename)
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
