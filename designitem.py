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
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with UXDesigner.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PyQt5.QtCore import QObject, QRectF, Qt
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QColor, QPen 


class DesignItem(QGraphicsItem, QObject):
    def __init__(self, scene, is_scene_rect):
        QGraphicsItem.__init__(self)
        QObject.__init__(self)
        self.scene = scene
        self.is_scene_rect = is_scene_rect
        self.id = ""
        self.hasHandles = False
        self.handles = []
    
    def setId(self ,id):
        self.id = id

    def setRect(self, x, y, w, h):
        self.rect = QRectF(x, y, w, h)

    def setWidth(self, value):
        self.rect.setWidth(value)

    def setHeight(self, value):
        self.rect.setHeight(value)

    def width(self):
        return self.rect.width()

    def height(self):
        return self.rect.height()

    def boundingRect(self):
        return self.rect

    def isSceneRect(self):
        return self.is_scene_rect

    def drawHighlightSelected(self, painter, option):
        itemPenWidth = self.pen.widthF()
        pad = itemPenWidth / 2
        penWidth = 0
        fgcolor = option.palette.windowText().color()
        if fgcolor.red() > 127:
            r = 0 
        else:
            r = 255
        if fgcolor.green() > 127:
            g =  0
        else:
            g = 255
        if fgcolor.blue()  > 127:
            b = 0
        else: 
            b = 255
        bgcolor = QColor(r, g, b)

        painter.setOpacity(1.0)
        painter.setPen(QPen(bgcolor, penWidth, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.boundingRect().adjusted(pad, pad, -pad, -pad))

        painter.setPen(QPen(option.palette.windowText(), 0, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.boundingRect().adjusted(pad, pad, -pad, -pad))

    def setHandlePositions(self):
        if not self.hasHandles:
            return

        halfwidth = self.handles[0].width() / 2.0
        self.handles[0].setPos(-halfwidth, -halfwidth)
        self.handles[1].setPos(rect().width() - halfwidth, -halfwidth)
        self.handles[2].setPos(rect().width() - halfwidth, rect().height() - halfwidth)
        self.handles[3].setPos(-halfwidth, rect().height() - halfwidth)
        self.handles[4].setPos(rect().width() / 2 - halfwidth, -halfwidth)
        self.handles[5].setPos(rect().width() - halfwidth, rect().height() / 2 - halfwidth)
        self.handles[6].setPos(rect().width() /2 - halfwidth, rect().height() - halfwidth)
        self.handles[7].setPos(- halfwidth, rect().height() / 2 - halfwidth)

        self.scene.update(x() - halfwidth - 5, y() - halfwidth - 5, x() + rect().width() + halfwidth * 2 + 5, y() + rect().height() + halfwidth * 2 + 5)
