from typing import List
from .constants import Values


class Separator:
    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        value = Values.SEPARATOR
        offset = len(module_matrix) - 8

        for i in range(8):
            module_matrix[i][7] = -value
            module_matrix[7][i] = -value
            module_matrix[offset + i][7] = -value
            module_matrix[offset + 0][i] = -value
            module_matrix[i][offset + 0] = -value
            module_matrix[7][offset + i] = -value
