# -*- coding: utf-8 -*-
"""
probeorbit module for SSVG
(c) 2016-2017 Shushi Uetsuki (whiskie14142)

This module computes the trajectory of the probe with numerical integration
This module can use gravitational attraction of all planets, Pluto, 
    the Moon, and the Sun for the numerical integration
This module uses ecliptic coordinate system (J2000.0) for position and 
    velocity
The origin of the coordinate system is barycenter of the solar system
"""

import numpy as np
import common
from scipy.integrate import ode


class ProbeOrbit:
    """class for the orbit (trajectory) of the probe　which flies in the
    solar system
    """

    def _ssnv(self, td, y, kernel):
        # compute normal vector of Solar Sail
        pos = y[0:3]
        vel = y[3:6]
        sunpos, sunvel =kernel[0,10].compute_and_differentiate(td)
        sunpos = common.eqn2ecl(sunpos) * 1000.0
        sunvel = common.eqn2ecl(sunvel) * 1000.0 / common.secofday
        nv = np.array([np.cos(self._sstheta) * np.cos(self._sselv), 
            np.sin(self._sstheta) * np.cos(self._sselv), 
            np.sin(self._sselv)])
        return common.sodv2ecldv(nv, pos, vel, sunpos, sunvel)

    def _ssacc(self, td, y, kernel):
        # comupte acceleration of Solar Sail
        pos = y[0:3]
        vel = y[3:6]
        sunpos, sunvel =kernel[0,10].compute_and_differentiate(td)
        sunpos = common.eqn2ecl(sunpos) * 1000.0
        sunvel = common.eqn2ecl(sunvel) * 1000.0 / common.secofday
        scpos = pos - sunpos
        r2 = np.dot(scpos, scpos)
        p0 = common.solark1 / 4.0 / np.pi / r2 / common.c
        nv = np.array([np.cos(self._sstheta) * np.cos(self._sselv), 
            np.sin(self._sstheta) * np.cos(self._sselv), 
            np.sin(self._sselv)])
        xax = np.array([1.0, 0., 0.,])
        costheta = np.dot(xax, nv)
        cos2theta = costheta ** 2
        f = 2.0 * cos2theta * p0 * self._ssarea
        acc = nv * (f / self._pmass)
        if costheta < 0.0:
            acc = acc * (-1.0)
        return common.sodv2ecldv(acc, pos, vel, sunpos, sunvel)

    def _sseclacc(self, td, y, kernel):
        # compute acceleration of Solar Sail when tvmode='E'
        pos = y[0:3]
        sunpos =kernel[0,10].compute(td)
        sunpos = common.eqn2ecl(sunpos) * 1000.0
        scpos = pos - sunpos
        r2 = np.dot(scpos, scpos)
        p0 = common.solark1 / 4.0 / np.pi / r2 / common.c
        xax = scpos / np.sqrt(r2)
        costheta = np.dot(xax, self._sseclnv)
        cos2theta = costheta ** 2
        f = 2.0 * cos2theta * p0 * self._ssarea
        acc = self._sseclnv * (f / self._pmass)
        if costheta < 0.0:
            acc = acc * (-1.0)
        return acc

    def _epacc(self, td, y, kernel):
        # comupte acceleration of Electric Propulsion System
        acc = np.array([self._epdv * np.cos(self._epelv) * np.cos(self._epphi),
            self._epdv * np.cos(self._epelv) * np.sin(self._epphi), 
            self._epdv * np.sin(self._epelv)])
        pos = y[0:3]
        vel = y[3:6]
        sunpos, sunvel =kernel[0,10].compute_and_differentiate(td)
        sunpos = common.eqn2ecl(sunpos) * 1000.0
        sunvel = common.eqn2ecl(sunvel) * 1000.0 / common.secofday
        return common.ldv2ecldv(acc, pos, vel, sunpos, sunvel)

    def _func(self, t, y, kernel, body_f, body_mu):
        # t: JD by seconds
        # y: position and velocity, origin=solar system barycenter, ecliptic.
        # kernel: kernel of SPK
        # body_f: source of grav. [0]Mercury~[8]Pluto,[9]Sun  True or False
        # body_mu: mu of the body
        yd = np.zeros(6)
        yd[0] = y[3]
        yd[1] = y[4]
        yd[2] = y[5]
        
        td = t / common.secofday
#        print(td)
        for i in range(12):
            if body_f[i]:
                n = common.planets_id[i][0]
                if n > 300:
                    pos = (kernel[0,3].compute(td) + kernel[3,n].compute(td)) \
                        * 1000.0
                else:
                    pos = kernel[0,n].compute(td) * 1000.0
                delta = common.eqn2ecl(pos) - y[0:3]
                r = np.sqrt(np.dot(delta, delta))
                yd[3:6] += delta * (body_mu[i] / r ** 3)
