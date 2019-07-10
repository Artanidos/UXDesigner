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

from PyQt5.QtWidgets import QGraphicsItem, QStyle
from PyQt5.QtGui import QColor, QBrush, QPen
from designitem import DesignItem


class Ellipse(DesignItem):
    def __init__(self, scene):
        super(Ellipse, self).__init__(scene)
        self.setRect(0, 0, 0, 0)
        self.pen = QPen()
        self.brush = QBrush()

    def typeName(self):
        return "Ellipse"

    def paint(self, paint, option, widget):
        paint.setPen(self.pen)
        paint.setBrush(self.brush)
        paint.drawEllipse(self.rect)
        
        if option.state & QStyle.State_Selected:
            self.drawHighlightSelected(paint, option)
