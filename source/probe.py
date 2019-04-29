# -*- coding: utf-8 -*-
"""
probe module for SSVG
(c) 2016-2019 Shushi Uetsuki (whiskie14142)
"""

import common
from probeorbit import ProbeOrbit
import numpy as np
import math
from PyQt5 import QtCore



class SpaceBase:
    """class for the space base
    """
    def __init__(self, base):
        for baseitem in common.bases:
            if base == baseitem[0]:
                self.SPKID = baseitem[1]['SPKID']
                self.factor = baseitem[1]['Factor']
                # print(self.SPKID, self.factor)
            
    def posvel(self, jd):
        pos, vel = common.SPKposvel(self.SPKID, jd)
        sunpos, sunvel = common.SPKposvel(10, jd)
        pos = (pos - sunpos) * self.factor + sunpos
        vel = (vel - sunvel) * self.factor + sunvel
        return pos, vel



class Probe:
    """class for the space probe
    """
    def __init__(self, name='myprobe', pmass=500.0, base='EarthL2'):
        self.name = name
        self.pmass = pmass
        self.spacebase = SpaceBase(base)
        self.orbit = ProbeOrbit(name, pmass)
        self.execinitialize()
        
        self._translate = QtCore.QCoreApplication.translate
        
        self.errormes01 = self._translate('probe.py', 'Invalid End Time of FLYTO : Earier than Current Time')
        self.errormes02 = self._translate('probe.py', "Invalid End Time of FLYTO : OUTSIDE of Target's Time Span")
        self.errormes03 = self._translate('probe.py', 'Invalid Manuever Type : {}')
        self.errormes04 = self._translate('probe.py', 'Numerical Integration Error(s) occured \nafter {}')
        self.errormes05 = self._translate('probe.py', "Invalid Start Time : OUTSIDE of Target's Time Span")
        self.errormes06 = self._translate('probe.py', 'Invalid Maneuver Type : {}  Your Probe is not in flight yet.')
        self.errormes07 = self._translate('probe.py', 'Invalid Maneuver Type : {}  Your Probe is in flight already.')

    def execinitialize(self):
        self.trj_record = []
        self.onflight = False
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.jd = 0.0
        self.orbit.statusinitialize()
        self.checkpoint = False
        self.accumdv = {'CP':0.0, 'EP':0.0, 'SS':0.0}

