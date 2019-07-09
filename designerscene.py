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

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import QRectF, Qt, QPointF
from rectangle import Rectangle
from itemhandle import ItemHandle
from designitem import DesignItem
from command import AddItemCommand, MoveItemCommand


class DesignerScene(QGraphicsScene):
    SELECT = 0 
    RECTANGLE = 1 
    ELLIPSE = 2
    TEXT = 3 
    BITMAP = 4 
    SVG = 5 
    PLUGIN = 6

    def __init__(self):
        super(DesignerScene, self).__init__()
        self.initialize()

    def initialize(self):
        self.setSceneRect(0, 0, 1200, 720)
        self.edit_mode = DesignerScene.SELECT
        self.copy = None
        self.movingItem = None
        self.scaling = 1
        self.addBackgroundRect()
        self.blackSelectionRect = None

    def setScaling(self, scaling):
        self.scaling = scaling

    def setUndostack(self, st):
        self.undostack = st

    def reset(self):
        self.clear()
        self.initialize()
        self.undoStack.clear()

    def addBackgroundRect(self):
        self.rect = Rectangle(self, True)
        self.rect.setId("Scene")
        self.rect.setPos(0,0)
        self.rect.setWidth(self.width())
        self.rect.setHeight(self.height())
        backgroundColor = QColor("#404244")
        self.rect.setBrush(QBrush(QColor(backgroundColor)))
        self.addItem(self.rect)

    def setCursor(self, cursor):
        self.rect.setCursor(cursor)

    def setEditMode(self, mode):
        self.edit_mode = mode

    def mousePressEvent(self, mouseEvent):
        self.oldPos = QPointF(0, 0)
        self.movingItem = None

        if mouseEvent.button() != Qt.LeftButton:
            return

        if self.edit_mode == DesignerScene.SELECT:    
            handle = None
            mousePos = QPointF(mouseEvent.buttonDownScenePos(Qt.LeftButton).x(), mouseEvent.buttonDownScenePos(Qt.LeftButton).y())
            itemList = self.items(mousePos)
            for item in itemList:
                if isinstance(item, ItemHandle):
                    handle = item
                    break
                elif isinstance(item, DesignItem):
                    if not item.isSceneRect():
                        self.movingItem = item
                        self.oldPos = item.pos()
                        break
                
            if not self.movingItem and not handle:
                self.blackSelectionRect = self.addRect(0, 0, 1, 1, QPen(QColor("#000000")))
                self.blackSelectionRect.setPos(mousePos)
                self.whiteSelectionRect = self.addRect(1, 1, 1, 1, QPen(QColor("#ffffff")))
                self.whiteSelectionRect.setPos(mousePos)
            
            super().mousePressEvent(mouseEvent)
        else:
            filter = ""
            fileName = ""
            if self.edit_mode == DesignerScene.BITMAP:
                filter = "Image Files (*.png *.jpeg *.jpg *.gif *.bmp)All Files (*)"
                title = "Open Bitmap"
            elif self.edit_mode == DesignerScene.SVG:
                filter = "SVG Files (*.svg)All Files (*)"
                title = "Open SVG"
            if filter:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.AnyFile)
                dialog.setNameFilter(filter)
                dialog.setWindowTitle(title)
                dialog.setOption(QFileDialog.DontUseNativeDialog, true)
                dialog.setAcceptMode(QFileDialog.AcceptOpen)
                if dialog.exec():
                    fileName = dialog.selectedFiles().first()
                del dialog
                if not fileName:
                    return
            
            addCommand = AddItemCommand(mouseEvent.scenePos().x(), mouseEvent.scenePos().y(), self.edit_mode, fileName, self)
            self.undostack.push(addCommand)

    def mouseMoveEvent(self, mouseEvent):
        if self.edit_mode == DesignerScene.SELECT and self.blackSelectionRect:
            self.blackSelectionRect.setRect(0, 0, mouseEvent.lastScenePos().x() - self.blackSelectionRect.pos().x(), mouseEvent.lastScenePos().y() - self.blackSelectionRect.pos().y())
            self.whiteSelectionRect.setRect(1, 1, mouseEvent.lastScenePos().x() - self.blackSelectionRect.pos().x(), mouseEvent.lastScenePos().y() - self.blackSelectionRect.pos().y())
        super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.edit_mode == DesignerScene.SELECT and self.blackSelectionRect:
            itemList = self.items(self.blackSelectionRect.pos().x(), self.blackSelectionRect.pos().y(), self.blackSelectionRect.rect().width(), self.blackSelectionRect.rect().height(), Qt.IntersectsItemShape, Qt.AscendingOrder)
            for item in itemList:
                item.setSelected(True)
            
            self.removeItem(self.blackSelectionRect)
            self.removeItem(self.whiteSelectionRect)
            del self.blackSelectionRect
            del self.whiteSelectionRect
            self.blackSelectionRect = None
            self.whiteSelectionRect = None
        
        if self.movingItem and mouseEvent.button() == Qt.LeftButton:
            if self.oldPos != self.movingItem.pos():
                cmd = MoveItemCommand(self.movingItem.x(), self.movingItem.y(), self.oldPos.x(), self.oldPos.y(), self.movingItem)
                self.undostack.push(cmd)
            
            self.movingItem = None
        
        super().mouseReleaseEvent(mouseEvent)
    