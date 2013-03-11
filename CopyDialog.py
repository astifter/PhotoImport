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
The CopyDialog module shows a file list and the preview for each single day
and asks the user for a folder to put the files in.
"""
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Nov  6 17:17:06 2010

import wx

# begin wxGlade: dependencies
from ImagePanel import ImagePanel
# end wxGlade

# begin wxGlade: extracode

# end wxGlade


class CopyDialog(wx.Dialog):
    """ Shows the filelist, asks user for folder and shows previews. """

    def __init__(self, *args, **kwds):
        # begin wxGlade: CopyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.headerlbl = wx.TextCtrl(self, -1, "These files will be copied for date <date>:", style=wx.NO_BORDER)
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3D | wx.SP_BORDER)
        self.filelst = wx.ListCtrl(self.splitter, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.previewpane = ImagePanel(self.splitter, -1)
        self.destlbl = wx.StaticText(self, -1, "Dest. Folder")
        self.destvalue = wx.TextCtrl(self, -1, "")
        self.namelbl = wx.StaticText(self, -1, "Name Pattern")
        self.namevalue = wx.TextCtrl(self, -1, "")
        self.spacepanel1 = wx.Panel(self, -1)
        self.cancelbtn = wx.Button(self, wx.ID_CANCEL, "")
        self.neverbtn = wx.Button(self, -1, "&Never")
        self.okbtn = wx.Button(self, wx.ID_OK, "")
        self.gauge = wx.Gauge(self, -1, 100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.evt_filelst_select, self.filelst)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.evt_splitter_resize, self.splitter)
        self.Bind(wx.EVT_BUTTON, self.evt_cancelbtn, self.cancelbtn)
        self.Bind(wx.EVT_BUTTON, self.evt_neverbtn, self.neverbtn)
        self.Bind(wx.EVT_BUTTON, self.evt_okbtn, self.okbtn)
        # end wxGlade
        self.Bind(wx.EVT_SIZE, self.evt_splitter_resize, self)

        self.handler = None
        self.date = None

    def __set_properties(self):
        # begin wxGlade: CopyDialog.__set_properties
        self.SetTitle("Copy Files")
        self.SetSize((786, 620))
        self.headerlbl.SetMinSize((300, 27))
        self.filelst.SetMinSize((393, 473))
        self.destlbl.SetMinSize((100, 17))
        self.destvalue.SetMinSize((300, 27))
        self.destvalue.Enable(False)
        self.namelbl.SetMinSize((100, 17))
        self.namevalue.SetMinSize((300, 27))
        self.cancelbtn.SetMinSize((70, 29))
        self.neverbtn.SetMinSize((85, 29))
        self.okbtn.SetMinSize((100, 29))
        self.gauge.SetMinSize((100, 28))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CopyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.headerlbl, 1, wx.ALL, 4)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.splitter.SplitVertically(self.filelst, self.previewpane)
        sizer_1.Add(self.splitter, 1, wx.EXPAND, 0)
        sizer_3.Add(self.destlbl, 0, wx.ALL | wx.ALIGN_RIGHT, 8)
        sizer_3.Add(self.destvalue, 1, wx.ALL, 4)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.namelbl, 0, wx.ALL | wx.ALIGN_RIGHT, 8)
        sizer_4.Add(self.namevalue, 1, wx.ALL, 4)
        sizer_1.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_5.Add(self.spacepanel1, 1, wx.EXPAND, 0)
        sizer_5.Add(self.cancelbtn, 0, wx.ALL, 4)
        sizer_5.Add(self.neverbtn, 0, wx.ALL, 4)
        sizer_5.Add(self.okbtn, 0, wx.ALL, 4)
        sizer_1.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_6.Add(self.gauge, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_6, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def setconfig(self, config, date, files, handler, done, total):
        """ This gets all the configuration values and configures the UI. """
        self.date = date

        text = self.headerlbl.GetValue()
        text = text.replace("<date>", "%s (%d of %d)" % (date, done, total))
        self.headerlbl.SetValue(text)

        self.destvalue.SetValue(config.destvalue)

        self.namevalue.SetValue(config.foldernamevalue.replace("<date>", date))

        self.filelst.InsertColumn(0, "Name", width=wx.LIST_AUTOSIZE)
        for i in files.keys():
            self.filelst.InsertStringItem(100, i)
        self.filelst.SetColumnWidth(0, width=wx.LIST_AUTOSIZE)

        self.handler = handler

    def setprogress(self, value):
        self.gauge.SetValue(value*self.gauge.GetRange())
        wx.Yield()

    def showprogess(self, show=True):
        self.gauge.Show(show)
        wx.Yield()

    def evt_splitter_resize(self, event): # wxGlade: CopyDialog.<event_handler>
        """ Resizes the preview pane. """
        idx = self.filelst.GetFirstSelected()
        if idx != -1:
            self.previewpane.display(self.filelst.GetItemText(idx))
        event.Skip()

    def evt_filelst_select(self, event): # wxGlade: CopyDialog.<event_handler>
        """ Sets new picture to preview pane. """
        idx = self.filelst.GetFirstSelected()
        if idx != -1:
            self.previewpane.display(self.filelst.GetItemText(idx))
        event.Skip()

    def evt_cancelbtn(self, event): # wxGlade: CopyDialog.<event_handler>
        """ Closes the window. """
        self.Destroy()

    def evt_okbtn(self, event): # wxGlade: CopyDialog.<event_handler>
        """ Calls back the handler to actually copy the pictures. """
        self.handler(self.date, self.namevalue.GetValue(), True)
        self.Destroy()

    def evt_neverbtn(self, event): # wxGlade: CopyDialog.<event_handler>
        """ Calls back the handler to mark the file as never. """
        self.handler(self.date, self.namevalue.GetValue(), False)
        self.Destroy()

# end of class CopyDialog
