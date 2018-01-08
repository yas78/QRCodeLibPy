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
        ret = [None] * (len(module_matrix) + cls._QUIET_ZONE_WIDTH * 2)  # type: List[List[int]]
        
        for i in range(len(ret)):
            ret[i] = [0] * len(ret)
        
        for i in range(len(module_matrix)):   
            ArrayUtil.copy(module_matrix[i], 
                           0, 
                           ret[i + cls._QUIET_ZONE_WIDTH], 
                           cls._QUIET_ZONE_WIDTH, 
                           len(module_matrix[i]))
        return ret
