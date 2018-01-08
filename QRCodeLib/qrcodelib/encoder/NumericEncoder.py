from EncodingMode import EncodingMode
from encoder.QRCodeEncoder import QRCodeEncoder
from format.ModeIndicator import ModeIndicator
from misc.BitSequence import BitSequence


class NumericEncoder(QRCodeEncoder):
    """
        数字モードエンコーダー
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
        return EncodingMode.NUMERIC

    @property
    def mode_indicator(self) -> int:
        """
            モード指示子を取得します。
        """
        return ModeIndicator.NUMERIC_VALUE

    def append(self, c: str) -> int:
        """
            文字を追加します。
        """
        assert type(c) == str and len(c) == 1

        wd = int(c)

        if self._char_counter % 3 == 0:
            self._code_words.append(wd)
            ret = 4
        else:
            self._code_words[-1] *= 10
            self._code_words[-1] += wd
            ret = 3
        
        self._char_counter += 1
        self._bit_counter += ret

        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        """
            指定の文字をエンコードしたコード語のビット数を返します。
        """
        if self._char_counter % 3 == 0:
            return 4
        else:
            return 3

    def get_bytes(self) -> bytearray:
        """
            エンコードされたデータのバイト配列を返します。
        """
        bs = BitSequence()
        bit_length = 10

        for i in range(len(self._code_words) - 1):
            bs.append(self._code_words[i], bit_length)

        if self._char_counter % 3 == 1:
            bit_length = 4
        elif self._char_counter % 3 == 2:
            bit_length = 7
        else:
            bit_length = 10

        bs.append(self._code_words[-1], bit_length)

        return bs.get_bytes()

    @classmethod
    def is_in_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの文字集合に含まれる場合は true を返します。
        """
        return "0" <= c <= "9"

    @classmethod
    def is_in_exclusive_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの排他的部分文字集合に含まれる場合は true を返します。
        """
        return NumericEncoder.is_in_subset(c)
