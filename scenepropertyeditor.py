#############################################################################
# Copyright (C) 2019 Olaf Japp
#
# self. file is part of UXDesigner.
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

from PyQt5.QtWidgets import QWidget, QSpinBox, QLabel, QGridLayout, QVBoxLayout
from coloreditor import ColorEditor
from expander import Expander


class ScenePropertyEditor(QWidget):
    def __init__(self):
        super(ScenePropertyEditor ,self).__init__()
        vbox = QVBoxLayout()
        exp = Expander("Scene")
        self.colorEditor = ColorEditor("Backgroundcolor")
        self.width = QSpinBox()
        self.height = QSpinBox()
        self.width.setMaximum(10000)
        self.height.setMaximum(10000)
        labelWidth = QLabel("W")
        labelHeight = QLabel("H")
        labelWidth.setFixedWidth(15)
        labelHeight.setFixedWidth(15)
        layout = QGridLayout()
        layout.addWidget(QLabel("Size"), 0, 0)
        layout.addWidget(labelWidth, 0, 1)
        layout.addWidget(self.width, 0, 2)
        layout.addWidget(labelHeight, 0, 3)
        layout.addWidget(self.height, 0, 4)
        layout.addWidget(self.colorEditor, 1, 0, 1, 5)
        exp.addLayout(layout)
        vbox.addWidget(exp)
        vbox.addStretch()
        self.setLayout(vbox)

        #connect(self.width, SIGNAL(valueChanged(int)), self., SLOT(widthChanged(int)))
        #connect(self.height, SIGNAL(valueChanged(int)), self., SLOT(heightChanged(int)))
        #connect(self.fps, SIGNAL(valueChanged(int)), self., SLOT(fpsChanged(int)))
        #connect(self.colorEditor, SIGNAL(colorChanged(QColor)), self., SLOT(colorChanged(QColor)))
        #connect(self.colorEditor, SIGNAL(addKeyframe()), self., SLOT(addKeyFrame()))

    def setScene(self ,scene):
        self.scene = scene