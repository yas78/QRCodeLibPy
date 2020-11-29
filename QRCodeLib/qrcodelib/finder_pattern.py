from typing import List


class FinderPattern:
    _finder_pattern = [
        [2,  2,  2,  2,  2,  2, 2],
        [2, -2, -2, -2, -2, -2, 2],
        [2, -2,  2,  2,  2, -2, 2],
        [2, -2,  2,  2,  2, -2, 2],
        [2, -2,  2,  2,  2, -2, 2],
        [2, -2, -2, -2, -2, -2, 2],
        [2,  2,  2,  2,  2,  2, 2]
    ]

    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        offset = len(module_matrix) - len(cls._finder_pattern)

        for i in range(len(cls._finder_pattern)):
            for j in range(len(cls._finder_pattern[i])):
                v = cls._finder_pattern[i][j]
                module_matrix[i][j] = v
                module_matrix[i][j + offset] = v
                module_matrix[i + offset][j] = v
