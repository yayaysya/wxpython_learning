#!/usr/bin/env python
#coding=gbk

import wx
import wx.py.images as images

class Frame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent,id,'Frame with Button', size=(400,400))
        panel = wx.Panel(self)
        button = wx.Button(panel,label='Close',pos=(100,100), size=(50,50),)
        self.Bind(wx.EVT_BUTTON, self.OnCloseButton, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        frameColor = self.SetBackgroundColour('grey')
        statusBar = self.CreateStatusBar() #�ײ�״̬��
        toolbar = self.CreateToolBar() #�ڶ��й����� ��Ϊ��һ���ǲ˵���
        toolbar.AddSimpleTool(wx.NewId(), images.getPyBitmap(), '����', '����һ������Ĳ���')
        toolbar.Realize()
        #�˵���
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()

        menu1.Append(wx.NewId(),'New Preject','Create a new file')
        menu1.Append(wx.NewId(),'Close Project','Close the project')
        menu1.AppendSeparator()
        menu1.Append(wx.NewId(),'Setting','Setting')

        menu2.Append(wx.NewId(),'Cut','Cut to clipboard')
        menu2.Append(wx.NewId(),'Copy','Copy to clipboard')
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(),'Delete','Delete select items')

        menuBar.Append(menu1,'File')
        menuBar.Append(menu2,'Edit')
        self.SetMenuBar(menuBar)

    def OnCloseButton(self, event):
        self.Close(True) #�ر�frame���

    def OnCloseWindow(self, event):
        self.Destroy()
        print 'OnCloseWindow'

if __name__ == '__main__':
    app = wx.App()
    frame = Frame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
