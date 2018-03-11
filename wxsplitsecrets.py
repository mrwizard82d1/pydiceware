#! /cygdrive/c/Python25/python.exe


"""GUI application (using wxPython) to create passphrases."""


import wx

import diceware


class SplitSecretFrame(wx.Frame):
    """The application frame."""
    
    def __init__(self):
        """Initialize the application frame."""

        wx.Frame.__init__(self, parent=None,
                          title='Diceware Passphrases')

        self.menuBar = self.CreateMenu()
        self.statusBar = self.CreateStatusBar()

        self.CreateView()
        self.LayoutView()
        self.view.SetSizer(self.viewSizer)
        self.view.Fit()

    def CreateMenu(self):
        """Create the application menu."""
        self.menuBar = wx.MenuBar()
        
        self.fileMenu = wx.Menu()
        self.fileMenu.AppendSeparator()
        exitItem = self.fileMenu.Append(-1,
                                        'E&xit', 'Exits the program.')
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        
        self.menuBar.Append(self.fileMenu, '&File')
        self.SetMenuBar(self.menuBar)

    def CreateView(self):
        """Create the application view."""
        self.view = wx.Panel(self, -1)

        # Create box for split information.
        self.splitBox = wx.StaticBox(self.view, -1, 'Split')
        
        # Create password control.
        self.passwordLabel = wx.StaticText\
                             (self.view, -1,
                              'Enter password or passphrase:')
        generatedTextWidth = 233
        generatedTextHeight = 89
        self.passwordText = wx.TextCtrl(self.view, -1,
                                        size=(generatedTextWidth, -1),
                                        style=wx.TE_MULTILINE)
        self.passwordText.Bind(wx.EVT_TEXT, self.OnPassword)
        
        # Create split controls.
        self.countLabel = wx.StaticText(self.view, -1, 'Share count:')
        self.countSpinner = wx.SpinCtrl(self.view, -1)
        self.countSpinner.SetRange(2, 10)
        self.countSpinner.SetValue(5)

        # Create split button.
        self.splitButton = wx.Button(self.view, -1, 'Split')
        self.splitButton.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnSplit, self.splitButton)

        # Create box for shares information.
        self.sharesBox = wx.StaticBox(self.view, -1, 'Shares')
        self.sharesLabel = wx.StaticText(self.view, -1,
                                         'Enter shares (one per line):')
        generatedTextWidth = 73
        generatedTextHeight = 450
        self.sharesText = wx.TextCtrl(self.view, -1,
                                      size=(generatedTextWidth,
                                            generatedTextHeight),
                                      style=wx.TE_MULTILINE)
        self.sharesText.Bind(wx.EVT_TEXT, self.OnShares)

        self.restoreButton = wx.Button(self.view, -1, 'Restore')
        self.restoreButton.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnRestore, self.restoreButton)

    def LayoutView(self):
        """Layout the application view."""
        self.viewSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Layout the split view.
        self.splitView = wx.StaticBoxSizer(self.splitBox,
                                           wx.VERTICAL)
        self.splitView.Add(self.passwordLabel,
                           proportion=0, flag=wx.EXPAND)
        self.splitView.Add(self.passwordText,
                           proportion=1, flag=wx.EXPAND)

        self.countView = wx.BoxSizer(wx.VERTICAL)
        self.countView.Add(self.countLabel, proportion=0)
        self.countView.Add(self.countSpinner, proportion=0)

        self.actionView = wx.BoxSizer(wx.HORIZONTAL)
        self.actionView.Add(self.countView,
                            proportion=0, flag=wx.ALIGN_BOTTOM)
        self.actionView.Add((10, 10), proportion=1,
                            flag=(wx.ALIGN_BOTTOM |
                                  wx.ALIGN_CENTER_HORIZONTAL))
        self.actionView.Add(self.splitButton, proportion=0,
                            flag=(wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM))

        self.splitView.Add(self.actionView,
                           proportion=0, flag=wx.EXPAND)
        
        # Layout the shares view
        self.sharesView = wx.StaticBoxSizer(self.sharesBox,
                                            wx.VERTICAL)
        self.sharesView.Add(self.sharesLabel,
                            proportion=0,
                            flag=wx.EXPAND)
        self.sharesView.Add(self.sharesText,
                            proportion=1,
                            flag=wx.EXPAND)
        self.sharesView.Add(self.restoreButton,
                            proportion=0, flag=wx.ALIGN_RIGHT)

        # Layout the view
        self.viewSizer.Add(self.splitView,
                           flag=wx.EXPAND);
        self.viewSizer.Add(self.sharesView,
                           proportion=1, flag=wx.EXPAND)
        
    def OnExit(self, event):
        """Handle the user selecting the exit menu item."""
        self.Close()

    def OnPassword(self, event):
        """Handle the user changing the password / passphrase text."""
        self.splitButton.Enable(len(self.passwordText.\
                                    GetValue().strip()) != 0)
    
    def OnRestore(self, event):
        """Handle the user pressing the restore button."""
        # Get the shares to restore.
        theSharesText = self.sharesText.GetValue()
        theShares = theSharesText.split('\n')

        # Restore the shares to generate the password.
        thePassword = diceware.restoreSecret(theShares)
        self.passwordText.SetValue(thePassword)

        """Handle the user changing the shares."""
        self.restoreButton.Enable(len(self.sharesText.\
                                      GetValue().strip()) != 0)

    def OnShares(self, event):
        """Handle the user changing the shares."""
        self.restoreButton.Enable(len(self.sharesText.\
                                      GetValue().strip()) != 0)
    
    def OnSplit(self, event):
        """Handle the user pressing the split button."""
        # Split the password into shares.
        password = self.passwordText.GetValue()
        theCount = int(self.countSpinner.GetValue())
        theShares = list(diceware.splitSecret(password, theCount))

        # Display the shares.
        theSharesText = '\n'.join(theShares)
        self.sharesText.SetValue(theSharesText)
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = SplitSecretFrame()
    frame.Show(True)
    app.MainLoop()
    


