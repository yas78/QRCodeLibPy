import wx

from FormMain import FormMain

app = wx.App()
form = FormMain(parent=None)
form.Show()
app.MainLoop()
