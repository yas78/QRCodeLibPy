from typing import List
from .misc.array_util import ArrayUtil


class QuietZone:
    """
        クワイエットゾーン
    """
    _WIDTH_LOWER_LIMIT = 4
    _width = _WIDTH_LOWER_LIMIT

    @classmethod
    def get_width(cls) -> int:
        return cls._width

    @classmethod
    def set_width(cls, value: int) -> None:
        if value < cls._WIDTH_LOWER_LIMIT:
            raise ValueError("value")

        cls._width = value

    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> List[List[int]]:
        """
            クワイエットゾーンを追加します。
        """
        size = len(module_matrix) + cls.get_width() * 2
        ret = [[0] * size for _ in range(size)]

        for i, row in enumerate(module_matrix):
            ArrayUtil.copy(row, 0, ret[i + cls.get_width()], cls.get_width(), len(row))

        return ret
