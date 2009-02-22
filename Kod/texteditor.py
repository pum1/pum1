# -*- coding: utf-8 -*-
# Get the GUI stuff
import wx

# We're going to be handling files and directories
import os

#Importera codecs för filhantering med utf-8
import codecs

# Set up some button numbers for the menu

ID_ABOUT=101
ID_OPEN=102
ID_SAVE=103
ID_EXIT=200
ID_CLEAR=400

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        # based on a frame, so set up the frame
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size=(650, 550))

        # Add a text editor and a status bar
        # Each of these is within the current instance
        # so that we can refer to them later.
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu. filemenu is a local variable at this stage.
        filemenu= wx.Menu()
        editmenu = wx.Menu()
        # use ID_ for future easy reference - much better that "48", "404" etc
        # The & character indicates the short cut key
        editmenu.Append(ID_CLEAR, "&Clear", "Clears all text written")
        filemenu.Append(ID_OPEN, "&Open"," Open a file to edit")
        filemenu.Append(ID_SAVE, "&Save"," Save file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(editmenu,"&Edit")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        # Note - previous line stores the whole of the menu into the current object
        
        
        # Define the code to be run when a menu option is selected
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave); # just "pass" in our demo
        wx.EVT_MENU(self, ID_CLEAR, self.OnClear)

        # Set up the overall frame verically - text edit window
        # We want to arrange the buttons vertically below the text edit window
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control,1,wx.EXPAND)

        #Kommenterade ut denna bit för den gjorde rutan skitliten
        #Antagligen för att den då automagiskt väljer storlek istället för
        #den som jag har satt i wxFrame.__init__
        # Tell it which sizer is to be used for main frame
        # It may lay out automatically and be altered to fit window
        #self.SetSizer(self.sizer)
        #self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        # Show it !!!
        self.Show(1)
        # Put the window in the middle of the screen
        self.Centre()

        # Define widgets early even if they're not going to be seen
        # so that they can come up FAST when someone clicks for them!
        self.aboutme = wx.MessageDialog( self, " A sample editor \n"
                            " in wxPython","About Sample Editor", wx.OK)
        #La till unicode(string, 'utf-8') för att åäö skulle fungera korrekt
        #Kanske finns något smidigare sätt.
        self.doiexit = wx.MessageDialog( self, unicode(" Är du säker på att du vill \n"
                                         "avsluta denna awesome editerare?", 'utf-8'),
                        "GOING away ...", wx.YES_NO)

        # dirname is an APPLICATION variable that we're choosing to store
        # in with the frame - it's the parent directory for any file we
        # choose to edit in this frame
        self.dirname = ''

    def OnAbout(self,e):
        # A modal show will lock out the other windows until it has
        # been dealt with. Very useful in some programming tasks to
        # ensure that things happen in an order that  the programmer
        # expects, but can be very frustrating to the user if it is
        # used to excess!
        self.aboutme.ShowModal() # Shows it
        # widget / frame defined earlier so it can come up fast when needed

    #Test att ta bort all text som finns i editeringsrutan.
    #Verkar funka fint
    def OnClear(self, e):
        self.control.SetValue('')
        
    def OnExit(self,e):
        # A modal with an "are you sure" check - we don't want to exit
        # unless the user confirms the selection in this case ;-)
        igot = self.doiexit.ShowModal() # Shows it
        if igot == wx.ID_YES:
            self.Close(True)  # Closes out this simple application

    def OnOpen(self,e):
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        dlg = wx.FileDialog(self, "Choose a file kthnx. ", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()

            # Open the file, read the contents and set them into
            # the text edit window
            #Ändrade från open(...) till codecs.open(...) eftersom den inte kunde läsa
            #in annat är ASCII och det failar om man har med åäö
            filehandle=codecs.open(os.path.join(self.dirname, self.filename),'r',"utf-8")
            self.control.SetValue(filehandle.read())
            filehandle.close()

            # Report on name of latest file read
            self.SetTitle("Editing ... "+self.filename)
            # Later - could be enhanced to include a "changed" flag whenever
            # the text is actually changed, could also be altered on "save" ...
        dlg.Destroy()

    def OnSave(self,e):
        # Save away the edited text
        # Open the file, do an RU sure check for an overwrite!
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Grab the content to be saved
            itcontains = self.control.GetValue()

              # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            #Pss som i OnOpen.
            filehandle=codecs.open(os.path.join(self.dirname, self.filename),'w', "utf-8")
            filehandle.write(itcontains)
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()

# Set up a window based app, and create a main window in it
app = wx.PySimpleApp()
view = MainWindow(None, "Dwiki editor yo")
# Enter event loop
app.MainLoop()