#                print(delta * (body_mu[i] / r ** 3))
        if self._epon:
            if self._epmode == 'L':
                yd[3:6] += self._epacc(td, y, kernel)
            else:
                yd[3:6] += self._epeclacc
        if self._sson:
            if self._ssmode == 'L':
                yd[3:6] += self._ssacc(td, y, kernel)
            else:
                yd[3:6] += self._sseclacc(td, y, kernel)
        return yd
    
    def __init__(self, pname, pmass):
        self._pname = pname
        self._pmass = pmass # mass of probe (kg)
        self.statusinitialize()
  
    def statusinitialize(self):      
        self._epon = False
        self._epdv = 0.0    # absolute accelaration of the EP
        self._epphi = 0.0   # angle phi of the EP
        self._epelv = 0.0   # angle elv of the EP
        self._epmode = 'L'
        self._epeclacc = []
        
        self._sson = False
        self._ssarea = 0.0      # area of the solar sail
        self._sstheta = 0.0     # angle theta of the solar sail
        self._sselv = 0.0       # angle elv of the solar sail
        self._ssmode = 'L'
        self._sseclnv = []

    def set_epstatus(self, epon, epdv, epphi, epelv, tvmode='L', kernel=None):
        self._epon = epon
        self._epdv = epdv
        self._epphi = epphi
        self._epelv = epelv
        self._epmode = tvmode
        if tvmode != 'L':
            td = self._t0 / common.secofday
            y = self._y0
            self._epeclacc = self._epacc(td, y, kernel)
        
    def get_epstatus(self):
        return self._epon, self._epdv, self._epphi, self._epelv, self._epmode,\
            self._epeclacc.copy()
            
    def resume_epstatus(self, epstatus):
        self._epon = epstatus[0]
        self._epdv = epstatus[1]
        self._epphi = epstatus[2]
        self._epelv = epstatus[3]
        self._epmode = epstatus[4]
        self._epeclacc = epstatus[5]
    
    def set_ssstatus(self, sson, ssarea, sstheta, sselv, tvmode='L', 
                     kernel=None):
        self._sson = sson
        self._ssarea = ssarea
        self._sstheta = sstheta
        self._sselv = sselv
        self._ssmode = tvmode
        if tvmode != 'L':
            td = self._t0 / common.secofday
            y = self._y0
            self._sseclnv = self._ssnv(td, y, kernel)
        
    def get_ssstatus(self):
        return self._sson, self._ssarea, self._sstheta, self._sselv, \
            self._ssmode, self._sseclnv.copy()
    
    def resume_ssstatus(self, ssstatus):
        self._sson = ssstatus[0]
        self._ssarea = ssstatus[1]
        self._sstheta = ssstatus[2]
        self._sselv = ssstatus[3]
        self._ssmode = ssstatus[4]
        self._sseclnv = ssstatus[5]

    def setCurrentCart(self, t, pos, vel):
        # t should be in seconds,
        # pos should be in meters,
        # vel should be in meters per second
        self._t0 = t
        self._y0 = np.zeros(6)
        self._y0[0:3] = pos
        self._y0[3:6] = vel

    def compssdvpd(self, tsec, y, kernel):
        td = tsec / common.secofday
        if self._ssmode == 'L':
            acc = self._ssacc(td, y, kernel)
        else:
            acc = self._sseclacc(td, y, kernel)
        return np.sqrt(np.dot(acc, acc)) * common.secofday
        
        
    def trj(self, endsec, inter, kernel, body_f, body_mu, atol, rtol, pbar):
        runerror = False
        ninter = int((endsec - self._t0) / inter)
        if (self._t0 + ninter * inter) < endsec:
            ndata = ninter + 2
            remainder = True
        else:
            ndata = ninter + 1
            remainder = False
        r = ode(self._func).set_integrator('dopri5', atol=atol, rtol=rtol)
        r.set_initial_value(self._y0, self._t0).set_f_params(kernel, body_f, 
            body_mu)
        t = np.zeros(ndata); t[0] = self._t0
        x = np.zeros(ndata); x[0] = self._y0[0]
        y = np.zeros(ndata); y[0] = self._y0[1]
        z = np.zeros(ndata); z[0] = self._y0[2]
        xd = np.zeros(ndata); xd[0] = self._y0[3]
        yd = np.zeros(ndata); yd[0] = self._y0[4]
        zd = np.zeros(ndata); zd[0] = self._y0[5]
        ssdvpd = np.zeros(ndata)
        if self._sson:
            ssdvpd[0] = self.compssdvpd(self._t0, self._y0, kernel)

        for i in range(1, ninter+1):
            posvel = r.integrate(self._t0 + i * inter)
            if not r.successful(): 
                runerror = True
                print('Unsuccessful numerical integration.')
            t[i] = r.t
            x[i] = posvel[0]
            y[i] = posvel[1]
            z[i] = posvel[2]
            xd[i] = posvel[3]
            yd[i] = posvel[4]
            zd[i] = posvel[5]
            if self._sson:
                ssdvpd[i] = self.compssdvpd(r.t, posvel, kernel)
            if pbar != None:
                if i % 10 == 0:
                    percent = i * 100 // ninter
                    pbar.setValue(percent)
        if remainder:
            posvel = r.integrate(endsec)
            if not r.successful(): 
                runerror = True
                print('Unsuccessful numerical integration.')
            t[ndata-1] = r.t
            x[ndata-1] = posvel[0]
            y[ndata-1] = posvel[1]
            z[ndata-1] = posvel[2]
            xd[ndata-1] = posvel[3]
            yd[ndata-1] = posvel[4]
            zd[ndata-1] = posvel[5]
            if self._sson:
                ssdvpd[ndata-1] = self.compssdvpd(r.t, posvel, kernel)
        return t, x, y, z, xd, yd, zd, ssdvpd, runerror
    
        
        
        
        
        
        
        
        


        
        
