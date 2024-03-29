# WxPython Demo
from typing import List, Optional
import os.path
import wx
import QRCodeLib.qrcodelib as qr
from QRCodeLib.qrcodelib import Symbols


class FormMain(wx.Frame):

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self._init_widgets()

        self._images: List[wx.Bitmap] = []
        self._module_size = int()

    def _init_widgets(self) -> None:
        # self
        self.Title = "QR Code"
        self.SetSize(700, 550)
        self.SetMinSize(self.GetSize())
        font = wx.Font(
            10,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL
        )
        self.SetFont(font)
        # create panel
        self._pnl_top = self._create_top_panel()
        self._pnl_middle = self._create_middle_panel()
        self._pnl_bottom = self._create_bottom_panel()
        # sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(self._pnl_top, proportion=1, flag=wx.EXPAND)
        sizer.Add(self._pnl_middle, flag=wx.EXPAND)
        sizer.Add(self._pnl_bottom, flag=wx.EXPAND)

    def _create_top_panel(self) -> wx.Panel:
        panel = wx.Panel(self)
        return panel

    def _create_middle_panel(self) -> wx.Panel:
        panel = wx.Panel(self, size=(self.GetSize().Width, 120))
        # lbl_data
        lbl_data = wx.StaticText(panel, label='Data :')
        # txt_data
        self._txt_data = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB
        )
        self._txt_data.SetFocus()
        self._txt_data.Bind(wx.EVT_TEXT, self.update_image)
        # sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        sizer.Add(
            lbl_data,
            flag=wx.TOP | wx.LEFT,
            border=10
        )
        sizer.Add(
            self._txt_data,
            proportion=1,
            flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT,
            border=10
        )
        return panel

    def _create_bottom_panel(self) -> wx.Panel:
        panel = wx.Panel(
            self,
            size=(self.GetSize().width, 70)
        )
        # lbl_ec_levell
        wx.StaticText(panel, label="Error Correction Level :", pos=(10, 9), size=(143, 21))
        # cmb_ec_level
        self._cmb_ec_level = wx.ComboBox(
            panel,
            pos=(160, 5),
            size=(48, 21),
            choices=["L", "M", "Q", "H"],
            style=wx.CB_READONLY
        )
        self._cmb_ec_level.SetValue("M")
        self._cmb_ec_level.Bind(wx.EVT_COMBOBOX, self.update_image)
        # lbl_byte_enc
        self._lbl_byte_enc = wx.StaticText(
            panel,
            label="Byte mode Encoding :",
            pos=(225, 8)
        )
        # cmb_byte_enc
        self._cmb_byte_enc = wx.ComboBox(
            panel,
            pos=(358, 5),
            size=(315, 21),
            choices=["Shift_JIS", "UTF-8"],
            style=wx.CB_READONLY
        )
        self._cmb_byte_enc.SetValue("Shift_JIS")
        self._cmb_byte_enc.Bind(wx.EVT_COMBOBOX, self.update_image)
        # lbl_max_ver
        wx.StaticText(panel, label="Max Version :", pos=(10, 39))
        # cmb_max_ver
        self._cmb_max_ver = wx.ComboBox(
            panel,
            pos=(160, 35),
            size=(48, 21),
            choices=[str(item + 1) for item in range(40)],
            style=wx.CB_READONLY
        )
        self._cmb_max_ver.SetValue(str(40))
        self._cmb_max_ver.Bind(wx.EVT_COMBOBOX, self.update_image)
        # chk_structured_append
        self._chk_structured_append = wx.CheckBox(
            panel,
            label="Structured Append",
            pos=(225, 39)
        )
        self._chk_structured_append.SetValue(False)
        self._chk_structured_append.Bind(wx.EVT_CHECKBOX, self.update_image)
        # lbl_module_size
        wx.StaticText(panel, label="Module Size :", pos=(380, 39))
        # spn_module_size
        self._spn_module_size = wx.SpinCtrlDouble(
            panel,
            pos=(460, 35),
            size=(48, 21),
            min=1,
            max=100,
            initial=5
        )
        self._spn_module_size.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_image)
        # btn_save
        self._btn_save = wx.Button(
            panel,
            label="Save",
            pos=(553, 35),
            size=(120, 23)
        )
        self._btn_save.Bind(wx.EVT_BUTTON, self.on_btn_save_clicked)
        return panel

    def create_symbols(self) -> Optional[Symbols]:
        data = self._txt_data.GetValue()
        if not data:
            return None

        ec_level = qr.ErrorCorrectionLevel.to_int(self._cmb_ec_level.GetValue())
        max_ver = int(self._cmb_max_ver.GetValue())
        structured_append = self._chk_structured_append.GetValue()
        enc_mode = self._cmb_byte_enc.GetValue()

        symbols = qr.Symbols(ec_level, max_ver, structured_append, enc_mode)
        try:
            symbols.append_text(self._txt_data.GetValue())
        except Exception as e:
            wx.MessageBox(str(e), parent=self)
            return None

        return symbols

    def update_image(self, event) -> None:
        self._pnl_top.DestroyChildren()

        symbols = self.create_symbols()
        if not symbols:
            return

        self._images.clear()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._pnl_top.SetSizer(sizer)
        self._pnl_top.Freeze()

        module_size = int(self._spn_module_size.GetValue())

        for symbol in symbols:
            (data, width, height) = symbol.get_rgb_bytes(module_size)
            bitmap = wx.Bitmap.FromBuffer(width, height, data)
            self._images.append(bitmap)

        for image in self._images:
            static_bitmap = wx.StaticBitmap(self._pnl_top, bitmap=image)
            sizer.Add(static_bitmap, flag=wx.ALL, border=2)

        self._pnl_top.Layout()
        self._pnl_top.Thaw()

    def on_btn_save_clicked(self, event) -> None:
        symbols = self.create_symbols()
        if not symbols:
            return

        wildcard = (
            "Monochrome Bitmap (*.bmp)|*.bmp|"
            "24-bit Bitmap (*.bmp)|*.bmp|"
            "Portable Pixmap (*.ppm)|*.ppm|"
            "X11 Bitmap (*.xbm)|*.xbm|"
            "SVG (*.svg)|*.svg"
        )
        dlg = wx.FileDialog(self, wildcard=wildcard,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        (root, ext) = os.path.splitext(dlg.GetPath())
        module_size = int(self._spn_module_size.GetValue())

        for i, symbol in enumerate(symbols):
            if symbols.count == 1:
                path = root
            else:
                path = root + "_" + str(i)

            if dlg.FilterIndex == 0:
                path += ".bmp"
                symbol.save_bitmap(path, module_size, True)

            if dlg.FilterIndex == 1:
                path += ".bmp"
                symbol.save_bitmap(path, module_size, False)

            if dlg.FilterIndex == 2:
                path += ".ppm"
                symbol.save_ppm(path, module_size)

            if dlg.FilterIndex == 3:
                path += ".xbm"
                symbol.save_xbm(path, module_size)

            if dlg.FilterIndex == 4:
                path += ".svg"
                symbol.save_svg(path, module_size)

        dlg.Destroy()


def main() -> None:
    app = wx.App()
    form = FormMain(parent=None)
    form.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
