#!/usr/bin/env python
# coding=gbk

import wx

class Frame(wx.Frame):
    def __init__(self,parent,id,pos,size):
        wx.Frame.__init__(self, parent, id, 'frame with dialog', pos, size=(400, 400)) #�����Ĵ��ݰ���˳��
        self.panel = wx.Panel(self,-1)
        self.button = wx.Button(self.panel, -1, '��Ҫ����', pos = (200,200), size=(80,40))
        self.Bind(wx.EVT_BUTTON, self.OnClickMe2, self.button) #��wx.EVT_BUTTON��Ϊwx.EVT_LEFT_DOWN�ǲ��е�, 'module' object has no attribute 'EVT_LEFT_BUTTON'
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.button.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.button.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.button.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
        self.button.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)


    def OnClickMe(self,event):    #�������OnClickMe2��ΪOnClickMe��ִ����δ���,��������ڲ���dlg��
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
        self.button.SetLabel('���Ұ�')

    def OnLeaveWindow(self,event):
        self.button.SetLabel('��Ҫ����')

    def OnLeftDown(self,event):
        self.button.SetLabel('������')
        self.panel.SetBackgroundColour('Yellow')
        self.panel.Refresh()
        event.Skip()  #�������鷢������������Ͳ�ִ�е���������������(����ɫ����)

    def OnRightDown(self,event):
        self.button.SetLabel('�Ҽ����')
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