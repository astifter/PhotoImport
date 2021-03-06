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

import sys
import stat
import subprocess

import logging
import FileDB
import ExifHandler


def getfiledate(filename):
    """ 
    This takes a filename and tries to read the last modification date from
    exif or filesystem. 
    """
    try:
        filedate = ExifHandler.getfiledate(filename)
    except:
        try:
            filestat = os.stat(filename)
            filedate = datetime.datetime.fromtimestamp(filestat.st_mtime)
            logging.info("Can not read EXIF date, using file system date.")
        except:
            logging.error("Can not access file modification date for %s, skipping." % filename)
            return None
    return filedate


class FileList:
    """
    This module reads a list of files, sorts the into "days" and asks the user
    for a folder for each day. It then copies the files and optionally renames
    them.
    """

    def __init__ (self, config, parent, loghandler):

        self.loghandler = loghandler
        self.parent = parent
        self.config = config
        self.files = {}
        self.statusdb = FileDB.FileDB()

        if self.config.srcrecursive:
            filelist = []
            try:
                for (dirp, dirs, files) in os.walk(self.config.srcvalue + os.sep):
                    for filename in files:
                        filelist.append(os.path.join(dirp, filename))
            except:
                logging.error("Can not read recursive folders, aborting.")
                return
        else:
            try:
                filelist = glob.glob(self.config.srcvalue + os.sep + "*")
            except:
                logging.error("Can not read files from folder %s, aborting." % self.config.srcvalue)
                return

        for filename in filelist:
            if filename.endswith("PhotoImport.db") or filename.endswith(".CTG"):
                continue

            filedate = getfiledate(filename)
            if filedate is None:
                continue

            if filedate.hour < 6:
                date = filedate - datetime.timedelta(days=1)
            else:
                date = filedate

            datestr = date.strftime("%Y%m%d")

            if not self.files.has_key(datestr):
                self.files[datestr] = {}

            self.files[datestr][filename] = date
            logging.info("Read file %s with date %s." % (filename, datestr))
            
        self.finished = True

    def filter(self):
        """
        This removes all the files where the status is already set.
        """

        if not self.finished:
            logging.error("Can not filter files, was not read.")

        for date in self.files.keys():
            for filepath in self.files[date].keys():
                status = self.statusdb.getstatus(filepath)
                if status is not None:
                    logging.debug("Removed %s from filelist (status %s)." % (filepath, status))
                    del self.files[date][filepath]

            if len(self.files[date].keys()) <= 0:
                logging.debug("Removed %s from filelist." % date)
                del self.files[date]

    def showdialog(self):
        """ This shows the CopyDialog for each days. """

        if not self.finished:
            logging.error("Can not show copy dialog, was not read.")

        foldercount = len(self.files.keys())
        donecount = 0

        for date in sorted(self.files.keys()):
            try:
                donecount += 1
                import CopyDialog
                self.copydialog = CopyDialog.CopyDialog(self.parent, -1, "")
                self.copydialog.setconfig(self.config, date, self.files[date], self.copy, donecount, foldercount)
                self.copydialog.ShowModal()
            except:
                logging.error("Error during CopyDialog.")

        if len(self.files.keys()) == 0:
            if not os.path.isdir(self.config.srcvalue):
                message = "Source folder does not exist, no images copied."
                logging.error(message)
            else:
                message = "No new images were copied."
                logging.info(message)

        if self.loghandler.hasMessages():
            import NoImageCopied
            self.nocopieddialog = NoImageCopied.NoImageCopied(self.parent, -1, message=self.loghandler.getMessages())
            self.nocopieddialog.ShowModal()

    def copy(self, date, folder, do_copy=True):
        """
        This actually copies the files, they are optionally renamed. 
        """

        if not self.finished:
            logging.error("Can not copy files, was not read.")

        dest = os.path.join(self.config.destvalue, folder)

        if do_copy and not os.path.exists(dest):
            try:
                os.mkdir(dest)
                logging.info("Created folder %s." % dest)
            except:
                logging.error("Can not create folder %s, skipping." % dest)
                return

        self.copydialog.showprogess(True)

        filecount = len(self.files[date].items())
        donecount = 0.0

        for (filename, filedate) in self.files[date].items():
            if self.statusdb.getstatus(filename) is not None:
                logging.error("File %s has status set but was not filtered.")
                continue

            if not do_copy:
                logging.info("Marking %s as never." % filename)
                self.statusdb.setstatus(filename, "never")
                continue

            if self.config.renamefiles:
                (root, ext) = os.path.splitext(filename)
                ext = ext[1:]
                newname = self.config.filenamevalue.replace("<date>", date)
                newname = newname.replace("<time>", filedate.strftime("%H%M%S"))
                newname = newname.replace("<ext>", ext)
                path = os.path.join(dest, newname)
            else:
                path = os.path.join(dest, os.path.basename(filename))

            if os.path.exists(path):
                logging.error("File %s already exists in path %s, skipping." % (filename, path))
                continue

            try:
                shutil.copy2(filename, path)
                logging.info("Copied file %s to %s." % (filename, path))
                self.statusdb.setstatus(filename, "copied to %s" % path)
            except:
                logging.error("Can not copy file %s to %s, skipping." % (filename, path))

            donecount += 1.0
            self.copydialog.setprogress(donecount/filecount)

        self.copydialog.showprogess(False)
