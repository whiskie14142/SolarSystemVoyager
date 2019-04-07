# -*- coding: utf-8 -*-
"""
mandescription module for SSVG (Solar System Voyager)
(c) 2019 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from editmandesc import EditManDesc

from globaldata import g
#     g : container of global data

from ui.maneuverdescription import *

class ManDescription(QDialog):
    """class for 'Description Editor' window
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mother = parent
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left+650, top+740, 600, 211)
        self.ui = Ui_ManeuverDescription()
        self.ui.setupUi(self)

        self.ui.editButton.clicked.connect(self.editDesc)
        
        self._translate = QtCore.QCoreApplication.translate
        self.manDescAttrib = self._translate('mandescription.py', 'Line {0},  {1}')
        self.descKey = 'description_' + g.i_languagecode

        
    def closeEvent(self, event):
        g.maneuverdescription = None
        event.accept()
        
    def showText(self, currentrow):
        self.currentrow = currentrow
        if len(g.maneuvers) <= self.currentrow:
            self.man = None
        else:
            self.man = g.maneuvers[self.currentrow]

        if self.man is None:
            self.desctext = ''
            self.ui.editButton.setEnabled(False)
            self.attribute = self.manDescAttrib.format(self.currentrow+1, '')
        else:
            self.ui.editButton.setEnabled(True)
            self.attribute = self.manDescAttrib.format(self.currentrow+1,
                             self.man['type'])
            if self.descKey in self.man:
                self.desctext = self.man[self.descKey]
            else:
                self.desctext = ''
            
        self.ui.type_and_line.setText(self.attribute)
        self.ui.description.setPlainText(self.desctext)

    def editDesc(self):
        editor = EditManDesc(self, desctext=self.desctext, attribute=self.attribute)
        ans =editor.exec_()
        if ans == QDialog.Rejected:
            return
        
        self.man[self.descKey] = g.saveddescription
        g.manplan_saved = False
        self.mother.dispmanfilename()
        self.showText(self.currentrow)
        
        