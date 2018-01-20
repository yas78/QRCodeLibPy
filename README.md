# QRCodeLibPy
QRCodeLibPyは、Python3.5で書かれたQRコード生成ライブラリです。  
JIS X 0510に基づくモデル２コードシンボルを生成します。

## 特徴
- 数字・英数字・8ビットバイト・漢字モードに対応しています
- 分割QRコードを作成可能です
- 1bppまたは24bpp BMPファイル(DIB)、PPM、XBMファイルへ保存可能です
- 画像の配色(前景色・背景色)を指定可能です
- 8ビットバイトモードでの文字コードを指定可能です

## クイックスタート
qrcodelibパッケージへのビルドパスを設定してください。

## 使用方法
### 例１．単一シンボルで構成される(分割QRコードではない)QRコードの、最小限のコードを示します。

```python
from Symbols import Symbols
from Symbol import Symbol

symbols = Symbols()
symbols.append_string("012345abcdefg")

symbol = symbols.item(0)
symbol.save_24bpp_dib("D:\\qrcode.bmp")
```

### 例２．誤り訂正レベルを指定する
Symbolsクラスのコンストラクタ引数に、ErrorCorrectionLevelクラスの定数を設定します。

```python
from ErrorCorrectionLevel import ErrorCorrectionLevel

symbols = Symbols(ErrorCorrectionLevel.H)

```

### 例３．型番の上限を指定する
Symbolsクラスのコンストラクタで設定します。
```python
symbols = Symbols(max_version=10)
```

### 例４．8ビットバイトモードで使用する文字コードを指定する
Symbolsクラスのコンストラクタで設定します。
```python
symbols = Symbols(byte_mode_encoding="utf-8")
```

### 例５．分割QRコードを作成する
Symbolsクラスのコンストラクタで設定します。型番の上限を指定しない場合は、型番40を上限として分割されます。

```python
symbols = Symbols(allow_structured_append=True)
```

型番1を超える場合に分割し、各QRコードをファイルへ保存する例を示します。

```python
symbols = Symbols(max_version=1, allow_structured_append=True)
symbols.append_string("abcdefghijklmnopqrstuvwxyz")

for i in range(0, symbols.count):
    symbols.item(i).save_24bpp_dib("D:\\qrcode_" + str(i) + ".bmp")
```

### 例６．BMPファイルへ保存する
SymbolクラスのSave1bppDIB、またはSave24bppDIBメソッドを使用します。

```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

symbol.save_1bpp_dib("D:\\qrcode.bmp")
symbol.save_1bpp_dib("D:\\qrcode.bmp", module_size=10)
symbol.save_1bpp_dib("D:\\qrcode.bmp", fore_rgb="#0000FF", back_rgb="#FFFFFF")

symbol.save_24bpp_dib("D:\\qrcode.bmp")
symbol.save_24bpp_dib("D:\\qrcode.bmp", module_size=10)
symbol.save_24bpp_dib("D:\\qrcode.bmp", fore_rgb="#0000FF", back_rgb="#FFFFFF")
```

### 例７．PPMファイルへ保存する
```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

symbol.save_ppm("D:\\qrcode.ppm")
symbol.save_ppm("D:\\qrcode.ppm", module_size=10)
symbol.save_ppm("D:\\qrcode.ppm", fore_rgb="#0000FF", back_rgb="#FFFFFF")
```

### 例８．XBMファイルへ保存する
```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

symbol.save_xbm("D:\\qrcode.xbm")
symbol.save_xbm("D:\\qrcode.xbm", module_size=10)
```

### 例１０．RGB RAW画像を取得する
```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes()
(data, width, height) = symbol.get_rgb_bytes(module_size=10)
(data, width, height) = symbol.get_rgb_bytes(fore_rgb="#0000FF", back_rgb="#FFFFFF")
```

### 例１１．tkinter.BitmapImageオブジェクトを取得する
```python
import tkinter as tk
from Symbols import Symbols
from Symbol import Symbol

tkRoot = tk.Tk()

symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

xbm = symbol.get_xbm()
#xbm = symbol.get_xbm(module_size=10)

image = tk.BitmapImage(data=xbm, foreground="#000000", background="#FFFFFF")
```

### 例１２．tkinter.PhotoImageオブジェクトを取得する
```python
import tkinter as tk
from Symbols import Symbols
from Symbol import Symbol

tkRoot = tk.Tk()

symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

ppm = symbol.get_ppm()
#ppm = symbol.get_ppm(module_size=10)
#ppm = symbol.get_ppm(fore_rgb="#0000FF", back_rgb="#FFFFFF")

image = tk.PhotoImage(data=ppm)
```

### 例１３．wxPython.Bitmapオブジェクトを取得する
```python
import wx
from Symbols import Symbols
from Symbol import Symbol

symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes() 
bitmap = wx.Bitmap.FromBuffer(width, height, data)
```

### 例１４．Pillow (PIL) を使用して、その他の画像形式で保存する
```python
import PIL.Image
from Symbols import Symbols
from Symbol import Symbol

symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

(data, width, height) = symbol.get_rgb_bytes()
#(data, width, height) = symbol.get_rgb_bytes(module_size=10)
#(data, width, height) = symbol.get_rgb_bytes(fore_rgb="#0000FF", back_rgb="#FFFFFF")

image = PIL.Image.frombytes("RGB", (width, height), data)

# PNG
image.save("D:\\qrcode.png", "PNG")
# GIF
image.save("D:\\qrcode.gif", "GIF")
# JPEG
image.save("D:\\qrcode.jpg", "JPEG")
```

