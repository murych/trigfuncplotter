import wx
from math import *
import math as m
from pylab import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt


class p1(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()

    def plot(self):
        x = np.linspace((-2 * m.pi), (2 * m.pi), 256, endpoint=True)
        functypes = ['sin', 'cos', 'tg', 'ctg']
        if functype in functypes:
            if functype == 'sin':
                data = (a * np.sin(x * k) + shiftx) + shifty
                gcolor = 'r-'
            elif functype == 'cos':
                data = (a * np.cos(x * k) + shiftx) + shifty
                gcolor = 'b-'
            elif functype == 'tg':
                data = (a * np.tan(x * k) + shiftx) + shifty
                gcolor = 'g-'
            elif functype == 'ctg':
                data = (a * (1 / np.tan(x * k)) + shiftx) + shifty
                gcolor = 'g-'
        else:
            wx.MessageBox('Incorrect function type', 'Error',
                          wx.OK | wx.ICON_ERROR)
        ax = self.figure.add_subplot(111)
        ax.hold(False)

        ax.plot(x, data, gcolor, linewidth=2, label=functype + '(x)')

        legend(loc='upper left')

        ax = gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        xlim(x.min() * 1.1, x.max() * 1.1)
        xticks([(-2 * m.pi), (-3 * m.pi / 2), -m.pi, -m.pi / 2, 0, m.pi / 2, m.pi, (3 * m.pi / 2), (2 * m.pi)],
               [r'$-2\pi$', r'$-3/2\pi$', r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$', r'$+3/2\pi$', r'$+2\pi$'])
        ylim(-4, 4)
        yticks([-5, -4, -3, -2, -1, +1, +2, +3, +4, +5], [r'$-5$', r'$-4$',
                                                          r'$-3$', r'$-2$', r'$-1$', r'$+1$', r'$+2$', r'$+3$', r'$+4$', r'$+5$'])

        ax.grid()

        self.canvas.draw()


class TestFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(645, 620), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU |
                          wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)

        self.sp.SplitHorizontally(self.p1, self.p2, 470)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Wow")

        examplepic = wx.Image("./ex.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.example = wx.StaticBitmap(
            self.p2, -1, examplepic, (10, 10), (examplepic.GetWidth(), examplepic.GetHeight()))

        self.functypeentername = wx.StaticText(
            self.p2, -1, pos=(10, 35), label='Type:')
        self.functypeenter = wx.TextCtrl(
            self.p2, -1, size=(40, 20), pos=(50, 30), value='sin')

        self.functypeentername = wx.StaticText(
            self.p2, -1, pos=(95, 35), label='a:')
        self.amplitudeenter = wx.TextCtrl(
            self.p2, -1, size=(40, 20), pos=(110, 30), value='1')

        self.functypeentername = wx.StaticText(
            self.p2, -1, pos=(155, 35), label='k:')
        self.ciclycfreqenter = wx.TextCtrl(
            self.p2, -1, size=(40, 20), pos=(170, 30), value='1')

        self.functypeentername = wx.StaticText(
            self.p2, -1, pos=(215, 35), label='shiftx:')
        self.shiftxenter = wx.TextCtrl(
            self.p2, -1, size=(40, 20), pos=(260, 30), value='0')

        self.functypeentername = wx.StaticText(
            self.p2, -1, pos=(305, 35), label='shifty:')
        self.shiftyenter = wx.TextCtrl(
            self.p2, -1, size=(40, 20), pos=(350, 30), value='0')

        self.plotbut = wx.Button(
            self.p2, -1, "Plot", size=(60, 20), pos=(400, 30))
        self.plotbut.Bind(wx.EVT_BUTTON, self.plot)

        self.sibut = wx.Button(
            self.p2, -1, "Zoom", size=(60, 20), pos=(10, 63))
        self.sibut.Bind(wx.EVT_BUTTON, self.zoom)

        self.hibut = wx.Button(self.p2, -1, "Pan", size=(60, 20), pos=(70, 63))
        self.hibut.Bind(wx.EVT_BUTTON, self.pan)

        self.hmbut = wx.Button(
            self.p2, -1, "Home", size=(60, 20), pos=(130, 63))
        self.hmbut.Bind(wx.EVT_BUTTON, self.home)

        self.savebut = wx.Button(
            self.p2, -1, "Save Graph", size=(100, 20), pos=(190, 63))
        self.savebut.Bind(wx.EVT_BUTTON, self.savegraph)

        filemenu = wx.Menu()

        menuAbout = filemenu.Append(
            wx.ID_ABOUT, '&About', 'Information about this program')
        menuExit = filemenu.Append(
            wx.ID_EXIT, '&Exit', 'Terminate the program')

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, '&File')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def zoom(self, event):
        self.statusbar.SetStatusText("Zoom")
        self.p1.toolbar.zoom()

    def home(self, event):
        self.statusbar.SetStatusText("Home")
        self.p1.toolbar.home()

    def pan(self, event):
        self.statusbar.SetStatusText("Pan")
        self.p1.toolbar.pan()

    def plot(self, event):
        self.statusbar.SetStatusText("Plot")
        global functype, a, k, shiftx, shifty
        functype = self.functypeenter.GetValue()
        a = float(self.amplitudeenter.GetValue())
        k = float(self.ciclycfreqenter.GetValue())
        shiftx = float(self.shiftxenter.GetValue())
        shifty = float(self.shiftyenter.GetValue())
        self.p1.plot()

    def savegraph(self, event):
        self.statusbar.SetStatusText('Save Graph')
        savefigdlg = wx.TextEntryDialog(
            self, 'Enter Graph Name', 'Saving Graph', 'graph1')
        if savefigdlg.ShowModal() == wx.ID_OK:
            graphname = savefigdlg.GetValue()
        elif savefigdlg.ShowModal() == wx.ID_CANCEL:
            savefigdlg.Destroy()
        plt.savefig(graphname + '.png')

    def OnAbout(self, e):
        dlg = wx.MessageDialog(
            self, "Trigonometry functions plotter by Timur Mayzenberg\nVersion 0.1", "About", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

app = wx.App(redirect=False)
frame = TestFrame(None, "Trigonometry functions plotter")
frame.Show()
app.MainLoop()
