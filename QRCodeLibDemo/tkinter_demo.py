# TkInter Demo
from typing import List, Optional
import os.path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfdlg
from tkinter.scrolledtext import ScrolledText
from tkinter import PhotoImage
import QRCodeLib.qrcodelib as qr


class FormMain(tk.Frame):

    def __init__(self, master=None) -> None:
        super().__init__(master)

        self._init_widgets()
        self._images: List[PhotoImage] = []
        # master
        master.title("QR Code")
        master.propagate(True)
        master.update()
        master.minsize(master.winfo_width(), master.winfo_height())

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
        self._fra_middle.pack(expand=False, fill=tk.BOTH, anchor=tk.S, padx=4, pady=4)
        # bottom_frame
        self._fra_bottom = self._create_bottom_frame()
        self._fra_bottom.pack(expand=False, fill=tk.X, anchor=tk.NW, padx=4, pady=4)

    def _create_top_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray80", height=320)
        frame.propagate(False)
        return frame

    def _create_middle_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray95", height=120)
        # lbl_data
        lbl_data = tk.Label(frame, text="Data :")
        lbl_data.pack(anchor=tk.W, padx=4)
        # txt_data
        self._txt_data = ScrolledText(frame, height=6)
        self._txt_data.pack(anchor=tk.NW, expand=True, fill=tk.X, padx=4)
        self._txt_data.focus_set()
        self._txt_data.bind("<KeyRelease>", self._update_image_handler)
        return frame

    def _create_bottom_frame(self) -> tk.Frame:
        pad = {"padx": 4, "pady": 4}
        frame = tk.Frame(self, bg="gray95", height=70)
        # lbl_ec_level
        lbl_ec_level = tk.Label(frame, text="Error Correction Level :")
        lbl_ec_level.grid(row=0, column=0, sticky=tk.W, cnf=pad)
        # cmb_ec_level
        self._cmb_ec_level_var = tk.StringVar()
        cmb_ec_level = ttk.Combobox(frame, state="readonly", width=4, textvariable=self._cmb_ec_level_var)
        cmb_ec_level["values"] = ["L", "M", "Q", "H"]
        cmb_ec_level.current(1)
        cmb_ec_level.grid(row=0, column=1, sticky=tk.W, cnf=pad)
        cmb_ec_level.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_max_ver
        lbl_max_ver = tk.Label(frame, text="Max Version :")
        lbl_max_ver.grid(row=1, column=0, sticky=tk.W, cnf=pad)
        # cmb_max_ver
        self._cmb_max_ver_var = tk.StringVar()
        cmb_max_ver = ttk.Combobox(frame, state="readonly", width=4, height=20, textvariable=self._cmb_max_ver_var)
        cmb_max_ver["values"] = [i + 1 for i in range(40)]
        cmb_max_ver.current(len(cmb_max_ver["values"]) - 1)
        cmb_max_ver.grid(row=1, column=1, sticky=tk.W, cnf=pad)
        cmb_max_ver.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_byte_enc
        lbl_byte_enc = tk.Label(frame, text="Byte mode Encoding :")
        lbl_byte_enc.grid(row=0, column=2, sticky=tk.W, cnf=pad)
        # cmb_byte_enc
        self._cmb_byte_enc_var = tk.StringVar()
        cmb_byte_enc = ttk.Combobox(frame, state="readonly", width=56, textvariable=self._cmb_byte_enc_var)
        cmb_byte_enc["values"] = ["Shift_JIS", "UTF-8"]
        cmb_byte_enc.current(0)
        cmb_byte_enc.grid(row=0, column=3, columnspan=2, sticky=tk.W, cnf=pad)
        cmb_byte_enc.bind("<<ComboboxSelected>>", self._update_image_handler)
        # chk_structured_append
        self._chk_structured_append_var = tk.BooleanVar(value=False)
        chk_structured_append = ttk.Checkbutton(
            frame, text="Structured Append", variable=self._chk_structured_append_var)
        chk_structured_append.grid(row=1, column=2, sticky=tk.W, cnf=pad)
        chk_structured_append.bind("<Button-1>", self._update_image_handler)
        # fra_module_size
        fra_module_size = tk.Frame(frame)
        fra_module_size.grid(row=1, column=3, sticky=tk.W)
        # lbl_module_size
        lbl_module_size = tk.Label(fra_module_size, text="Module Size :")
        lbl_module_size.pack(anchor=tk.W, side=tk.LEFT, cnf=pad)
        # spn_module_size
        self._spn_module_size_var = tk.IntVar(value=5)
        spn_module_size = tk.Spinbox(
            fra_module_size, from_=2, to_=100, width=4, state="readonly", textvariable=self._spn_module_size_var)
        spn_module_size.pack(anchor=tk.W, side=tk.LEFT, cnf=pad)
        spn_module_size.bind("<KeyPress-Up>", self._update_image_handler)
        spn_module_size.bind("<KeyPress-Down>", self._update_image_handler)
        # btn_save
        btn_save = ttk.Button(frame, text="Save", width=19)
        btn_save.grid(row=1, column=4, sticky=tk.E, cnf=pad)
        btn_save.bind("<ButtonRelease-1>", self._btn_save_handler)
        btn_save.bind("<Key-Return>", self._btn_save_handler)
        btn_save.bind("<Key-space>", self._btn_save_handler)

        return frame

    def create_symbols(self) -> Optional[qr.Symbols]:
        data = self._txt_data.get("1.0", tk.END + "-1c")
        if not data:
            return None

        ec_level = qr.ErrorCorrectionLevel.to_int(self._cmb_ec_level_var.get())
        max_ver = int(self._cmb_max_ver_var.get())
        structured_append = bool(self._chk_structured_append_var.get())
        enc_mode = self._cmb_byte_enc_var.get()

        symbols = qr.Symbols(ec_level, max_ver, structured_append, enc_mode)
        try:
            symbols.append_text(data)
        except Exception as e:
            tkmsg.showwarning(message=e)
            return None

        return symbols

    def update_image(self, event) -> None:
        if self._fra_top.winfo_children():
            for widget in self._fra_top.winfo_children():
                widget.destroy()

        symbols = self.create_symbols()
        if not symbols:
            return

        self._images.clear()
        module_size = self._spn_module_size_var.get()

        for symbol in symbols:
            image = symbol.tk_photo_image(module_size)
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
            ("X11 Bitmap", "*.xbm"),
            ("SVG", "*.svg")
        ]
        filename = tkfdlg.asksaveasfilename(defaultextension="bmp", filetypes=filetypes)
        (root, ext) = os.path.splitext(filename)
        ext = ext.lower()

        module_size = self._spn_module_size_var.get()

        for i, symbol in enumerate(symbols):
            if symbols.count == 1:
                path = root + ext
            else:
                path = root + "_" + str(i) + ext

            if ext == ".bmp":
                symbol.save_bitmap(path, module_size, True, )

            if ext == ".ppm":
                symbol.save_ppm(path, module_size)

            if ext == ".xbm":
                symbol.save_xbm(path, module_size)

            if ext == ".svg":
                symbol.save_svg(path, module_size)


def main():
    root = tk.Tk()
    form = FormMain(root)
    form.mainloop()


if __name__ == "__main__":
    main()
