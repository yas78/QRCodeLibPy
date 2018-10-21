from typing import List

from misc.ArrayUtil import ArrayUtil


class QuietZone(object):
    """
        クワイエットゾーン
    """    
    _QUIET_ZONE_WIDTH = 4

    @classmethod
    def place(cls, module_matrix: List[List[int]]) -> List[List[int]]:
        """
            クワイエットゾーンを追加します。
        """
        num_modules_one_side = len(module_matrix) + cls._QUIET_ZONE_WIDTH * 2
        ret = [[0] * num_modules_one_side for row in range(num_modules_one_side)]

        for i, row in enumerate(module_matrix):   
            ArrayUtil.copy(row, 
                           0, 
                           ret[i + cls._QUIET_ZONE_WIDTH], 
                           cls._QUIET_ZONE_WIDTH, 
                           len(row))

        return ret
