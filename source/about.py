# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:17:47 2018

@author: shush_000
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.aboutSSVG import *

# global variables: SSVG sets real instances
g = None



class AboutSSVG(QtGui.QDialog):
    """class for 'About SSVG' dialog
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_aboutSSVG()
        self.ui.setupUi(self)
        abouttext = """SSVG (Solar System Voyager) (c) 2016-2018 Shushi Uetsuki (whiskie14142)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Source code and license terms will be retrieved from:
<https://github.com/whiskie14142/SolarSystemVoyager/>

This program uses following programs and modules:
  Numpy : http://www.numpy.org/
    Copyright (c) 2005-2016, NumPy Developers.
    All rights reserved.
  Scipy : http://scipy.org/
    Copyright (c) 2001, 2002 Enthought, Inc.
    All rights reserved.
    Copyright (c) 2003-2013 SciPy Developers.
    All rights reserved.
  matplotlib : http://matplotlib.org/
    Copyright (c) 2012-2013 Matplotlib Development Team;
    All Rights Reserved
  PyQt4 : https://www.riverbankcomputing.com/news/
  jplephem : https://github.com/brandon-rhodes/python-jplephem/
  julian : https://github.com/dannyzed/julian/
    Copyright (c) 2016 Daniel Zawada
  pytwobodyorbit : https://github.com/whiskie14142/pytwobodyorbit/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  spktype01 : https://github.com/whiskie14142/spktype01/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  PyInstaller : http://www.pyinstaller.org/"""

        self.ui.versionlabel.setText(g.version)        
        self.ui.licensetext.setPlainText(abouttext)
        self.connect(self.ui.okButton, SIGNAL('clicked()'), self.accept)
                
