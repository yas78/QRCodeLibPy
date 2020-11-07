from typing import List


class Separator:
    """
        分離パターン
    """    
    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        """
            分離パターンを配置します。
        """
        offset = len(module_matrix) - 8

        for i in range(8):
            module_matrix[i][7] = -2
            module_matrix[7][i] = -2
            module_matrix[offset + i][7] = -2
            module_matrix[offset + 0][i] = -2
            module_matrix[i][offset + 0] = -2
            module_matrix[7][offset + i] = -2
