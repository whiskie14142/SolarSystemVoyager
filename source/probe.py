# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 13:44:30 2016

@author: shush_000
"""

import common
from probeorbit import ProbeOrbit
import numpy as np
import math



class SpaceBase:
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
    
    def __init__(self, name='myprobe', pmass=500.0, base='EarthL2'):
        self.name = name
        self.pmass = pmass
        self.spacebase = SpaceBase(base)
        self.orbit = ProbeOrbit(name, pmass)
        self.execinitialize()

    def execinitialize(self):
        self.trj_record = []
        self.onflight = False
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.jd = 0.0
        self.orbit.statusinitialize()
        self.checkpoint = False

#        
    def exec_man(self, man, pbar=None, plabel=None, ptext=''):
        if man['type'] != 'START' and not self.onflight:
            print('Your probe has not started yet.  Man. Type : ', man['type'])
            return False
        if man['type'] == 'START' and self.onflight:
            print('Your probe has started already.  Man. Type : ', man['type'])
            return False

        cman = man.copy()
        status = np.zeros(7)

        if man['type'] == 'START':
            self.jd = man['time']
            self.pos, self.vel = self.pseudostart(self.jd, dv=man['dv'], 
                                            elv=man['elv'], phi=man['phi'])
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            self.onflight = True
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.trj_record.append([cman, status])
            return True
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
            self.trj_record.append([cman, status])
            return True
        elif man['type'] == 'EP_ON':
            dv = man['dvpd'] / common.secofday
            phi = math.radians(man['phi'])
            elv = math.radians(man['elv'])
            self.orbit.set_epstatus(True, dv, phi, elv)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.trj_record.append([cman, status])
            return True
        elif man['type'] == 'EP_OFF':
            self.orbit.set_epstatus(False, 0.0, 0.0, 0.0)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.trj_record.append([cman, status])
            return True
        elif man['type'] == 'SS_ON':
            aria = man['aria']
            theta = math.radians(man['theta'])
            elv = math.radians(man['elv'])
            self.orbit.set_ssstatus(True, aria, theta, elv)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.trj_record.append([cman, status])
            return True
        elif man['type'] == 'SS_OFF':
            self.orbit.set_ssstatus(False, 0.0, 0.0, 0.0)
            status[0] = self.jd
            status[1:4] = self.pos.copy()
            status[4:] = self.vel.copy()
            self.trj_record.append([cman, status])
            return True
        elif man['type'] == 'FLYTO':
            jdto = man['time']
            if jdto < self.jd:
                print('Invalid FLYTO time : ', common.jd2datetime(jdto))
                return False
            if pbar != None:
                pbar.setVisible(True)
                pbar.setValue(0)
                plabel.setText(ptext)
            inter = man['inter'] * common.secofday
            secto = jdto * common.secofday
            pt, px, py, pz, pxd, pyd, pzd, runerror = self.orbit.trj(secto, 
                inter, common.SPKkernel, common.planets_grav, 
                common.planets_mu, common.integ_abs_tol, common.integ_rel_tol, 
                pbar)
            if pbar != None:
                pbar.setVisible(False)
                plabel.setText('')
            if runerror: return False
            pt = pt / common.secofday
            self.trj_record.append([cman, pt, px, py, pz, pxd, pyd, pzd])
            self.jd = pt[-1]
            self.pos = np.array([px[-1], py[-1], pz[-1]])
            self.vel = np.array([pxd[-1], pyd[-1], pzd[-1]])
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            return True
        else:
            print('invalid manuever type : ',man['type'])
            return False
            
    def reset(self):
        self.onflight = False
        self.trj_record = []
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.jd = 0.0
        return
        
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
        
    def resumeCheckpoint(self):
        if self.checkpoint:
            self.pos = self.checkpointdata['pos'].copy()
            self.vel = self.checkpointdata['vel'].copy()
            self.trj_record = self.checkpointdata['trj_record'].copy()
            self.jd = self.checkpointdata['jd']
            self.orbit.setCurrentCart(self.jd*common.secofday, self.pos, 
                                      self.vel)
            self.orbit.set_epstatus(*self.checkpointdata['epstatus'])
            self.orbit.set_ssstatus(*self.checkpointdata['ssstatus'])
            
