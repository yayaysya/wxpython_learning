#!/usr/bin/env python


import wx
import sys

class Frame(wx.Frame):

    def __init__(self,parent, id,title,pos,size):
        print 'Frame init'
        wx.Frame.__init__(self,parent,id,title,pos,size)

class App(wx.App):
    def __init__(self, redirect=True,filename=None):
        print 'redirect=True'
        wx.App.__init__(self, redirect,filename)

    def OnInit(self):
        print 'OnInit'
        self.frame = Frame(parent=None,id=-1,title='Startup',pos=(0,0),size=(400,400))
        self.frame.Show()
        self.SetTopWindow(self.frame)
        print >>sys.stderr, "This is a error message"
        return True

    def OnExit(self):
        print 'OnExit'

if __name__ == '__main__':
    app = App(redirect=True)
    print "before MainLoop()"
    app.MainLoop()
    print 'after MainLoop'