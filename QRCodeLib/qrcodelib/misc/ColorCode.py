from typing import Tuple

import re


class ColorCode(object):

    WHITE = "#FFFFFF"
    BLACK = "#000000"
    
    @classmethod
    def valid(cls, color: str) -> bool:
        return bool(re.match("^#[0-9A-Fa-f]{6}$", color, re.MULTILINE))
    
    @classmethod
    def to_rgb(cls, color: str) -> Tuple[int, int, int]:
        if not cls.valid(color):
            raise ValueError("color")

        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        return r, g, b
