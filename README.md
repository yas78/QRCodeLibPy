# QRCodeLibPy
QRCodeLibPyは、Python3で書かれたQRコード生成ライブラリです。  
JIS X 0510に基づくモデル２コードシンボルを生成します。

## 特徴
- 数字・英数字・8ビットバイト・漢字モードに対応しています
- 分割QRコードを作成可能です
- 1bppまたは24bpp BMP、PPM、XBM SVG形式でファイルに保存可能です
- Base64エンコードされたBitmapデータを取得可能です
- 画像の前景色、背景色を指定可能です
- 8ビットバイトモードでの文字コードを指定可能です

## クイックスタート
qrcodelibパッケージをインポートしてください。

## デモ
TkInter版は TkInterDemo.py 。WxPython版は WxPythonDemo.py モジュールを実行してください。  
WxPython版はWxPythonのインストールが必要です。

## 使用方法
### 例１．単一シンボルで構成される(分割QRコードではない)QRコードの、最小限のコードを示します。

```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")

symbol = symbols.item(0)
```

### 例２．誤り訂正レベルを指定する
Symbolsクラスのコンストラクタ引数に、ErrorCorrectionLevelクラスの定数を設定します。
```python
import qrcodelib as qr

symbols = qr.Symbols(qr.ErrorCorrectionLevel.L)
```

### 例３．型番の上限を指定する
Symbolsクラスのコンストラクタで設定します。
```python
import qrcodelib as qr

symbols = qr.Symbols(max_version=10)
```

### 例４．8ビットバイトモードで使用する文字コードを指定する
Symbolsクラスのコンストラクタで設定します。
```python
import qrcodelib as qr

symbols = qr.Symbols(byte_mode_encoding="utf-8")
```

### 例５．分割QRコードを作成する
Symbolsクラスのコンストラクタで設定します。型番の上限を指定しない場合は、型番40を上限として分割されます。
```python
import qrcodelib as qr

symbols = qr.Symbols(allow_structured_append=True)
```

型番1を超える場合に分割し、各QRコードをファイルへ保存する例を示します。
```python
import qrcodelib as qr

symbols = qr.Symbols(max_version=1, allow_structured_append=True)
symbols.append_text("abcdefghijklmnopqrstuvwxyz")

for i in range(symbols.count):
    symbols.item(i).save_bitmap(f"qrcode_{str(i)}.bmp")
```

### 例６．ファイルへ保存する
```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

# 24bpp DIB
symbol.save_bitmap("qrcode.bmp")
# 1bpp DIB
symbol.save_bitmap("qrcode.bmp", monochrome=True)
# 10 pixels per module
symbol.save_bitmap("qrcode.bmp", module_size=10)
# Specify foreground and background colors
symbol.save_bitmap("qrcode.bmp", fore_rgb="#0000FF", back_rgb="#FFFFFF")

# PPM
symbol.save_ppm("qrcode.ppm")
# XBM
symbol.save_xbm("qrcode.xbm")
# SVG
symbol.save_svg("qrcode.svg")
```

### 例７．RGB RAW画像を取得する
```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes()
```

### 例８．SVG画像を取得する
```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

svg = symbol.get_svg()
```

### 例９．tkinter.BitmapImage, tkinter.PhotoImageオブジェクトを取得する
```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

# BitmapImage
image = symbol.tk_bitmap_image()
# PhotoImage
image = symbol.tk_photo_image()
```

### 例１０．wxPython.Bitmapオブジェクトを取得する
```python
import wx
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes() 
bitmap = wx.Bitmap.FromBuffer(width, height, data)
```

### 例１１．Pillow (PIL) を使用して、様々な画像形式で保存する
```python
import PIL.Image
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes()
image = PIL.Image.frombytes("RGB", (width, height), data)

# PNG
image.save("qrcode.png", "PNG")
# GIF
image.save("qrcode.gif", "GIF")
# JPEG
image.save("qrcode.jpg", "JPEG")
```

### 例１２．base64エンコードされたビットマップデータを取得する
```python
import qrcodelib as qr

symbols = qr.Symbols()
symbols.append_text("012345abcdefg")
symbol = symbols.item(0)

base64 = symbol.get_bitmap_base64()
```
