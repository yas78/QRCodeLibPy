from ctypes import Structure, c_char


class RGBQUAD(Structure):
    """
        RGBQUAD構造体
    """
    _fields_ = [
        ("rgbBlue", c_char),
        ("rgbGreen", c_char),
        ("rgbRed", c_char),
        ("rgbReserved", c_char)
    ]
