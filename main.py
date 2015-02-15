# -*- coding: utf-8 -*-
import wx
import wx.html as html
from math import *
import math as m
from pylab import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt
import os
import wx.lib.agw.multidirdialog as MDD
 
wildcard = "PNG Image (*.png)|*.png|" \
            "All files (*.*)|*.*"
#declare list of functions
global functypes, functype, plotcolors, plotcolor
functypes = ['sin', 'cos', 'tg', 'ctg','arcsin','arccos','arctg','arcctg']
plotcolors = ['red','blue','green','yellow','cyan','black']
functype = ['sin']
plotcolor = ['red']

class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()

    def plot(self):
        #set size of the axes ticks
        matplotlib.rc('xtick', labelsize=14)
        matplotlib.rc('ytick', labelsize=14)
        #set limit of the plotting
        x = np.linspace((-2*m.pi), (2 * m.pi), 256,endpoint=True)
        if functype[0] == 'sin': data = (a*np.sin(x*k)+shiftx)+shifty
        elif functype[0] == 'cos': data = (a*np.cos(x*k)+shiftx)+shifty
        elif functype[0] == 'tg': data = (a*np.tan(x*k)+shiftx)+shifty
        elif functype[0] == 'ctg': data = (a*(1/np.tan(x*k))+shiftx)+shifty
        elif functype[0] == 'arcsin': data = (a*np.arcsin(x*k)+shiftx)+shifty
        elif functype[0] == 'arccos': data = (a*np.arccos(x*k)+shiftx)+shifty
        elif functype[0] == 'arctg': data = (a*np.arctan(x*k)+shiftx)+shifty
        elif functype[0] == 'arcctg': data = (a*(1/np.arctan(x*k))+shiftx)+shifty
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        #plotting
        ax.plot(x, data, plotcolor[0], linewidth=2, 
            label=functype[0]+'(x)\na: '+str(int(a))+'\nk: '+str(int(k))+'\nshiftx: '+str(int(shiftx))+'\nshifty: '+str(int(shifty)))
        #adding legend
        legend(loc='upper left',prop={'size':10})
        #setting ticks
        ax = gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data',0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data',0))
        xlim(x.min()*1.1, x.max()*1.1)
        xticks([(-2 * m.pi), (-3 * m.pi/2), -m.pi, -m.pi/2, 0, m.pi/2, m.pi, (3 * m.pi/2), (2 * m.pi)], 
            [r'$-2\pi$', r'$-\frac{3}{2\pi}$', r'$-\pi$', r'$-\frac{\pi}{2}$', r'$0$', r'$+\frac{\pi}{2}$', 
            r'$+\pi$', r'$+\frac{3}{2\pi}$', r'$+2\pi$'])
        ylim(-4, 4)
        yticks([-5, -4, -3, -2, -1, +1, +2, +3, +4, +5], 
            [r'$-5$', r'$-4$', r'$-3$', r'$-2$', r'$-1$', r'$+1$', r'$+2$', r'$+3$', r'$+4$', r'$+5$'])
        #enable grid
        ax.grid()
        #draw
        self.canvas.draw()    
       
 
