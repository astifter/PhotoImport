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
This modules handles exif data for files.
"""

import os
import datetime

try:
    import pyexiv2
    hasPyExif2=True
except:
    hasPyExif2=False

if not hasPyExif2:
    try:
        import EXIF
        hasEXIF=True
    except:
        hasEXIF=False


import sys
import stat
import subprocess

import wx
import io
import logging


hasExifTool=False
exiftool_name = 'exiftool.exe'
if hasattr(sys, 'frozen'):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
exiftool_path = os.path.join(application_path, exiftool_name)

try:
    statinfo = os.stat(exiftool_path)
    if (statinfo[stat.ST_MODE] & stat.S_IXUSR) > 0:
        hasExifTool=True
except:
    pass


def getfiledate(filename):
    filedate = None

    if hasPyExif2:
        exif = pyexiv2.ImageMetadata(filename)
        exif.read()
        try:
            filedate = exif['Exif.Photo.DateTimeOriginal'].value
        except:
            filedate = exif['Exif.Photo.DateTime'].value
    elif hasEXIF:
        f = open(filename,'rb')
        exif = EXIF.process_file(f, details=False)
        try:
            filedatestr = exif['EXIF DateTimeOriginal']
        except:
            filedatestr = exif['EXIF DateTimeDigitized']
        filedate = datetime.datetime.strptime(str(filedatestr),"%Y:%m:%d %H:%M:%S")
    elif hasExifTool:
        filedatestr = subprocess.Popen([exiftool_path,"-b","-DateTimeOriginal",filename],stdout=subprocess.PIPE).communicate()[0]
        filedate = datetime.datetime.strptime(filedatestr,"%Y:%m:%d %H:%M:%S")

    return filedate


def getthumbnail(imagename):
    imagedata = None

    if hasPyExif2:
        try:
            exif = pyexiv2.ImageMetadata(imagename)
            exif.read()
        except:
            logging.error("Can not read EXIF info from file %s, no preview." % imagename)
            return

        imagetype = ""
        if exif.mime_type == 'image/jpeg' or exif.mime_type == 'image/png':
            try:
                filereader = open(imagename,"rb")
                data = filereader.read()
                filereader.close()
            except:
                logging.error("Can not read file %s, no preview." % imagename)
                return
            imagetype = exif.mime_type
        else:
            try:
                data = exif.previews[-1].data
            except:
                logging.error("Can not read EXIF preview from file %s, no preview." % imagename)
                return
            imagetype = 'image/jpeg'
    elif hasEXIF:
        try:
            f = open(imagename,'rb')
            exif = EXIF.process_file(f, details=False)
            data = exif['JPEGThumbnail']
            imagetype = 'image/jpeg'
        except:
            logging.error("Can not read file %s, no preview." % imagename)
            return
    elif hasExifTool:
        try:
            data = subprocess.Popen([exiftool_path,"-b","-ThumbnailImage",imagename],stdout=subprocess.PIPE).communicate()[0]
            imagetype = 'image/jpeg'
        except:
            pass

    try:
        if imagetype == 'image/jpeg':
            imagedata = wx.ImageFromStream(io.BytesIO(data), wx.BITMAP_TYPE_JPEG)
        elif imagetype == 'image/png':
            imagedata = wx.ImageFromStream(io.BytesIO(data), wx.BITMAP_TYPE_PNG)
    except:
        logging.error("Can not convert image %s with type %s, no preview." % (imagename, imagetype))

    return imagedata
