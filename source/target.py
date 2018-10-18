# -*- coding: utf-8 -*-
"""
target module for SSVG
(c) 2016-2017 Shushi Uetsuki (whiskie14142)
"""

import common
from pytwobodyorbit import TwoBodyOrbit
from spktype01 import SPKType01
from spktype21 import SPKType21


class Target:
    """class for the target
    """
    def de430_ephem(self, jd):
        pos, vel = self.kernel[self.idx1a, self.idx1b].compute_and_differentiate(jd)
        if self.idx2a != 0:
            pos2, vel2 = self.kernel[self.idx2a, self.idx2b].compute_and_differentiate(jd)
            pos = pos + pos2
            vel = vel + vel2
        pos = common.eqn2ecl(pos) * 1000.0
        vel = common.eqn2ecl(vel) / common.secofday * 1000.0
        return pos, vel

    def nasa_sb_type01(self, jd):
        pos, vel = self.sbkernel.compute_type01(self.idx1a, self.idx1b, jd)
        pos = common.eqn2ecl(pos) * 1000.0
        vel = common.eqn2ecl(vel) * 1000.0
        return pos, vel

    def nasa_sb_type21(self, jd):
        pos, vel = self.sbkernel.compute_type21(self.idx1a, self.idx1b, jd)
        pos = common.eqn2ecl(pos) * 1000.0
        vel = common.eqn2ecl(vel) * 1000.0
        return pos, vel

        
    def __init__(self, name='Mars', file='', SPKID1A=0, SPKID1B=4, SPKID2A=0, 
                 SPKID2B=0, data_type=21):
        if file == '':
            self.kernel = common.SPKkernel
            self.ephem = self.de430_ephem
        else:
            filename = os.path.basename(file)
            if data_type == 1:
                try:
                    self.sbkernel = SPKType01.open(file)
                except FileNotFoundError:
                    try:
                        self.sbkernel = SPKType01.open(
                            os.path.join(common.bspdir, filename))
                    except FileNotFoundError:
                        raise RuntimeError("Target's SPK file is not found: "
                            + filename)
                self.ephem = self.nasa_sb_type01
            elif data_type == 21:
                try:
                    self.sbkernel = SPKType21.open(file)
                except FileNotFoundError:
                    try:
                        self.sbkernel = SPKType21.open(
                            os.path.join(common.bspdir, filename))
                    except FileNotFoundError:
                        raise RuntimeError("Target's SPK file is not found: "
                            + filename)
                self.ephem = self.nasa_sb_type21
            else:
                raise RuntimeError("Illegal data_type: " + str(data_type))
        self.name = name
        self.idx1a = SPKID1A
        self.idx1b = SPKID1B
        self.idx2a = SPKID2A
        self.idx2b = SPKID2B
        self.data_type = data_type
        return
    
    def posvel(self, jd):
        return self.ephem(jd)

    def points(self, jd, ndata):
        sunpos, sunvel = common.SPKposvel(10, jd)
        tpos, tvel = self.posvel(jd)
        tpos -= sunpos
        tvel -= sunvel
        orbit = TwoBodyOrbit(self.name, 'Sun', common.solarmu)
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
        
        
    
        