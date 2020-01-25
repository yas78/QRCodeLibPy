from io import BytesIO
from .bitmapfileheader import BITMAPFILEHEADER
from .bitmapinfoheader import BITMAPINFOHEADER
from .color import Color
from .rgbquad import RGBQUAD


class DIB(object):

    @classmethod
    def build_1bpp_dib(cls,
                       bitmap_data: bytes,
                       width: int,
                       height: int,
                       fore_color: Color,
                       back_color: Color) -> bytes:
        bfh = BITMAPFILEHEADER(
            0x4D42,
            62 + len(bitmap_data),
            0,
            0,
            62
        )

        bih = BITMAPINFOHEADER(
            40,
            width,
            height,
            1,
            1,
            0,
            0,
            3780,
            3780,
            0,
            0
        )

        palette1 = RGBQUAD(fore_color.r, fore_color.g, fore_color.b)
        palette2 = RGBQUAD(back_color.r, back_color.g, back_color.b)

        with BytesIO() as buffer:
            buffer.write(bfh)
            buffer.write(bih)
            buffer.write(palette1)
            buffer.write(palette2)
            buffer.write(bitmap_data)
            ret = buffer.getvalue()

        return ret

    @classmethod
    def build_24bpp_dib(cls, bitmap_data: bytes, width: int, height: int) -> bytes:
        bfh = BITMAPFILEHEADER(
            0x4D42,
            54 + len(bitmap_data),
            0,
            0,
            54
        )

        bih = BITMAPINFOHEADER(
            40,
            width,
            height,
            1,
            24,
            0,
            0,
            3780,
            3780,
            0,
            0
        )

        with BytesIO() as buffer:
            buffer.write(bfh)
            buffer.write(bih)
            buffer.write(bitmap_data)
            ret = buffer.getvalue()

        return ret
