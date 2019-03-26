# TkInter Demo
import os.path

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfdlg
from tkinter.scrolledtext import ScrolledText

import qrcodelib as qr


class FormTk(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw) -> None:
        super().__init__(master, cnf, **kw)
        self._master = master
        self._init_widgets()

        self._images = []

        self._ec_level = int()
        self._max_ver = int()
        self._structured_append = bool()
        self._enc_mode = str()
        self._module_size = int()

    def _init_widgets(self):
        # event handler
        self._update_image_handler = lambda event: self.update_image(event)
        self._btn_save_handler = lambda event: self.on_btn_save_clicked(event)

        # self
        self.propagate(False)
        self.config(width=700, height=550)
        self.pack(expand=True, fill=tk.BOTH)
        # top_frame
        self._fra_top = self._create_top_frame()
        self._fra_top.pack(expand=True, fill=tk.BOTH, anchor=tk.S)
        # middle_frame
        self._fra_middle = self._create_middle_frame()
        self._fra_middle.pack(expand=False, fill=tk.BOTH, anchor=tk.S)
        # bottom_frame
        self._fra_bottom = self._create_bottom_frame()
        self._fra_bottom.pack(expand=False, fill=tk.X, anchor=tk.NW)
        # master
        self._master.title("QR Code")
        self._master.propagate(True)
        self._master.update()
        self._master.minsize(self._master.winfo_width(), self._master.winfo_height())

    def _create_top_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray80", height=320)
        frame.propagate(False)
        return frame

    def _create_middle_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray95", height=120)
        # lbl_data
        self._lbl_data = tk.Label(frame, text="Data :")
        self._lbl_data.pack(anchor=tk.NW, padx=8)
        # txt_data
        self._txt_data = ScrolledText(frame, height=6)
        self._txt_data.pack(anchor=tk.NW, expand=True, fill=tk.X, padx=8, pady=3)
        self._txt_data.focus_set()
        self._txt_data.bind("<KeyRelease>", self._update_image_handler)
        return frame

    def _create_bottom_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray95", height=70)
        # lbl_ec_level
        self._lbl_ec_level = tk.Label(frame, text="Error Correnction Level :")
        self._lbl_ec_level.place(x=8, y=10)
        # cmb_ec_level
        self._cmb_ec_level = ttk.Combobox(frame, state="readonly", width=4)
        self._cmb_ec_level["values"] = ["L", "M", "Q", "H"]
        self._cmb_ec_level.current(1)
        self._cmb_ec_level.place(x=150, y=10)
        self._cmb_ec_level.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_max_ver
        self._lbl_max_ver = tk.Label(frame, text="Max Version :")
        self._lbl_max_ver.place(x=8, y=40)
        # cmb_max_ver
        self._cmb_max_ver = ttk.Combobox(frame, state="readonly", width=4)
        self._cmb_max_ver["values"] = [item + 1 for item in range(40)]
        self._cmb_max_ver.current(len(self._cmb_max_ver["values"]) - 1)
        self._cmb_max_ver.place(x=150, y=40)
        self._cmb_max_ver.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_byte_enc
        self._lbl_byte_enc = tk.Label(frame, text="Byte mode Encoding :")
        self._lbl_byte_enc.place(x=210, y=10)
        # cmb_byte_enc
        self._cmb_byte_enc = ttk.Combobox(frame, state="readonly", width=56)
        self._cmb_byte_enc["values"] = ["Shift_JIS", "UTF-8"]
        self._cmb_byte_enc.current(0)
        self._cmb_byte_enc.place(x=335, y=10)
        self._cmb_byte_enc.bind("<<ComboboxSelected>>", self._update_image_handler)
        # chk_structured_append
        self._var_chk_structured_append = tk.BooleanVar(value=False)
        self._chk_structured_append = ttk.Checkbutton(
            frame, text="Structured Append", variable=self._var_chk_structured_append)
        self._chk_structured_append.place(x=210, y=40)
        self._chk_structured_append.bind("<Button-1>", self._update_image_handler)
        # lbl_module_size
        self._lbl_module_size = tk.Label(frame, text="Module Size :")
        self._lbl_module_size.place(x=360, y=40)
        # spn_module_size
        self._spn_module_size = tk.Spinbox(
            frame, from_=1, to_=100, width=4, state="readonly")
        self._spn_module_size["textvariable"] = tk.StringVar(value="5")
        self._spn_module_size.place(x=440, y=40)
        self._spn_module_size.bind("<KeyPress-Up>", self._update_image_handler)
        self._spn_module_size.bind("<KeyPress-Down>", self._update_image_handler)
        # btn_save
        self._btn_save = ttk.Button(frame, text="Save", width=19)
        self._btn_save.place(x=570, y=35)
        self._btn_save.bind("<ButtonRelease-1>", self._btn_save_handler)
        self._btn_save.bind("<Key-Return>", self._btn_save_handler)
        self._btn_save.bind("<Key-space>", self._btn_save_handler)
        return frame

    def create_symbols(self):
        data = self._txt_data.get("1.0", tk.END + "-1c")
        if not data:
            return None

        self._ec_level = qr.ErrorCorrectionLevel.to_int(self._cmb_ec_level.get())
        self._max_ver = int(self._cmb_max_ver.get())
        self._structured_append = bool(self._var_chk_structured_append.get())
        self._enc_mode = self._cmb_byte_enc.get()
        self._module_size = int(self._spn_module_size.get())

        symbols = qr.Symbols(
            self._ec_level, self._max_ver, self._structured_append, self._enc_mode)
        try:
            symbols.append_text(data)
        except Exception as e:
            tkmsg.showwarning(message=e)
            return None

        return symbols

    def update_image(self, event):
        if self._fra_top.winfo_children() is not None:
            for widget in self._fra_top.winfo_children():
                widget.destroy()

        symbols = self.create_symbols()
        if not symbols:
            return

        self._images.clear()

        for symbol in symbols:
            image = symbol.tk_photo_image(self._module_size)
            self._images.append(image)

        for image in self._images:
            qrcode = tk.Label(self._fra_top, image=image)
            qrcode.pack(expand=False, fill=tk.NONE, anchor=tk.NW, side=tk.LEFT)

    def on_btn_save_clicked(self, event):
        symbols = self.create_symbols()
        if not symbols:
            return

        filetypes = [
            ("Monochrome Bitmap", "*.bmp"),
            ("Portable Pixmap", "*.ppm"),
            ("X11 Bitmap", "*.xbm")
        ]
        filename = tkfdlg.asksaveasfilename(defaultextension="bmp", filetypes=filetypes)
        (root, ext) = os.path.splitext(filename)
        ext = ext.lower()

        num = 0

        for symbol in symbols:
            num += 1

            if symbols.count == 1:
                path = root + ext
            else:
                path = root + "_" + str(num) + ext

            if ext == ".bmp":
                symbol.save_1bpp_dib(path, self._module_size)

            if ext == ".ppm":
                symbol.save_ppm(path, self._module_size)

            if ext == ".xbm":
                symbol.save_xbm(path, self._module_size)


def main():
    app = tk.Tk()
    form = FormTk(app)
    app.mainloop()


main()
