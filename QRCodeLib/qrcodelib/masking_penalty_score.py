from typing import List
import math
from .quiet_zone import QuietZone
from .misc.array_util import ArrayUtil


class MaskingPenaltyScore:
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
            ArrayUtil.rotate90(module_matrix))

        return penalty

    @classmethod
    def _calc_adjacent_modules_in_row_in_same_color(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行の同色隣接モジュールパターンの失点を計算します。
        """
        penalty = 0

        for row in module_matrix:
            cnt = 1

            for c in range(len(row) - 1):
                if (row[c] > 0) == (row[c + 1] > 0):
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
                if (module_matrix[r + 0][c + 0] > 0) == \
                   (module_matrix[r + 0][c + 1] > 0) == \
                   (module_matrix[r + 1][c + 0] > 0) == \
                   (module_matrix[r + 1][c + 1] > 0):
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
        penalty += cls._calc_module_ratio_in_row(module_matrix_temp)
        penalty += cls._calc_module_ratio_in_row(ArrayUtil.rotate90(module_matrix_temp))

        return penalty

    @classmethod
    def _calc_module_ratio_in_row(
            cls, module_matrix: List[List[int]]) -> int:
        """
            行の1 : 1 : 3 : 1 : 1 比率パターンの失点を計算します。
        """
        penalty = 0

        for row in module_matrix:
            ratio3_ranges = cls._get_ratio3_ranges(row)

            for rng in ratio3_ranges:
                ratio3 = rng[1] + 1 - rng[0]
                ratio1 = ratio3 // 3
                ratio4 = ratio1 * 4
                impose = False

                i = rng[0] - 1

                # light ratio 1
                cnt = 0
                while i >= 0:
                    if row[i] > 0:
                        break
                    cnt += 1
                    i -= 1

                if cnt != ratio1:
                    continue

                # dark ratio 1
                cnt = 0
                while i >= 0:
                    if row[i] <= 0:
                        break
                    cnt += 1
                    i -= 1

                if cnt != ratio1:
                    continue

                # light ratio 4
                cnt = 0
                while i >= 0:
                    if row[i] > 0:
                        break
                    cnt += 1
                    i -= 1

                if cnt >= ratio4:
                    impose = True

                i = rng[1] + 1

                # light ratio 1
                cnt = 0
                while i < len(row):
                    if row[i] > 0:
                        break
                    cnt += 1
                    i += 1

                if cnt != ratio1:
                    continue

                # dark ratio 1
                cnt = 0
                while i < len(row):
                    if row[i] <= 0:
                        break
                    cnt += 1
                    i += 1

                if cnt != ratio1:
                    continue

                # light ratio 4
                cnt = 0
                while i < len(row):
                    if row[i] > 0:
                        break
                    cnt += 1
                    i += 1

                if cnt >= ratio4:
                    impose = True

                if impose:
                    penalty += 40

        return penalty

    @classmethod
    def _get_ratio3_ranges(cls, arg: List[int]):
        ret = []
        s = 0

        for i in range(1, len(arg) - 1):
            if arg[i] > 0:
                if arg[i - 1] <= 0:
                    s = i

                if arg[i + 1] <= 0:
                    if (i + 1 - s) % 3 == 0:
                        ret.append([s, i])

        return ret

    @classmethod
    def _calc_proportion_of_dark_modules(
            cls, module_matrix: List[List[int]]) -> int:
        """
            全体に対する暗モジュールの占める割合について失点を計算します。
        """
        dark_count = 0

        for row in module_matrix:
            for value in row:
                if value > 0:
                    dark_count += 1

        num_modules = float(len(module_matrix) ** 2)
        temp = int(math.ceil(dark_count / num_modules * 100))
        temp = abs(temp - 50)
        temp = (temp + 4) // 5
        return temp * 10

