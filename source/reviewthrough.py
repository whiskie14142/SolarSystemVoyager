# -*- coding: utf-8 -*-
"""
reviewthrough module for SSVG (Solar System Voyager)
(c) 2016-2019 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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


from ui.reviewthroughoutcontrol import *

class ReviewThroughoutControl(QDialog):
    """class for 'Review Throughout' window
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left, top+740, 640, 211)
        self.ui = Ui_ReviewThroughoutControl()
        self.ui.setupUi(self)
        
        self._translate = QtCore.QCoreApplication.translate
        self.timecap_real = self._translate('reviewthrough.py', 'Real')
        self.sysMes01 = self._translate('reviewthrough.py', 'Received: Flight records, from SSVG')
        self.sysMes02 = self._translate('reviewthrough.py', 'Reviewing: {0}, Line {1}')

        # Get Settings of 'Look at' from showorbitsettings
        if g.showorbitsettings is not None:
            s = g.showorbitsettings
            self.ui.tobarycenter.setChecked(s['SSB'])
            self.ui.toprobe.setChecked(s['Probe'])
            self.ui.totarget.setChecked(s['Target'])

        self.ui.forward.clicked.connect(self.forward)
        self.ui.backward.clicked.connect(self.backward)
        self.ui.fastforward.clicked.connect(self.fastforward)
        self.ui.fastbackward.clicked.connect(self.fastbackward)
        self.ui.previousman.clicked.connect(self.previousman)
        self.ui.nextman.clicked.connect(self.nextman)
        self.ui.check_Ptrj.clicked.connect(self._statuschanged)
        self.ui.check_PKepler.clicked.connect(self._statuschanged)
        self.ui.check_TKepler.clicked.connect(self._statuschanged)
        self.ui.showplanets.clicked.connect(self._statuschanged)
        self.ui.showmantype.clicked.connect(self._statuschanged)
        self.ui.tobarycenter.clicked.connect(self._statuschanged)
        self.ui.toprobe.clicked.connect(self._statuschanged)
        self.ui.totarget.clicked.connect(self._statuschanged)

        self.mainwindow = parent
        self.artist_of_probe = None
        self.artist_of_target = None
        self.artist_of_sun = None
        self.artist_of_type = None
        
        self.tbpred = TwoBodyPred(g.myprobe.name)
        self.man_index = 0
        self.man_count = len(g.myprobe.trj_record)
        self.ui.previousman.setEnabled(False)

        self.drawmanFromSSVG()
        
        if self.man_count == 1 and self.c_mantype != 'FLYTO':
             self.ui.nextman.setEnabled(False)

    def drawmanFromSSVG(self):
