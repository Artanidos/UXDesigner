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
from PyQt5.QtGui import QColor, QBrush, QPen, QTransform
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from designitem import DesignItem


class Vectorgraphic(DesignItem):
    def __init__(self, filename, scene):
        super(Vectorgraphic, self).__init__(scene)
        self.renderer = QSvgRenderer()
        self.renderer.load(filename)
        self.svg = QGraphicsSvgItem(self)
        self.svg.setSharedRenderer(self.renderer)
        self.setRect(0, 0, self.svg.boundingRect().width(), self.svg.boundingRect().height())

    def typeName(self):
        return "Vectorgraphic"

    def paint(self, paint, option, widget):
        if option.state & QStyle.State_Selected:
            self.drawHighlightSelected(paint, option)

    def scaleObjects(self):
        self.xscale = self.rect.width() / self.svg.boundingRect().width()
        self.yscale = self.rect.height() / self.svg.boundingRect().height()
        trans = QTransform()
        trans.scale(self.xscale, self.yscale)
        self.svg.setTransform(trans)

    def setScale(self, x, y):
        self.xscale = x
        self.yscale = y
        trans = QTransform()
        trans.scale(self.xscale, self.yscale)
        self.svg.setTransform(trans)
        self.setRect(0, 0, self.svg.boundingRect().width() * x, self.svg.boundingRect().height() * y)
