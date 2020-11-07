from typing import Callable, List
import copy
import sys
from .format_info import FormatInfo
from .masking_penalty_score import MaskingPenaltyScore
from .version_info import VersionInfo


class Masking:
    """
        シンボルマスク
    """    
    @classmethod
    def apply(cls, 
              version: int, 
              ec_level: int,
              module_matrix: List[List[int]]) -> int:
        """
            マスクを適用します。
        """
        min_penalty = sys.maxsize
        mask_pattern_reference = 0
        masked_matrix = []

        for i in range(8):
            temp = copy.deepcopy(module_matrix)

            cls._mask(i, temp) 
            FormatInfo.place(ec_level, i, temp)

            if version >= 7:
                VersionInfo.place(version, temp)
            
            penalty = MaskingPenaltyScore.calc_total(temp)
            
            if penalty < min_penalty:
                min_penalty = penalty
                mask_pattern_reference = i
                masked_matrix = temp

        module_matrix[:] = masked_matrix
        return mask_pattern_reference

    @classmethod
    def _mask(cls, 
              mask_pattern_reference: int,
              module_matrix: List[List[int]]) -> None:
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
