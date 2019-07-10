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

import os
from PyQt5.QtCore import QObject, pyqtProperty, QFileInfo, Q_CLASSINFO
from PyQt5.QtQml import QQmlListProperty


class Project(QObject):
    def __init__(self, parent=None):
        super(Project, self).__init__(parent)
        self._name = ""
        self.filename = ""
        self.source_path = ""
        self.win = None

    @pyqtProperty('QString')
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def setFilename(self, filename):
        info = QFileInfo(filename)
        self.filename = info.fileName()
        self.source_path = info.path()

    def setWindow(self, win):
        self.win = win

    def save(self):
        fname = os.path.join(self.source_path, self.filename)
        with open(fname, "w") as f:
            f.write("import UXDesigner 1.0\n\n")
            f.write("Project {\n")
            f.write("    name: \"" + self._name + "\"\n")
            f.write("}\n")