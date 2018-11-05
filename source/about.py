# -*- coding: utf-8 -*-
"""
about module for SSVG (Solar System Voyager)
(c) 2016-2018 Shushi Uetsuki (whiskie14142)
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.aboutSSVG import *

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



class AboutSSVG(QDialog):
    """class for 'About SSVG' dialog
    """
    def __init__(self, parent=None):
        super().__init__(parent)
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
    Copyright (c) 2005-2018, NumPy Developers.
    All rights reserved.
  Scipy : http://scipy.org/
    Copyright (c) 2001, 2002 Enthought, Inc.
    All rights reserved.
    Copyright (c) 2003-2013 SciPy Developers.
    All rights reserved.
  matplotlib : http://matplotlib.org/
    Copyright (c) 2012-2013 Matplotlib Development Team;
    All Rights Reserved
  PyQt5 : https://www.riverbankcomputing.com/software/pyqt/intro
  jplephem : https://github.com/brandon-rhodes/python-jplephem/
  julian : https://github.com/dannyzed/julian/
    Copyright (c) 2016 Daniel Zawada
  pytwobodyorbit : https://github.com/whiskie14142/pytwobodyorbit/
    Copyright (c) 2016 Shushi Uetsuki (whiskie14142)
  spktype01 : https://github.com/whiskie14142/spktype01/
    Copyright (c) 2016-2018 Shushi Uetsuki (whiskie14142)
  spktype21 : https://github.com/whiskie14142/spktype21
    Copyright (c) 2018 Shushi Uetsuki (whiskie14142)
  PyInstaller : http://www.pyinstaller.org/"""

        self.ui.versionlabel.setText(g.version)        
        self.ui.licensetext.setPlainText(abouttext)
        self.ui.okButton.clicked.connect(self.accept)
                
