from typing import List


class TimingPattern(object):
    """
        タイミングパターン
    """    
    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> None:
        """
            タイミングパターンを配置します。
        """
        for i in range(8, len(module_matrix) - 8):
            v = 2 if i % 2 == 0 else -2
            module_matrix[6][i] = v
            module_matrix[i][6] = v
