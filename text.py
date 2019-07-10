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
from PyQt5.QtGui import QColor, QBrush, QPen, QTransform, QFont, QFontMetrics
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from designitem import DesignItem


class Text(DesignItem):
    def __init__(self, text, scene):
        super(Text, self).__init__(scene)
        self.font = QFont("Arial")
        self.font.setPointSize(14)
        self.font.setStyleName("Standard")
        self.text = text
        self.textcolor = QColor(Qt.black)

        self.data = str.encode(self.getSvg())
        self.renderer = QSvgRenderer()
        self.renderer.load(self.data)
        self.svg = QGraphicsSvgItem(self)
        self.svg.setSharedRenderer(self.renderer)
        self.setRect(0, 0, self.svg.boundingRect().width(), self.svg.boundingRect().height())

    def typeName(self):
        return "Text"

    def paint(self, paint, option, widget):      
        if option.state & QStyle.State_Selected:
            self.drawHighlightSelected(paint, option)

    def getTextTag(self, id):
        fm = QFontMetrics(self.font)
        svg = "<text "
        if id:
            svg += "id=\"" + id + "\" "
        svg += "x=\"0\" y=\"" + str(fm.ascent()) + "\" "
        svg += "font-family=\"" + self.font.family() + "\" "
        svg += "font-size=\"" + str(self.font.pointSize() * 1.25) + "px\" "
        if self.font.bold():
            svg += "font-weight=\"bold\" "
        if self.font.italic():
            svg += "font-style=\"italic\" "
        svg += "fill=\"" + self.textcolor.name() + "\" "
        svg += "opacity=\"" + str(self.opacity()) + "\" "
        svg += ">"
        svg += self.text
        svg += "</text>"
        return svg
        
    def getSvg(self):
        font = QFont(self.font.family())
        font.setBold(self.font.bold())
        font.setItalic(self.font.italic())
        font.setPixelSize(self.font.pointSize() * 1.25)
        fm = QFontMetrics(font)
        self.width = fm.width(self.text) + 2
        self.height = fm.height()

        svg = "<svg width=\"" + str(self.width) + "\" "
        svg += "height=\"" + str(self.height) + "\" >"
        svg += self.getTextTag("")
        svg += "</svg>"
        return svg

    def setScale(self, x, y):
        self.xscale = x
        self.yscale = y
        trans = QTransform()
        trans.scale(self.xscale, self.yscale)
        self.svg.setTransform(trans)
        self.setRect(0, 0, self.svg.boundingRect().width() * x, self.svg.boundingRect().height() * y)

    def scaleObjects(self):
        self.xscale = self.rect.width() / self.svg.boundingRect().width()
        self.yscale = self.rect.height() / self.svg.boundingRect().height()
        trans = QTransform()
        trans.scale(self.xscale, self.yscale)
        self.svg.setTransform(trans)