# -*- coding: utf-8 -*-
"""
editmandesc module for SSVG (Solar System Voyager)
(c) 2019 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from globaldata import g
#     g : container of global data

from ui.descriptioneditor import *

class EditManDesc(QDialog):
    """class for 'Description Editor' window
    """
    def __init__(self, parent=None, desctext=''):
        super().__init__(parent)
        self.mother = parent
        g.saveddescription = desctext
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left+650, top+740, 600, 211)
        self.ui = Ui_DescriptionEditor()
        self.ui.setupUi(self)
        
        self.ui.description.undoAvailable.connect(self.undoavailable)
        self.ui.description.redoAvailable.connect(self.redoavailable)
        
        self.ui.description.setPlainText(desctext)

    def closeEvent(self, event):
        g.descriptioneditor = None
        g.saveddescription = self.ui.description.toPlainText()
        event.accept()

    def undoavailable(self, available):
        self.ui.undoButton.setEnabled(available)
        
    def redoavailable(self, available):
        self.ui.redoButton.setEnabled(available)
        
    def getText(self):
        return self.ui.description.toPlainText()