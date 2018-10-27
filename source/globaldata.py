# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 07:26:19 2018

@author: shush_000
"""

from datetime import datetime
import matplotlib.pyplot as plt
import common


class _Gdata:
    """Container of global data
    """
    __slots__ = [
        'version',                  # version no. of this program
        'options',                  # runtime options
        'ax',                       # axes of matplotlib
        'currentdir',               # current directory of application
        'clipboard',                # system clipboard object
        'editedman',                # edited maneuver : output of EditManDialog
        'fig',                      # figure of matplotlib
        'logfile',                  # file object of the SSVG LOG
        'mainform',                 # mainform of this application
        'maneuvers',                # list of maneuvers
        'manfilename',              # file name of maneuver plan
        'manplan',                  # maneuver plan
        'manplan_saved',            # flag for saved or not saved
        'myprobe',                  # instance of space probe
        'mytarget',                 # instance of Target (destination of the probe)
        'ndata',                    # number of points to draw orbit
        'ndata_s',                  # number of points to draw orbit (shortend)
        'nextman',                  # index of next maneuver
        'probe_trj',                # list of probe trajectories of each FLYTO
        'probe_Kepler',             # points of Kepler orbit of probe
        'target_Kepler',            # points of Kepler orbit of target
        'artist_Ptrj',              # list of artists of matplotlib for probe trajectories
        'artist_PKepler',           # artist of matplotlib for probe orbit
        'artist_TKepler',           # artist of matplotlib for target orbit
        'artist_mark_of_planets',   # artist of matplotlib for planet marks
        'artist_name_of_planets',   # artist of matplotlib for planet names
        'artist_of_time',           # artist of matplotlib for time and its type
        'showorbitcontrol',         # instance of ShowOrbitDialog
        'showorbitsettings',        # current settings of ShowOrbitDialog
        'flightreviewcontrol',      # instance of FlightReviewControl
        'reviewthroughoutcontrol',  # instance of ReviewThroughoutControl
        'finish_exec',              # return code of EditManDialog for finish and execute (== 2)
        'fta_parameters'            # return parameters from FTAsettingDialog
        ]
    
# global data container instance    
g = _Gdata()
    
def erase_Ptrj():
    for artist in g.artist_Ptrj:
        artist[0].remove()
    g.artist_Ptrj = []
    
def draw_Ptrj():
    g.artist_Ptrj = []
    for trj in g.probe_trj:
        g.artist_Ptrj.append(g.ax.plot(*trj[2:5], color='blue', lw=0.75))
    
def erase_PKepler():
    if g.artist_PKepler is not None:
        g.artist_PKepler[0].remove()
    g.artist_PKepler = None
    
def draw_PKepler():
    if g.probe_Kepler is not None:
        g.artist_PKepler = g.ax.plot(*g.probe_Kepler, color='red', lw=0.75)
    
def erase_TKepler():
    if g.artist_TKepler is not None:
        g.artist_TKepler[0].remove()
    g.artist_TKepler = None
    
def draw_TKepler():
    if g.target_Kepler is not None:
        g.artist_TKepler = g.ax.plot(*g.target_Kepler, color='green', lw=0.75)

def remove_planets():
    if g.artist_mark_of_planets is not None:
        g.artist_mark_of_planets.remove()
        g.artist_mark_of_planets = None
    for art in g.artist_name_of_planets:
        art.remove()
    g.artist_name_of_planets = []
    
def replot_planets(jd):
    markx = []
    marky = []
    markz = []
    names = []
    id_of_target = g.mytarget.getID()
    id_of_EMB = 3
    id_of_Moon = 301
    id_of_Sun = 10
    
    for i in range(12):
        if common.planets_id[i][0] == id_of_target: continue
        if common.planets_id[i][0] == id_of_EMB: continue
        if common.planets_id[i][0] == id_of_Sun: continue
        pos, vel = common.SPKposvel(common.planets_id[i][0], jd)
        markx.append(pos[0])
        marky.append(pos[1])
        markz.append(pos[2])
        if common.planets_id[i][0] == id_of_Moon:
            names.append('')
        else:
            names.append(common.planets_id[i][1])
    
    g.artist_mark_of_planets = g.ax.scatter(markx, marky, markz, marker='+', 
                                           s=20, c='c', depthshade=False)
    g.artist_name_of_planets = []
    for i in range(len(names)):
        g.artist_name_of_planets.append(g.ax.text(markx[i], marky[i], markz[i],
                                      ' '+names[i], color='c', fontsize=9))

def remove_time():
    if g.artist_of_time is not None:
        g.artist_of_time.remove()
        g.artist_of_time = None

def replot_time(jd, ttype=''):
    s = common.jd2isot(jd) + ' (' + ttype + ')'
    g.artist_of_time = g.ax.text2D(0.02, 0.96, s, transform=g.ax.transAxes)

def nowtimestr():
    # returns "YYYY-MM-DDTHH:MM:SS"
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
def nowtimestrf():
    # returns "YYYYMMDD_HHMMSS" (this string can be used as a file name)
    return datetime.now().strftime('%Y%m%d_%H%M%S')

