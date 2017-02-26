# -*- coding: utf-8 -*-
"""
common module for SSVG
(c) 2016-2017 Shushi Uetsuki (whiskie14142)
"""

import numpy as np
import math
import sys

solarmu = 1.32712440041e20      # solar gravitational constant
solark1 = 3.85e26               # total solar flux
c = 2.99792458e8                # velocity of light
au = 1.495978707e11             # meters of an astronomical unit
_eclinc = math.radians(8.4381406e4 / 3600.0)    # ecliptic inc. of J2000.0
secofday = 86400.0     # seconds of a day

planets_mu = (  solarmu * 1.6601e-7,       # Mercury
                solarmu * 2.4478e-6,       # Venus
                3.986004356e14 * 1.012300, # Earth + Moon
                solarmu * 3.2272e-7,       # Mars
                solarmu * 9.5479e-4,       # Jupiter
                solarmu * 2.8589e-4,       # Saturn
                solarmu * 4.3662e-5,       # Uranus
                solarmu * 5.1514e-5,       # Neptune
                3.986004356e14 * 0.00218,  # Pluto
                solarmu,                   # Sun
                solarmu * 3.6943e-8,       # Moon
                3.986004356e14  )          # Earth

# SPKIDs for planets (objects in de430.bsp)
planets_id = (  (1, 'Mercury'),
                (2, 'Venus'),
                (3, 'EMB'),
                (4, 'Mars'),
                (5, 'Jupiter'),
                (6, 'Saturn'),
                (7, 'Uranus'),
                (8, 'Neptune'),
                (9, 'Pluto'),
                (10, 'Sol'),
                (301, 'Moon'),
                (399, 'Earth')  )

# space bases
bases = (
    ('EarthL1', {'SPKID':3, 'Factor':0.98992}), # experimental value
    ('EarthL2', {'SPKID':3, 'Factor':1.01008}), # experimental value
    ('MercuryL1', {'SPKID':1, 'Factor':0.99619}),
    ('MercuryL2', {'SPKID':1, 'Factor':1.00381}),
    ('VenusL1', {'SPKID':2, 'Factor':0.99066}),
    ('VenusL2', {'SPKID':2, 'Factor':1.00934}),
    ('MarsL1', {'SPKID':4, 'Factor':0.99524}),
    ('MarsL2', {'SPKID':4, 'Factor':1.00476}),
    ('JupiterL1', {'SPKID':5, 'Factor':0.93172}),
    ('JupiterL2', {'SPKID':5, 'Factor':1.06828}),
    ('SaturnL1', {'SPKID':6, 'Factor':0.95432}),
    ('SaturnL2', {'SPKID':6, 'Factor':1.04568}),
    ('UranusL1', {'SPKID':7, 'Factor':0.97558}),
    ('UranusL2', {'SPKID':7, 'Factor':1.02442}),
    ('NeptuneL1', {'SPKID':8, 'Factor':0.97420}),
    ('NeptuneL2', {'SPKID':8, 'Factor':1.02580})
        )

# constants for numerical integration
planets_grav = [True, True, False, True, True,  # Mer., Ven., EMB, Mars, Jup.,
              True, True, True, False, True,  # Sat., Ura., Nep., Plu., Sun
              True, True]                       # Moon, Earth
integ_abs_tol = [1.0, 1.0, 1.0, 0.001, 0.001, 0.001]    # absolute tolerance in meter
integ_rel_tol = [1e-10,1e-10,1e-10,1e-10,1e-10,1e-10]   # relative tolerance

# directories
bspdir = './data/'
logdir = './log/'

# SPK kernel
from jplephem.spk import SPK
try:
    SPKkernel = SPK.open( bspdir + 'de430.bsp')
except FileNotFoundError:
    print("\n  Cannot open the SPK file 'de430.bsp'")
    print("  Please consult 'Install SSVG' section of the Users Guide")
    print("")
    print("  SPKファイル 'de430.bsp' を開くことができません")
    print("  ユーザーズガイドの 'インストール' の項を参照してください")
    print("")
    print("Type Enter to exit")
    print("Enterキーで終了します")
    input("")
    sys.exit()

_TX = np.array([[1., 0., 0.,],
                [0., np.cos(_eclinc), np.sin(_eclinc)],
                [0., (-1.)*np.sin(_eclinc), np.cos(_eclinc)]])

def eqn2ecl(eqnxyz):
    # convert equinoctial XYZ to ecliptic XYZ
    return np.dot(_TX, eqnxyz)

