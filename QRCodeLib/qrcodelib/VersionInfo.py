from typing import List


class VersionInfo(object):
    """
        型番情報
    """
    _version_info_values = [
        -1, -1, -1, -1, -1, -1, -1,
        0x007C94, 0x0085BC, 0x009A99, 0x00A4D3, 0x00BBF6, 0x00C762, 0x00D847, 0x00E60D,
        0x00F928, 0x010B78, 0x01145D, 0x012A17, 0x013532, 0x0149A6, 0x015683, 0x0168C9,
        0x0177EC, 0x018EC4, 0x0191E1, 0x01AFAB, 0x01B08E, 0x01CC1A, 0x01D33F, 0x01ED75,
        0x01F250, 0x0209D5, 0x0216F0, 0x0228BA, 0x02379F, 0x024B0B, 0x02542E, 0x026A64,
        0x027541, 0x028C69
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
