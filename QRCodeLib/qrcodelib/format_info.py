from typing import List
from .error_correction_level import ErrorCorrectionLevel


class FormatInfo:
    _format_info_values = [
        0x0000, 0x0537, 0x0A6E, 0x0F59, 0x11EB, 0x14DC, 0x1B85, 0x1EB2, 0x23D6, 0x26E1,
        0x29B8, 0x2C8F, 0x323D, 0x370A, 0x3853, 0x3D64, 0x429B, 0x47AC, 0x48F5, 0x4DC2,
        0x5370, 0x5647, 0x591E, 0x5C29, 0x614D, 0x647A, 0x6B23, 0x6E14, 0x70A6, 0x7591,
        0x7AC8, 0x7FFF
    ]

    _format_info_mask_array = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]

    @classmethod
    def place(cls,
              ec_level: int,
              mask_pattern_reference: int,
              module_matrix: List[List[int]]) -> None:
        format_info_value = cls.get_format_info_value(ec_level, mask_pattern_reference)

        r1 = 0
        c1 = len(module_matrix) - 1

        for i in range(8):
            temp = ((1 if (format_info_value & (1 << i)) > 0 else 0)
                    ^ cls._format_info_mask_array[i])
            
            v = 3 if temp > 0 else -3

            module_matrix[r1][8] = v
            module_matrix[8][c1] = v

            r1 += 1
            c1 -= 1

            if r1 == 6:
                r1 += 1

        r2 = len(module_matrix) - 7
        c2 = 7

        for i in range(8, 15):
            temp = ((1 if (format_info_value & (1 << i)) > 0 else 0)
                    ^ cls._format_info_mask_array[i])

            v = 3 if temp > 0 else -3
            module_matrix[r2][8] = v
            module_matrix[8][c2] = v

            r2 += 1
            c2 -= 1

            if c2 == 6:
                c2 -= 1

    @classmethod
    def place_temp_blank(cls, module_matrix: List[List[int]]) -> None:
        num_modules_one_side = len(module_matrix)

        for i in range(9):
            # タイミグパターンの領域ではない場合
            if i != 6:
                module_matrix[8][i] = -3
                module_matrix[i][8] = -3

        for i in range(num_modules_one_side - 8, num_modules_one_side):
            module_matrix[8][i] = -3
            module_matrix[i][8] = -3

        # 固定暗モジュールを配置(マスクの適用前に配置する)
        module_matrix[num_modules_one_side - 8][8] = 2

    @classmethod
    def get_format_info_value(cls, 
                              ec_level: int, 
                              mask_pattern_reference: int) -> int:
        if ec_level == ErrorCorrectionLevel.L:
            indicator = 1
        elif ec_level == ErrorCorrectionLevel.M:
            indicator = 0
        elif ec_level == ErrorCorrectionLevel.Q:
            indicator = 3
        elif ec_level == ErrorCorrectionLevel.H:
            indicator = 2
        else:
            raise ValueError("ec_level")
        
        return cls._format_info_values[(indicator << 3) | mask_pattern_reference]
