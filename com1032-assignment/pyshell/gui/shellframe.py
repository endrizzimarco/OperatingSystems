import wx
import os

class ShellFrame(wx.Frame):

    def __init__(self, shell):
        self.app = wx.App(False)
        wx.Frame.__init__(self, None, title="OS Shell", size=(450, 300))
        self.shell = shell
        self.historyIndex = 0
        self.SetBackgroundColour(wx.BLACK)
        self.initComponents()
        self.initEvents()
        self.Centre()
        self.Show(True)

    def initComponents(self):
        self.txtHistory = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.txtHistory.SetBackgroundColour(wx.BLACK)
        self.txtHistory.SetForegroundColour(wx.WHITE)
        self.txtHistory.Refresh()
        self.txtCommand = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.txtCommand.SetBackgroundColour(wx.BLACK)
        self.txtCommand.SetForegroundColour(wx.WHITE)
        self.txtCommand.Refresh()
        self.txtCommand.SetFocus()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txtHistory, 1, wx.EXPAND)
        sizer.Add(self.txtCommand, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def initEvents(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnterCommand, self.txtCommand)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPressed, self.txtCommand)

    def onEnterCommand(self, event):
        command = event.GetString()
        self.printLn("> " + command)
        if command and not self.shell.runCommand(command):
            self.printLn("No command '" + command + "' found.")
        self.txtCommand.Clear()
        self.historyIndex = 0

    def onKeyPressed(self, event):
        if event.GetKeyCode() == wx.WXK_DOWN:
            self.showNextCommand()
        elif event.GetKeyCode() == wx.WXK_UP:
            self.showPrevCommand()
        else:
            event.Skip()

    def showPrevCommand(self):
        try:
            command = self.shell.history[self.historyIndex - 1]
            self.historyIndex = self.historyIndex - 1
            self.showCommand(command)
        except IndexError:
            pass

    def showNextCommand(self):
        index = self.historyIndex + 1
        if index == 0:
            self.showCommand("")
            self.historyIndex = index
        elif index < 0:
            command = self.shell.history[index]
            self.showCommand(command)
            self.historyIndex = index

    def showCommand(self, command):
        self.txtCommand.Clear()
        self.txtCommand.AppendText(command)

    def printLn(self, text):
        self.txtHistory.AppendText(text)
        self.txtHistory.AppendText(os.linesep)

    def start(self):
        self.app.MainLoop()
