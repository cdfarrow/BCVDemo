#
#   BCVDemo.py
#
#   A simple Wx app to demonstrate the SmartReferenceControl
#
#

import wx
from SmartReferenceControl import SmartReferenceControl

#----------------------------------------------------------- 

class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        fgs = wx.FlexGridSizer(cols=3, hgap=10, vgap=10)

        self.smartRef = SmartReferenceControl(self, size=(250,-1))
        self.smartRef.SetReferenceHandler(self.OnNewReference)
        fgs.Add(self.smartRef)
        fgs.Add((10,10))
        fgs.Add(wx.StaticText(self, -1, "SmartReferenceControl"))

        bs = wx.BoxSizer(wx.HORIZONTAL)

        btn1 = wx.Button(self, label="Previous")
        btn1.Bind(wx.EVT_BUTTON, self.OnPrevious)
        btn2 = wx.Button(self, label="Next")
        btn2.Bind(wx.EVT_BUTTON, self.OnNext)

        bs.Add(btn1)
        bs.Add((10, 10))
        bs.Add(btn2)

        fgs.Add(bs)
        fgs.Add((10, 10))
        fgs.Add((10, 10))

        self.refLogCtrl = wx.TextCtrl(self, size=(250,-1), style=wx.TE_MULTILINE)
        fgs.Add(self.refLogCtrl)
        fgs.Add((10,10))
        fgs.Add(wx.StaticText(self, -1, "<-- Event on ENTER"))

        box = wx.BoxSizer()
        box.Add(fgs, 1, wx.EXPAND|wx.ALL, 20)
        self.SetSizer(box)
        box.Fit(parent)

    def OnPrevious(self, evt):
        self.smartRef.PreviousChapter()

    def OnNext(self, evt):
        self.smartRef.NextChapter()

    def OnNewReference(self, evt):
        bk, ch = evt.Reference
        self.refLogCtrl.AppendText(f"Reference: {bk}[{ch}]\n")

#----------------------------------------------------------------------

class App(wx.App):
    
    def OnInit(self):
        frame = wx.Frame(None, -1, "SmartReferenceControl Demo")
        TestPanel(frame)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#------------------------------------------------------------------------
if __name__ == '__main__':
    app = App(False)
    app.MainLoop()


