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

from PyQt5.QtCore import QObject, QRectF, Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QColor, QPen, QGuiApplication, QBrush
from itemhandle import ItemHandle
from command import ScaleItemCommand


class DesignItem(QGraphicsItem, QObject):
    positionChanged = pyqtSignal(int, int)

    def __init__(self, scene, is_scene_rect=False):
        QGraphicsItem.__init__(self)
        QObject.__init__(self)
        self.scene = scene
        self.is_scene_rect = is_scene_rect
        self.id = ""
        self.pen = QPen()
        self.brush = QBrush()
        self.hasHandles = False
        self.handles = [None, None, None, None, None, None, None, None]
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
    
    def setId(self ,id):
        self.id = id

    def setBrush(self, brush):
        self.brush = brush

    def setPen(self, pen):
        self.pen = pen

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

    def scaleObjects(self):
        pass

    def setHandlePositions(self):
        if not self.hasHandles:
            return

        halfwidth = self.handles[0].width / 2.0
        self.handles[0].setPos(-halfwidth, -halfwidth)
        self.handles[1].setPos(self.rect.width() - halfwidth, -halfwidth)
        self.handles[2].setPos(self.rect.width() - halfwidth, self.rect.height() - halfwidth)
        self.handles[3].setPos(-halfwidth, self.rect.height() - halfwidth)
        self.handles[4].setPos(self.rect.width() / 2 - halfwidth, -halfwidth)
        self.handles[5].setPos(self.rect.width() - halfwidth, self.rect.height() / 2 - halfwidth)
        self.handles[6].setPos(self.rect.width() /2 - halfwidth, self.rect.height() - halfwidth)
        self.handles[7].setPos(- halfwidth, self.rect.height() / 2 - halfwidth)

        self.scene.update(self.x() - halfwidth - 5, self.y() - halfwidth - 5, self.x() + self.rect.width() + halfwidth * 2 + 5, self.y() + self.rect.height() + halfwidth * 2 + 5)

    def sceneEventFilter(self, watched, event):
        if isinstance(watched, ItemHandle):
            handle = watched
        else:
            return False
        
        if isinstance(event, QGraphicsSceneMouseEvent):
            mevent = event
        else:
            return False
        

        if mevent.type() == QEvent.GraphicsSceneMousePress:
            self.oldx = self.pos().x()
            self.oldy = self.pos().y()
            self.oldwidth = self.rect.width()
            self.oldheight = self.rect.height()

            handle.setMouseState(ItemHandle.MOUSE_DOWN)
            handle.mouseDownX = mevent.pos().x()
            handle.mouseDownY = mevent.pos().y()
        elif mevent.type() == QEvent.GraphicsSceneMouseRelease:
            if self.oldx  != self.pos().x() and self.oldy != self.pos().y() and self.oldwidth != self.rect.width() and self.oldheight != self.rect.height():
                undostack = self.scene.undostack
                cmd = ScaleItemCommand(self.pos().x(), self.pos().y(), self.rect().width(), self.rect().height(), self.oldx, self.oldy, self.oldwidth, self.oldheight, self.scene, self)
                undoStack.push(cmd)
            
            handle.setMouseState(ItemHandle.MOUSE_RELEASED)
        elif mevent.type() == QEvent.GraphicsSceneMouseMove:
            handle.setMouseState(ItemHandle.MOUSE_MOVING )
        else:
            return False
        

        if handle.getMouseState() == ItemHandle.MOUSE_MOVING:
            x = mevent.pos().x() 
            y = mevent.pos().y()

            XaxisSign = 0
            YaxisSign = 0
            if handle.getCorner() == 0:
                XaxisSign = +1
                YaxisSign = +1
            elif handle.getCorner() == 1:
                XaxisSign = -1
                YaxisSign = +1
            elif handle.getCorner() == 2:
                XaxisSign = -1
                YaxisSign = -1
            elif handle.getCorner() == 3:
                XaxisSign = +1
                YaxisSign = -1
            elif handle.getCorner() == 4:
                YaxisSign = +1
            elif handle.getCorner() == 5:
                XaxisSign = -1
            elif handle.getCorner() == 6:
                YaxisSign = -1
            elif handle.getCorner() == 7:
                XaxisSign = +1
            
            xMoved = handle.mouseDownX - x
            yMoved = handle.mouseDownY - y

            newWidth = self.rect.width() + ( XaxisSign * xMoved)
            if newWidth < 20: 
                newWidth  = 20

            newHeight = self.rect.height() + (YaxisSign * yMoved)
            if newHeight < 20:
                newHeight = 20

            deltaWidth = newWidth - self.rect.width()
            deltaHeight = newHeight - self.rect.height()

            shiftPressed = False
            controlPressed = False
            modifiers = QGuiApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                shiftPressed = True
            elif modifiers == Qt.ControlModifier:
                controlPressed = True
            elif modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
                shiftPressed = True
                controlPressed = True
            
            if controlPressed:
                # keep ratio
                ratio = self.rect.width() / self.rect.height()
                if handle.getCorner() < 4: # corners
                    if newWidth > newHeight:
                        deltaWidth = int(deltaHeight * ratio)
                    else:
                        deltaHeight = int(deltaWidth / ratio)
                else:
                    if handle.getCorner() == 4 or handle.getCorner() == 6: # top | bottom
                        deltaWidth = deltaHeight * ratio
                    else: # left | right
                        deltaHeight = deltaWidth / ratio
                
            self.setRect(0,0,self.rect.width() + deltaWidth, self.rect.height() + deltaHeight)
            self.scaleObjects()

            deltaWidth *= (-1)
            deltaHeight *= (-1)

            newXpos = self.pos().x()
            newYpos = self.pos().y()

            if handle.getCorner() == 0: # top left
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                else:
                    newXpos = self.pos().x() + deltaWidth
                    newYpos = self.pos().y() + deltaHeight
            elif handle.getCorner() == 1: # top right
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                else:
                    newYpos = self.pos().y() + deltaHeight            
            elif handle.getCorner() == 2: # bottom right
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
            elif handle.getCorner() == 3: # bottom left
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                else:
                    newXpos = self.pos().x() + deltaWidth
            elif handle.getCorner() == 4: # top
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                elif controlPressed:
                    newYpos = self.pos().y() + deltaHeight
                    newXpos = self.pos().x() + deltaWidth / 2
                else:
                    newYpos = self.pos().y() + deltaHeight
            elif handle.getCorner() == 5: # right
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                elif controlPressed:
                    newYpos = self.pos().y() + deltaHeight / 2
            elif handle.getCorner() == 6: # bottom
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                elif controlPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
            elif handle.getCorner() == 7: # left
                if shiftPressed:
                    newXpos = self.pos().x() + deltaWidth / 2
                    newYpos = self.pos().y() + deltaHeight / 2
                elif controlPressed:
                    newXpos = self.pos().x() + deltaWidth
                    newYpos = self.pos().y() + deltaHeight / 2
                else:
                    newXpos = self.pos().x() + deltaWidth

            if newXpos != self.pos().x() or newYpos != self.pos().y():
                self.setPos(newXpos, newYpos)
                self.posChanged(newXpos, newYpos)
            
            self.setHandlePositions()
            self.update()
        return True
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value:
                if not self.hasHandles:
                    for i in range(8):
                        self.handles[i] = ItemHandle(self, i, self.scene.scaling)
                        self.handles[i].installSceneEventFilter(self)
                    
                    self.hasHandles = True
                    self.setHandlePositions()
            else:
                for i in range(8):
                    self.scene.removeItem(self.handles[i])
                    self.handles[i] = None
                self.hasHandles = False
        elif change == QGraphicsItem.ItemPositionHasChanged:
            if self.isSelected():
                newPos = value
                self.posChanged(newPos.x(), newPos.y())
                self.setHandlePositions()
        return super().itemChange(change, value)
    
    def posChanged(self, x, y):
        pass
        #self.positionChanged.emit(x, y)