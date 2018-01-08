from typing import List


class RemainderBit(object):
    """
        残余ビット
    """    
    @classmethod
    def place(cls, module_matrix: List[List[int]]):
        """
            残余ビットを配置します。
        """
        for r in range(len(module_matrix)):
            for c in range(len(module_matrix[r])):
                if module_matrix[r][c] == 0:
                    module_matrix[r][c] = -1
