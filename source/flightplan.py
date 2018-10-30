# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:07:31 2018

@author: shush_000
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
        QWidget.__init__(self, parent)
        self.ui = Ui_NewFlightPlanDialog()
        self.ui.setupUi(self)
        
        spacebaselist = []
        for baseitem in common.bases:
            spacebaselist.append(baseitem[0])
        self.ui.spacebase.addItems(spacebaselist)
        self.ui.spacebase.setCurrentIndex(1)
        
        for planet_id in common.planets_id:
            if planet_id[1] == 'EMB': continue
            if planet_id[1] == 'Sun': continue
            self.ui.planets.addItem(planet_id[1])
        self.ui.planets.setCurrentIndex(0)
        
#        self.connect(self.ui.planetbutton, SIGNAL('clicked()'), 
#                     self.planetbuttonclicked)
        self.ui.planetbutton.clicked.connect(self.planetbuttonclicked)
#        self.connect(self.ui.smallbodybutton, SIGNAL('clicked()'), 
#                     self.planetbuttonclicked)
        self.ui.smallbodybutton.clicked.connect(self.planetbuttonclicked)
#        self.connect(self.ui.spkfileselect, SIGNAL('clicked()'), 
#                     self.spkfileselectclicked)
        self.ui.spkfileselect.clicked.connect(self.spkfileselectclicked)
#        self.connect(self.ui.okbutton, SIGNAL('clicked()'), self.ok_clicked)
        self.ui.okbutton.clicked.connect(self.ok_clicked)
#        self.connect(self.ui.cancelbutton, SIGNAL('clicked()'), self.reject)
        self.ui.cancelbutton.clicked.connect(self.reject)
            
    def planetbuttonclicked(self):
        if self.ui.planetbutton.isChecked():
            self.ui.planets.setEnabled(True)
            self.ui.targetgroupbox.setEnabled(False)
        if self.ui.smallbodybutton.isChecked():
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            
    def spkfileselectclicked(self):
        ans = QFileDialog.getOpenFileName(parent=self,
            caption='Select SPK file', directory=os.path.join(common.bspdir),
            filter='SPK Files (*.bsp);;All Files (*.*)')
        ans = ans[0]
        if ans == '': return
        filename = os.path.basename(ans)
        filepath = os.path.join(common.bspdir, filename)
        try:
            tempk = SPKType21.open(filepath)
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 
                'SPK file must be stored in "data" folder', QMessageBox.Ok)
            return
        self.ui.spkfilepath.setText(filename)
        
        # Check center of coordinates. it should be 0
        center0 = tempk.segments[0].center
        if center0 != 0:
            mes = 'Invalid SPK file: center is {0}'.format(center0)
            QMessageBox.critical(self, 'Invalid SPK file',
                mes, QMessageBox.Ok)
            tempk.close()
            return
        self.center = center0

        # Check data_type. it should be 1 or 21, and all segments has same type
        datatype0 = tempk.segments[0].data_type
        if datatype0 != 1 and datatype0  != 21:
            mes = 'Invalid SPK file: data_type is {0}'.format(datatype0)
            QMessageBox.critical(self, 'Invalid SPK file',
                mes, QMessageBox.Ok)
            tempk.close()
            return

        for seg in tempk.segments:
            if datatype0 != seg.data_type:
                QMessageBox.critical(self, 'Invalid SPK file',
                    'Invalid SPK file: more than one data type', QMessageBox.Ok)
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
        probe['base'] = self.ui.spacebase.currentText()
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 
                            'Probe mass should be a float number.', QMessageBox.Ok)
            return
        if mass <= 0.0:
            QMessageBox.critical(self, 'Error', 'Invalid Probe mass.', 
                                    QMessageBox.Ok)
            return
        probe['pmass'] = mass
        
        target = {}
        if self.ui.planetbutton.isChecked():
            target['name'] = self.ui.planets.currentText()
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
                QMessageBox.critical(self, 'Error', 
                                    'Enter Target name.', QMessageBox.Ok)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.critical(self, 'Error', 
                    'Click Find button and pecify SPK file of the Target', 
                    QMessageBox.Ok)
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
        index = self.ui.spacebase.findText(probe['base'])
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
            index = self.ui.planets.findText(target['name'])
            self.ui.planets.setCurrentIndex(index)
        
        self.center = target['SPKID1A']

        self.setWindowTitle('Edit Probe Properties')
        self.ui.target_box.setEnabled(False)
        
    def ok_clicked(self):
        probe = {}
        probe['name'] = self.ui.probename.text()
        probe['base'] = self.ui.spacebase.currentText()
        try:
            mass = float(self.ui.probemass.text())
        except ValueError:
            QMessageBox.critical(self, 'Error', 
                            'Probe mass should be a float number.', QMessageBox.Ok)
            return
        if mass <= 0.0:
            QMessageBox.critical(self, 'Error', 'Invalid Probe mass.', 
                                    QMessageBox.Ok)
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
        index = self.ui.spacebase.findText(probe['base'])
        self.ui.spacebase.setCurrentIndex(index)
        
        if target['file'] != '':
            self.ui.planetbutton.setChecked(False)
            self.ui.smallbodybutton.setChecked(True)
            self.ui.planets.setEnabled(False)
            self.ui.targetgroupbox.setEnabled(True)
            self.ui.targetname.setText(target['name'])
            self.ui.spkfilepath.setText(target['file'])

            temppath = target['file']
            if temppath != '':
                try:
                    tempk = SPKType21.open(temppath)
                except FileNotFoundError:
                    try:
                        fname = os.path.basename(temppath)
                        tempk = SPKType21.open(os.path.join(common.bspdir, fname))
                    except FileNotFoundError:
                        QMessageBox.critical(self, 'File not Found',
                            "Target's SPK file {0} is not found.  Store it in 'data' folder".format(fname),
                            QMessageBox.Ok)
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
            index = self.ui.planets.findText(target['name'])
            self.ui.planets.setCurrentIndex(index)
        
        self.center = target['SPKID1A']

        self.setWindowTitle('Select New Target')
        self.ui.probe_box.setEnabled(False)
        
    def ok_clicked(self):
        target = {}
        if self.ui.planetbutton.isChecked():
            target['name'] = self.ui.planets.currentText()
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
                QMessageBox.critical(self, 'Error', 
                                    'Enter Target name.', QMessageBox.Ok)
                return
            target['file'] = self.ui.spkfilepath.text()
            if target['file'].strip() == '':
                QMessageBox.critical(self, 'Error', 
                    'Click Find button and pecify SPK file of the Target', 
                    QMessageBox.Ok)
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
        
