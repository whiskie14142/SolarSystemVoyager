# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:41:18 2018

@author: shush_000
"""


from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib.pyplot as plt
import numpy as np

import common
from twobodypred import TwoBodyPred

from ui.orbitoptimizedialog import *

# global variables: SSVG sets real instances
g = None
erase_PKepler = None
draw_PKepler = None
erase_TKepler = None
draw_TKepler = None
erase_Ptrj = None
draw_Ptrj = None

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
        tsjd, tejd = g.mytarget.getsejd()
        # Probe Kepler Orbit
        ndata = self.sl_maxval - self.sl_minval + 1
        x = []
        y = []
        z = []
        for i in range(ndata):
            pos = i + self.sl_minval
            jd = self.sl_pos2real(self.itfrom, self.itto, pos) + self.itcenter
            if jd >= tsjd and jd < tejd:
                ppos, pvel = self.orgorbposvel(jd)
                x.append(ppos[0])
                y.append(ppos[1])
                z.append(ppos[2])
        g.probe_Kepler = [x, y, z]
        
        # Target Kepler Orbit
        if self.itcenter >= tsjd and self.itcenter < tejd:
            jd = self.itcenter
        else:
            jd = (tsjd + tejd) * 0.5
        x, y, z, t = g.mytarget.points(jd, g.ndata)
        g.target_Kepler = [x, y, z]
        
        self.fixedorbitchanged()
        
    def draworbit(self):
        self.ui.finishbutton.setEnabled(False)        
        
        # Check time
        tsjd, tejd = g.mytarget.getsejd()
        if self.itcurrent < tsjd or self.itcurrent >= tejd:
            return
        if self.ttcurrent < tsjd or self.ttcurrent >= tejd:
            return

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
        if self.itcurrent + common.minft >= self.ttcurrent:
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
        self.ui.finishbutton.setEnabled(True)
        
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
            self.ttcenter = 250.0
            self.ttfrom = self.ttcenter - dev
            self.ttto = self.ttcenter + dev
            pos = self.sl_real2pos(self.ttfrom, self.ttto, self.cduration)
            while pos < self.sl_minval:
                self.ttfrom -= dev
                self.ttto -= dev
                self.ttcenter -= dev
                pos = self.sl_real2pos(self.ttfrom, self.ttto, self.cduration)
            while pos > self.sl_maxval:
                self.ttfrom += dev
                self.ttto += dev
                self.ttcenter += dev
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
