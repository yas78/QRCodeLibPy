import math
import re


class Color:
    BLACK = "#000000"
    WHITE = "#FFFFFF"

    def __init__(self, r: int, g: int, b: int) -> None:
        if (not (0 <= r <= 255)) or (not (0 <= g <= 255)) or (not (0 <= b <= 255)):
            raise ValueError('Argument our of range')

        self._r = math.floor(r)
        self._g = math.floor(g)
        self._b = math.floor(b)

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError('value')
        self._r = math.floor(value)

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError('value')
        self._g = math.floor(value)

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError('value')
        self._b = math.floor(value)

    @classmethod
    def decode(cls, html_color: str):
        if not cls.is_html_color(html_color):
            raise ValueError('html_color')

        ret = Color(int(html_color[1:3], 16), int(html_color[3:5], 16), int(html_color[5:7], 16))
        return ret

    @classmethod
    def is_html_color(cls, html_color: str) -> bool:
        return bool(re.match("^#[0-9A-Fa-f]{6}$", html_color, re.MULTILINE))
