'''
Created on Oct 22, 2015

@author: peterp
'''

from Tkinter import *
import matplotlib
import math

from numpy import frompyfunc
from PartProperty import PartPropertyDelay
from Files import *

from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

if not 'matplotlib.backends' in sys.modules:
    matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from matplotlib.figure import Figure

class ViewerProperty(Frame):
    def __init__(self,parentFrame,partProperty,callBack):
        Frame.__init__(self,parentFrame)
        self.pack(side=TOP,fill=X,expand=YES)
        self.parentFrame=parentFrame
        self.partProperty=partProperty
        self.callBack=callBack
        self.pack(side=TOP,fill=X,expand=YES)
        self.propertyString=StringVar(value=str(self.partProperty.PropertyString(stype='entry')))
        propertyLabel = Label(self,width=25,text=self.partProperty.description+': ',anchor='e')
        propertyLabel.pack(side=LEFT, expand=NO, fill=X)
        propertyEntry = Entry(self,textvariable=self.propertyString)
        propertyEntry.config(width=15)
        propertyEntry.bind('<Return>',self.onEntered)
        propertyEntry.bind('<FocusIn>',self.onTouched)
        propertyEntry.bind('<Button-3>',self.onUntouched)
        propertyEntry.bind('<Escape>',self.onUntouched)
        propertyEntry.bind('<FocusOut>',self.onUntouched)
        propertyEntry.pack(side=LEFT, expand=YES, fill=X)
    def onEntered(self,event):
        self.partProperty.SetValueFromString(self.propertyString.get())
        self.onUntouched(event)
    def onTouched(self,event):
        self.propertyString.set('')
    def onUntouched(self,event):
        self.propertyString.set(self.partProperty.PropertyString(stype='entry'))
        self.callBack()
        self.parentFrame.focus()

class SParametersDialogMenu(Menu):
    def __init__(self,parent):
        self.parent=parent
        Menu.__init__(self,self.parent)
        self.parent.config(menu=self)
        self.FileMenu=Menu(self)
        self.add_cascade(label='File',menu=self.FileMenu)
        self.FileMenu.add_command(label="Save",command=self.parent.onWriteSParametersToFile)
        self.FileMenu.add_command(label="Open File",command=self.parent.onReadSParametersFromFile)
        self.CalcMenu=Menu(self)
        self.add_cascade(label='Calculate',menu=self.CalcMenu)
        self.CalcMenu.add_command(label='Calculation Properties',command=self.parent.onCalculationProperties)
        #self.CalcMenu.add_command(label='S-parameter Viewer',command=self.parent.onSParameterViewer)
        self.CalcMenu.add_separator()
        self.CalcMenu.add_command(label='Resample',command=self.parent.onResample)

class SParametersDialogToolBar(Frame):
    def __init__(self,parent):
        self.parent=parent
        Frame.__init__(self,self.parent)
        self.pack(side=TOP,fill=X,expand=NO)
        filesFrame=self
        self.openProjectButtonIcon = PhotoImage(file='./icons/png/16x16/actions/document-open-2.gif')
        self.openProjectButton = Button(filesFrame,command=self.parent.onReadSParametersFromFile,image=self.openProjectButtonIcon)
        self.openProjectButton.pack(side=LEFT,fill=NONE,expand=NO)
        self.saveProjectButtonIcon = PhotoImage(file='./icons/png/16x16/actions/document-save-2.gif')
        self.saveProjectButton = Button(filesFrame,command=self.parent.onWriteSParametersToFile,image=self.saveProjectButtonIcon)
        self.saveProjectButton.pack(side=LEFT,fill=NONE,expand=NO)
        separator=Frame(self,bd=2,relief=SUNKEN)
        separator.pack(side=LEFT,fill=X,padx=5,pady=5)

