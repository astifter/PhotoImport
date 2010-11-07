import glob
import os
import datetime

class FileList:

    def __init__ (self, parent):

        self._parent = parent
        self._source = parent.GetSource()
        self._dest = parent.GetDest()
        self._pattern = parent.GetName()
        self._files = {}
        
        filelist = glob.glob(self._source + "/*")

        for f in filelist:

            fs = os.stat(f)
            fm = datetime.datetime.fromtimestamp(fs.st_mtime)

            if fm.hour < 6:
                date = fm - datetime.timedelta(days=1)
            else:
                date = fm

            datestr = date.strftime("%Y%m%d")

            if not self._files.has_key(datestr):
                self._files[datestr] = []

            self._files[datestr].append(f)


    def Filter(self):

        for date in sorted(self._files.keys()):
            
            destpath = self._pattern.replace("<date>", date);
            destpath = destpath.replace("<name>", "*");

            if len(glob.glob(self._dest + "/" + destpath)) > 0:
                del self._files[date]


    def Copy(self):

        for date in sorted(self._files.keys()):
            import CopyDialog
            cf = CopyDialog.CopyDialog(self._parent, -1, "")
            cf.SetDate(date)
            cf.SetDestination(self._dest)
            cf.SetPattern(self._pattern.replace("<date>", date))
            cf.SetFiles(self._files[date])
            cf.ShowModal()


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

    fl.Copy(None)
