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
"""
Contains class ConfigData.
"""

import wx
import logging

class ConfigData:
    """
    This class holds and stores all the configuration data for the PhotoImport
    classes. This includes storing and reloading those values from a
    configuration file.
    """

    def __init__(self):
        self.srcrecursive = False
        self.srcvalue = ""
        self.destvalue = ""
        self.foldernamevalue = ""
        self.renamefiles = False
        self.filenamevalue = ""
        self.load()

    def load(self):
        """
        This loads the configuration from the wx.Config facility and stores
        these values in attributes.
        """
        try:
            config = wx.Config("PhotoImport")
            if not config.HasGroup("ConfigFrame"):
                logging.error("Can not find configuration section ConfigFrame, aborting.")
                return
            config.SetPath("ConfigFrame")
        except:
            logging.error("Can not open configuration, aborting.")
            return

        try:
            self.srcrecursive = config.ReadBool("Recursive", False)
            self.srcvalue = config.Read("Source", "")
            self.destvalue = config.Read("Destination", "")
            self.foldernamevalue = config.Read("FolderPattern", "")
            self.renamefiles = config.ReadBool("RenameFiles", False)
            self.filenamevalue = config.Read("FilePattern", "")
        except:
            logging.error("Can not load configuration, aborting.")
            return

    def save(self):
        """
        This stores the configuration to the wx.Config.
        """
        try:
            config = wx.Config("PhotoImport")
            config.SetPath("ConfigFrame")
        except:
            logging.error("Can not open configuration, aborting.")
            return

        try:
            config.WriteBool("Recursive", self.srcrecursive)
            config.Write("Source", self.srcvalue)
            config.Write("Destination", self.destvalue)
            config.Write("FolderPattern", self.foldernamevalue)
            config.WriteBool("RenameFiles", self.renamefiles)
            config.Write("FilePattern", self.filenamevalue)
        except:
            logging.error("Can not save configuration, aborting.")
            return
