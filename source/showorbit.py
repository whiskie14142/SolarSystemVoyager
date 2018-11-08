# -*- coding: utf-8 -*-
"""
showorbit module for SSVG (Solar System Voyager)
(c) 2016-2018 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np

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

from ui.showorbitcontrol import *

class ShowOrbitDialog(QDialog):
    """class for 'Show Orbit' window
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mother = parent
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+740, 640, 211)
        self.ui = Ui_ShowOrbitControl()
        self.ui.setupUi(self)
        
        self.ui.forward.clicked.connect(self.forward)
        self.ui.backward.clicked.connect(self.backward)
        self.ui.fastforward.clicked.connect(self.fastforward)
        self.ui.fastbackward.clicked.connect(self.fastbackward)
        self.ui.check_Ptrj.clicked.connect(self._statuschanged)
        self.ui.check_PKepler.clicked.connect(self._statuschanged)
        self.ui.check_TKepler.clicked.connect(self._statuschanged)
        self.ui.showplanets.clicked.connect(self._statuschanged)
        self.ui.tobarycenter.clicked.connect(self._statuschanged)
        self.ui.toprobe.clicked.connect(self._statuschanged)
        self.ui.totarget.clicked.connect(self._statuschanged)
        self.ui.dtApply.clicked.connect(self.dtapply)

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
        if g.myprobe is None:
            QMessageBox.information(self, 'Info', 
                                    'You have no valid probe.', QMessageBox.Ok)
            return
        if not g.myprobe.onflight:
            QMessageBox.information(self, 'Info', 
                                    'Your probe has no valid orbit.', QMessageBox.Ok)
            return

        self.jd = g.myprobe.jd
        self.ui.currentdate.setText(common.jd2isot(self.jd))

        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        
        self.ppos = g.myprobe.pos
        self.pvel = g.myprobe.vel
        if self.tbpred is None:
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
        tempjd = self.jd + self.delta_jd
        self.ui.preddate.setText(common.jd2isot(tempjd))

        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None

        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None

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

        self.artist_of_probe = g.ax.scatter(*probe_pos, s=40, c='r', 
                                            depthshade=False, marker='x')
        
        self.artist_of_target = g.ax.scatter(*self.target_pos, s=50, c='g', 
                                             depthshade=False, marker='+')
            
        if self.artist_of_sun is not None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*self.sun_pos, s=50, c='#FFAF00',
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

        if g.fig is not None: plt.draw()
        
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
        self.delta_jd = dt
        self.dtapply()

    def get_pred_jd(self):
        return self.jd + self.delta_jd
        
    def forward(self):
        exp = self.ui.timescale.value()
        self.delta_jd += 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)
        
    def backward(self):
        exp = self.ui.timescale.value()
        self.delta_jd -= 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)
        
    def fastforward(self):
        exp = self.ui.timescale.value() + 1
        self.delta_jd += 10.0 ** exp
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)

    def fastbackward(self):
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

    def dtapply(self):
        text = self.ui.delta_t_edit.text()
        try:
            value = float(text)
        except ValueError:
            QMessageBox.warning(self, 'Warning', 
                'Invalid Elapsed Time.  It cannot be apply', QMessageBox.Ok)
            return
        self.delta_jd = value
        self.ui.delta_t_edit.setText('{:.8f}'.format(self.delta_jd))
        self._redrawmark()
        if self.affect_parent:
            self.mother.gettime(self.jd + self.delta_jd)

    def closeEvent(self, event):
        g.showorbitcontrol = None
        self.save_settings()
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
        if g.showorbitsettings is not None:
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

        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if self.jd < tsjd or self.jd >= tejd:
            oormes = "Start Time is OUTSIDE of Target's time span.\n" + \
                     "Enter approrpiate Start Time."
            QMessageBox.critical(self, 'Invalid Start Time', oormes, QMessageBox.Ok)
            return

        if self.tbpred is None:
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
