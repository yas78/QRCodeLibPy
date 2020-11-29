from typing import List


class RemainderBit:
    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        for r in range(len(module_matrix)):
            for c in range(len(module_matrix[r])):
                if module_matrix[r][c] == 0:
                    module_matrix[r][c] = -1
