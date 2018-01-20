# QRCodeLibPy
QRCodeLibPyは、Python3.5で書かれたQRコード生成ライブラリです。  
JIS X 0510に基づくモデル２コードシンボルを生成します。

## 特徴
- 数字・英数字・8ビットバイト・漢字モードに対応しています
- 分割QRコードを作成可能です
- 1bppまたは24bpp BMPファイル(DIB)、PPM、XBMファイルへ保存可能です
- 1bppまたは24bpp tkinter.BitmapImageオブジェクトとして取得可能です  
- 画像の配色(前景色・背景色)を指定可能です
- 8ビットバイトモードでの文字コードを指定可能です


## クイックスタート
QRCodeLibプロジェクト、またはビルドした QRCodeLib.dll を参照設定してください。


## 使用方法
### 例１．単一シンボルで構成される(分割QRコードではない)QRコードの、最小限のコードを示します。

```python
from Symbols import Symbols

def Example():
    symbols = Symbols()
    symbols.append_string("012345abcdefg")
    
    symbol = symbols.item(0)
    symbol.save_24bpp_dib("D:\\qrcode.bmp")
```

### 例２．誤り訂正レベルを指定する
Symbolsクラスのコンストラクタ引数に、ErrorCorrectionLevel列挙型の値を設定します。

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

symbol.save_1bpp_dib("D:\\qrcode1.bmp")
symbol.save_1bpp_dib("D:\\qrcode2.bmp", 10)  # 10 pixels per module
symbol.save_24bpp_dib("D:\\qrcode3.bmp")
symbol.save_24bpp_dib("D:\\qrcode4.bmp", 10)  # 10 pixels per module
```

### 例７．PPMファイルへ保存する
```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

symbol.save_ppm_binary("D:\\qrcode.ppm")
```

### 例８．XBMファイルへ保存する
```python
symbols = Symbols()
symbols.append_string("012345abcdefg")
symbol = symbols.item(0)

symbol.save_xbm("D:\\qrcode.xbm")
```



その他の画像形式で保存するには、Imageオブジェクト使用します。

```csharp
using System.Drawing;
using System.Drawing.Imaging;

Symbols symbols = new Symbols();
symbols.AppendString("012345");

Image image = symbols[0].Get24bppImage();
// PNG
image.Save(@"D:\qrcode.png", ImageFormat.Png);
// GIF
image.Save(@"D:\qrcode.gif", ImageFormat.Gif);
// JPEG
image.Save(@"D:\qrcode.jpg", ImageFormat.Jpeg);
```

