from ctypes import Structure, c_uint16, c_uint32


class BITMAPFILEHEADER(Structure):
    _pack_ = 2
    _fields_ = [
        ("bfType", c_uint16),
        ("bfSize", c_uint32),
        ("bfReserved1", c_uint16),
        ("bfReserved2", c_uint16),
        ("bfOffBits", c_uint32)
    ]