#        self.ui.sysMessage.clear()
        self.ui.sysMessage.appendPlainText(self.sysMes01)
        self.fromNextman = False   
        self.drawman()
        
    def drawman(self):
        record = g.myprobe.trj_record[self.man_index]
        mantype = record[0]['type']
        self.c_maninfo = record[0]
        self.c_mantype = mantype
        self.mantext = '   ' + str(self.man_index + 1) + ' ' + mantype
        status = np.zeros(7)
        self.ui.sysMessage.appendPlainText(self.sysMes02.format(self.c_mantype, self.man_index+1))
        self.ui.sysMessage.centerCursor()
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
            if self.fromNextman:
                self.c_index = len(self.last_trj[0]) - 1
                self.ui.fastbackward.setEnabled(True)
                self.ui.backward.setEnabled(True)
                self.ui.forward.setEnabled(False)
                self.ui.fastforward.setEnabled(False)
            else:
                self.c_index = 0
                self.ui.fastbackward.setEnabled(False)
                self.ui.backward.setEnabled(False)
                self.ui.forward.setEnabled(True)
                self.ui.fastforward.setEnabled(True)
            self.ui.timescale.setEnabled(True)
            self.ui.label_2.setEnabled(True)
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
            self.ui.label_2.setEnabled(False)

        self.savedstatus = np.copy(status)        
        
        if mantype == 'START':
            self.ui.starttime.setText(common.jd2isot(record[1][0]))
            self.start_time = status[0]
        target_pos, target_vel = g.mytarget.posvel(status[0])

        erase_Ptrj()
        if self.ui.check_Ptrj.isChecked():
            draw_Ptrj()

        # Kepler Orbit of target
        xs, ys, zs, ts = g.mytarget.points(status[0], g.ndata)
        g.target_Kepler = [xs, ys, zs]
        erase_TKepler()
        if self.ui.check_TKepler.isChecked():
            draw_TKepler()

        self.mainwindow.ui.manplans.selectRow(self.man_index)
        if mantype == 'FLYTO':
            self.drawFLYTO()
            return
        
        # adjust center of image
        xlim = g.ax.get_xlim3d()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = status[1:4]
        else:
            cent = target_pos
        g.ax.set_xlim3d(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim3d(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim3d(cent[2]-hw, cent[2]+hw)

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

        # Probe mark
        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*status[1:4], s=40, c='r',
                                            depthshade=False, marker='x')
        
        # Maneuver Type
        if self.artist_of_type is not None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            self.artist_of_type = g.ax.text(*status[1:4], self.mantext, 
                                            color='r', fontsize=10)
        
        # Target mark
        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=50, c='g',
                                             depthshade=False, marker='+')
        
        # Sun mark
        if self.artist_of_sun is not None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        sun_pos, sun_vel = common.SPKposvel(10, status[0])
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='#FFAF00',
                                          depthshade=False, marker='o')
        
        # time
        remove_time()
        replot_time(status[0], self.timecap_real)
        
        if g.fig is not None: plt.draw()
        
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
        
        self.savedstatus[0] = np.copy(c_time)
        self.savedstatus[1:4] = np.copy(ppos)
        self.savedstatus[4:7] = np.copy(pvel)

        erase_PKepler()
        if self.ui.check_PKepler.isChecked():
            self.tbpred.fix_state(c_time, ppos, pvel)
            x, y, z, t = self.tbpred.points(g.ndata_s)
            g.probe_Kepler = [x, y, z]
            draw_PKepler()

        target_pos, target_vel = g.mytarget.posvel(c_time)
        sun_pos, sun_vel = common.SPKposvel(10, c_time)        

        xlim = g.ax.get_xlim3d()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = ppos
        else:
            cent = target_pos
        
        g.ax.set_xlim3d(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim3d(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim3d(cent[2]-hw, cent[2]+hw)

        # redraw planets
        remove_planets()
        if self.ui.showplanets.isChecked():
            replot_planets(c_time)

        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        self.artist_of_probe = g.ax.scatter(*ppos, s=40, c='r',
                                            depthshade=False, marker='x')
        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None

        # Maneuver Type
        if self.artist_of_type is not None:
            self.artist_of_type.remove()
            self.artist_of_type = None
        if self.ui.showmantype.isChecked():
            acctext = ''
            if self.c_maninfo['sson']:
                acctext = ' SSacc={:.3f}'.format(ssacc)
            if self.c_index == 0:
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext+
                    ' (start)', color='r', fontsize=10)
            elif self.c_index + 1 == len(self.last_trj[0]):
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext+
                    ' (end)', color='r', fontsize=10)
            else:
                self.artist_of_type = g.ax.text(*ppos, self.mantext+acctext, 
                    color='r', fontsize=10)

        self.artist_of_target = g.ax.scatter(*target_pos, s=50, c='g',
                                             depthshade=False, marker='+')
        if self.artist_of_sun is not None:
            self.artist_of_sun.remove()
            self.artist_of_sun = None
        self.artist_of_sun = g.ax.scatter(*sun_pos, s=50, c='#FFAF00',
                                          depthshade=False, marker='o')

        remove_time()
        replot_time(c_time, self.timecap_real)
        
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

    def redrawTargetFromSSVG(self):
        status = self.savedstatus
        target_pos, target_vel = g.mytarget.posvel(status[0])
        sun_pos, sun_vel = common.SPKposvel(10, status[0])

        # adjust center of image
        xlim = g.ax.get_xlim3d()
        hw = (xlim[1] - xlim[0]) * 0.5
        if self.ui.tobarycenter.isChecked():
            cent = [0.0, 0.0, 0.0]
        elif self.ui.toprobe.isChecked():
            cent = status[1:4]
        else:
            cent = target_pos
        g.ax.set_xlim3d(cent[0]-hw, cent[0]+hw)
        g.ax.set_ylim3d(cent[1]-hw, cent[1]+hw)
        g.ax.set_zlim3d(cent[2]-hw, cent[2]+hw)

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

        # Target mark
        if self.artist_of_target is not None:
            self.artist_of_target.remove()
            self.artist_of_target = None
        self.artist_of_target = g.ax.scatter(*target_pos, s=50, c='g',
                                             depthshade=False, marker='+')
        
        # display relative position and velocity
        rel_pos = target_pos - status[1:4]
        rel_pos = common.eclv2lv(rel_pos, status[1:4], 
                                 status[4:], sun_pos, sun_vel)
        trange, tphi, telv = common.rect2polar(rel_pos)
        rel_vel = target_vel - status[4:]
        rel_vel = common.eclv2lv(rel_vel, status[1:4], 
                                 status[4:], sun_pos, sun_vel)
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
            self.ui.backward.setEnabled(True)
            self.ui.fastbackward.setEnabled(True)
            self.ui.previousman.setEnabled(True)
            if self.c_index + 1 == len(self.last_trj[0]):
                self.ui.forward.setEnabled(False)
                self.ui.fastforward.setEnabled(False)
                if self.man_index + 1 == self.man_count:
                    self.ui.nextman.setEnabled(False)
    
    def backward(self):
        if self.c_index > 0:
            self.c_index -= 1
            self.drawFLYTO()
            self.ui.forward.setEnabled(True)
            self.ui.fastforward.setEnabled(True)
            self.ui.nextman.setEnabled(True)
            if self.c_index == 0:
                self.ui.backward.setEnabled(False)
                self.ui.fastbackward.setEnabled(False)
                if self.man_index == 0:
                    self.ui.previousman.setEnabled(False)
        
    def fastforward(self):
        if self.c_index == len(self.last_trj[0]) - 1: return
        hopping = self.ui.timescale.value()
        self.c_index += hopping
        if self.c_index >= len(self.last_trj[0]):
            self.c_index = len(self.last_trj[0]) - 1
        self.drawFLYTO()
        self.ui.backward.setEnabled(True)
        self.ui.fastbackward.setEnabled(True)
        self.ui.previousman.setEnabled(True)
        if self.c_index + 1 == len(self.last_trj[0]):
            self.ui.forward.setEnabled(False)
            self.ui.fastforward.setEnabled(False)
            if self.man_index + 1 == self.man_count:
                self.ui.nextman.setEnabled(False)

    def fastbackward(self):
        if self.c_index == 0: return
        hopping = self.ui.timescale.value()
        self.c_index -= hopping
        if self.c_index < 0:
            self.c_index = 0
        self.drawFLYTO()
        self.ui.forward.setEnabled(True)
        self.ui.fastforward.setEnabled(True)
        self.ui.nextman.setEnabled(True)
        if self.c_index == 0:
            self.ui.backward.setEnabled(False)
            self.ui.fastbackward.setEnabled(False)
            if self.man_index == 0:
                self.ui.previousman.setEnabled(False)

    def previousman(self):
        if self.c_mantype == 'FLYTO':
            if self.c_index == 0:
                if self.man_index == 0:
                    return
                self.man_index -= 1
                self.fromNextman = True
                self.drawman()
                if self.man_index == 0:
                    self.ui.previousman.setEnabled(False)
            else:
                self.c_index = 0
                self.drawFLYTO()
                self.ui.forward.setEnabled(True)
                self.ui.fastforward.setEnabled(True)
                self.ui.backward.setEnabled(False)
                self.ui.fastbackward.setEnabled(False)
        else:
            if self.man_index == 0:
                return
            self.man_index -= 1
            self.fromNextman = True
            self.drawman()
        self.ui.nextman.setEnabled(True)
    
    def nextman(self):
        if self.c_mantype == 'FLYTO':
            length = len(self.last_trj[0])
            if self.c_index + 1 == length:
                if self.man_index + 1 == self.man_count:
                    return
                self.man_index += 1
                self.fromNextman = False
                self.drawman()
                if self.man_index + 1 == self.man_count and self.c_mantype != 'FLYTO':
                    self.ui.nextman.setEnabled(False)
            else:
                self.c_index = length - 1
                self.drawFLYTO()
                self.ui.forward.setEnabled(False)
                self.ui.fastforward.setEnabled(False)
                self.ui.backward.setEnabled(True)
                self.ui.fastbackward.setEnabled(True)
                if self.man_index + 1 == self.man_count:
                    self.ui.nextman.setEnabled(False)
        else:
            if self.man_index + 1 == self.man_count:
                return
            self.man_index += 1
            self.fromNextman = False
            self.drawman()
            if self.man_index + 1 == self.man_count and self.c_mantype != 'FLYTO':
                self.ui.nextman.setEnabled(False)
        self.ui.previousman.setEnabled(True)
        
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
        if g.showorbitsettings is not None:
            s = g.showorbitsettings
            s['SSB'] = self.ui.tobarycenter.isChecked()
            s['Probe'] = self.ui.toprobe.isChecked()
            s['Target'] = self.ui.totarget.isChecked()
            g.showorbitsettings = s
        
    def closeEvent(self, event):
        g.reviewthroughoutcontrol = None
        event.accept()
        if self.artist_of_probe is not None:
            self.artist_of_probe.remove()
            self.artist_of_probe = None
        if self.artist_of_type is not None:
            self.artist_of_type.remove()
            self.artist_of_type = None
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
