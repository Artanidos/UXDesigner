#############################################################################
# Copyright (C) 2019 Olaf Japp
#
#  This file is part of UXDesigner.
#
#  UXDesigner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  UXDesigner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with UXDesigner.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PyQt5.QtWidgets import QGraphicsItem, QStyle
from PyQt5.QtGui import QColor, QBrush, QPen, QImage
from designitem import DesignItem


class Bitmap(DesignItem):
    def __init__(self, filename, scene):
        super(Bitmap, self).__init__(scene)
        self.image = QImage()
        self.image.load(filename)
        self.setRect(0, 0, self.image.width(), self.image.height())

    def typeName(self):
        return "Bitmap"

    def paint(self, paint, option, widget):
        paint.drawImage(0, 0, self.image.scaled(self.rect.width(), self.rect.height()))
        
        if option.state & QStyle.State_Selected:
            self.drawHighlightSelected(paint, option)
