#!/usr/bin/env python
#coding=gbk

'''
    ����һ���滭���,ѧϰʹ�ø����wxpython���첿��
'''

import wx
import pickle
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class WindowMe(wx.Window):  #�½�һ������Window,�̳���wx.Window ֻ�ǵ����ó��������ظ�ʹ��,��������,�͵�FRAME��
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1, (0,0), (300,300), name='WindowMe')
        self.SetBackgroundColour('White')

        self.lines=[]
        self.curLine=[]  #��ǰ����, ��ֹ����ʹ�õ�ʱ��û�д���
        self.pos = (0,0)

        self.color = 'Blue'
        self.thickness = 10  #�ʵĿ��width
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)  #wx.SOLIDΪ�ʵ�����

        self.InitBuffer()

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaintEvent)

    def InitBuffer(self):
        size = self.GetClientSize() #��ǰ�ؼ��ĳߴ�
        #����һ��������豸������
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer) #wx.BufferedDC�� ����ʹ���ܹ����͵����Ļ��������������Ȼ��һ���Եذ����ǻ��Ƶ���Ļ
        #ʹ���豸������
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        # self.DrawLines(dc)�������ڳߴ�ı䣨�����ڴ��ļ����룩init��ʱ��, Ҫ��ԭ��ȥ֮ǰ�Ļ滭����
        # ������Ǳ����洢��ʵ������self.lines���е��б�Ϊÿ�����´������ʣ�
        # Ȼ������������ÿһ���ߡ�

        self.reInitBuffer = False  #ÿ�ο��в���ִ��init֮��, Ҫ�Ѹñ�־��Ϊfalse

    def SetColour(self, colour):
        self.color = colour
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:  #ԭ��:�Լ������˳ߴ�ı�Ķ����ᵼ��init, ����֮ǰ������������lines��,init��ʱ��ԭ
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def OnLeftDown(self, event):
        self.curLine = []  #��������ʱ���ʼ��line,����Ӧ�����ߵĹ켣
        self.pos = event.GetPositionTuple() #�õ�����λ��
        self.CaptureMouse()  #???

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color, self.thickness,self.curLine)) #���ſ���ʱ��ѹ켣��������䵽lines
            self.curLine = []
            self.ReleaseMouse()

    def OnMotion(self, event):   #motion�����ֻҪ�ƶ��ͻᴥ��
        if event.Dragging() and event.LeftIsDown():  #������϶���ʱ��ѭ��ִ����������
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.drawMotion(dc, event)
        event.Skip()

    def drawMotion(self, dc, event):   #���Ƶ㵽������
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()  #�������λ��,�²�Ӧ����ƫ��ֵ
        coords = self.pos + newPos
        self.curLine.append(coords)  #����λ�ñ��浽curLine��
        dc.DrawLine(*coords)    #�����λ�õĵ�
        self.pos = newPos

    def OnPaintEvent(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)  #����PaintDC����������Զ��豸������ͼ��ʱˢ��

    def OnSize(self,event):
        self.reInitBuffer = True

    def OnIdle(self, event):  #�޲�����ʱ��ͻᴥ��������, ֻ����OnSize֮��,��־���ı�ͻ����initBuffer()
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)  #�Ӳ��Ӷ���,Ĭ�ϲ�ˢ����Ļ

    def SetLinesData(self,lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()   #���ڵ������Ǵ��ļ�֮��,ͼ��û������ˢ��

class FrameMe(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, 'FrameMe', pos=(0,0), size=(400,400))
        self.winme = WindowMe(self)  #self-->parent
        self.InitStatusBar()
        self.InitMenuBar()

        self.winme.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def InitStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)           ##��ʾ״̬��������
        self.statusbar.SetStatusWidths([-3,-1])  #��ʾ״̬������Ϊ3:1

    def InitMenuBar(self):
        self.filename = None
        """
        FileMenu = wx.Menu()
        FileMenuOpen = FileMenu.Append(-1, '��', '���ļ�')
        FileMenuSave = FileMenu.Append(-1, '����', '�����ļ�')
        FileMenuSaveAs = FileMenu.Append(-1, '���Ϊ', '���Ϊ�ļ�')
        FileMenu.AppendSeparator()
        FileMenuExit = FileMenu.Append(-1, '�˳�', '�˳�����')
        self.Bind(wx.EVT_MENU, self.OnFileMenuOpen, FileMenuOpen)
        self.Bind(wx.EVT_MENU, self.OnFileMenuSave, FileMenuSave)
        self.Bind(wx.EVT_MENU, self.OnFileMenuSaveAs, FileMenuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnFileMenuExit, FileMenuExit)

        EditMenu = wx.Menu()
        EditMenuColor = EditMenu.Append(-1, '��ɫ', '������ɫ')
        self.Bind(wx.EVT_MENU, self.OnEditMenuColor, EditMenuColor)

        HelpMenu = wx.Menu()
        HelpMenuAbout = HelpMenu.Append(-1, '����', '��������')
        self.Bind(wx.EVT_MENU, self.OnHelpMenuAbout, HelpMenuAbout)

        PaintMenuBar = wx.MenuBar()
        PaintMenuBar.Append(FileMenu, '�ļ�')
        PaintMenuBar.Append(EditMenu, '�༭')
        PaintMenuBar.Append(HelpMenu, '����')
        self.SetMenuBar(PaintMenuBar)  #Ϊ���frame���MenuBar
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
        if dlg.ShowModal() == wx.ID_OK:  #dlg.ShowModal()������ʾѡȡ�ļ��Ĵ���, ����wx.ID_OK/wx.ID_CANCEL----> ��/ȡ��
            self.filename = dlg.GetPath()  #dlg.GetPath()���ڻ�ȡ�ļ���
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
        #���ļ���
        dlg_save = wx.FileDialog(self, 'Save a file', style = wx.SAVE)
        if dlg_save.ShowModal() == wx.ID_OK:  #��֮ǰ�򿪵�����
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
        event.Skip()  #��֤OnMotion�滭����������, ȥ���ͻᵼ�»滭�������� ,���������,����Ӧ�����ϲ�������, Ӧ���ǻ滭����,�������������
        #����, ��������ͬһ�����������, ����Ӧ�ô���һ��, ��������д���Ǹ���, �Լ�֮������֤...

    #EDIT

    def OnEditMenuColor(self, event):  #��ɫ���ں��ļ���������, ������ɫ��Ҫͨ��GetColourData()��������ȡ
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.winme.SetColour(dlg.GetColourData().GetColour())  #ʹ��dlg.GetColourData().GetColour()����ȡ��ɫ
        dlg.Destroy()

def main():
    app = wx.App()
    frame = FrameMe(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()