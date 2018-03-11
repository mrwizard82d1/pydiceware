#! /cygdrive/c/Python25/python.exe


"""GUI application (using wxPython) to create passphrases."""


import wx

import diceware


class DicewareFrame(wx.Frame):
    """The application frame."""
    
    def __init__(self):
        """Initialize the application frame."""

        wx.Frame.__init__(self, parent=None,
                          title='Diceware Passphrases')

        self.styleHandler = {'Basic': self.makeBasic,
                             'NT Login': self.makeNtLogin,
                             'XP Login': self.makeXpLogin}
        
        self.menuBar = self.CreateMenu()
        self.statusBar = self.CreateStatusBar()

        self.CreateView()
        self.LayoutView()
        self.view.SetSizer(self.viewSizer)
        self.view.Fit()

        self.generator = None
        self.cachedBasic = None
        self.cachedNtLogin = None
        self.cachedXpLogin = None

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
        
        self.paramsBox = wx.StaticBox(self.view, -1, 'Parameters')

        choices = self.styleHandler.keys()
        choices.sort()
        self.styles = wx.RadioBox(self.view, -1, '', choices=choices,
                                  style=wx.RA_SPECIFY_ROWS)

        self.countLabel = wx.StaticText(self.view, -1, 'Count:')
        self.countSpinner = wx.SpinCtrl(self.view, -1)
        self.countSpinner.SetRange(2, 10)
        self.countSpinner.SetValue(5)

        self.generateButton = wx.Button(self.view, -1, 'Generate')
        self.Bind(wx.EVT_BUTTON, self.OnGenerate, self.generateButton)

        generatedTextWidth = 233
        generatedTextHeight = 89
        self.generatedBox = wx.StaticBox(self.view, -1,
                                         'Generated Passphrases')
        self.generatedText = wx.TextCtrl(self.view, -1,
                                         size=(generatedTextWidth,
                                               generatedTextHeight),
                                         style=wx.TE_MULTILINE)
        self.editBox = wx.StaticBox(self.view, -1,
                                    'Type Passphrases')
        self.editText = wx.TextCtrl(self.view, -1,
                                    size=(generatedTextWidth, -1),
                                    style=wx.TE_MULTILINE)

    def LayoutView(self):
        """Layout the application view."""
        self.viewSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.actionView = wx.BoxSizer(wx.VERTICAL)
        
        self.paramsView = wx.StaticBoxSizer(self.paramsBox,
                                            wx.VERTICAL)
        self.paramsView.Add(self.styles)
        self.paramsView.Add((10, 10))
        self.paramsView.Add(self.countLabel)
        self.paramsView.Add(self.countSpinner)
        
        self.actionView.Add(self.paramsView)
        self.actionView.Add((10, 10))
        self.actionView.Add(self.generateButton)
        
        self.passphraseView = wx.BoxSizer(wx.VERTICAL)

        self.generatedView = wx.StaticBoxSizer(self.generatedBox,
                                               wx.VERTICAL)
        self.generatedView.Add(self.generatedText,
                               flag=wx.EXPAND)

        self.editView = wx.StaticBoxSizer(self.editBox,
                                          wx.VERTICAL)
        self.editView.Add(self.editText,
                          proportion=1,
                          flag=wx.EXPAND)

        self.passphraseView.Add(self.generatedView, flag=wx.EXPAND)
        self.passphraseView.Add(self.editView,
                                proportion=1, flag=wx.EXPAND)

        self.viewSizer.Add(self.actionView,
                           proportion=0, flag=wx.EXPAND)
        self.viewSizer.Add(self.passphraseView,
                           proportion=1, flag=wx.EXPAND)

    def makeBasic(self):
        """Create a basic passphrase generator."""
        if not self.cachedBasic:
            self.cachedBasic = diceware.makeBasicGenerator()
        return self.cachedBasic

    def makeNtLogin(self):
        """Create an NT login passphrase generator."""
        if not self.cachedNtLogin:
            self.cachedNtLogin = diceware.makeLoginGenerator()
        return self.cachedNtLogin

    def makeXpLogin(self):
        """Create an XP login passphrase generator."""
        if not self.cachedXpLogin:
            self.cachedXpLogin = diceware.SpecialGenerator(count=4)
        return self.cachedXpLogin

    def OnExit(self, event):
        """Handle the user selecting the exit menu item."""
        self.Close()

    def OnGenerate(self, event):
        """Handle the user pressing the generate button."""
        # determine what to generate
        self.generator = \
                       self.styleHandler[self.styles.
                                         GetStringSelection()]()
                                         
        for i in range(self.countSpinner.GetValue()):
            if len(self.generatedText.GetValue()) > 0:
                self.generatedText.AppendText('\n')
            self.generatedText.AppendText('%s' % self.generator.next())
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = DicewareFrame()
    frame.Show(True)
    app.MainLoop()
    


