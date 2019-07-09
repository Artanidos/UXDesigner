#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# This file is part of UXDesigner.
#
#  UXDesigner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  UXDesigner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with UXDesigner.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
    

class Ruler(QWidget):
    Horizontal = 0
    Vertical = 1

    def __init__(self, rulerType, parent=None):
        super(Ruler, self).__init__(parent)

        self.rulerType = rulerType
        self.origin = 0.0
        self.rulerUnit = 1.0
        self.rulerZoom = 1.0
        self.mouseTracking = True
        self.drawText = False

        self.setMouseTracking(True)
        txtFont = QFont("Arial", 7, 20)
        self.setFont(txtFont)