class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(645,620), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.icon = wx.Icon('images/app-icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.currentDirectory = os.getcwd()
        self.colourData = None
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.p1,self.p2,470)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Wow")

        fist_row_elements_size = [60,20,90,100,110]
        """ [0] - width 60
            [1] - height 30
            [2] - width 90
            [3] - width 100
            [4] - width 110 """

        first_row_elements_pos = []

        second_row_elements_size = [40,20,60]
        """ [0] - width 40
            [1] - height 30
            [2] - width 60 """

        second_row_elements_pos = []

        self.sibut = wx.Button(self.p2,-1,"Zoom",size=(fist_row_elements_size[0],fist_row_elements_size[1]),pos=(10,10))
        self.sibut.Bind(wx.EVT_BUTTON,self.zoom)

        self.hibut = wx.Button(self.p2,-1,"Pan",size=(fist_row_elements_size[0],fist_row_elements_size[1]),pos=(70,10))
        self.hibut.Bind(wx.EVT_BUTTON,self.pan)
         
        self.hmbut = wx.Button(self.p2,-1,"Home",size=(fist_row_elements_size[0],fist_row_elements_size[1]),pos=(130,10))
        self.hmbut.Bind(wx.EVT_BUTTON,self.home)

        # self.addgraphbut = wx.Button(self.p2,-1,'Add Graph',size=(fist_row_elements_size[2],fist_row_elements_size[1]),pos=(190,10))

        # self.delgraphbut = wx.Button(self.p2,-1,'Delete Graph',size=(fist_row_elements_size[4],fist_row_elements_size[1]),pos=(280,10))

        self.plotbut = wx.Button(self.p2,-1,"Plot", size=(second_row_elements_size[2],
            second_row_elements_size[1]),pos=(390,10))
        self.plotbut.Bind(wx.EVT_BUTTON,self.plot)

        self.savebut = wx.Button(self.p2, -1, "Save Graph", size=(fist_row_elements_size[3],fist_row_elements_size[1]), pos=(520,10))
        self.savebut.Bind(wx.EVT_BUTTON,self.savegraph)

        self.functypeentername = wx.StaticText(self.p2,-1,pos=(10,50),label='Type:')
        self.typepick = wx.Choice(self.p2, -1, pos=(50,45), choices=functypes)
        self.Bind(wx.EVT_CHOICE,self.typepicker,self.typepick)

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(130,50), label='a:')
        self.amplitudeenter = wx.TextCtrl(self.p2, -1, size=(second_row_elements_size[0],
            second_row_elements_size[1]), pos=(145,45), value='1')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(190,50), label='k:')
        self.ciclycfreqenter = wx.TextCtrl(self.p2, -1, size=(second_row_elements_size[0],
            second_row_elements_size[1]), pos=(205,45), value='1')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(250,50), label='shiftx:')
        self.shiftxenter = wx.TextCtrl(self.p2, -1, size=(second_row_elements_size[0],
            second_row_elements_size[1]), pos=(295,45), value='0')

        self.functypeentername = wx.StaticText(self.p2, -1, pos=(340,50), label='shifty:')
        self.shiftyenter = wx.TextCtrl(self.p2, -1, size=(second_row_elements_size[0],
            second_row_elements_size[1]), pos=(385,45), value='0')

        self.functypeentername = wx.StaticText(self.p2,-1,pos=(430,50),label='Color:')
        self.colorpick = wx.Choice(self.p2, -1, pos=(460,45), choices=plotcolors)
        self.Bind(wx.EVT_CHOICE,self.colorpicker,self.colorpick)

        filemenu = wx.Menu()
        helpmenu = wx.Menu()

        menuExit = filemenu.Append(wx.ID_EXIT, '&Exit', 'Terminate the program')
        menuHelp = helpmenu.Append(wx.ID_HELP,'&Help', 'Help with usage of this program')
        menuChangelog = helpmenu.Append(wx.ID_ANY, '&Changelog', '')
        menuAbout = helpmenu.Append(wx.ID_ABOUT, '&About', 'Information about this program')

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, '&File')
        menuBar.Append(helpmenu, '&Help')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnChange, menuChangelog)
         
         
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
        self.statusbar.SetStatusText("Plot")
        global functype, a, k, shiftx, shifty
        a = float(self.amplitudeenter.GetValue())
        k = float(self.ciclycfreqenter.GetValue())
        shiftx = float(self.shiftxenter.GetValue())
        shifty = float(self.shiftyenter.GetValue())
        self.p1.plot()

    def savegraph(self, event):
        savedlg = wx.FileDialog(
            self, message="Save graph as ...", 
            defaultDir=self.currentDirectory, 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        if savedlg.ShowModal() == wx.ID_OK:
            path = savedlg.GetPath()
            plt.savefig(path, dpi=200)
        savedlg.Destroy()
        
    def typepicker(self,event):
        """This function picks type of function"""
        del functype[0]
        functype.insert(0,str(self.typepick.GetStringSelection()))

    def colorpicker(self,event):
        """This function picks type of function"""
        del plotcolor[0]
        plotcolor.insert(0,str(self.colorpick.GetStringSelection()))

    def OnAbout(self, e):
        
        description = """TrigPlot is an application for plotting Trigonometry
functions graphics for the Unix  and Windows operating systems. """

        licence = """TrigPlot is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

TrigPlot is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA"""

        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('images/about-icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('TrigPlot')
        info.SetVersion('1.3')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 Timur Mayzenberg')
        info.SetWebSite('https://github.com/murych/trigfuncplotter')
        info.SetLicence(licence)
        info.AddDeveloper('Timur Mayzenberg')

        wx.AboutBox(info)

    def OnHelp(self, e):
        help_window = HelpWindow(None,'Help',wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.CAPTION)
        help_window.Show()

    def OnChange(self, e):
        changelog_window = ChangelogWindow(None,'Help',wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.CAPTION)
        changelog_window.Show()

    #exit
    def OnExit(self, e):
        self.Close(True)    

help_page_html = '<h1>TrigPlot Help</h1>\
<p><img alt="" src="images/help-image.png" /></p>\
<ol>\
    <li>Amplitude</li>\
    <li>Function type (sin, cos, ect.)</li>\
    <li>Cycliq Frequency</li>\
    <li>Shift on OX</li>\
    <li>Shift on OY</li>\
</ol>\
<p>Enter parametrs of your graphic into text input fields and press &quot;<strong>Plot</strong>&quot; button.</p>\
<p>Use &quot;<strong>Zoom</strong>&quot; button to select area You want to zoom.</p>\
<p>Use &quot;<strong>Pan</strong>&quot; button to navigate through Your plot.</p>\
<p>Use &quot;<strong>Home</strong>&quot; button to restore the default view.</p>\
<p>Use &quot;<strong>Add Graph</strong>&quot; button to add and &quot;<strong>Delete Graph</strong>&quot; to delete additional graphs.</p>\
<p>Use &quot;<strong>Save Graph</strong>&quot; button to save Your plot as an image.</p>'

changelog_page_html = '<h1>Changelog</h1>\
<ul>\
    <li><strong>Version 1.3</strong>\
    <ul>\
        <li>improved file saving dialog, now You can choose location to save Your graph</li>\
        <li>added additional variables into legend</li>\
    </ul>\
    </li>\
    <li><strong>Version 1.2</strong>\
    <ul>\
        <li>added&nbsp;<em>Changelog&nbsp;</em>section</li>\
        <li>added color picker for graphs: red, blue, green, yellow, cyan and black</li>\
        <li>moved <em>Plot</em> button</li>\
    </ul>\
    </li>\
    <li><strong>Version 1.1</strong>\
    <ul>\
        <li>added <em>Help</em> section</li>\
        <li>added new&nbsp;<em>About</em>&nbsp;sectidon</li>\
    </ul>\
    </li>\
    <li><b>Version 1.0</b>\
    <ul>\
        <li>added 4 new functions: arcsin, arccos, arctg, arcctg</li>\
        <li>change types of functions with drop-down menu</li>\
        <li>axis tips are shown as fractions</li>\
        <li>added ability to save plot as <em>.png&nbsp;</em>file in program&#39;s directory</li>\
        <li>added project&#39;s home page on GitHub in <em>About&nbsp;</em>menu</li>\
        <li>removed sample pic</li>\
    </ul>\
    </li>\
    <li><strong>Version 0.1</strong>\
    <ul>\
        <li>plotting 4 types of functions: sin, cos, tg, ctg</li>\
        <li>zoomig, pan, restore default view</li>\
        <li>change types of functions by typing their names</li>\
        <li>sample pic above input section</li>\
    </ul>\
    </li>\
</ul>'

class HelpWindow(wx.Frame):
    def __init__(self,parent,title,style):
        wx.Frame.__init__(self,parent,title=title,size=(450,400),style=style)
        help_panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        help_window_html = html.HtmlWindow(help_panel, -1)
        help_window_html.SetBackgroundColour(wx.RED)
        help_window_html.SetStandardFonts()
        help_window_html.SetPage(help_page_html)
        vbox.Add((-1,10),0)
        vbox.Add(help_window_html, 1, wx.EXPAND | wx.ALL, 9)
        help_panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)

class ChangelogWindow(wx.Frame):
    def __init__(self,parent,title,style):
        wx.Frame.__init__(self,parent,title=title,size=(450,400),style=style)
        changelog_panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        changelog_window_html = html.HtmlWindow(changelog_panel, -1)
        changelog_window_html.SetBackgroundColour(wx.RED)
        changelog_window_html.SetStandardFonts()
        changelog_window_html.SetPage(changelog_page_html)
        vbox.Add((-1,10),0)
        vbox.Add(changelog_window_html, 1, wx.EXPAND | wx.ALL, 9)
        changelog_panel.SetSizer(vbox)
        self.Centre()
        self.Show(True)
        

app = wx.App(redirect=False)
frame = TestFrame(None,"TrigPlot")
frame.Show()
app.MainLoop()
