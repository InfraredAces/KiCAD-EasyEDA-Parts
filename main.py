import os
import sys
import logging

import wx
import pcbnew

try:
    import easyeda2kicad.__main__ as easyeda2kicad
except ImportError:
    easyeda2kicad = None

# TODO:
#  - update library tables
#  - download folder selection

logger = logging.getLogger()


def download_part(lcsc_id, absolute_path, project_dir, download_dir, lib_prefix):
    prev_wd = os.getcwd()

    # download_dir = "libs/easyeda"
    # lib_prefix = "easyeda"
    full_path = os.path.join(project_dir, download_dir, lib_prefix)
    download_path = os.path.join(download_dir, lib_prefix)

    logger.error("--- Current Working Directory ---")
    logger.error(os.getcwd())

    if(absolute_path):
        logger.error("--- Using Absolute Path ---")
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        easyeda2kicad.main(["--full", f"--lcsc_id={lcsc_id}", "--output", download_path, "--overwrite"])
    else:
        logger.error("--- Using Project Relative Path ---")
        os.chdir(project_dir)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        easyeda2kicad.main(["--full", f"--lcsc_id={lcsc_id}", "--output", download_path, "--overwrite", "--project-relative"])

    os.chdir(prev_wd)
    

class Plugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "EasyEDA Parts"
        self.category = "Library download"
        self.description = "Download footprints, symbols and 3d models from EasyEDA."
        self.show_toolbar_button = True
        path, filename = os.path.split(os.path.abspath(__file__))
        self.icon_file_name = os.path.join(path, "icon.png")

    def Run(self):
        dialog = Dialog(None)
        dialog.Centre()
        dialog.Show()


class Dialog(wx.Dialog):
    def __init__(self, parent):
        if sys.platform != "darwin":
            self.app = wx.App()
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="EasyEDA Parts",
            pos=wx.DefaultPosition,
            size=wx.Size(400, 300),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )

        board = pcbnew.GetBoard()
        project_dir = f"{os.path.dirname(board.GetFileName())}"

        content = wx.BoxSizer(wx.VERTICAL)

        grid = wx.GridSizer(2, 2, 5, 5)

        # LCSC Part Number
        text_lcsc_id_title = wx.StaticText(self, wx.ID_ANY, "LCSC ID:")
        grid.Add(text_lcsc_id_title, 0, wx.EXPAND |
                 wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        text_edit_lcsc_id = wx.TextCtrl(
            self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        text_edit_lcsc_id.SetHint("e.g. C2040")
        grid.Add(text_edit_lcsc_id, 0, wx.EXPAND)

        # Absolute or Project Relative
        text_absolute_path_title = wx.StaticText(
            self, wx.ID_ANY, "Absolute Path")
        grid.Add(text_absolute_path_title, 0, wx.EXPAND |
                 wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
        checkbox_absolute_path = wx.CheckBox( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        grid.Add(checkbox_absolute_path, 0, wx.EXPAND)

        # Download Directory
        text_download_dir_title = wx.StaticText(
            self, wx.ID_ANY, "Download Dir:")
        grid.Add(text_download_dir_title, 0, wx.EXPAND |
                 wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        text_edit_download_dir = wx.TextCtrl(
            self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        text_edit_download_dir.SetValue("./lib/easyeda")
        text_edit_download_dir.SetHint("e.g. lib/easyeda")
        grid.Add(text_edit_download_dir, 0, wx.EXPAND)

        # Library Prefix
        text_lib_prefix_title = wx.StaticText(
            self, wx.ID_ANY, "Library Prefix:")
        grid.Add(text_lib_prefix_title, 0, wx.EXPAND |
                 wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)

        text_edit_lib_prefix = wx.TextCtrl(
            self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        text_edit_lib_prefix.SetValue("easyeda")
        text_edit_lib_prefix.SetHint("e.g. easyeda")
        grid.Add(text_edit_lib_prefix, 0, wx.EXPAND)

        download_button = wx.Button(self, wx.ID_ANY, "Download")
        download_button.Bind(wx.EVT_BUTTON,
                             lambda event: self._on_download_click(text_edit_lcsc_id.GetValue().upper(), checkbox_absolute_path.IsChecked(),project_dir, text_edit_download_dir.GetValue(), text_edit_lib_prefix.GetValue()))
        grid.Add(download_button, 0, wx.EXPAND)

        done_button = wx.Button(self, wx.ID_OK, "Done")
        grid.Add(done_button, 0, wx.EXPAND)

        if easyeda2kicad:
            content.Add(grid, 0, flag=wx.EXPAND | wx.ALL, border=10)

        text_log = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                               wx.DefaultPosition, wx.DefaultSize,
                               wx.TE_MULTILINE | wx.TE_READONLY)
        logger.addHandler(TextCtrlHandler(text_log))
        content.Add(text_log, 1, wx.EXPAND, 5)

        self.SetSizer(content)
        self.Layout()
        self.Centre(wx.BOTH)

        if not easyeda2kicad:
            logger.error(
                "easyeda2kicad not found, please install it first with `pip install easyeda2kicad`")

    def _on_download_click(self, lcsc_id, absolute_path, project_dir, download_dir, lib_prefix):
        download_part(lcsc_id, absolute_path, project_dir, download_dir, lib_prefix)


class TextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        wx.CallAfter(self.ctrl.WriteText, s)


class TextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        wx.CallAfter(self.ctrl.WriteText, s)
