#!/usr/bin/env python2.7
#coding=utf-8

import wx

class Frame(wx.Frame):       #扩展wx.Frame类,更容易控制外观
    def __init__(self,image,parent=None,id = -1, pos = wx.DefaultPosition,title = 'hallo,wxpython'):
        temp = image.ConvertToBitmap()    #转换为位图,适应StaticBitmap的需要
        size = temp.GetWidth(), temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,size)     #创建一个图片大小的框架
        self.bmp = wx.StaticBitmap(parent = self,bitmap = temp)

class App(wx.App):          #将导入的wx.App模块子类化
    def OnInit(self):       #OnInit函数会在程序启动的时候被wx.App自动调用
        image = wx.Image('E:\\wx.png',wx.BITMAP_TYPE_PNG)
        self.frame = Frame(image)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App() #创建一个App实例
    app.MainLoop() #进入主事件循环

if __name__ == '__main__':
    main()