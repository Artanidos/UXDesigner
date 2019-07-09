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

from PyQt5.QtWidgets import QGraphicsView, QGridLayout, QWidget
from PyQt5.QtGui import QPalette
from ruler import Ruler

class SceneView(QGraphicsView):
    def __init__(self, scene):
        super(SceneView, self).__init__(scene)
        self.setMouseTracking(True)
        self.setViewportMargins(20, 20, 0, 0)
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        self.horizontalRuler = Ruler(Ruler.Horizontal)
        self.verticalRuler = Ruler(Ruler.Vertical)

        self.corner = QWidget()
        self.corner.setBackgroundRole(QPalette.Window)
        self.corner.setFixedSize(20, 20)
        gridLayout.addWidget(self.corner, 0, 0)
        gridLayout.addWidget(self.horizontalRuler, 0, 1)
        gridLayout.addWidget(self.verticalRuler, 1, 0)
        gridLayout.addWidget(self.viewport(), 1, 1)

        self.setLayout(gridLayout)