#        
    def exec_man(self, man, target, pbar=None, plabel=None, ptext=''):
        if man['type'] != 'START' and not self.onflight:
            return False, self.errormes06.format(man['type'])
        if man['type'] == 'START' and self.onflight:
            return False, self.errormes07.format(man['type'])

        cman = man.copy()
        cman['epon'] = False
        cman['epdvpd'] = 0.0
        cman['epmode'] = 'L'
        cman['sson'] = False
        cman['ssmode'] = 'L'
        status = np.zeros(7)
        tsjd, tejd = target.getsejd()

        if man['type'] == 'START':
            self.jd = man['time']
            if self.jd < tsjd or self.jd >= tejd:
                return False, self.errormes05
            self.pos, self.vel = self.pseudostart(self.jd, dv=man['dv'], 
                                            elv=man['elv'], phi=man['phi'])
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            self.onflight = True
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            return True, ''
        elif man['type'] == 'CP':
            dv = man['dv']
            elv = math.radians(man['elv'])
            phi = math.radians(man['phi'])
            ldv = np.array([                    \
                dv * np.cos(elv) * np.cos(phi), \
                dv * np.cos(elv) * np.sin(phi), \
                dv * np.sin(elv)                \
                ])
            sunpos, sunvel = common.SPKposvel(10, self.jd)
            self.vel += common.ldv2ecldv(ldv, self.pos, self.vel, sunpos, 
                                         sunvel)
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            self.accumdv['CP'] += dv
            return True, ''
        elif man['type'] == 'EP_ON':
            dv = man['dvpd'] / common.secofday
            phi = math.radians(man['phi'])
            elv = math.radians(man['elv'])
            self.orbit.set_epstatus(True, dv, phi, elv, man['tvmode'],
                                    common.SPKkernel)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            return True, ''
        elif man['type'] == 'EP_OFF':
            self.orbit.set_epstatus(False, 0.0, 0.0, 0.0)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            return True, ''
        elif man['type'] == 'SS_ON':
            area = man['area']
            theta = math.radians(man['theta'])
            elv = math.radians(man['elv'])
            self.orbit.set_ssstatus(True, area, theta, elv, man['tvmode'],
                                    common.SPKkernel)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            return True, ''
        elif man['type'] == 'SS_OFF':
            self.orbit.set_ssstatus(False, 0.0, 0.0, 0.0)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.get_epssstatus(cman)
            self.trj_record.append([cman, status])
            return True, ''
        elif man['type'] == 'FLYTO':
            jdto = man['time']
            if jdto < self.jd:
                return False, self.errormes01
            if jdto >= tejd:
                return False, self.errormes02

            duration = jdto - self.jd
            if pbar is not None:
                pbar.setVisible(True)
                pbar.setValue(0)
                plabel.setText(ptext)
            inter = man['inter'] * common.secofday
            secto = jdto * common.secofday
            pt, px, py, pz, pxd, pyd, pzd, ssdvpd, runerror = self.orbit.trj(
                secto, inter, common.SPKkernel, common.planets_grav, 
                common.planets_mu, common.integ_abs_tol, common.integ_rel_tol, 
                pbar)
            if pbar is not None:
                pbar.setVisible(False)
                plabel.setText('')
            if runerror: 
                lastsuccess = 0.0
                length = len(pt)
                for i in range(length):
                    if pt[i] < 1.0: break
                    lastsuccess = pt[i]
                lastsuccess = lastsuccess / common.secofday
                return False, self.errormes04.format(common.jd2isot(lastsuccess))
            pt = pt / common.secofday
            self.get_epssstatus(cman)
            self.trj_record.append([cman, pt, px, py, pz, pxd, pyd, pzd, 
                                    ssdvpd])
            self.jd = pt[-1]
            self.pos = np.array([px[-1], py[-1], pz[-1]])
            self.vel = np.array([pxd[-1], pyd[-1], pzd[-1]])
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            if cman['epon']:
                self.accumdv['EP'] += duration * cman['epdvpd']
            if cman['sson']:
                ssdv = man['inter'] * ssdvpd[0]
                for i in range(1, len(pt)):
                    ssdv += (pt[i] -pt[i-1]) * ssdvpd[i]
                self.accumdv['SS'] += ssdv
            return True, ''
        else:
            return False, self.errormes03.format(man['type'])
        
    def pseudostart(self, jd, dv, phi, elv):
        elv = math.radians(elv)
        phi = math.radians(phi)
        ldv = np.array([
            dv * np.cos(elv) * np.cos(phi), 
            dv * np.cos(elv) * np.sin(phi), 
            dv * np.sin(elv)
            ])
        bpos, bvel = self.spacebase.posvel(jd)
        sunpos, sunvel = common.SPKposvel(10, jd)
        return bpos, bvel + common.ldv2ecldv(ldv, bpos, bvel, sunpos, sunvel)
        
    def createCheckpoint(self):
        self.checkpoint = True
        self.checkpointdata = {}
        self.checkpointdata['pos'] = self.pos.copy()
        self.checkpointdata['vel'] = self.vel.copy()
        self.checkpointdata['trj_record'] = self.trj_record.copy()
        self.checkpointdata['jd'] = self.jd
        self.checkpointdata['epstatus'] = self.orbit.get_epstatus()
        self.checkpointdata['ssstatus'] = self.orbit.get_ssstatus()
        self.checkpointdata['accumdv'] = self.accumdv.copy()
        
    def resumeCheckpoint(self):
        if self.checkpoint:
            self.pos = self.checkpointdata['pos'].copy()
            self.vel = self.checkpointdata['vel'].copy()
            self.trj_record = self.checkpointdata['trj_record'].copy()
            self.jd = self.checkpointdata['jd']
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            self.orbit.resume_epstatus(self.checkpointdata['epstatus'])
            self.orbit.resume_ssstatus(self.checkpointdata['ssstatus'])
            self.accumdv = self.checkpointdata['accumdv'].copy()
            
    def get_epssstatus(self, cman):
        epstatus = self.orbit.get_epstatus()
        ssstatus = self.orbit.get_ssstatus()
        cman['epon'] = epstatus[0]
        cman['epdvpd'] = epstatus[1] * common.secofday
        cman['epmode'] = epstatus[4]
        cman['sson'] = ssstatus[0]
        cman['ssmode'] = ssstatus[4]
        
        
            
