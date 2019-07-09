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

from PyQt5.QtWidgets import QUndoCommand, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from rectangle import Rectangle


class AddItemCommand(QUndoCommand):
    def __init__(self, x, y, mode, fileName, scene, parent=None):
        super(AddItemCommand, self).__init__(parent)

        from designerscene import DesignerScene
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

        # elif mode == DesignerScene.ModeEllipse:
        #     self.item = Ellipse(self.scene)
        #     self.item.setId("Ellipse")
        #     self.item.setPen(QPen(Qt.black))
        #     self.item.setBrush(QBrush(Qt.blue))
        #     self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
        #     self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
        #     self.item.setPos(x, y)
        #     self.item.setWidth(50)
        #     self.item.setHeight(50)
        #     self.setText("Add Ellipse")
        #     break
        # elif mode == DesignerScene.ModeText:
        #     self.item = Text("Lorem ipsum dolor", self.scene)
        #     self.item.setId("Text")
        #     self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
        #     self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
        #     self.item.setPos(x, y)
        #     self.setText("Add Text")
        #     break
            
            # case AnimationScene.EditMode.ModeBitmap:
            
            #     self.item = Bitmap(fileName, self.scene)
            #     self.item.setId("Bitmap")
            #     self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
            #     self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
            #     self.item.setPos(x, y)
            #     setText(QObject.tr("Add Bitmap"))
            #     break
            
            # case AnimationScene.EditMode.ModeSvg:
            
            #     self.item = Vectorgraphic(fileName, self.scene)
            #     self.item.setId("Vectorgraphic")
            #     self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
            #     self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
            #     self.item.setPos(x, y)
            #     setText(QObject.tr("Add Vectorgraphic"))
            #     break
            
            # case AnimationScene.EditMode.ModePlugin:
            
            #     ItemInterface *item = Plugins.getItemPlugin(self.scene.actPluginName())
            #     self.item = item.getInstance(self.scene)
            #     self.item.setId(item.displayName())
            #     self.item.setFlag(QGraphicsItem.ItemIsMovable, true)
            #     self.item.setFlag(QGraphicsItem.ItemIsSelectable, true)
            #     self.item.setPos(x, y)
            #     self.item.setPlayheadPosition(self.scene.playheadPosition())
            #     setText("Add " + item.displayName())
            #     break
    

    def undo(self):
        self.scene.clearSelection()
        self.scene.removeItem(self.item)
        self.item.setDeleted(true)
        #self.scene.itemRemoved.emit(self.item)
    
    def redo(self):
        self.scene.clearSelection()
        self.scene.addItem(self.item)
        #self.scene.itemAdded.emit(self.item)
    

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
