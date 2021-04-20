# -*- coding: utf-8 -*-
"""
common module for SSVG (Solar System Voyager)
(c) 2016-2019 Shushi Uetsuki (whiskie14142)
"""

import numpy as np
import math
import sys
import os
import json

# get configuration params
configfile = open('SSVGconfig.json', 'r')
config = json.load(configfile)
configfile.close()
planetsSPK = config['system']['planetsSPK']     # name of the SPK file for planets
projection = config['system']['3Dproj']         # proj. type of the 3D orbit window
print('current configuration:')
print('  file name of the SPK file for planets = ', planetsSPK)
print('  projection type of 3D figures = ', projection)

solarmu = 1.32712440041e20      # solar gravitational constant
solark1 = 3.85e26               # total solar flux
c = 2.99792458e8                # velocity of light
au = 1.495978707e11             # meters of an astronomical unit
_eclinc = math.radians(8.4381406e4 / 3600.0)    # ecliptic inc. of J2000.0
secofday = 86400.0     # seconds of a day

planets_mu = (  # source: ftp://ssd.jpl.nasa.gov/pub/xfr/gm_Horizons.pck
                2.2031868551400003e13,  # Mercury
                3.2485859200000000e14,  # Venus
                4.0350323562548019e14,  # Earth + Moon
                4.2828375815756102e13,  # Mars
                1.2671276409999998e17,  # Jupiter
                3.7940584841799997e16,  # Saturn
                5.7945563999999985e15,  # Uranus
                6.8365271005803989e15,  # Neptune
                9.7550000000000000e11,  # Pluto
                1.3271244004127942e20,  # Sun
                4.9028001184575496e12,  # Moon
                3.9860043550702266e14   # Earth
             )

solarmu = planets_mu[9]                    # solar gravitational constant

# SPKIDs for planets (objects in the planetsSPK file)
planets_id = (  (1, 'Mercury'),
                (2, 'Venus'),
                (3, 'EMB'),
                (4, 'Mars'),
                (5, 'Jupiter'),
                (6, 'Saturn'),
                (7, 'Uranus'),
                (8, 'Neptune'),
                (9, 'Pluto'),
                (10, 'Sun'),
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
bspdir = 'SSVG_data'
logdir = 'SSVG_log'
plandir = 'SSVG_plan'
i18ndir = 'SSVG_i18n'

# minimum flight time (days)
minft = 1.0

# SPK kernel
from jplephem.spk import SPK
try:
    SPKkernel = SPK.open(os.path.join(bspdir, planetsSPK))
except FileNotFoundError:
    print("\n  Cannot open the SPK file '{0}'".format(planetsSPK))
    print("  Please consult 'Install SSVG' section of the Users Guide")
    print("")
    print("  SPKファイル '{0}'を開くことができません".format(planetsSPK))
    print("  ユーザーズガイドの 'インストール' の項を参照してください")
    print("")
    print("Type Enter to exit")
    print("Enterキーで終了します")
    input("")
    sys.exit()

# Start time of SPKkernel (inclusive)
SPKstart = 2287184.50

# end time of SPKkernel (inclusive)
SPKend = 2688976.50


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
    return isot[:-2]

def isot2jd(isot):
    # convert ISOT (str) to Julian Day
    dt = datetime.fromisoformat(isot + '00')
    return julian.to_jd(dt)
    
def jd2datetime(jd):
    # convert Julian Day to Date(str) and Time(str)
    dt = julian.from_jd(jd, fmt='jd')
    d_and_t = dt.isoformat(sep='T').split('T')
    if dt.microsecond == 0:
        d_and_t[1] = d_and_t[1] + '.000000'
    return d_and_t[0], d_and_t[1][:-2]

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
