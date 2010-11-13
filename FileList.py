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
This modules handles all the files.
"""

import glob
import os
import datetime
import shutil
import pyexiv2

class FileList:
    """
    This module reads a list of files, sorts the into "days" and asks the user
    for a folder for each day. It then copies the files and optionally renames
    them.
    """

    def __init__ (self, config, parent):

        self.parent = parent
        self.config = config
        self.files = {}

        if self.config.srcrecursive:
            filelist = []
            for (dirp, dirs, files) in os.walk(self.config.srcvalue + "/"):
                for filename in files:
                    filelist.append(os.path.join(dirp, filename))
        else:
            filelist = glob.glob(self.config.srcvalue + "/*")

        for filename in filelist:
            exif = pyexiv2.ImageMetadata(filename)
            try:
                exif.read()
            except:
                continue

            try:
                filedate = exif['Exif.Photo.DateTimeOriginal'].value
            except:
                try:
                    filedate = exif['Exif.Photo.DateTime'].value
                except:
                    filestat = os.stat(filename)
                    filedate = datetime.datetime.fromtimestamp(filestat.st_mtime)

            if filedate.hour < 6:
                date = filedate - datetime.timedelta(days=1)
            else:
                date = filedate

            datestr = date.strftime("%Y%m%d")

            if not self.files.has_key(datestr):
                self.files[datestr] = {}

            self.files[datestr][filename] = date

    def filter(self):
        """
        This removes all the files where the date already has a folder.
        """

        for date in sorted(self.files.keys()):

            destpath = self.config.foldernamevalue.replace("<date>", date)
            destpath = destpath.replace("<name>", "*")

            if len(glob.glob(self.config.destvalue + "/" + destpath)) > 0:
                del self.files[date]


    def showdialog(self):
        """ This shows the CopyDialog for each days. """

        for date in sorted(self.files.keys()):
            import CopyDialog
            copydialog = CopyDialog.CopyDialog(self.parent, -1, "")
            copydialog.setconfig(self.config, date, self.files[date], self.copy)
            copydialog.ShowModal()

    def copy(self, date, folder):
        """
        This actually copies the files, they are optionally renamed. 
        """

        dest = self.config.destvalue + "/" + folder

        print dest + "\n"
        os.mkdir(dest)

        for (filename, filedate) in self.files[date].items():
            path = dest
            if self.config.renamefiles:
                (root, ext) = os.path.splitext(filename)
                ext = ext[1:]
                filename = self.config.filenamevalue.replace("<date>", date)
                filename = filename.replace("<time>", filedate.strftime("%H%M%S"))
                filename = filename.replace("<ext>", ext)
                path = os.path.join(path, filename)

            print filename + " " + path + "\n"
            shutil.copy2(filename, path)

    def __str__(self):

        retval = []

        for date in sorted(self.files.keys()):
            retval.append("date: " + date)
            for filename in self.files[date]:
                retval.append(filename)

        return "\n".join(retval)
