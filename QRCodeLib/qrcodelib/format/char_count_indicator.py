from ..encoding_mode import EncodingMode


class CharCountIndicator(object):
    """
        文字数指示子
    """    
    @classmethod
    def get_length(cls, version: int, encoding: int) -> int:
        """
            文字数指示子のビット数を返します。
        """
        if 1 <= version <= 9:
            if encoding == EncodingMode.NUMERIC:
                return 10

            if encoding == EncodingMode.ALPHA_NUMERIC:
                return 9
            
            if encoding == EncodingMode.EIGHT_BIT_BYTE:
                return 8
            
            if encoding == EncodingMode.KANJI:
                return 8
            
            raise ValueError("encoding")

        elif 10 <= version <= 26:
            if encoding == EncodingMode.NUMERIC:
                return 12

            if encoding == EncodingMode.ALPHA_NUMERIC:
                return 11
            
            if encoding == EncodingMode.EIGHT_BIT_BYTE:
                return 16
            
            if encoding == EncodingMode.KANJI:
                return 10
            
            raise ValueError("encoding")

        elif 27 <= version <= 40:
            if encoding == EncodingMode.NUMERIC:
                return 14
            
            if encoding == EncodingMode.ALPHA_NUMERIC:
                return 13
            
            if encoding == EncodingMode.EIGHT_BIT_BYTE:
                return 16
            
            if encoding == EncodingMode.KANJI:
                return 12
            
            raise ValueError("encoding")

        else:
            raise ValueError("version")
