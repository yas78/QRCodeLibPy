import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("abcdefghijklmn")
symbols.item(0).save_bitmap(r"C:\Users\owner\Documents\Visual Studio 2019\Projects\github\QRCodeLibPy\test.bmp")