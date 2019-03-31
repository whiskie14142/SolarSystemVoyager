# -*- coding: utf-8 -*-
"""
flightplan module for SSVG (Solar System Voyager)
(c) 2016-2019 Shushi Uetsuki (whiskie14142)
"""

import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import common
from spktype21 import SPKType21

from globaldata import *
# Import followings
#     g : container of global data
#     erase_Ptrj()
#     draw_Ptrj()
#     erase_PKepler()
#     draw_PKepler()
#     erase_TKepler()
#     draw_TKepler()
#     remove_planets()
#     replot_planets(jd)
#     remove_time()
#     replot_time(jd, ttype='')
#     nowtimestr()
#     nowtimestrf()

from ui.newflightplandialog import *

class NewFlightPlanDialog(QDialog):
    """class for 'New Flight Plan' dialog
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        self.ui = Ui_NewFlightPlanDialog()
        self.ui.setupUi(self)
        
        self.ui.spacebase.addItems(g.i_spacebases)
        self.ui.spacebase.setCurrentIndex(1)
        
        for planet in g.i_planetnames:
            self.ui.planets.addItem(planet[0])
        self.ui.planets.setCurrentIndex(2)
        
        self.ui.planetbutton.clicked.connect(self.planetbuttonclicked)
        self.ui.smallbodybutton.clicked.connect(self.planetbuttonclicked)
        self.ui.spkfileselect.clicked.connect(self.spkfileselectclicked)
        self.ui.okbutton.clicked.connect(self.ok_clicked)
        self.ui.cancelbutton.clicked.connect(self.reject)

        self._translate = QtCore.QCoreApplication.translate
        
        self.winTtl_SPK = self._translate('flightplan.py', 'Select SPK file')
        self.winTtl_EP = self._translate('flightplan.py', 'Edit Probe Properties')
        self.winTtl_ET = self._translate('flightplan.py', 'Select New Target')
        self.mbTtl01 = self._translate('flightplan.py', 'Invalid SPK file')
        self.mbMes01 = self._translate('flightplan.py', 'Invalid file format: the file is not an SPK file')
        self.mbMes02 = 'Invalid SPK file: center is {0}, which should be zero'          # No translation is required
        self.mbMes03 = 'Invalid SPK file: data type is {0}, which should be 1 or 21'    # No translation is required
        self.mbMes04 = self._translate('flightplan.py', 'Invalid SPK file: the file contains more than one data type')
        self.mbTtl05 = self._translate('flightplan.py', 'Input Error')
        self.mbMes05 = self._translate('flightplan.py', 'Probe mass should be a float number.')
        self.mbMes06 = self._translate('flightplan.py', 'Invalid Probe mass')
        self.mbMes07 = self._translate('flightplan.py', 'No Taget name is specified. \nEnter Target name')
        self.mbMes08 = self._translate('flightplan.py', 'No SPK file is specified. \nClick Find button and specify SPK file of the Target')
        self.mbTtl09 = 'SPK File not Found'     # No translation is required
        self.mbMes09 = "Target's SPK file {0} is not found.  Store it in 'SSVG_data' folder" # No translation is required
            
    def planetbuttonclicked(self):
        if self.ui.planetbutton.isChecked():
            self.ui.planets.setEnabled(True)
            self.ui.targetgroupbox.setEnabled(False)
        if self.ui.smallbodybutton.isChecked():
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            
    def spkfileselectclicked(self):
        ans = QFileDialog.getOpenFileName(parent=self,
            caption=self.winTtl_SPK, directory=os.path.join(common.bspdir),
            filter='SPK Files (*.bsp);;All Files (*.*)')
        ans = ans[0]
        if ans == '': return
        try:
            filename = os.path.relpath(ans, start=common.bspdir)
        except ValueError:
            filename = ans
            filepath = ans
        else:
            filepath = os.path.join(common.bspdir, filename)
            
        try:
            tempk = SPKType21.open(filepath)
        except ValueError:
            QMessageBox.critical(self, self.mbTtl01, self.mbMes01, QMessageBox.Ok)
            return
        self.ui.spkfilepath.setText(filename)
        self.ui.targetname.setText(os.path.splitext(os.path.basename(filename))[0])
        
        # Check center of coordinates. it should be 0
        center0 = tempk.segments[0].center
        if center0 != 0:
            mes = self.mbMes02.format(center0)
            QMessageBox.critical(self, self.mbTtl01, mes, QMessageBox.Ok)
            tempk.close()
            return
        self.center = center0

        # Check data_type. it should be 1 or 21, and all segments has same type
        datatype0 = tempk.segments[0].data_type
        if datatype0 != 1 and datatype0  != 21:
            mes = self.mbMes03.format(datatype0)
            QMessageBox.critical(self, self.mbTtl01, mes, QMessageBox.Ok)
            tempk.close()
            return

        for seg in tempk.segments:
            if datatype0 != seg.data_type:
                QMessageBox.critical(self, self.mbTtl01, self.mbMes04, QMessageBox.Ok)
                tempk.close()
                return
        g.data_type = datatype0
        # Prepare the combo-box of SPKID
        # idlist is a list of [SPKID]
        idlist = [tempk.segments[0].target]
        for seg in tempk.segments:
            found = False
            for i in range(len(idlist)):
                if idlist[i] == seg.target:
                    found = True
                    break
            if not found:
                idlist.append(seg.target)
        idlist.sort()
        combo = self.ui.spkid_list
        combo.clear()
        for spkid in idlist:
            combo.addItem(str(spkid))
        combo.setCurrentIndex(0)
        
        tempk.close()

    def ok_clicked(self):
        newplan = {}
        
        probe = {}
        probe['name'] = self.ui.probename.text()
        ix = self.ui.spacebase.currentIndex()
        probe['base'] = common.bases[ix][0]
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.critical(self, self.mbTtl05, self.mbMes05, QMessageBox.Ok)
            return
        if mass <= 0.0:
            QMessageBox.critical(self, self.mbTtl05, self.mbMes06, QMessageBox.Ok)
            return
        probe['pmass'] = mass
        
        target = {}
        if self.ui.planetbutton.isChecked():
            ix = self.ui.planets.currentIndex()
            target['name'] = common.planets_id[g.i_planetnames[ix][1]][1]
            target['file'] = ''
            target['SPKID1A'] = 0
            g.data_type = 0
            for planet in common.planets_id:
                if planet[1] != target['name']: continue
                if planet[1] == 'Moon' or planet[1] == 'Earth':
                    target['SPKID1B'] = 3
                    target['SPKID2A'] = 3
                    target['SPKID2B'] = planet[0]
                else:
                    target['SPKID1B'] = planet[0]
                    target['SPKID2A'] = 0
                    target['SPKID2B'] = 0
        if self.ui.smallbodybutton.isChecked():
            target['name'] = self.ui.targetname.text()
            if target['name'].strip() == '':
                QMessageBox.critical(self, self.mbTtl05, self.mbMes07, QMessageBox.Ok)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.critical(self, self.mbTtl05, self.mbMes08, QMessageBox.Ok)
                return
#
#       From May 2017, NASA-JPL HORIZONS produces barycentric SPK files 
#       for small bodies
#
            target['SPKID1A'] = self.center
            target['SPKID2A'] = 0
            target['SPKID2B'] = 0
            target['SPKID1B'] = int(self.ui.spkid_list.currentText())
            
        newplan['probe'] = probe
        newplan['target'] = target
        newplan['maneuvers'] = []
        g.manplan = newplan
        self.accept()



class EditProbeDialog(NewFlightPlanDialog):
    """class for the dialog to edit probe information of a flight plan
    """

    def __init__(self, parent=None, manplan=None):
        super().__init__(parent)
        self.manplan = manplan
        probe = self.manplan['probe']
        target = self.manplan['target']
        self.ui.probename.setText(probe['name'])
        self.ui.probemass.setText('{:.3f}'.format(probe['pmass']))
        for ix in range(16):
            if common.bases[ix][0] == probe['base']:
                index = ix
                break
        self.ui.spacebase.setCurrentIndex(index)
        
        if target['file'] != '':
            self.ui.planetbutton.setChecked(False)
            self.ui.smallbodybutton.setChecked(True)
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            self.ui.targetname.setText(target['name'])
            
            
            self.ui.spkfilepath.setText(target['file'])
            combo = self.ui.spkid_list
            combo.clear()
            combo.addItem(str(target['SPKID1B']))
            combo.setCurrentIndex(0)
        else:
            for ix in range(12):
                if target['name'] == common.planets_id[ix][1]:
                    for iy in range(10):
                        if g.i_planetnames[iy][1] == ix:
                            index = iy
                            break
                    break
            self.ui.planets.setCurrentIndex(index)
        
        self.center = target['SPKID1A']

        self.setWindowTitle(self.winTtl_EP)
        self.ui.target_box.setEnabled(False)
        
    def ok_clicked(self):
        probe = {}
        probe['name'] = self.ui.probename.text()
        index = self.ui.spacebase.currentIndex()
        probe['base'] = common.bases[index][0]
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.critical(self, self.mbTtl05, self.mbMes05, QMessageBox.Ok)
            return
        if mass <= 0.0:
            QMessageBox.critical(self, self.mbTtl05, self.mbMes06, QMessageBox.Ok)
            return
        probe['pmass'] = mass
        
        self.manplan['probe'] = probe
        self.accept()
    
        
class EditTargetDialog(NewFlightPlanDialog):
    """class for the dialog to edit target information of the flight plan
    """
    def __init__(self, parent=None, manplan=None):
        super().__init__(parent)
        self.manplan = manplan
        probe = self.manplan['probe']
        target = self.manplan['target']
        self.ui.probename.setText(probe['name'])
        self.ui.probemass.setText('{:.3f}'.format(probe['pmass']))
        for ix in range(16):
            if common.bases[ix][0] == probe['base']:
                index = ix
                break
        self.ui.spacebase.setCurrentIndex(index)
        
        if target['file'] != '':
            self.ui.planetbutton.setChecked(False)
            self.ui.smallbodybutton.setChecked(True)
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            self.ui.targetname.setText(target['name'])
            self.ui.spkfilepath.setText(target['file'])

            temppath = target['file']
            fname = os.path.basename(temppath)
            if temppath != '':
                if os.path.isabs(temppath):
                    try:
                        tempk = SPKType21.open(temppath)
                    except FileNotFoundError:
                        try:
                            tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                        except FileNotFoundError:
                            QMessageBox.critical(self, self.mbTtl09, 
                                self.mbMes09.format(fname), QMessageBox.Ok)
                            return
                else:
                    temppath = os.path.join(common.bspdir, temppath)
                    try:
                        tempk = SPKType21.open(temppath)
                    except FileNotFoundError:
                        try:
                            tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                        except FileNotFoundError:
                            QMessageBox.critical(self, self.mbTtl09, 
                                self.mbMes09.format(fname), QMessageBox.Ok)
                            return

                idlist = [tempk.segments[0].target]
                for seg in tempk.segments:
                    found = False
                    for i in range(len(idlist)):
                        if idlist[i] == seg.target:
                            found = True
                            break
                    if not found:
                        idlist.append(seg.target)
                idlist.sort()
                combo = self.ui.spkid_list
                combo.clear()
                for spkid in idlist:
                    combo.addItem(str(spkid))
                index = combo.findText(str(target['SPKID1B']))
                combo.setCurrentIndex(index)
                tempk.close()
        else:
            for ix in range(12):
                if target['name'] == common.planets_id[ix][1]:
                    for iy in range(10):
                        if g.i_planetnames[iy][1] == ix:
                            index = iy
                            break
                    break
            self.ui.planets.setCurrentIndex(index)
        
        self.center = target['SPKID1A']

        self.setWindowTitle(self.winTtl_ET)
        self.ui.probe_box.setEnabled(False)
        
    def ok_clicked(self):
        target = {}
        if self.ui.planetbutton.isChecked():
            ix = self.ui.planets.currentIndex()
            target['name'] = common.planets_id[g.i_planetnames[ix][1]][1]
            target['file'] = ''
            target['SPKID1A'] = 0
            g.data_type = 0
            for planet in common.planets_id:
                if planet[1] != target['name']: continue
                if planet[1] == 'Moon' or planet[1] == 'Earth':
                    target['SPKID1B'] = 3
                    target['SPKID2A'] = 3
                    target['SPKID2B'] = planet[0]
                else:
                    target['SPKID1B'] = planet[0]
                    target['SPKID2A'] = 0
                    target['SPKID2B'] = 0
        if self.ui.smallbodybutton.isChecked():
            target['name'] = self.ui.targetname.text()
            if target['name'].strip() == '':
                QMessageBox.critical(self, self.mbTtl05, self.mbMes07, QMessageBox.Ok)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.critical(self, self.mbTtl05, self.mbMes08, QMessageBox.Ok)
                return
#
#       From May 2017, NASA-JPL HORIZONS produces barycentric SPK files 
#       for small bodies
#
            target['SPKID1A'] = self.center
            target['SPKID2A'] = 0
            target['SPKID2B'] = 0
            target['SPKID1B'] = int(self.ui.spkid_list.currentText())
            
        self.manplan['target'] = target
        self.accept()
        
