from typing import List


class VersionInfo:
    """
        型番情報
    """
    _version_info_values = [
        -1, -1, -1, -1, -1, -1, -1,
        0x07C94, 0x085BC, 0x09A99, 0x0A4D3, 0x0BBF6, 0x0C762, 0x0D847, 0x0E60D,
        0x0F928, 0x10B78, 0x1145D, 0x12A17, 0x13532, 0x149A6, 0x15683, 0x168C9,
        0x177EC, 0x18EC4, 0x191E1, 0x1AFAB, 0x1B08E, 0x1CC1A, 0x1D33F, 0x1ED75,
        0x1F250, 0x209D5, 0x216F0, 0x228BA, 0x2379F, 0x24B0B, 0x2542E, 0x26A64,
        0x27541, 0x28C69
    ]
    
    @classmethod
    def place(cls, version: int, module_matrix: List[List[int]]) -> None:
        """
            型番情報を配置します。
        """
        num_modules_per_side = len(module_matrix)

        version_info_value = cls._version_info_values[version]

        p1 = 0
        p2 = num_modules_per_side - 11

        for i in range(18):
            v = 3 if (version_info_value & (1 << i)) > 0 else -3

            module_matrix[p1][p2] = v
            module_matrix[p2][p1] = v

            p2 += 1

            if i % 3 == 2:
                p1 += 1
                p2 = num_modules_per_side - 11
        
    @classmethod
    def place_temp_blank(cls, module_matrix: List[List[int]]) -> None:
        """
            型番情報の予約領域を配置します。
        """
        num_modules_per_side = len(module_matrix)

        for i in range(6):
            for j in range(num_modules_per_side - 11, num_modules_per_side - 8):
                module_matrix[i][j] = -3
                module_matrix[j][i] = -3
