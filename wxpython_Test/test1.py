#! /usr/bin/env python2.7
#coding=utf-8

import wx

app = wx.App()
window = wx.Frame(None, title = 'wxpthon editor', size = (400, 300))
#panel = wx.Panel(window)
#label = wx.StaticText(panel, label='hallo world', pos = (100, 100))


#按钮
loadButton = wx.Button(window, label = 'open', pos = (0,0), size = (80,25))
saveButton = wx.Button(window, label = 'Save', pos = (80,0),size = (80,25))
fileName = wx.TextCtrl(window, pos = (160,0), size = (240,25))
fileContents = wx.TextCtrl(window, pos = (0,25), size = (400,275), style = wx.TE_MULTILINE | wx.HSCROLL)
#wx.TE_MULTILINE为多行文件 wx.HSCROLL为滚动条


window.Show(True)
app.MainLoop()