def SPKposvel(ID, jd):
    # return position and velocity of planet, Moon, or Sun
    # units are meter, and meter per second
    # coordinate origin is SSB
    if ID <= 10:
        pos, vel = SPKkernel[0, ID].compute_and_differentiate(jd)
    else:
        pos1, vel1 = SPKkernel[0, 3].compute_and_differentiate(jd)
        pos2, vel2 = SPKkernel[3, ID].compute_and_differentiate(jd)
        pos = pos1 + pos2
        vel = vel1 + vel2
    pos = eqn2ecl(pos) * 1000.0
    vel = eqn2ecl(vel) / secofday * 1000.0
    return pos, vel

def ldv2ecldv(ldv, ppos, pvel, sunpos, sunvel):
    # convert local delta-V of probe to equinoctial delta-V
    # local X axis direct sun centered prove velocity
    # local Y axis lies on orbital plane
    norm = lambda x : x / np.sqrt(np.dot(x,x))
    
    ssppos = ppos - sunpos
    sspvel = pvel - sunvel
    p = norm(sspvel)    # unit vector directed to local X
    w = norm(np.cross(ssppos, sspvel))  # unit vector prependicular to orbital plane
    q = np.cross(w, p)  # unit vector directed to local Y
    mx = np.array([p, q, w])
    return np.dot(mx.T, ldv)

def eclv2lv(eclv, ppos, pvel, sunpos, sunvel):
    # convert equinoctial vector to local vetor
    # local X axis direct sun centered prove velocity
    # local Y axis lies on orbital plane
    norm = lambda x : x / np.sqrt(np.dot(x,x))
    
    ssppos = ppos - sunpos
    sspvel = pvel - sunvel
    p = norm(sspvel)    # unit vector directed to local X
    w = norm(np.cross(ssppos, sspvel))  # unit vector prependicular to orbital plane
    q = np.cross(w, p)  # unit vector directed to local Y
    mx = np.array([p, q, w])
    return np.dot(mx, eclv)

def sodv2ecldv(sodv, ppos, pvel, sunpos, sunvel):
    # convert local sun oriented delta-V of probe to equinoctial delta-V
    # local X axis direct probe from sun
    # local Y axis lies on orbital plane
    norm = lambda x : x / np.sqrt(np.dot(x,x))
    
    ssppos = ppos - sunpos
    sspvel = pvel - sunvel
    p = norm(ssppos)    # unit vector directed to local X
    w = norm(np.cross(ssppos, sspvel))  # unit vector prependicular to orbital plane
    q = np.cross(w, p)  # unit vector directed to local Y
    mx = np.array([p, q, w])
    return np.dot(mx.T, sodv)

from datetime import datetime
import julian

def jd2isot(jd):
    # convert Julian Day to ISOT (str)
    dt = julian.from_jd(jd, fmt='jd')
    isot = dt.isoformat(sep='T')
    if dt.microsecond == 0:
        isot = isot + '.000000'
    return isot

def isot2jd(isot):
    # convert ISOT (str) to Julian Day
    d_and_t = isot.split('T')
    ymd = d_and_t[0].split('-')
    hms = d_and_t[1].split(':')
    year = int(ymd[0])
    month = int(ymd[1])
    day = int(ymd[2])
    hour = int(hms[0])
    minute = int(hms[1])
    fsec = float(hms[2])
    second = int(fsec)
    msecond = int((fsec - second) * 1.0e6)
    dt = datetime(year, month, day, hour, minute, second, msecond)
    return julian.to_jd(dt)
    
def jd2datetime(jd):
    # convert Julian Day to Date(str) and Time(str)
    dt = julian.from_jd(jd, fmt='jd')
    d_and_t = dt.isoformat(sep='T').split('T')
    if dt.microsecond == 0:
        d_and_t[1] = d_and_t[1] + '.000000'
    return d_and_t[0], d_and_t[1]

def datetime2jd(sdate, stime):
    # convert Date(str) and Time(str) to Julian Day
    isot = sdate + 'T' + stime
    return isot2jd(isot)


def rect2polar(vect):
    # convert rectangular presentation of the vector to polar coordinate presentation 
    v = np.array(vect)
    r = np.sqrt(np.dot(v, v))
    phi = np.arctan2(v[1], v[0])
    elv = np.arctan(v[2] / np.sqrt(v[0]**2 + v[1]**2))
    phi = math.degrees(phi)
    elv = math.degrees(elv)
    return r, phi, elv
    
def polar2rect(r, phi, elv):
    # convert a polar coordinate presentation of the vector to rectangular presentation
    rphi = math.radians(phi)
    relv = math.radians(elv)
    v = np.zeros(3)
    v[0] = r * np.cos(relv) * np.cos(rphi)
    v[1] = r * np.cos(relv) * np.sin(rphi)
    v[2] = r * np.sin(relv)
    return v

