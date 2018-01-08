from format.Codeword import Codeword
from format.DataCodeword import DataCodeword


class RSBlock(object):
    """
        RSブロック
    """
    # RSブロック数    
    _total_numbers = [
        [
            -1,
             1,  1,  1,  1,  1,  2,  2,  2,  2,  4,
             4,  4,  4,  4,  6,  6,  6,  6,  7,  8,
             8,  9,  9, 10, 12, 12, 12, 13, 14, 15,
            16, 17, 18, 19, 19, 20, 21, 22, 24, 25
        ],
        [
            -1,
             1,  1,  1,  2,  2,  4,  4,  4,  5,  5,
             5,  8,  9,  9, 10, 10, 11, 13, 14, 16,
            17, 17, 18, 20, 21, 23, 25, 26, 28, 29,
            31, 33, 35, 37, 38, 40, 43, 45, 47, 49
        ],
        [
            -1,
             1,  1,  2,  2,  4,  4,  6,  6,  8,  8,
             8, 10, 12, 16, 12, 17, 16, 18, 21, 20,
            23, 23, 25, 27, 29, 34, 34, 35, 38, 40,
            43, 45, 48, 51, 53, 56, 59, 62, 65, 68
        ],
        [
            -1,
             1,  1,  2,  4,  4,  4,  5,  6,  8,  8,
            11, 11, 16, 16, 18, 16, 19, 21, 25, 25,
            25, 34, 30, 32, 35, 37, 40, 42, 45, 48,
            51, 54, 57, 60, 63, 66, 70, 74, 77, 81
        ]
    ]

    @classmethod
    def get_total_number(cls, ec_level: int, version: int, preceding: bool) -> int:
        """
            RSブロック数を返します。
        """
        num_data_codewords = DataCodeword.get_total_number(ec_level, version)
        num_rs_blocks = cls._total_numbers[ec_level][version]

        num_fol_blocks = num_data_codewords % num_rs_blocks

        if preceding:
            return num_rs_blocks - num_fol_blocks
        else:
            return num_fol_blocks

    @classmethod
    def get_number_data_codewords(cls, ec_level: int, version: int, preceding: bool) -> int:
        """
            RSブロックのデータコード語数を返します。
        """
        num_data_codewords = DataCodeword.get_total_number(ec_level, version)
        num_rs_blocks = cls._total_numbers[ec_level][version]

        num_pre_block_codewords = num_data_codewords // num_rs_blocks

        if preceding:
            return num_pre_block_codewords
        else:
            num_pre_blocks = cls.get_total_number(ec_level, version, True)
            num_fol_blocks = cls.get_total_number(ec_level, version, False)
            
            if num_fol_blocks > 0:
                return (
                    (num_data_codewords - num_pre_block_codewords * num_pre_blocks)
                    // num_fol_blocks
                )
            else:
                return 0

    @classmethod
    def get_number_ec_codewords(cls, ec_level: int, version: int) -> int:
        """
            RSブロックの誤り訂正コード語数を返します。
        """
        num_data_codewords = DataCodeword.get_total_number(ec_level, version)
        num_rs_blocks = cls._total_numbers[ec_level][version]

        return ((Codeword.get_total_number(version) // num_rs_blocks)
                - (num_data_codewords // num_rs_blocks))
