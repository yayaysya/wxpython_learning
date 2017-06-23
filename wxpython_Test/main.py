#!/usr/bin/env python
#coding=gbk

'''
    这是一个绘画软件,学习使用更多的wxpython建造部件
'''

import wx
import pickle
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class WindowMe(wx.Window):  #新建一个对象Window,继承自wx.Window 只是单独拿出来方便重复使用,不用在意,就当FRAME用
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1, (0,0), (300,300), name='WindowMe')
        self.SetBackgroundColour('White')

        self.lines=[]
        self.curLine=[]  #提前声明, 防止下面使用的时候没有创建
        self.pos = (0,0)

        self.color = 'Blue'
        self.thickness = 10  #笔的宽度width
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)  #wx.SOLID为笔的类型

        self.InitBuffer()

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaintEvent)

    def InitBuffer(self):
        size = self.GetClientSize() #当前控件的尺寸
        #创建一个缓存的设备上下文
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer) #wx.BufferedDC： 缓冲使你能够发送单独的绘制命令到缓冲区，然后一次性地把它们绘制到屏幕
        #使用设备上下文
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        # self.DrawLines(dc)：当由于尺寸改变（和由于从文件载入）init的时候, 要还原回去之前的绘画数据
        # 这里，我们遍历存储在实例变量self.lines中行的列表，为每行重新创建画笔，
        # 然后根据坐标绘制每一条线。

        self.reInitBuffer = False  #每次空闲操作执行init之后, 要把该标志置为false

    def SetColour(self, colour):
        self.color = colour
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:  #原因:自己定义了尺寸改变的动作会导致init, 所以之前画的线条存在lines中,init的时候还原
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def OnLeftDown(self, event):
        self.curLine = []  #按下鼠标的时候初始化line,猜想应该是线的轨迹
        self.pos = event.GetPositionTuple() #得到鼠标的位置
        self.CaptureMouse()  #???

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color, self.thickness,self.curLine)) #鼠标放开的时候把轨迹和属性填充到lines
            self.curLine = []
            self.ReleaseMouse()

    def OnMotion(self, event):   #motion是鼠标只要移动就会触发
        if event.Dragging() and event.LeftIsDown():  #鼠标在拖动的时候循环执行下面的语句
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.drawMotion(dc, event)
        event.Skip()

    def drawMotion(self, dc, event):   #绘制点到画布上
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()  #获得鼠标的位置,猜测应该是偏移值
        coords = self.pos + newPos
        self.curLine.append(coords)  #鼠标的位置保存到curLine中
        dc.DrawLine(*coords)    #画鼠标位置的点
        self.pos = newPos

    def OnPaintEvent(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)  #利用PaintDC及其子类可以对设备上下文图像及时刷新

    def OnSize(self,event):
        self.reInitBuffer = True

    def OnIdle(self, event):  #无操作的时候就会触发该命令, 只是在OnSize之后,标志被改变就会进行initBuffer()
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)  #加不加都可,默认不刷新屏幕

    def SetLinesData(self,lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()   #现在的问题是打开文件之后,图像没有立即刷新

class FrameMe(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, 'FrameMe', pos=(0,0), size=(400,400))
        self.winme = WindowMe(self)  #self-->parent
        self.InitStatusBar()
        self.InitMenuBar()

        self.winme.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def InitStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)           ##表示状态栏有两栏
        self.statusbar.SetStatusWidths([-3,-1])  #表示状态栏比例为3:1

    def InitMenuBar(self):
        self.filename = None
        """
        FileMenu = wx.Menu()
        FileMenuOpen = FileMenu.Append(-1, '打开', '打开文件')
        FileMenuSave = FileMenu.Append(-1, '保存', '保存文件')
        FileMenuSaveAs = FileMenu.Append(-1, '另存为', '另存为文件')
        FileMenu.AppendSeparator()
        FileMenuExit = FileMenu.Append(-1, '退出', '退出程序')
        self.Bind(wx.EVT_MENU, self.OnFileMenuOpen, FileMenuOpen)
        self.Bind(wx.EVT_MENU, self.OnFileMenuSave, FileMenuSave)
        self.Bind(wx.EVT_MENU, self.OnFileMenuSaveAs, FileMenuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnFileMenuExit, FileMenuExit)

        EditMenu = wx.Menu()
        EditMenuColor = EditMenu.Append(-1, '颜色', '画笔颜色')
        self.Bind(wx.EVT_MENU, self.OnEditMenuColor, EditMenuColor)

        HelpMenu = wx.Menu()
        HelpMenuAbout = HelpMenu.Append(-1, '关于', '关于作者')
        self.Bind(wx.EVT_MENU, self.OnHelpMenuAbout, HelpMenuAbout)

        PaintMenuBar = wx.MenuBar()
        PaintMenuBar.Append(FileMenu, '文件')
        PaintMenuBar.Append(EditMenu, '编辑')
        PaintMenuBar.Append(HelpMenu, '帮助')
        self.SetMenuBar(PaintMenuBar)  #为框架frame添加MenuBar
        """

        PaintMenuBar = wx.MenuBar()
        tree = ET.ElementTree(file='menu.xml')
        root = tree.getroot()
        for RootSon in root:
            TmpMenu = wx.Menu()
            for RootSonSon in RootSon:
                TmpMenuSon = TmpMenu.Append(-1, RootSonSon.text, RootSonSon.text)
                TmpFun = self.GetFunName(str(RootSonSon.attrib['bind']))
                self.Bind(wx.EVT_MENU, TmpFun, TmpMenuSon)
            PaintMenuBar.Append(TmpMenu, RootSon.attrib['name'])
        self.SetMenuBar(PaintMenuBar)

    def GetFunName(self, NameString):
        Str2FunName = {
            'OnFileMenuOpen':self.OnFileMenuOpen,
            'OnFileMenuSave':self.OnFileMenuSave,
            'OnFileMenuSaveAs':self.OnFileMenuSaveAs,
            'OnFileMenuExit':self.OnFileMenuExit,
            'OnEditMenuColor':self.OnEditMenuColor,
            'OnHelpMenuAbout': self.OnHelpMenuAbout,
        }
        return Str2FunName[NameString]


    def OnFileMenuOpen(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', style = wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:  #dlg.ShowModal()用于显示选取文件的窗口, 返回wx.ID_OK/wx.ID_CANCEL----> 打开/取消
            self.filename = dlg.GetPath()  #dlg.GetPath()用于获取文件名
            print self.filename
            self.ReadFile()
        dlg.Destroy()

    def ReadFile(self):
        if self.filename:
            try:
                self.fp = open(self.filename, 'rb+')
                data = pickle.load(self.fp)
                self.winme.SetLinesData(data)
                self.fp.close()
            except:
                wx.MessageBox('%s is not a legal file'%self.filename)

    def SaveFile(self):
        if self.filename:
            try:
                self.fp = open(self.filename, 'wb+')
                #self.fp.write(str(self.winme.lines))
                pickle.dump(self.winme.lines, self.fp)
                self.fp.close()
            except:
                wx.MessageBox('can\'t write to %s'%self.filename)

    def OnFileMenuSave(self, event):
        if self.filename:
            self.SaveFile()
        else:
            self.OnFileMenuSaveAs(event)

    def OnFileMenuSaveAs(self,event):
        #打开文件夹
        dlg_save = wx.FileDialog(self, 'Save a file', style = wx.SAVE)
        if dlg_save.ShowModal() == wx.ID_OK:  #跟之前打开的类似
            self.filename = dlg_save.GetPath()
            self.SaveFile()
        dlg_save.Destroy()

    def OnFileMenuExit(self, event):
        self.Close()

    def OnHelpMenuAbout(self, event):
        wx.MessageBox('Author : SongShouli')

    def OnMouseMotion(self, event):
        self.statusbar.SetStatusText('Pos:%s'%str(event.GetPositionTuple()), 0)
        self.statusbar.SetStatusText('Lines:%s'%len(self.winme.lines), 1)
        event.Skip()  #保证OnMotion绘画函数被触发, 去掉就会导致绘画不进行了 ,不过很奇怪,不是应该是上层容器吗, 应该是绘画触发,但是这个不触发
        #不对, 他们是在同一层容器里面的, 所以应该触发一个, 可能是先写的那个吧, 自己之后再验证...

    #EDIT

    def OnEditMenuColor(self, event):  #颜色窗口和文件窗口类似, 就是颜色需要通过GetColourData()函数来获取
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.winme.SetColour(dlg.GetColourData().GetColour())  #使用dlg.GetColourData().GetColour()来获取颜色
        dlg.Destroy()

def main():
    app = wx.App()
    frame = FrameMe(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()