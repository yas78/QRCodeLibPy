from EncodingMode import EncodingMode
from encoder.QRCodeEncoder import QRCodeEncoder
from encoder.NumericEncoder import NumericEncoder
from format.ModeIndicator import ModeIndicator
from misc.BitSequence import BitSequence


class AlphanumericEncoder(QRCodeEncoder):
    """
        英数字モードエンコーダー
    """
    def __init__(self) -> None:
        """
            インスタンスを初期化します。
        """
        super().__init__()

    @property
    def encoding_mode(self) -> int:
        """
            符号化モードを取得します。
        """
        return EncodingMode.ALPHA_NUMERIC

    @property
    def mode_indicator(self) -> int:
        """
            モード指示子を取得します。
        """
        return ModeIndicator.ALPAHNUMERIC_VALUE

    def append(self, c: str) -> int:
        """
            文字を追加します。
        """
        wd = self._convert_char_code(c)

        if self._char_counter % 2 == 0:
            self._code_words.append(wd)
            ret = 6
        else:
            self._code_words[-1] *= 45
            self._code_words[-1] += wd
            ret = 5
        
        self._char_counter += 1
        self._bit_counter += ret
        
        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        """
            指定の文字をエンコードしたコード語のビット数を返します。
        """
        if self._char_counter % 2 == 0:
            return 6
        else:
            return 5

    def get_bytes(self) -> bytearray:
        """
            エンコードされたデータのバイト配列を返します。
        """
        bs = BitSequence()
        bit_length = 11 

        for i in range(len(self._code_words) - 1):
            bs.append(self._code_words[i], bit_length)

        if self._char_counter % 2 == 0:
            bit_length = 11
        else:
            bit_length = 6

        bs.append(self._code_words[-1], bit_length)

        return bs.get_bytes()

    @classmethod
    def _convert_char_code(cls, c: str) -> int:
        """
            指定した文字の、英数字モードにおけるコード値を返します。
        """
        assert len(c) == 1
        
        char_bytes = c.encode("ascii", "ignore")

        if len(char_bytes) != 1:
            raise ValueError("c")

        if "A" <= c <= "Z":
            return char_bytes[0] - 55

        if "0" <= c <= "9":
            return char_bytes[0] - 48

        if c == " ":
            return 36

        if c == "$" or c == "%":
            return char_bytes[0] + 1

        if c == "*" or c == "+":
            return char_bytes[0] - 3

        if c == "-" or c == ".":
            return char_bytes[0] - 4

        if c == "/":
            return 43

        if c == ":":
            return 44

        raise ValueError("c")
    
    @classmethod
    def is_in_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの文字集合に含まれる場合は true を返します。
        """
        return (
            "A" <= c <= "Z" or
            "0" <= c <= "9" or
            c == " " or
            c == "." or
            c == "-" or
            c == "$" or
            c == "%" or
            c == "*" or
            c == "+" or
            c == "/" or
            c == ":"
        )

    @classmethod
    def is_in_exclusive_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの排他的部分文字集合に含まれる場合は true を返します。
        """
        if NumericEncoder.is_in_subset(c):
            return False
        
        return AlphanumericEncoder.is_in_subset(c)
