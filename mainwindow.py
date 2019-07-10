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

import sys
from os import path, remove, walk, getcwd
from pathlib import Path
from shutil import copy
from PyQt5.QtCore import (QByteArray, QCoreApplication, QPropertyAnimation,
                          QSettings, Qt, QUrl, QSize)
from PyQt5.QtGui import (QColor, QFont, QIcon, QKeySequence, QPalette,
                         QTextCursor, QImage, QPixmap, QPainter, QCursor)
from PyQt5.QtQml import QQmlComponent, QQmlEngine
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget, QUndoStack,
                             QFileDialog, QHBoxLayout, QLineEdit, QListWidget,
                             QListWidgetItem, QMainWindow, QMessageBox, QActionGroup,
                             QScrollArea, QSizePolicy, QSplitter, QProxyStyle, QToolBar,
                             QStyleFactory, QTextEdit, QVBoxLayout, QWidget, QStyle, QComboBox)
from dark import DarkFusion
from settingsdialog import SettingsDialog
from sceneview import SceneView
from designerscene import DesignerScene
from scenepropertyeditor import ScenePropertyEditor
import resources


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.install_directory = getcwd()
        self.app = app
        self.undostack = QUndoStack()
        self.scene = DesignerScene()
        self.scene.setUndostack(self.undostack)
        self.filename = ""
        self.initTheme()
        self.createUi()
        self.createMenus()
        self.createStatusBar()
        self.readSettings()

    def initTheme(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        self.theme = settings.value("theme", "Fusion")
        hilite_color = settings.value("hiliteColor", self.palette().highlight().color().name())
        self.changeStyle(self.theme, hilite_color)

    def showEvent(self, event):
       pass

    def changeStyle(self, theme, hilite_color):
        self.theme = theme
        if theme == "DarkFusion":
            QApplication.setStyle(DarkFusion(hilite_color))
        else:
            QApplication.setStyle(QStyleFactory.create(theme))
            pal = self.app.palette()
            pal.setColor(QPalette.Highlight, QColor(hilite_color))
            self.app.setPalette(pal)

    def createUi(self):
        self.setWindowTitle(QCoreApplication.applicationName())
        self.view = SceneView(self.scene)
        self.view.setSceneRect(-100, -100, self.scene.width() + 200,self.scene.height() + 200)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        #connect(self.scene, SIGNAL(selectionChanged()), this, SLOT(sceneSelectionChanged()))
        #connect(self.scene, SIGNAL(itemAdded(QGraphicsItem*)), this, SLOT(sceneItemAdded(QGraphicsItem*)))
        #connect(self.scene, SIGNAL(sizeChanged(int,int)), this, SLOT(sceneSizeChanged(int, int)))
        #connect(self.scene, SIGNAL(itemRemoved(AnimationItem*)), this, SLOT(sceneItemRemoved(AnimationItem*)))
        #connect(self.scene, SIGNAL(animationResetted()), this, SLOT(reset()))
        w = QWidget()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        zoom = QComboBox()
        zoom.addItem("1:2")
        zoom.addItem("1:1")
        zoom.addItem("2:1")
        zoom.addItem("4:1")
        zoom.addItem("8:1")
        zoom.setCurrentIndex(1)
        #connect(zoom, SIGNAL(currentIndexChanged(int)), this, SLOT(changeZoom(int)))
        vbox.addWidget(self.view)
        vbox.addLayout(hbox)
        hbox.addWidget(zoom)
        hbox.addStretch()
        w.setLayout(vbox)
        self.setCentralWidget(w)

        toolpanel = QToolBar()
        anActionGroup = QActionGroup(toolpanel)
        self.selectAct = QAction("Select", anActionGroup)
        self.selectAct.setIcon(QIcon(":/images/arrow.png"))
        self.selectAct.setCheckable(True)

        self.rectangleAct = QAction("Rectangle", anActionGroup)
        self.rectangleAct.setIcon(QIcon(":/images/rectangle.png"))
        self.rectangleAct.setCheckable(True)

        self.ellipseAct = QAction("Ellipse", anActionGroup)
        self.ellipseAct.setIcon(QIcon(":/images/ellipse.png"))
        self.ellipseAct.setCheckable(True)

        self.textAct = QAction("Text", anActionGroup)
        self.textAct.setIcon(QIcon(":/images/text.png"))
        self.textAct.setCheckable(True)

        self.bitmapAct = QAction("Bitmap", anActionGroup)
        self.bitmapAct.setIcon(QIcon(":/images/camera.png"))
        self.bitmapAct.setCheckable(True)

        self.svgAct = QAction("Vectorgraphic", anActionGroup)
        self.svgAct.setIcon(QIcon(":/images/svg.png"))
        self.svgAct.setCheckable(True)
        
        toolpanel.setOrientation(Qt.Vertical)
        toolpanel.addAction(self.selectAct)
        toolpanel.addAction(self.rectangleAct)
        toolpanel.addAction(self.ellipseAct)
        toolpanel.addAction(self.textAct)
        toolpanel.addAction(self.bitmapAct)
        toolpanel.addAction(self.svgAct)
    
        self.tooldock = QDockWidget("Tools", self)
        self.tooldock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tooldock.setWidget(toolpanel)
        self.tooldock.setObjectName("Tools")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tooldock)

        self.scenePropertyEditor = ScenePropertyEditor()
        self.scenePropertyEditor.setScene(self.scene)
        self.propertiesdock = QDockWidget("Properties", self)
        self.propertiesdock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.propertiesdock.setWidget(self.scenePropertyEditor)
        self.propertiesdock.setObjectName("Properties")
        self.addDockWidget(Qt.RightDockWidgetArea, self.propertiesdock)

        self.selectAct.triggered.connect(self.setSelectMode)
        self.rectangleAct.triggered.connect(self.setRectangleMode)
        self.ellipseAct.triggered.connect(self.setEllipseMode)
        self.textAct.triggered.connect(self.setTextMode)
        self.bitmapAct.triggered.connect(self.setBitmapMode)
        self.svgAct.triggered.connect(self.setSvgMode)

    def openSettings(self):
        dlg = Settings(self.book)
        dlg.exec()
        if dlg.saved:
            self.setWindowTitle(QCoreApplication.applicationName() + " - " + self.book.name)

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def createMenus(self):
        new_icon = QIcon(QPixmap(":/images/new.svg"))
        open_icon = QIcon(QPixmap(":/images/open.svg"))
        book_icon = QIcon(QPixmap(":/images/book.svg"))
        bold_icon = QIcon(QPixmap(":/images/bold.svg"))
        italic_icon = QIcon(QPixmap(":/images/italic.svg"))
        image_icon = QIcon(QPixmap(":/images/image.svg"))
        table_icon = QIcon(QPixmap(":/images/table.svg"))

        new_act = QAction(new_icon, "&New", self)
        new_act.setShortcuts(QKeySequence.New)
        new_act.setStatusTip("Create a new project")
        new_act.triggered.connect(self.newFile)
        new_act.setToolTip("Create new project")

        open_act = QAction(open_icon, "&Open", self)
        open_act.setShortcuts(QKeySequence.Open)
        open_act.setStatusTip("Open an existing project")
        open_act.triggered.connect(self.open)
        open_act.setToolTip("Open an existing project")

        settings_act = QAction("&Settings", self)
        settings_act.setStatusTip("Open settings dialog")
        settings_act.triggered.connect(self.settingsDialog)
        settings_act.setToolTip("Open settings dialog")

        exit_act = QAction("E&xit", self)
        exit_act.setShortcuts(QKeySequence.Quit)
        exit_act.setStatusTip("Exit the application")
        exit_act.triggered.connect(self.close)

        about_act = QAction("&About", self)
        about_act.triggered.connect(self.about)
        about_act.setStatusTip("Show the application's About box")

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addSeparator()
        file_menu.addAction(settings_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(about_act)

        file_tool_bar = self.addToolBar("File")
        file_tool_bar.addAction(new_act)
        file_tool_bar.addAction(open_act)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def about(self):
        QMessageBox.about(self, "About " + QCoreApplication.applicationName(), "UXDesigner\nVersion: " + QCoreApplication.applicationVersion() + "\n(C) Copyright 2019 Olaf Japp. All rights reserved.\n\nThis program is provided AS IS with NO\nWARRANTY OF ANY KIND, INCLUDING THE\nWARRANTY OF UXDesigner, MERCHANTABILITY AND\nFITNESS FOR A PATICULAR PURPOSE.")

    def writeSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())

    def readSettings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        geometry = settings.value("geometry", QByteArray())
        if not geometry:
            availableGeometry = QApplication.desktop().availableGeometry(self)
            self.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)
        else:
            self.restoreGeometry(geometry)

    def open(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("UXDesigner (*.uxd)All (*)")
        dialog.setWindowTitle("Load Project")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(path.join(self.install_directory, "sources"))
        if dialog.exec_():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if not fileName:
            return
        self.loadProject(fileName)

    def settingsDialog(self):
        dlg = SettingsDialog(self.theme, self.palette().highlight().color().name(), parent=self)
        dlg.exec()
        if dlg.theme != self.theme or dlg.hilite_color != self.palette().highlight().color().name():
            settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
            settings.setValue("theme", dlg.theme)
            settings.setValue("hiliteColor", dlg.hilite_color)

            msgBox = QMessageBox()
            msgBox.setText("Please restart the app to change the theme!")
            msgBox.exec()

    def loadProject(self, filename):
        self.last_project = filename
        self.filename = ""
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl(filename))
        self.project = component.create()
        if self.project is not None:
            self.project.setFilename(filename)
            self.project.setWindow(self)
        else:
            for error in component.errors():
                print(error.toString())
                return

    def newFile(self):
        pass

    def setSelectMode(self):
        self.scene.setEditMode(DesignerScene.SELECT)
        self.scene.setCursor(Qt.ArrowCursor)

    def setRectangleMode(self):
        self.scene.clearSelection()
        self.scene.setCursor(QCursor(QPixmap.fromImage(QImage(":/images/rect_cursor.png"))))
        self.scene.setEditMode(DesignerScene.RECTANGLE)

    def setEllipseMode(self):
        self.scene.clearSelection()
        self.scene.setCursor(QCursor(QPixmap.fromImage(QImage(":/images/ellipse_cursor.png"))));
        self.scene.setEditMode(DesignerScene.ELLIPSE)

    def setTextMode(self):
        self.scene.clearSelection()
        self.scene.setCursor(QCursor(QPixmap.fromImage(QImage(":/images/text_cursor.png"))));
        self.scene.setEditMode(DesignerScene.TEXT)

    def setBitmapMode(self):
        self.scene.clearSelection()
        self.scene.setCursor(QCursor(QPixmap.fromImage(QImage(":/images/bitmap_cursor.png"))))
        self.scene.setEditMode(DesignerScene.BITMAP)

    def setSvgMode(self):
        self.scene.clearSelection()
        self.scene.setCursor(QCursor(QPixmap.fromImage(QImage(":/images/svg_cursor.png"))))
        self.scene.setEditMode(DesignerScene.SVG)

# void MainWindow::setEllipseMode()
# {
#     m_scene->clearSelection();
#     m_scene->setCursor(QCursor(QPixmap::fromImage(QImage(":/images/ellipse_cursor.png"))));
#     m_scene->setEditMode(AnimationScene::EditMode::ModeEllipse);
# }

# void MainWindow::setTextMode()
# {
#     m_scene->clearSelection();
#     m_scene->setCursor(QCursor(QPixmap::fromImage(QImage(":/images/text_cursor.png"))));
#     m_scene->setEditMode(AnimationScene::EditMode::ModeText);
# }

# void MainWindow::setBitmapMode()
# {
#     m_scene->clearSelection();
#     m_scene->setCursor(QCursor(QPixmap::fromImage(QImage(":/images/bitmap_cursor.png"))));
#     m_scene->setEditMode(AnimationScene::EditMode::ModeBitmap);
# }

# void MainWindow::setSvgMode()
# {
#     m_scene->clearSelection();
#     m_scene->setCursor(QCursor(QPixmap::fromImage(QImage(":/images/svg_cursor.png"))));
#     m_scene->setEditMode(AnimationScene::EditMode::ModeSvg);
# }
