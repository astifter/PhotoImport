#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Nov  7 01:10:24 2010

import wx
from ConfigFrame import ConfigFrame

class PhotoImport(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        cfgfrm = ConfigFrame(None, -1, "")
        self.SetTopWindow(cfgfrm)
        cfgfrm.Show()
        return 1

# end of class PhotoImport

if __name__ == "__main__":
    PhotoImport = PhotoImport(0)
    PhotoImport.MainLoop()