#!/usr/bin/env python
# coding=gbk

import wx

class Frame(wx.Frame):
    def __init__(self,parent,id,pos,size):
        wx.Frame.__init__(self, parent, id, 'frame with dialog', pos, size=(400, 400)) #参数的传递按照顺序
        self.panel = wx.Panel(self,-1)
        self.button = wx.Button(self.panel, -1, '不要点我', pos = (200,200), size=(80,40))
        self.Bind(wx.EVT_BUTTON, self.OnClickMe2, self.button) #将wx.EVT_BUTTON改为wx.EVT_LEFT_DOWN是不行的, 'module' object has no attribute 'EVT_LEFT_BUTTON'
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.button.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.button.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.button.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
        self.button.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)


    def OnClickMe(self,event):    #把上面的OnClickMe2改为OnClickMe就执行这段代码,这段是用于测试dlg的
        dlg = wx.MessageDialog(None,'Can you tell me your name?','MessageMe',wx.YES_NO|wx.ICON_INFORMATION)
        dlg_input = wx.TextEntryDialog(None, 'Please inter your name','Name', 'Shaw Song')
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            dlg.Destroy()
            result_input = dlg_input.ShowModal()
            if result_input == wx.ID_OK:
                print dlg_input.GetValue()
            dlg_input.Destroy()
        else:
            print 'Thank you ',result, wx.ID_YES
    def OnClickMe2(self,event):
        self.panel.SetBackgroundColour('Green')
        self.panel.Refresh()

    def OnCloseWindow(self,event):
        self.Destroy()

    def OnEnterWindow(self,event):
        self.button.SetLabel('点我啊')

    def OnLeaveWindow(self,event):
        self.button.SetLabel('不要点我')

    def OnLeftDown(self,event):
        self.button.SetLabel('左键点击')
        self.panel.SetBackgroundColour('Yellow')
        self.panel.Refresh()
        event.Skip()  #经过试验发现如果不加这句就不执行单独点击的命令代码(变绿色代码)

    def OnRightDown(self,event):
        self.button.SetLabel('右键点击')
        self.panel.SetBackgroundColour('Red')
        self.panel.Refresh()
        event.Skip()


def main():
    app = wx.App()
    frame = Frame(parent=None, id=-1, pos=(0,0), size=(500,500))
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()