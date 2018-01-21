from typing import List

import math

from ModuleRatio import ModuleRatio
from QuietZone import QuietZone


class MaskingPenaltyScore(object):
    """
        マスクされたシンボルの失点評価
    """    
    @classmethod
    def calc_total(cls, module_matrix: List[List[int]]) -> int:
        """
            マスクパターン失点の合計を返します。
        """
        total = 0
        penalty = cls._calc_adjacent_modules_in_same_color(module_matrix)
        total += penalty
        penalty = cls._calc_block_of_modules_in_same_color(module_matrix)
        total += penalty
        penalty = cls._calc_module_ratio(module_matrix)
        total += penalty
        penalty = cls._calc_proportion_of_dark_modules(module_matrix)
        total += penalty
        return total

    @classmethod
    def _calc_adjacent_modules_in_same_color(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行／列の同色隣接モジュールパターンの失点を計算します。
        """
        penalty = 0
        penalty += cls._calc_adjacent_modules_in_row_in_same_color(
            module_matrix)
        penalty += cls._calc_adjacent_modules_in_row_in_same_color(
            cls._matrix_rotate_90(module_matrix))
        return penalty

    @classmethod
    def _calc_adjacent_modules_in_row_in_same_color(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行の同色隣接モジュールパターンの失点を計算します。
        """
        penalty = 0

        for columns in module_matrix:
            cnt = 1

            for c in range(len(columns) - 1):
                if (columns[c] > 0) == (columns[c + 1] > 0):
                    cnt += 1
                else:
                    if cnt >= 5:
                        penalty += 3 + (cnt - 5)
                    cnt = 1

            if cnt >= 5:
                penalty += 3 + (cnt - 5)
            
        return penalty

    @classmethod
    def _calc_block_of_modules_in_same_color(
            cls, module_matrix: List[List[int]]) -> int:
        """
            2x2の同色モジュールパターンの失点を計算します。
        """
        penalty = 0

        for r in range(len(module_matrix) - 1):
            for c in range(len(module_matrix[r]) - 1):
                if ((module_matrix[r + 0][c + 0] > 0) ==
                    (module_matrix[r + 0][c + 1] > 0) ==
                    (module_matrix[r + 1][c + 0] > 0) ==
                    (module_matrix[r + 1][c + 1] > 0)):
                        penalty += 3

        return penalty

    @classmethod
    def _calc_module_ratio(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行／列における1 : 1 : 3 : 1 : 1 比率パターンの失点を計算します。
        """
        module_matrix_temp = QuietZone.place(module_matrix)

        penalty = 0
        penalty += cls._calc_module_ratio_in_row(
            module_matrix_temp)
        penalty += cls._calc_module_ratio_in_row(
            cls._matrix_rotate_90(module_matrix_temp))
        return penalty

    @classmethod
    def _calc_module_ratio_in_row(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行の1 : 1 : 3 : 1 : 1 比率パターンの失点を計算します。
        """
        penalty = 0

        for columns in module_matrix:
            start_indexes = [0]

            for c in range(len(columns) - 1):
                if columns[c] > 0 and columns[c + 1] <= 0:
                    start_indexes.append(c + 1)

            max_index = len(columns) - 1

            for index in start_indexes:
                module_ratio = ModuleRatio()

                while index <= max_index and columns[index] <= 0:
                    module_ratio.pre_light4 += 1
                    index += 1

                while index <= max_index and columns[index] > 0:
                    module_ratio.pre_dark1 += 1
                    index += 1

                while index <= max_index and columns[index] <= 0:
                    module_ratio.pre_light1 += 1
                    index += 1
                
                while index <= max_index and columns[index] > 0:
                    module_ratio.center_dark3 += 1
                    index += 1

                while index <= max_index and columns[index] <= 0:
                    module_ratio.fol_light1 += 1
                    index += 1

                while index <= max_index and columns[index] > 0:
                    module_ratio.fol_dark1 += 1
                    index += 1

                while index <= max_index and columns[index] <= 0:
                    module_ratio.fol_light4 += 1
                    index += 1
                
                if module_ratio.penalty_imposed():
                    penalty += 40
                
        return penalty

    @classmethod
    def _calc_proportion_of_dark_modules(
            cls, module_matrix: List[List[int]]) -> int:
        """
            全体に対する暗モジュールの占める割合について失点を計算します。
        """
        dark_count = 0

        for columns in module_matrix:
            for value in columns:
                if value > 0:
                    dark_count += 1

        num_modules = float(len(module_matrix) ** 2)
        temp = math.ceil(dark_count / num_modules * 100)
        temp = abs(temp - 50)
        temp = (temp + 4) // 5
        return temp * 10

    @classmethod
    def _matrix_rotate_90(cls, arg: List[List[int]]) -> List[List[int]]:
        ret = [None] * len(arg[0])  # type: List[List[int]]
    
        for i in range(len(ret)):
            ret[i] = [0] * len(arg)
    
        k = len(ret) - 1
    
        for i in range(len(ret)):
            for j in range(len(ret[i])):
                ret[i][j] = arg[j][k - i]

        return ret
