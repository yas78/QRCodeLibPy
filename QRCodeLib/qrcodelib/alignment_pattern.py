from typing import List
from .misc.array_util import ArrayUtil


class AlignmentPattern(object):
    """
        位置合わせパターン
    """
    _center_pos_arrays = [
        None,
        None,
        [6, 18],
        [6, 22],
        [6, 26],
        [6, 30],
        [6, 34],
        [6, 22, 38],
        [6, 24, 42],
        [6, 26, 46],
        [6, 28, 50],
        [6, 30, 54],
        [6, 32, 58],
        [6, 34, 62],
        [6, 26, 46, 66],
        [6, 26, 48, 70],
        [6, 26, 50, 74],
        [6, 30, 54, 78],
        [6, 30, 56, 82],
        [6, 30, 58, 86],
        [6, 34, 62, 90],
        [6, 28, 50, 72, 94],
        [6, 26, 50, 74, 98],
        [6, 30, 54, 78, 102],
        [6, 28, 54, 80, 106],
        [6, 32, 58, 84, 110],
        [6, 30, 58, 86, 114],
        [6, 34, 62, 90, 118],
        [6, 26, 50, 74, 98, 122],
        [6, 30, 54, 78, 102, 126],
        [6, 26, 52, 78, 104, 130],
        [6, 30, 56, 82, 108, 134],
        [6, 34, 60, 86, 112, 138],
        [6, 30, 58, 86, 114, 142],
        [6, 34, 62, 90, 118, 146],
        [6, 30, 54, 78, 102, 126, 150],
        [6, 24, 50, 76, 102, 128, 154],
        [6, 28, 54, 80, 106, 132, 158],
        [6, 32, 58, 84, 110, 136, 162],
        [6, 26, 54, 82, 110, 138, 166],
        [6, 30, 58, 86, 114, 142, 170]
    ]

    @classmethod
    def place(cls, version: int, module_matrix: List[List[int]]) -> None:
        """
            位置合わせパターンを配置します。
        """
        center_pos_array: List[int] = cls._center_pos_arrays[version]

        length = len(center_pos_array)
        max_index = length - 1

        for i in range(length):
            r = center_pos_array[i]

            for j in range(length):
                c = center_pos_array[j]

                # 位置検出パターンと重なる場合
                if (
                    i == 0 and j == 0 or
                    i == 0 and j == max_index or
                    i == max_index and j == 0
                ):
                    continue

                ArrayUtil.copy([2,  2,  2,  2,  2], 0, module_matrix[r - 2], c - 2, 5)
                ArrayUtil.copy([2, -2, -2, -2,  2], 0, module_matrix[r - 1], c - 2, 5)
                ArrayUtil.copy([2, -2,  2, -2,  2], 0, module_matrix[r + 0], c - 2, 5)
                ArrayUtil.copy([2, -2, -2, -2,  2], 0, module_matrix[r + 1], c - 2, 5)
                ArrayUtil.copy([2,  2,  2,  2,  2], 0, module_matrix[r + 2], c - 2, 5)
