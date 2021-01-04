from typing import List
from .constants import Values


class TimingPattern:
    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        for i in range(8, len(module_matrix) - 8):
            v = Values.TIMING if i % 2 == 0 else -Values.TIMING
            module_matrix[6][i] = v
            module_matrix[i][6] = v
