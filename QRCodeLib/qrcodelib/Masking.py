from typing import Callable, List

import copy
import sys

from .FormatInfo import FormatInfo
from .MaskingPenaltyScore import MaskingPenaltyScore
from .VersionInfo import VersionInfo


class Masking(object):
    """
        シンボルマスク
    """    
    @classmethod
    def apply(cls, 
              module_matrix: List[List[int]], 
              version: int, 
              ec_level: int) -> int:
        """
            マスクを適用します。
        """
        mask_pattern_reference = cls._select_mask_pattern(
            module_matrix, version, ec_level)
        cls._mask(module_matrix, mask_pattern_reference)

        return mask_pattern_reference

    @classmethod
    def _select_mask_pattern(cls, 
                             module_matrix: List[List[int]], 
                             version: int, 
                             ec_level: int) -> int:
        """
            マスクパターンを決定します。
        """
        min_penalty = sys.maxsize
        ret = 0

        for mask_pattern_reference in range(8):
            temp = copy.deepcopy(module_matrix)
            cls._mask(temp, mask_pattern_reference) 
            
            FormatInfo.place(temp, ec_level, mask_pattern_reference)

            if version >= 7:
                VersionInfo.place(temp, version)
            
            penalty = MaskingPenaltyScore.calc_total(temp)
            
            if penalty < min_penalty:
                min_penalty = penalty
                ret = mask_pattern_reference
            
        return ret

    @classmethod
    def _mask(cls, 
              module_matrix: List[List[int]], 
              mask_pattern_reference: int):
        """
            マスクパターンを適用したシンボルデータを返します。
        """
        condition = cls._get_condition(mask_pattern_reference)

        for r in range(len(module_matrix)):
            for c in range(len(module_matrix[r])):
                if abs(module_matrix[r][c]) == 1:
                    if condition(r, c):
                        module_matrix[r][c] *= -1

    @classmethod
    def _get_condition(cls, 
                       mask_pattern_reference: int) -> Callable[[int, int], bool]:
        """
            マスク条件を返します。
        """
        if mask_pattern_reference == 0:
            return lambda r, c: (r + c) % 2 == 0

        if mask_pattern_reference == 1:
            return lambda r, c: r % 2 == 0

        if mask_pattern_reference == 2:
            return lambda r, c: c % 3 == 0

        if mask_pattern_reference == 3:
            return lambda r, c: (r + c) % 3 == 0

        if mask_pattern_reference == 4:
            return lambda r, c: ((r // 2) + (c // 3)) % 2 == 0

        if mask_pattern_reference == 5:
            return lambda r, c: ((r * c) % 2 + (r * c) % 3) == 0

        if mask_pattern_reference == 6:
            return lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0

        if mask_pattern_reference == 7:
            return lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0

        raise ValueError("mask_pattern_reference")
