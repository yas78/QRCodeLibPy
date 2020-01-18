from typing import List
from .misc.array_util import ArrayUtil


class QuietZone(object):
    """
        クワイエットゾーン
    """
    _WIDTH = 4

    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> List[List[int]]:
        """
            クワイエットゾーンを追加します。
        """
        size = len(module_matrix) + cls._WIDTH * 2
        ret = [[0] * size for _ in range(size)]

        for i, row in enumerate(module_matrix):
            ArrayUtil.copy(row, 0, ret[i + cls._WIDTH], cls._WIDTH, len(row))

        return ret
