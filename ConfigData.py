################################################################################
# Copyright 2010 Andreas Neustifter (andreas.neustifter@gmail.com)
#
# This file is part of PhotoImport.
#
# PhotoImport is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PhotoImport is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PhotoImport. If not, see <http://www.gnu.org/licenses/>.
################################################################################

import wx

class ConfigData:

    def __init__(self):
        self.srcrecursive = False
        self.srcvalue = ""
        self.destvalue = ""
        self.foldernamevalue = ""
        self.renamefiles = False;
        self.filenamevalue = ""
        self.Load()

    def Load(self):
        config = wx.Config("PhotoImport")
        if not config.HasGroup("ConfigFrame"):
            return
        config.SetPath("ConfigFrame")
        self.srcrecursive = config.ReadBool("Recursive", False)
        self.srcvalue = config.Read("Source", "")
        self.destvalue = config.Read("Destination", "")
        self.foldernamevalue = config.Read("FolderPattern", "")
        self.renamefiles = config.ReadBool("RenameFiles", False)
        self.filenamevalue = config.Read("FilePattern", "")

    def Save(self):
        config = wx.Config("PhotoImport")
        config.SetPath("ConfigFrame")
        config.WriteBool("Recursive", self.srcrecursive)
        config.Write("Source", self.srcvalue)
        config.Write("Destination", self.destvalue)
        config.Write("FolderPattern", self.foldernamevalue)
        config.WriteBool("RenameFiles", self.renamefiles)
        config.Write("FilePattern", self.filenamevalue)
