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

from PyQt5.QtWidgets import QUndoCommand, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class AddItemCommand(QUndoCommand):
    def __init__(self, x, y, mode, fileName, scene, parent=None):
        super(AddItemCommand, self).__init__(parent)

        from designerscene import DesignerScene
        from rectangle import Rectangle
        from ellipse import Ellipse
        from text import Text
        from bitmap import Bitmap
        from vectorgraphic import Vectorgraphic
        self.scene = scene
        self.item = None

        if mode == DesignerScene.RECTANGLE:
            self.item = Rectangle(self.scene)
            self.item.setId("Rectangle")
            self.item.setPen(QPen(Qt.black))
            self.item.setBrush(QBrush(Qt.blue))
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.item.setWidth(50)
            self.item.setHeight(50)
            self.setText("Add Rectangle")

        elif mode == DesignerScene.ELLIPSE:
            self.item = Ellipse(self.scene)
            self.item.setId("Ellipse")
            self.item.setPen(QPen(Qt.black))
            self.item.setBrush(QBrush(Qt.blue))
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.item.setWidth(50)
            self.item.setHeight(50)
            self.setText("Add Ellipse")

        elif mode == DesignerScene.TEXT:
            self.item = Text("Lorem ipsum dolor", self.scene)
            self.item.setId("Text")
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.setText("Add Text")

        elif mode == DesignerScene.BITMAP:
            self.item = Bitmap(fileName, self.scene)
            self.item.setId("Bitmap")
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.setText("Add Bitmap")
            
        elif mode == DesignerScene.SVG:
            self.item = Vectorgraphic(fileName, self.scene)
            self.item.setId("Vectorgraphic")
            self.item.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            self.item.setPos(x, y)
            self.setText("Add Vectorgraphic")

    def undo(self):
        self.scene.clearSelection()
        self.scene.removeItem(self.item)
        self.item.setDeleted(true)
        self.scene.itemRemoved.emit(self.item)
    
    def redo(self):
        self.scene.clearSelection()
        self.scene.addItem(self.item)
        self.scene.itemAdded.emit(self.item)
    

class MoveItemCommand(QUndoCommand):
    def __init__(self, x, y, oldx, oldy, item, parent=None):
        super(MoveItemCommand, self).__init__(parent)
        self.x = x
        self.y = y
        self.oldx = oldx
        self.oldy = oldy
        self.item = item
        self.setText("Move " + item.typeName())
    
    def undo(self):
        self.item.setPos(self.oldx, self.oldy)

    def redo(self):
        self.item.setPos(self.x, self.y)


class ScaleItemCommand(QUndoCommand):
    def __init__(self, x, y, width, height, oldx, oldy, oldwidth, oldheight, scene, item, parent=None):
        super(ScaleItemCommand, self).__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.oldx = oldx
        self.oldy = oldy
        self.oldwidth = oldwidth
        self.oldheight = oldheight
        self.item = item
        self.setText("Scale " + item.typeName())
    
    def undo(self):
        self.item.setPos(self.oldx, self.oldy)
        self.item.setWidth(self.oldwidth)
        self.item.setHeight(self.oldheight)
        self.item.scaleObjects()
        self.item.posChanged(self.oldx, self.oldy)

    def redo(self):
        self.item.setPos(self.x, self.y)
        self.item.setWidth(self.width)
        self.item.setHeight(self.height)
        self.item.scaleObjects()
        self.item.posChanged(self.x, self.y)


class RaiseItemCommand(QUndoCommand):
    def __init__(self, item, parent=None):
        super(RaiseItemCommand, self).__init__(parent)
        self.item = item
        self.setText("Raise " + item.typeName())

    def undo(self):
        self.item.lowerItem()

    def redo(self):
        self.item.raiseItem()


class LowerItemCommand(QUndoCommand):
    def __init__(self, item, parent=None):
        super(LowerItemCommand, self).__init__(parent)
        self.item = item
        self.setText("Lower " + item.typeName())

    def undo(self):
        self.item.raiseItem()

    def redo(self):
        self.item.lowerItem()


class BringItemToFrontCommand(QUndoCommand):
    def __init__(self, item, parent=None):
        super(BringItemToFrontCommand, self).__init__(parent)
        self.item = item
        self.setText("Bring " + item.typeName() + " to front")

    def undo(self):
        self.item.sendToBack()

    def redo(self):
        self.item.bringToFront()


class SendItemToBackCommand(QUndoCommand):
    def __init__(self, item, parent=None):
        super(SendItemToBackCommand, self).__init__(parent)
        self.item = item
        self.setText("Send " + item.typeName() + " to back")

    def undo(self):
        self.item.bringToFront()

    def redo(self):
        self.item.sendToBack()


class DeleteItemCommand(QUndoCommand):
    def __init__(self, item, scene, parent=None):
        super(DeleteItemCommand, self).__init__(parent)
        self.item = item
        self.scene = scene
        self.setText("Delete " + item.typeName())

    def undo(self):
        self.scene.addItem(self.item)
        self.scene.itemAdded.emit(self.item)

    def redo(self):
        self.item.setSelected(False)
        self.scene.removeItem(self.item)
        self.scene.itemRemoved.emit(self.item)
