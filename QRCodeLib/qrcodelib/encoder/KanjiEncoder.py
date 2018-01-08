from EncodingMode import EncodingMode
from encoder.QRCodeEncoder import QRCodeEncoder
from format.ModeIndicator import ModeIndicator
from misc.BitSequence import BitSequence


class KanjiEncoder(QRCodeEncoder):
    """
        漢字モードエンコーダー
    """
    _textEncoding = "shift_jis"

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
        return EncodingMode.KANJI

    @property
    def mode_indicator(self) -> int:
        """
            モード指示子を取得します。
        """
        return ModeIndicator.KANJI_VALUE

    def append(self, c: str) -> int:
        """
            文字を追加します。
        """
        char_bytes = c.encode(self._textEncoding, "ignore")
        wd = (char_bytes[0] << 8) | char_bytes[1]

        if 0x8140 <= wd <= 0x9FFC:
            wd -= 0x8140
        elif 0xE040 <= wd <= 0xEBBF:
            wd -= 0xC140
        else:
            raise ValueError("c")

        wd = ((wd >> 8) * 0xC0) + (wd & 0xFF)

        self._code_words.append(wd)
        self._char_counter += 1
        self._bit_counter += 13

        return 13

    def get_codeword_bit_length(self, c: str) -> int:
        """
            指定の文字をエンコードしたコード語のビット数を返します。
        """
        return 13

    def get_bytes(self) -> bytearray:
        """
            エンコードされたデータのバイト配列を返します。
        """
        bs = BitSequence()

        for code_word in self._code_words:
            bs.append(code_word, 13)

        return bs.get_bytes()

    @classmethod
    def is_in_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの文字集合に含まれる場合は true を返します。
        """
        char_bytes = c.encode(cls._textEncoding, "ignore")

        if len(char_bytes) != 2:
            return False

        code = (char_bytes[0] << 8) | char_bytes[1]

        if (0x8140 <= code <= 0x9FFC or
                0xE040 <= code <= 0xEBBF):

            return (
                0x40 <= char_bytes[1] <= 0xFC and
                0x7F != char_bytes[1]
            )
        else:
            return False

    @classmethod
    def is_in_exclusive_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの排他的部分文字集合に含まれる場合は true を返します。
        """
        return cls.is_in_subset(c)
