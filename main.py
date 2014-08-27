import wx
import random
from math import *
import math as m
 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt
 
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()

    def plot(self):
        data = []
        if functype == 'sin':
            x = 0
            gcolor = 'r-'
            while x <= 5*pi:
                data.append((a*m.sin(x*k)+shiftx)+shifty)
                x += 0.01
        elif functype == 'cos':
            x = -5*pi
            gcolor = 'b-'
            while x <= 5*pi:
                data.append((a*m.cos(x*k)+shiftx)+shifty)
                x += 0.01
        elif functype == 'tg':
            x = -5*pi
            gcolor = 'g-'
            while x <= 5*pi:
                data.append((a*m.tan(x*k)+shiftx)+shifty)
                x += 0.01
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.set_autoscalex_on(False)
        ax.set_xscale('linear')
        ax.set_xlim(xmin=0, xmax=5)
        ax.plot(data, gcolor)
        ax.grid()
        ax.axis('tight')
        self.canvas.draw()    
       
 
class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.p1,self.p2,470)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Wow")

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(10,15), label='Type:')
        self.functypeenter = wx.TextCtrl(self.p2, -1, size=(40,30), pos=(50,10), value='sin')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(95,15), label='a:')
        self.amplitudeenter = wx.TextCtrl(self.p2, -1, size=(40,30), pos=(110,10), value='1')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(155,15), label='k:')
        self.ciclycfreqenter = wx.TextCtrl(self.p2, -1, size=(40,30), pos=(170,10), value='1')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(215,15), label='shiftx:')
        self.shiftxenter = wx.TextCtrl(self.p2, -1, size=(40,30), pos=(260,10), value='0')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(305,15), label='shifty:')
        self.shiftyenter = wx.TextCtrl(self.p2, -1, size=(40,30), pos=(350,10), value='0')
         
        self.plotbut = wx.Button(self.p2,-1,"Plot", size=(60,30),pos=(400,10))
        self.plotbut.Bind(wx.EVT_BUTTON,self.plot)
         
        self.sibut = wx.Button(self.p2,-1,"Zoom", size=(60,30),pos=(10,40))
        self.sibut.Bind(wx.EVT_BUTTON,self.zoom)
         
        self.hmbut = wx.Button(self.p2,-1,"Home", size=(60,30),pos=(70,40))
        self.hmbut.Bind(wx.EVT_BUTTON,self.home)
         
        self.hibut = wx.Button(self.p2,-1,"Pan", size=(60,30),pos=(130,40))
        self.hibut.Bind(wx.EVT_BUTTON,self.pan)
         
    def zoom(self,event):
        self.statusbar.SetStatusText("Zoom")
        self.p1.toolbar.zoom()
 
    def home(self,event):
        self.statusbar.SetStatusText("Home")
        self.p1.toolbar.home()
         
    def pan(self,event):
        self.statusbar.SetStatusText("Pan")
        self.p1.toolbar.pan()
 
    def plot(self,event):
        global functype, a, k, shiftx, shifty
        functype = str(self.functypeenter.GetValue())
        a = float(self.amplitudeenter.GetValue())
        k = float(self.ciclycfreqenter.GetValue())
        shiftx = float(self.shiftxenter.GetValue())
        shifty = float(self.shiftyenter.GetValue())
        self.p1.plot()       
 
app = wx.App(redirect=False)
frame = TestFrame(None,"Matplotlib and WxPython with Pan/Zoom functionality")
frame.Show()
app.MainLoop()
