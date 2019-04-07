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
    def __init__(self, parent=None, desctext='', attribute=''):
        super().__init__(parent)
        g.saveddescription = desctext
        
        flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)
        
        left = g.mainform.geometry().left()
        top = g.mainform.geometry().top()
        self.setGeometry(left+650, top+705, 600, 246)
        self.ui = Ui_DescriptionEditor()
        self.ui.setupUi(self)
        
        self.ui.description.undoAvailable.connect(self.undoavailable)
        self.ui.description.redoAvailable.connect(self.redoavailable)
        self.ui.finishButton.clicked.connect(self.finish_clicked)
        self.ui.cancelButton.clicked.connect(self.reject)
        
        self.setWindowTitle(self.windowTitle() + '    ' + attribute)
        self.ui.description.setPlainText(desctext)

    def undoavailable(self, available):
        self.ui.undoButton.setEnabled(available)
        
    def redoavailable(self, available):
        self.ui.redoButton.setEnabled(available)
        
    def finish_clicked(self):
        g.saveddescription = self.ui.description.toPlainText()
        self.accept()