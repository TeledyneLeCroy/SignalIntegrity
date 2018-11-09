"""
About.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>
import sys
if sys.version_info.major < 3:
    from Tkinter import Toplevel,PhotoImage,Frame,Button,Label,Message
    from Tkinter import TOP,BOTH,LEFT,YES,X,END,CENTER
    import webbrowser
    import textwrap
    from ScrolledText import ScrolledText
else:
    from tkinter import Toplevel,PhotoImage,Frame,Button,Label,Message
    from tkinter import TOP,BOTH,LEFT,YES,X,END,CENTER
    import webbrowser
    import textwrap
    from tkinter import scrolledtext

from SignalIntegrity.__about__ import __version__,__url__,__copyright__,__description__,__author__,__email__,__project__

class CreditsDialog(Toplevel):
    def __init__(self,parent):
        self.parent=parent
        textToShow = [' '+__project__+' was written by:','','\t {} \t <{}>'.format(__author__,__email__)]
        Toplevel.__init__(self, parent)
        self.img = PhotoImage(file=parent.parent.installdir+'/icons/png/AppIcon2.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.img)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title('Credits')
        if sys.version_info.major < 3:
            self.text=ScrolledText(self,height=8,width=50)
        else:
            self.text=scrolledtext.ScrolledText(self,height=8,width=50)
        self.text.pack(side=TOP, fill=BOTH, expand=YES)
        for line in textToShow:
            self.text.insert(END,line+'\n')
        buttonsFrame = Frame(self)
        buttonsFrame.pack(side=TOP,expand=YES,fill=X,anchor='s')
        closeButton = Button(buttonsFrame,text='Close',command=self.destroy)
        closeButton.pack(side=LEFT,expand=YES)
        self.text.focus_set()
        self.geometry("%+d%+d" % (self.parent.winfo_x()+self.parent.winfo_width()/2-self.winfo_width()/2,
            self.parent.winfo_y()+self.parent.winfo_height()/2-self.winfo_height()/2))
        self.text.configure(state='disabled')
 
class LicenseDialog(Toplevel):
    def __init__(self,parent):
        self.parent=parent
        textToShow = []
        try:
            licenseFile=open(parent.parent.installdir+'/../../LICENSE.txt','rU' if sys.version_info.major < 3 else 'r')
            for line in licenseFile:
                if line.strip()=='':
                    textToShow.append('\n')
                else:
                    textToShow=textToShow+textwrap.wrap(line,80)
            licenseFile.close()

        except IOError:
            textToShow = ['LICENSE FILE NOT FOUND']

        Toplevel.__init__(self, parent)
        self.img = PhotoImage(file=parent.parent.installdir+'/icons/png/AppIcon2.gif')
        self.gnuimg=PhotoImage(file=parent.parent.installdir+'/icons/png/gpl.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.img)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title('License')
        self.gnu=Button(self,image=self.gnuimg,command=self.onHyper)
        self.gnu.pack(side=TOP,fill=BOTH,expand=YES)
        if sys.version_info.major < 3:
            self.text=ScrolledText(self)
        else:
            self.text=scrolledtext.ScrolledText(self)
        self.text.pack(side=TOP, fill=BOTH, expand=YES)
        for line in textToShow:
            self.text.insert(END,line+'\n')
        buttonsFrame = Frame(self)
        buttonsFrame.pack(side=TOP,expand=YES,fill=X,anchor='s')
        closeButton = Button(buttonsFrame,text='Close',command=self.destroy)
        closeButton.pack(side=LEFT,expand=YES)
        self.text.focus_set()
        self.geometry("%+d%+d" % (self.parent.winfo_x()+self.parent.winfo_width()/2-self.winfo_width()/2,
            self.parent.winfo_y()+self.parent.winfo_height()/2-self.winfo_height()/2))
        self.text.configure(state='disabled')
    def onHyper(self):
        webbrowser.open_new(r"https://www.gnu.org/licenses/gpl-3.0.html")

class AboutDialog(Toplevel):
    def __init__(self,parent):
        self.parent = parent

        Toplevel.__init__(self, parent)

        self.img = PhotoImage(file=parent.installdir+'/icons/png/AppIcon2.gif')
        self.img2 = PhotoImage(file=parent.installdir+'/icons/png/tlecroy-logo-15.gif')
        self.tk.call('wm', 'iconphoto', self._w, self.img)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title('About '+__project__)
        self.focus_set()
        lecroyLabel = Label(self,image=self.img2)
        lecroyLabel.pack(side=TOP,expand=YES,fill=BOTH)
        iconLabel = Label(self, image=self.img)
        iconLabel.pack(side=TOP,expand=YES,fill=BOTH)
        msg = Message(self,text=__description__,justify=CENTER, width=500)
        msg.pack(side=TOP,expand=YES,fill=BOTH)
        msg = Message(self,text="version: %s" % (__version__),justify=CENTER, width=500)
        msg.pack(side=TOP,expand=YES,fill=BOTH)
        msg = Message(self,text=__copyright__,justify=CENTER, width=500)
        msg.pack(side=TOP,expand=YES,fill=BOTH)
        hyperLink = Button(self,text=__url__, command=self.onHyper, borderwidth=0)
        hyperLink.pack(side=TOP,expand=YES,fill=X)
        buttonsFrame = Frame(self)
        buttonsFrame.pack(side=TOP,expand=YES,fill=X,anchor='s')
        creditsButton = Button(buttonsFrame,text='Credits', command=self.onCredits, width=10)
        creditsButton.pack(side=LEFT,expand=YES)
        licenseButton = Button(buttonsFrame,text='License', command=self.onLicense, width=10)
        licenseButton.pack(side=LEFT,expand=YES)
        closeButton = Button(buttonsFrame,text='Close',command=self.destroy, width=10)
        closeButton.pack(side=LEFT,expand=YES)
        self.geometry("%+d%+d" % (self.parent.root.winfo_x()+self.parent.root.winfo_width()/2-self.winfo_width()/2,
            self.parent.root.winfo_y()+self.parent.root.winfo_height()/2-self.winfo_height()/2))

    def onCredits(self):
        CreditsDialog(self)

    def onLicense(self):
        LicenseDialog(self)

    def onHyper(self):
        webbrowser.open_new(__url__)