class SParametersDialog(Toplevel):
    def __init__(self, parent,sp):
        Toplevel.__init__(self, parent)
        self.parent=parent
        self.withdraw()
        self.title('S-parameters')
        img = PhotoImage(file='./icons/png/AppIcon2.gif')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.menu=SParametersDialogMenu(self)
        self.toolbar=SParametersDialogToolBar(self)

        topFrame=Frame(self)
        topFrame.pack(side=TOP,fill=BOTH,expand=YES)
        bottomFrame=Frame(self)
        bottomFrame.pack(side=TOP,fill=BOTH,expand=YES)
        topLeftFrame=Frame(topFrame)
        topLeftFrame.pack(side=LEFT,fill=BOTH,expand=YES)
        topRightFrame=Frame(topFrame)
        topRightFrame.pack(side=LEFT,fill=BOTH,expand=YES)
        bottomLeftFrame=Frame(bottomFrame)
        bottomLeftFrame.pack(side=LEFT,fill=BOTH,expand=YES)
        bottomRightFrame=Frame(bottomFrame)
        bottomRightFrame.pack(side=LEFT,fill=BOTH,expand=YES)

        self.topLeftFigure=Figure(figsize=(5,2), dpi=100)
        self.topLeftPlot=self.topLeftFigure.add_subplot(111)
        self.topLeftPlot.set_xlabel('frequency (GHz)')
        self.topLeftPlot.set_ylabel('magnitude (dB)')
        self.topLeftCanvas=FigureCanvasTkAgg(self.topLeftFigure, master=topLeftFrame)
        self.topLeftCanvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
        self.topLeftToolbar = NavigationToolbar2TkAgg( self.topLeftCanvas, topLeftFrame )
        self.topLeftToolbar.update()
        self.topLeftCanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.topRightFigure=Figure(figsize=(5,2), dpi=100)
        self.topRightPlot=self.topRightFigure.add_subplot(111)
        self.topRightPlot.set_xlabel('frequency (GHz)')
        self.topRightPlot.set_ylabel('phase (deg)')
        self.topRightCanvas=FigureCanvasTkAgg(self.topRightFigure, master=topRightFrame)
        self.topRightCanvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
        self.topRightToolbar = NavigationToolbar2TkAgg( self.topRightCanvas, topRightFrame )
        self.topRightToolbar.update()
        self.topRightCanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.topRightCanvasControlsFrame=Frame(topRightFrame)
        self.topRightCanvasControlsFrame.pack(side=TOP, fill=X, expand=NO)
        Button(self.topRightCanvasControlsFrame,text='unwrap',command=self.onUnwrap).pack(side=LEFT,expand=NO,fill=NONE)
        self.delay=PartPropertyDelay(0.)
        self.delayViewerProperty=ViewerProperty(self.topRightCanvasControlsFrame,self.delay,self.onDelayEntered)

        self.bottomLeftFigure=Figure(figsize=(5,2), dpi=100)
        self.bottomLeftPlot=self.bottomLeftFigure.add_subplot(111)
        self.bottomLeftPlot.set_xlabel('time (ns)')
        self.bottomLeftPlot.set_ylabel('amplitude')
        self.bottomLeftCanvas=FigureCanvasTkAgg(self.bottomLeftFigure, master=bottomLeftFrame)
        self.bottomLeftCanvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
        self.bottomLeftToolbar = NavigationToolbar2TkAgg( self.bottomLeftCanvas, bottomLeftFrame )
        self.bottomLeftToolbar.update()
        self.bottomLeftCanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.bottomRightFigure=Figure(figsize=(5,2), dpi=100)
        self.bottomRightPlot=self.bottomRightFigure.add_subplot(111)
        self.bottomRightPlot.set_xlabel('frequency (GHz)')
        self.bottomRightPlot.set_ylabel('phase (deg)')
        self.bottomRightCanvas=FigureCanvasTkAgg(self.bottomRightFigure, master=bottomRightFrame)
        self.bottomRightCanvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
        self.bottomRightToolbar = NavigationToolbar2TkAgg( self.bottomRightCanvas, bottomRightFrame )
        self.bottomRightToolbar.update()
        self.bottomRightCanvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        controlsFrame = Frame(self)
        controlsFrame.pack(side=TOP,fill=X,expand=NO)
        self.sButtonsFrame = Frame(controlsFrame, bd=1, relief=SUNKEN)
        self.sButtonsFrame.pack(side=LEFT,expand=NO,fill=NONE)
        self.resampleButton=Button(controlsFrame,text='resample',command=self.onResample)
        self.resampleButton.pack(side=LEFT,expand=NO,fill=NONE)

        self.sp=sp
        numPorts=self.sp.m_P

        self.buttons=[]
        for toP in range(numPorts):
            buttonrow=[]
            rowFrame=Frame(self.sButtonsFrame)
            rowFrame.pack(side=TOP,expand=NO,fill=NONE)
            for fromP in range(numPorts):
                thisButton=Button(rowFrame,text='s'+str(toP+1)+str(fromP+1),command=lambda x=toP+1,y=fromP+1: self.onSelectSParameter(x,y))
                thisButton.pack(side=LEFT,fill=NONE,expand=NO)
                buttonrow.append(thisButton)
            self.buttons.append(buttonrow)

        self.filename=None

        self.fromPort = 1
        self.toPort = 1

        self.buttons[self.toPort-1][self.fromPort-1].config(relief=SUNKEN)
        self.PlotSParameter()
        self.deiconify()

    def PlotSParameter(self):
        import SignalIntegrity as si
        self.topLeftPlot.cla()
        self.topRightPlot.cla()
        self.bottomLeftPlot.cla()
        self.bottomRightPlot.cla()

        fr=si.fd.FrequencyResponse(self.sp.f(),self.sp.Response(self.toPort,self.fromPort))
        ir=fr.ImpulseResponse()

        y=fr.Response('dB')
        x=fr.Frequencies('GHz')
        self.topLeftPlot.plot(x,y)
        self.topLeftPlot.set_ylim(ymin=max(min(y),-60.0))
        self.topLeftPlot.set_ylim(ymax=max(y)+1.)

        y=fr.Response('deg')
        x=fr.Frequencies('GHz')
        self.topRightPlot.plot(x,y)
        #self.topRightPlot.canvas.draw()

        if ir is not None:
            y=ir.Values()
            x=ir.Times('ns')
            self.bottomLeftPlot.plot(x,y)
            self.bottomLeftPlot.set_ylim(ymin=min(min(y)*1.05,-0.1))
            self.bottomLeftPlot.set_ylim(ymax=max(max(y)*1.05,0.1))
            self.bottomLeftPlot.set_xlim(xmin=min(x))
            self.bottomLeftPlot.set_xlim(xmax=max(x))

            firFilter=ir.FirFilter()
            stepWaveformTimeDescriptor=ir.TimeDescriptor()/firFilter.FilterDescriptor()
            stepWaveform=si.td.wf.StepWaveform(stepWaveformTimeDescriptor)
            stepResponse=stepWaveform*firFilter
            y=stepResponse.Values()
            x=stepResponse.Times('ns')
            self.bottomRightPlot.plot(x,y)
            self.bottomRightPlot.set_ylim(ymin=min(min(y)*1.05,-0.1))
            self.bottomRightPlot.set_ylim(ymax=max(max(y)*1.05,0.1))
            self.bottomRightPlot.set_xlim(xmin=min(x))
            self.bottomRightPlot.set_xlim(xmax=max(x))

        self.topLeftCanvas.draw()
        self.topRightCanvas.draw()
        self.bottomLeftCanvas.draw()
        self.bottomRightCanvas.draw()

    def onSelectSParameter(self,toP,fromP):
        self.buttons[self.toPort-1][self.fromPort-1].config(relief=RAISED)
        self.toPort = toP
        self.fromPort = fromP
        self.buttons[self.toPort-1][self.fromPort-1].config(relief=SUNKEN)
        self.PlotSParameter()

    def onAutoscale(self):
        self.plt.autoscale(True)
        self.f.canvas.draw()

    def UpdateWaveforms(self,waveformList, waveformNamesList):
        self.lift(self.parent)
        self.plt.cla()
        self.plt.set_xlabel('time (ns)',fontsize=10)
        self.plt.set_ylabel('amplitude',fontsize=10)

        if not self.waveformList == None:
            self.plt.autoscale(False)

        self.waveformList=waveformList
        self.waveformNamesList=waveformNamesList

        for wfi in range(len(self.waveformList)):
            self.plt.plot(self.waveformList[wfi].Times('ns'),self.waveformList[wfi].Values(),label=str(self.waveformNamesList[wfi]))

        self.plt.legend(loc='upper right',labelspacing=0.1)
        self.f.canvas.draw()
        return self

    def onUnwrap(self):
        import SignalIntegrity as si
        fr=si.fd.FrequencyResponse(self.sp.f(),self.sp.Response(self.toPort,self.fromPort))
        ir=fr.ImpulseResponse()
        if ir is not None:
            idx = ir.Values('abs').index(max(ir.Values('abs')))
            TD = ir.Times()[idx] # the time of the main peak
        else:
            TD=0.
        self.delay.SetValueFromString(str(TD))
        self.delayViewerProperty.onUntouched(None)

    def onDelayEntered(self):
        import SignalIntegrity as si
        self.topRightPlot.cla()
        fr=si.fd.FrequencyResponse(self.sp.f(),self.sp.Response(self.toPort,self.fromPort))
        TD = self.delay.GetValue()
        fr=fr._DelayBy(-TD)
        y=fr.Response('deg')
        x=fr.Frequencies('GHz')
        self.topRightPlot.plot(x,y)
        self.topRightCanvas.draw()

    def onReadSParametersFromFile(self):
        import SignalIntegrity as si
        filetypes = [('s-parameter files', ('*.s*p'))]
        filename=askopenfilename(filetypes=filetypes,parent=self)
        if filename == '':
            return
        filenametokens=filename.split('.')
        if len(filenametokens)==0:
            return

        filename=ConvertFileNameToRelativePath(filename)
        self.filename=filename
        self.sp=si.sp.File(filename)

        for widget in self.sButtonsFrame.winfo_children():
            widget.destroy()

        numPorts=self.sp.m_P
        self.buttons=[]
        for toP in range(numPorts):
            buttonrow=[]
            rowFrame=Frame(self.sButtonsFrame)
            rowFrame.pack(side=TOP,expand=NO,fill=NONE)
            for fromP in range(numPorts):
                thisButton=Button(rowFrame,text='s'+str(toP+1)+str(fromP+1),command=lambda x=toP+1,y=fromP+1: self.onSelectSParameter(x,y))
                thisButton.pack(side=LEFT,fill=NONE,expand=NO)
                buttonrow.append(thisButton)
            self.buttons.append(buttonrow)

        self.fromPort = 1
        self.toPort = 1
        self.buttons[self.toPort-1][self.fromPort-1].config(relief=SUNKEN)
        self.PlotSParameter()

    def onWriteSParametersToFile(self):
        ports=self.sp.m_P
        extension='.s'+str(ports)+'p'
        if self.filename == None:
            filename=asksaveasfilename(filetypes=[('s-parameters', extension)],defaultextension=extension,initialdir=os.getcwd(),parent=self)
        else:
            filename=asksaveasfilename(filetypes=[('s-parameters', extension)],defaultextension=extension,initialfile=self.filename,parent=self)
        if filename=='':
            return
        self.filename=filename
        self.sp.WriteToFile(filename)

    def onResample(self):
        import SignalIntegrity as si
        self.sp=self.sp.Resample(si.fd.EvenlySpacedFrequencyList(
            self.parent.calculationProperties.endFrequency,
            self.parent.calculationProperties.frequencyPoints))
        self.PlotSParameter()

    def onCalculationProperties(self):
        self.parent.onCalculationProperties()
        self.parent.calculationProperties.CalculationPropertiesDialog().lift(self)