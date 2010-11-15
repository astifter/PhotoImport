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
This module stores per folder the information about copied and excluded files.
"""

import os

class FileDB:
    """
    This class reads, stores and caches information about copied files.
    """

    def __init__ (self):
        self._db = {}

    def readorcache(self, folder):
        """ 
        This reads in the PhotoImport.db for a folder, if this file is missing
        it creates an empty dictionary. 
        """

        if not self._db.has_key(folder):

            filelist = {}

            try:
                dbfile = open(os.path.join(folder, "PhotoImport.db"), "r")
            except:
                self._db[folder] = filelist
                return

            filename = dbfile.readline()

            while filename != "":
                filestatus = dbfile.readline()

                filelist[filename.strip()] = filestatus.strip()

                filename = dbfile.readline()

            dbfile.close()

            self._db[folder] = filelist

    def getstatus(self, filepath):
        """ 
        This splits the filename into folder, filename and calls getstatus on
        that. 
        """

        (folder, filename) = os.path.split(filepath)

        return self.getstatus2(folder, filename)


    def getstatus2(self, folder, filename):
        """
        This reads the PhotoImport.db from folder and reads file information.
        """

        self.readorcache(folder)

        try:
            return self._db[folder][filename]
        except:
            return None

    def setstatus(self, filepath, status):
        """
        This first checks that file is not in PhotoImport.db and then sets status.
        """

        (folder, filename) = os.path.split(filepath)

        if self.getstatus2(folder, filename) is not None:
            raise Exception("Setting status of a file that has already status attached")

        self._db[folder][filename] = status

        dbfile = open(os.path.join(folder, "PhotoImport.db"), "a+")
        dbfile.write(filename + "\n")
        dbfile.write(status + "\n")
        dbfile.close()


if __name__ == "__main__":

    import sys
    fdb = FileDB()

    if sys.argv[1] == "get":
        print fdb.getstatus(sys.argv[2])
    elif sys.argv[1] == "set":
        fdb.setstatus(sys.argv[2], sys.argv[3])
