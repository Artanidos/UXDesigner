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

from PyQt5.QtWidgets import QGraphicsItem


MOUSE_RELEASED = 0
MOUSE_DOWN = 1
MOUSE_MOVING = 2

class ItemHandle(QGraphicsItem):
    def __init__(self, parent, corner, scaling):
        super(Rectangle, self).__init__(parent)
        self.mouseDownX(0),
        self.mouseDownY(0),
        self.color(Qt.black),
        self.pen(Qt.white),
        self.corner(corner),
        self.mouseButtonState(MOUSE_RELEASED)
        self.pen.setWidth(1)
        
        if scaling == 0:
            self.width = 18.0
            self.height = 18.0
        elif scaling == 1:
            self.width = 9.0
            self.height = 9.0
        elif scaling == 2:
            self.width = 4.5
            self.height = 4.5
        elif scaling == 3:
            self.width = 2.25
            self.height = 2.25
        elif scaling == 4:
            self.width = 2.25
            self.height = 2.25
        
        self.setAcceptHoverEvents(True)
        self.setZValue(100)

        if corner == 0 or corner == 2:
            self.setCursor(Qt.SizeFDiagCursor)
        elif corner == 1 or corner == 3:
            self.setCursor(Qt.SizeBDiagCursor)
        elif corner == 4 or corner == 6:
            self.setCursor(Qt.SizeVerCursor)
        elif corner == 5 or corner == 7:
            self.setCursor(Qt.SizeHorCursor)

    def setMouseState(self, s):
        self.mouseButtonState = s
    
    def getMouseState(self):
        return self.mouseButtonState
    
    def getCorner(self):
        return self.corner
    
    def mouseMoveEvent(self, event):
        event.setAccepted(False)
    
    def mouseReleaseEvent(self, event):
        event.setAccepted(True)
    
    def mousePressEvent(self, event):
        event.setAccepted(False)
    
    def hoverLeaveEvent(self, event):
        self.color = Qt.black
        self.update(0, 0, self.width, self.height)
    
    def hoverEnterEvent(self, event):
        self.color = QColor(255, 127, 42)
        self.update(0, 0, self.width, self.height)
    
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        self.pen.setCapStyle(Qt.SquareCap)
        self.pen.setStyle(Qt.SolidLine)
        painter.setPen(self.pen)
        topLeft = QPointF(0, 0)
        bottomRight = QPointF(self.width, self.height)
        rect = QRectF(topLeft, bottomRight)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        painter.drawRect(rect)
        painter.fillRect(rect, brush)
    