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

        self._init_widgets()
        self._images = []
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
        self._fra_middle.pack(expand=False, fill=tk.BOTH, anchor=tk.S)
        # bottom_frame
        self._fra_bottom = self._create_bottom_frame()
        self._fra_bottom.pack(expand=False, fill=tk.X, anchor=tk.NW)

    def _create_top_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray80", height=320)
        frame.propagate(False)
        return frame

    def _create_middle_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray95", height=120)
        # lbl_data
        lbl_data = tk.Label(frame, text="Data :")
        lbl_data.pack(anchor=tk.NW, padx=8)
        # txt_data
        self._txt_data = ScrolledText(frame, height=6)
        self._txt_data.pack(anchor=tk.NW, expand=True, fill=tk.X, padx=8, pady=3)
        self._txt_data.focus_set()
        self._txt_data.bind("<KeyRelease>", self._update_image_handler)
        return frame

    def _create_bottom_frame(self) -> tk.Frame:
        frame = tk.Frame(self, bg="gray95", height=70)
        # lbl_ec_level
        lbl_ec_level = tk.Label(frame, text="Error Correnction Level :")
        lbl_ec_level.place(x=8, y=10)
        # cmb_ec_level
        self._cmb_ec_level_var = tk.StringVar()
        cmb_ec_level = ttk.Combobox(frame, state="readonly", width=4, textvariable=self._cmb_ec_level_var)
        cmb_ec_level["values"] = ["L", "M", "Q", "H"]
        cmb_ec_level.current(1)
        cmb_ec_level.place(x=150, y=10)
        cmb_ec_level.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_max_ver
        lbl_max_ver = tk.Label(frame, text="Max Version :")
        lbl_max_ver.place(x=8, y=40)
        # cmb_max_ver
        self._cmb_max_ver_var = tk.StringVar()
        cmb_max_ver = ttk.Combobox(frame, state="readonly", width=4, height=20, textvariable=self._cmb_max_ver_var)
        cmb_max_ver["values"] = [item + 1 for item in range(40)]
        cmb_max_ver.current(len(cmb_max_ver["values"]) - 1)
        cmb_max_ver.place(x=150, y=40)
        cmb_max_ver.bind("<<ComboboxSelected>>", self._update_image_handler)
        # lbl_byte_enc
        lbl_byte_enc = tk.Label(frame, text="Byte mode Encoding :")
        lbl_byte_enc.place(x=210, y=10)
        # cmb_byte_enc
        self._cmb_byte_enc_var = tk.StringVar()
        cmb_byte_enc = ttk.Combobox(frame, state="readonly", width=56, textvariable=self._cmb_byte_enc_var)
        cmb_byte_enc["values"] = ["Shift_JIS", "UTF-8"]
        cmb_byte_enc.current(0)
        cmb_byte_enc.place(x=335, y=10)
        cmb_byte_enc.bind("<<ComboboxSelected>>", self._update_image_handler)
        # chk_structured_append
        self._chk_structured_append_var = tk.BooleanVar(value=False)
        chk_structured_append = ttk.Checkbutton(
            frame, text="Structured Append", variable=self._chk_structured_append_var)
        chk_structured_append.place(x=210, y=40)
        chk_structured_append.bind("<Button-1>", self._update_image_handler)
        # lbl_module_size
        lbl_module_size = tk.Label(frame, text="Module Size :")
        lbl_module_size.place(x=360, y=40)
        # spn_module_size
        self._spn_module_size_var = tk.IntVar(value=4)
        spn_module_size = tk.Spinbox(
            frame, from_=1, to_=100, width=4, state="readonly", textvariable=self._spn_module_size_var)
        spn_module_size.place(x=440, y=40)
        spn_module_size.bind("<KeyPress-Up>", self._update_image_handler)
        spn_module_size.bind("<KeyPress-Down>", self._update_image_handler)
        # btn_save
        btn_save = ttk.Button(frame, text="Save", width=19)
        btn_save.place(x=570, y=35)
        btn_save.bind("<ButtonRelease-1>", self._btn_save_handler)
        btn_save.bind("<Key-Return>", self._btn_save_handler)
        btn_save.bind("<Key-space>", self._btn_save_handler)
        return frame

    def create_symbols(self):
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

    def update_image(self, event):
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
            ("X11 Bitmap", "*.xbm")
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
                symbol.save_bitmap(path, module_size, True)

            if ext == ".ppm":
                symbol.save_ppm(path, module_size)

            if ext == ".xbm":
                symbol.save_xbm(path, module_size)


def main():
    root = tk.Tk()
    FormTk(root)
    root.mainloop()


if __name__ == "__main__":
    main()
