# -*- coding: utf-8 -*-
"""

Created on Wed May 04 21:40:34 2016

@author: shush_000
"""

import numpy as np
import common
from scipy.integrate import ode


class ProbeOrbit:
# 太陽系を飛行する探査機のクラス
# 経路は常に数値積分で計算する
# 全惑星と冥王星の重力を考慮できる
# 惑星の位置はjplephemで算出（ファイルはde430.bspを使用する）
# 座標系は太陽系重心の黄道座標（J2000.0）
# 長さの単位はメートル、時間の単位は秒でインタフェースする

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
        nv = np.array([np.cos(self._sstheta) * np.cos(self._sselv),  \
            np.sin(self._sstheta) * np.cos(self._sselv),  \
            np.sin(self._sselv)])
        xax = np.array([1.0, 0., 0.,])
        cos2theta = np.dot(xax, nv) ** 2
        f = 2.0 * cos2theta * p0 * self._ssarea
#        print(td,f) # for debug
        acc = nv * (f / self._pmass)
        return common.sodv2ecldv(acc, pos, vel, sunpos, sunvel)

    def _epacc(self, td, y, kernel):
        # comupte acceleration of Electric Propulsion System
        acc = np.array([self._epdv * np.cos(self._epelv) * np.cos(self._epphi), \
            self._epdv * np.cos(self._epelv) * np.sin(self._epphi),  \
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
            yd[3:6] += self._epacc(td, y, kernel)
        if self._sson:
            yd[3:6] += self._ssacc(td, y, kernel)
        return yd
    
    def __init__(self, pname, pmass):
        self._pname = pname
        self._pmass = pmass # mass of probe (kg)
        self.statusinitialize()
  
    def statusinitialize(self):      
        self._epon = False
        self._epdv = 0.0    # 電気推進の加速度絶対値
        self._epphi = 0.0   # 電気推進の推力方向φ
        self._epelv = 0.0   # 電気推進の推力方向elevation
        
        self._sson = False
        self._ssarea = 0.0      # ソーラーセイルの面積
        self._sstheta = 0.0     #　ソーラーセイルの向きθ
        self._sselv = 0.0       # ソーラーセイルの向きelevation

    def set_epstatus(self, epon, epdv, epphi, epelv):
        self._epon = epon
        self._epdv = epdv
        self._epphi = epphi
        self._epelv = epelv
    
    def set_ssstatus(self, sson, ssarea, sstheta, sselv):
        self._sson = sson
        self._ssarea = ssarea
        self._sstheta = sstheta
        self._sselv = sselv

    def setCurrentCart(self, t, pos, vel):
        self._t0 = t
        self._y0 = np.zeros(6)
        self._y0[0:3] = pos
        self._y0[3:6] = vel
        
    def trj(self, endsec, inter, kernel, body_f, body_mu, atol, rtol):
        runerror = False
        ninter = int((endsec - self._t0) / inter)
        if (self._t0 + ninter * inter) < endsec:
            ndata = ninter + 2
            remainder = True
        else:
            ndata = ninter + 1
            remainder = False
        r = ode(self._func).set_integrator('dopri5', atol=atol, rtol=rtol)
        r.set_initial_value(self._y0, self._t0).set_f_params(kernel, body_f, \
            body_mu)
        t = np.zeros(ndata); t[0] = self._t0
        x = np.zeros(ndata); x[0] = self._y0[0]
        y = np.zeros(ndata); y[0] = self._y0[1]
        z = np.zeros(ndata); z[0] = self._y0[2]
        xd = np.zeros(ndata); xd[0] = self._y0[3]
        yd = np.zeros(ndata); yd[0] = self._y0[4]
        zd = np.zeros(ndata); zd[0] = self._y0[5]
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
        return t, x, y, z, xd, yd, zd, runerror

def main(kernel):

    t = 2456800.5
    id = 3
    pn = id
    pos, vel = kernel[0,pn].compute_and_differentiate(t)
# 地球ー月の重心に探査機を置く
    pos = common.eqn2ecl(pos)
    vel = common.eqn2ecl(vel) / common.secofday
    print(t, pos, vel, '\n')
    
    probe = ProbeOrbit('MyP')
    probe.setCurrentCart(t*common.secofday, pos*1000.0, vel*1000.0)
    body_f = [True, True, False, True, True, # Mer. Ven. EMB Mars Jup.
              True, True, True, True, True,  # Sat. Ura. Nep. Plu. Sun
              False, False]                    # Moon Earth
    atol = [0.01, 0.01, 0.01, 0.00001, 0.00001, 0.00001]
    rtol = [1e-10,1e-10,1e-10,1e-10,1e-10,1e-10]
    pt, px, py, pz, pxd, pyd, pzd = probe.trj((t+365.00)*common.secofday, 366, \
        kernel, body_f, common.planets_mu, atol, rtol)
    
    for i in range(13):
        icheck = i * 30
        tp = pt[icheck] / common.secofday
        ppos, pvel = kernel[0,pn].compute_and_differentiate(tp)
        ppos = common.eqn2ecl(ppos) * 1000.0
        pvel = pvel / common.secofday
        pvel = common.eqn2ecl(pvel) * 1000.0
        print(tp, ppos[0]-px[icheck], ppos[1]-py[icheck], ppos[2]-pz[icheck])
    
if __name__ == '__main__' :
    main(common.SPKkernel)    
    
        
        
        
        
        
        
        
        


        
        
