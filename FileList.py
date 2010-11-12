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
import glob
import os
import datetime
import shutil
import pyexiv2

class FileList:

    def __init__ (self, parent):

        self._parent = parent
        self._source = parent.GetSource()
        self._dest = parent.GetDest()
        self._pattern = parent.GetName()
        self._recursive = parent.GetRecursive()
        self._files = {}

        if self._recursive:
            filelist = []
            for (dirp,dirs,files) in os.walk(self._source + "/"):
                for f in files:
                    filelist.append(os.path.join(dirp,f));
        else:
            filelist = glob.glob(self._source + "/*")

        for f in filelist:
            exif = pyexiv2.ImageMetadata(f)
            try:
                exif.read()
            except:
                continue

            try:
                fm = exif['Exif.Photo.DateTimeOriginal'].value
            except:
                try:
                    fm = exif['Exif.Photo.DateTime'].value
                except:
                    fs = os.stat(f)
                    fm = datetime.datetime.fromtimestamp(fs.st_mtime)

            if fm.hour < 6:
                date = fm - datetime.timedelta(days=1)
            else:
                date = fm

            datestr = date.strftime("%Y%m%d")

            if not self._files.has_key(datestr):
                self._files[datestr] = {}

            self._files[datestr][f] = date


    def Filter(self):

        for date in sorted(self._files.keys()):

            destpath = self._pattern.replace("<date>", date);
            destpath = destpath.replace("<name>", "*");

            if len(glob.glob(self._dest + "/" + destpath)) > 0:
                del self._files[date]


    def ShowDialog(self):

        for date in sorted(self._files.keys()):
            import CopyDialog
            cf = CopyDialog.CopyDialog(self._parent, -1, "")
            cf.SetDate(date)
            cf.SetDestination(self._dest)
            cf.SetPattern(self._pattern.replace("<date>", date))
            cf.SetFiles(self._files[date])
            cf.SetCopyHandler(self.Copy)
            cf.ShowModal()


    def Copy(self,date,folder):
        dest = self._dest + "/" + folder

        os.mkdir(dest)

        for f in self._files[date]:
            shutil.copy2(f,dest)


    def __str__(self):

        retval = []

        for date in sorted(self._files.keys()):
            retval.append("date: " + date)
            for f in self._files[date]:
                retval.append(f)

        return "\n".join(retval)


if __name__ == "__main__":

    fl = FileList("/media/EOS_DIGITAL/DCIM/100CANON", "/mnt/data/andi/fotos/sessions/", "<date>_<name>")
    print fl

    fl.Filter()
    print fl

    fl.ShowDialog()
