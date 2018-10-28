# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 08:12:16 2018

@author: shush_000
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import matplotlib.pyplot as plt

import common
from twobodypred import TwoBodyPred

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
        if g.showorbitsettings is not None:
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
#        if self.artist_of_orbit is not None:
#            self.artist_of_orbit[0].remove()
#            self.artist_of_orbit = None
        if g.myprobe is None:
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
            if self.tbpred is None:
                self.tbpred = TwoBodyPred(g.myprobe.name)
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata_s)
            g.probe_Kepler = [x, y, z]
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

        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*ppos, s=50, c='r',
                                            depthshade=False, marker='x')
        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=40, c='g',
                                             depthshade=False, marker='+')
        if self.artist_of_sun is not None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='w',
                                          depthshade=False, marker='o')

        if self.artist_of_epssinfo is not None:
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
        
        if g.fig is not None: plt.draw()
        
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
        if g.showorbitsettings is not None:
            s = g.showorbitsettings
            s['SSB'] = self.ui.tobarycenter.isChecked()
            s['Probe'] = self.ui.toprobe.isChecked()
            s['Target'] = self.ui.totarget.isChecked()
            g.showorbitsettings = s
        
    def closeEvent(self, event):
        g.flightreviewcontrol = None
        event.accept()
        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        if self.artist_of_sun is not None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        if self.artist_of_epssinfo is not None:
            self.artist_of_epssinfo.remove()
            self.artist_of_epssinfo = None
        erase_Ptrj()
        erase_PKepler()
        erase_TKepler()
        remove_planets()
        remove_time()