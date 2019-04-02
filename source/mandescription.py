# -*- coding: utf-8 -*-
"""
mandescription module for SSVG (Solar System Voyager)
(c) 2019 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
        
    def closeEvent(self, event):
        g.maneuverdescription = None
        event.accept()

    def setText(self, desctext):
        return self.ui.description.setPlainText(desctext)
    
    def setAttrib(self, attribText):
        self.ui.type_and_line.setText(attribText)
        