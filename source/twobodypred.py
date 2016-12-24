# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 22:41:00 2016

predict probe orbit and pos/vel through two body theory

@author: shush_000
"""

import common
from pytwobodyorbit import TwoBodyOrbit
from pytwobodyorbit import solveGauss
import numpy as np
import math


class TwoBodyPred:
    
    def __init__(self, pname):
        self.orbit = TwoBodyOrbit(pname, 'Sol', common.solarmu)
        return

    def fix_state(self, jd, ppos, pvel):
        self.jd = jd
        self.sunpos, self.sunvel = common.SPKposvel(10, self.jd)
#        spos, svel = common.SPKkernel[0, 10].compute_and_differentiate(self.jd)
#        self.sunpos = common.eqn2ecl(spos) * 1000.0
#        self.sunvel = common.eqn2ecl(svel) * 1000.0 / common.secofday
        jdsec = self.jd * common.secofday
        self.ppos = ppos
        self.pvel = pvel
        pos = self.ppos - self.sunpos
        vel = self.pvel - self.sunvel
        self.orbit.setOrbCart(jdsec, pos, vel)
        return
        
    def set_pred_dv(self, dv, phi, elv):
        relv = math.radians(elv)
        rphi = math.radians(phi)
        ldv = np.array([                    \
            dv * np.cos(relv) * np.cos(rphi), \
            dv * np.cos(relv) * np.sin(rphi), \
            dv * np.sin(relv)                \
            ])
        self.pred_vel = self.pvel + \
            common.ldv2ecldv(ldv, self.ppos, self.pvel, \
            self.sunpos, self.sunvel)
        jdsec = self.jd * common.secofday
        pos = self.ppos - self.sunpos
        vel = self.pred_vel - self.sunvel
        self.orbit.setOrbCart(jdsec, pos, vel)
        return
        
    def points(self, ndata):
        xs, ys, zs, times = self.orbit.points(ndata)
        return xs + self.sunpos[0], ys + self.sunpos[1], zs + self.sunpos[2], \
            times / common.secofday
        
    def posvelatt(self, jd):
        jdsec = jd * common.secofday
        pos, vel =self.orbit.posvelatt(jdsec)
        
        # sunpos, sunvel at jd
        spos, svel = common.SPKposvel(10, jd)
#        spos, svel = common.SPKkernel[0, 10].compute_and_differentiate(jd)
#        spos = common.eqn2ecl(spos) * 1000.0
#        svel = common.eqn2ecl(svel) * 1000.0 / common.secofday
        
        return pos + spos, vel + svel
        
    def fta(self, jd, tepos):
        # compute fixed time arrival guidance
        # jd : date of arrival
        # tepos position of target at jd (barycenter origin)
        dsec = (jd - self.jd) * common.secofday
        ipos = self.ppos - self.sunpos
        
        # sun position at end
        esunpos, esunvel = common.SPKposvel(10, jd)
        
        tpos = tepos - esunpos
        ivel, tvel = solveGauss(ipos, tpos, dsec, common.solarmu, ccw=True)
        iprobe_vel = self.pvel - self.sunvel
        delta_v = ivel - iprobe_vel
        
        localdv = common.eclv2lv(delta_v, self.ppos, self.pvel, self.sunpos, 
                                 self.sunvel)
        return common.rect2polar(localdv)
        
    def ftavel(self, jd, tepos):
        # compute fixed time arrival guidance
        # jd : date of arrival
        # tepos position of target at jd (barycenter origin)
        dsec = (jd - self.jd) * common.secofday
        ipos = self.ppos - self.sunpos
        
        # sun position and velocity at end
        esunpos, esunvel = common.SPKposvel(10, jd)
        
        tpos = tepos - esunpos
        ivel, tvel = solveGauss(ipos, tpos, dsec, common.solarmu, ccw=True)
        iprobe_vel = self.pvel - self.sunvel
        delta_v = ivel - iprobe_vel
        localdv = common.eclv2lv(delta_v, self.ppos, self.pvel, self.sunpos, 
                                 self.sunvel)
        dv, phi, elv = common.rect2polar(localdv)
        
        bc_ivel = ivel + self.sunvel
        bc_tvel = tvel + esunvel

        # returns intial velocity and terminal velocity (SSB origin)
        return dv, phi, elv, bc_ivel, bc_tvel
        
    def vta(self, jd, tpos, tvel):
        print('vta function is under construction')
        return
        
    def elmKepl(self):
        kepl = self.orbit.elmKepl()
        kepl['epoch'] /= common.secofday    # convert to 'JD(day)'
        kepl['T'] /= common.secofday        # convert to 'JD(day)'
        if kepl['e'] < 1.0:
            kepl['n'] *= common.secofday    # convert to 'deg/day'
            kepl['P'] /= common.secofday    # convert to 'days'
        return kepl
