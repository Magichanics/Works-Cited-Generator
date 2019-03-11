'''
Name: Jan Garong
Date: March 9th, 2019
'''

from __init__ import WorksCitedGenerator
from historyextract import HistoryExtract
import pandas as pd
import wx

class WCGSimpleFrame(wx.Frame):

    def __init__(self):

        # setup window
        wx.Frame.__init__(self, None, wx.ID_ANY, "Works Cited Generator")
        panel = wx.Panel(self, wx.ID_ANY)

        # create layout
        self.panel = WCGSimplePanel(self)
        self.Centre()
        self.Show()

class WCGSimplePanel(wx.Panel):

    def __init__(self, frame):

        wx.Panel.__init__(self, frame)

        # create button placements
        button_sizer = self._button_sizer(frame)

        # create textbox
        self.text_input = wx.TextCtrl(frame, size=(640, 400), style=wx.TE_MULTILINE)

        # add objects to GUI formatting
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text_input, proportion=1, flag=wx.EXPAND)
        vbox.Add(button_sizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.Fit()


    def _button_sizer(self, frame):

        # create new buttons
        btn_csv = wx.Button(self, -1, "Get CSV Metadata")
        btn_wcs = wx.Button(self, -1, "Get Works Cited Sheet")

        # bind into certain functions
        btn_csv.Bind(wx.EVT_BUTTON, self.fetch_urls)
        btn_wcs.Bind(wx.EVT_BUTTON, self.df_to_wcp)

        # format buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(btn_csv)
        button_sizer.Add((-1, -1), proportion=1)
        button_sizer.Add(btn_wcs)

        return button_sizer

    def fetch_urls(self, _):

        # store urls into a list
        urls = []

        for i in range(self.text_input.GetNumberOfLines()):

            # iterate through number of lines available, and add to urls
            urls.append(self.text_input.GetLineText(i))

        # create dataframe
        url_df = pd.DataFrame({'url': urls})

        self.generate_wcp(url_df, 'WorksCited_Manual.docx')

    # generate works cited page
    def generate_wcp(self, url_df, location):

        # set dataframe
        wcg = WorksCitedGenerator()
        wcg.url_df = url_df
        print('fetching metadata...')
        wcg.get_attributes()

        # get location using filedialog
        with wx.FileDialog(frame, "Save metadata.csv",
                           wildcard="CSV File (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # if the user wants to cancel

            # save the current contents in the file
            savepath = fileDialog.GetPath()
            wcg.export_table(savepath)

    def df_to_wcp(self, _):

        # open file
        with wx.FileDialog(frame, "Open metadata.csv",
                           wildcard="CSV File (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # if the user wants to cancel

            # open the file
            openpath = fileDialog.GetPath()
            wcg = WorksCitedGenerator()
            wcg.import_table(openpath)

            # save document
            self.save_wcp(wcg)

    def save_wcp(self, wcg):

        print("Creating Works Cited page")

        with wx.FileDialog(frame, "Save Works Cited Page",
                           wildcard="Document File (*.docx)|*.docx",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # if the user wants to cancel

            # save the document
            savepath = fileDialog.GetPath()
            wcg.citation_generator(savepath)


# create app
if __name__ == "__main__":

    # create app window
    app = wx.App()
    frame = WCGSimpleFrame()

    # set dimensions and position
    frame.SetDimensions(0, 0, 640, 480)
    frame.Centre()

    # show and iterate
    frame.Show()
    app.MainLoop()