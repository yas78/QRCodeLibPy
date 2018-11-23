from ..EncodingMode import EncodingMode
from .AlphanumericEncoder import AlphanumericEncoder
from .KanjiEncoder import KanjiEncoder
from .QRCodeEncoder import QRCodeEncoder
from ..format.ModeIndicator import ModeIndicator


class ByteEncoder(QRCodeEncoder):
    """
        バイトモードエンコーダー
    """
    def __init__(self, encoding: str = "shift_jis") -> None:
        """
            インスタンスを初期化します。
        """
        super().__init__()
        self._text_encoding = encoding

    @property
    def encoding_mode(self) -> int:
        """
            符号化モードを取得します。
        """
        return EncodingMode.EIGHT_BIT_BYTE

    @property
    def mode_indicator(self) -> int:
        """
            モード指示子を取得します。
        """
        return ModeIndicator.BYTE_VALUE

    def append(self, c: str) -> int:
        """
            文字を追加します。
        """
        char_bytes = c.encode(self._text_encoding, "ignore")
        ret = 0

        for b in char_bytes:
            self._code_words.append(b)
            self._char_counter += 1
            self._bit_counter += 8
            ret += 8

        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        """
            指定の文字をエンコードしたコード語のビット数を返します。
        """
        char_bytes = c.encode(self._text_encoding, "ignore")

        return 8 * len(char_bytes)

    def get_bytes(self) -> bytes:
        """
            エンコードされたデータのバイト配列を返します。
        """
        ret = bytearray(self._char_counter)

        for i, code_word in enumerate(self._code_words):
            ret[i] = code_word

        return bytes(ret)

    @classmethod
    def in_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの文字集合に含まれる場合は true を返します。
        """
        return bool(c)

    @classmethod
    def in_exclusive_subset(cls, c: str) -> bool:
        """
            指定した文字が、このモードの排他的部分文字集合に含まれる場合は true を返します。
        """
        if AlphanumericEncoder.in_subset(c):
            return False
        
        if KanjiEncoder.in_subset(c):
            return False
        
        return ByteEncoder.in_subset(c)
