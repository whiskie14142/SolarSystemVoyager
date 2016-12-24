# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 15:26:36 2016

@author: shush_000
"""

import common
from pytwobodyorbit import TwoBodyOrbit
from spktype01 import SPKType01


class Target:
    
    def de430_ephem(self, jd):
        pos, vel = self.kernel[self.idx1a, self.idx1b].compute_and_differentiate(jd)
        if self.idx2a != 0:
            pos2, vel2 = self.kernel[self.idx2a, self.idx2b].compute_and_differentiate(jd)
            pos = pos + pos2
            vel = vel + vel2
        pos = common.eqn2ecl(pos) * 1000.0
        vel = common.eqn2ecl(vel) / common.secofday * 1000.0
        return pos, vel

    def nasa_sb_ephem(self, jd):
        sunpos, sunvel = self.kernel[self.idx1a, self.idx1b].compute_and_differentiate(jd)
        sunvel = sunvel / common.secofday
        scpos, scvel = self.sbkernel.compute_type01(self.idx2a, self.idx2b, jd)
        pos = sunpos + scpos
        vel = sunvel + scvel
        pos = common.eqn2ecl(pos) * 1000.0
        vel = common.eqn2ecl(vel) * 1000.0
        return pos, vel
        
    def __init__(self, name='Mars', file='', SPKID1A=0, SPKID1B=4, SPKID2A=0, SPKID2B=0):
        if file == '':
            self.kernel = common.SPKkernel
            self.ephem = self.de430_ephem
        else:
            filename = file.split('/')[-1]
            try:
                self.sbkernel = SPKType01.open(file)
            except FileNotFoundError:
                self.sbkernel = SPKType01.open(common.bspdir + filename)
            self.kernel = common.SPKkernel
            self.ephem = self.nasa_sb_ephem
        self.name = name
        self.idx1a = SPKID1A
        self.idx1b = SPKID1B
        self.idx2a = SPKID2A
        self.idx2b = SPKID2B
        return
    
    def posvel(self, jd):
        return self.ephem(jd)

    def points(self, jd, ndata):
        sunpos, sunvel = common.SPKposvel(10, jd)
#        sunpos, sunvel = common.SPKkernel[0,10].compute_and_differentiate(jd)
#        sunpos = common.eqn2ecl(sunpos) * 1000.0
#        sunvel = common.eqn2ecl(sunvel) / common.secofday * 1000.0
        tpos, tvel = self.posvel(jd)
        tpos -= sunpos
        tvel -= sunvel
        orbit = TwoBodyOrbit(self.name, 'Sol', common.solarmu)
        orbit.setOrbCart(0.0, tpos, tvel)
        xs, ys, zs, ts = orbit.points(ndata)
        xs += sunpos[0]
        ys += sunpos[1]
        zs += sunpos[2]
        ts /= common.secofday
        return xs, ys, zs, ts
        
    def getID(self):
        if self.idx2a == 0:
            return self.idx1b
        else:
            return self.idx2b
        
        
    
        