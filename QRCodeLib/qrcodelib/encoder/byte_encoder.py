from ..encoding_mode import EncodingMode
from .alphanumeric_encoder import AlphanumericEncoder
from .kanji_encoder import KanjiEncoder
from .qrcode_encoder import QRCodeEncoder
from ..format.mode_indicator import ModeIndicator
from ..misc.charset import Charset


class ByteEncoder(QRCodeEncoder):
    def __init__(self, charset_name: str) -> None:
        super().__init__(charset_name)
        self._enc_alpha = AlphanumericEncoder(charset_name)

        if Charset.is_jp(charset_name):
            self._enc_kanji = KanjiEncoder(charset_name)
        else:
            self._enc_kanji = None

    @property
    def encoding_mode(self) -> int:
        return EncodingMode.EIGHT_BIT_BYTE

    @property
    def mode_indicator(self) -> int:
        return ModeIndicator.BYTE_VALUE

    def append(self, c: str) -> int:
        char_bytes = c.encode(self._charset_name, "ignore")
        self._code_words.extend(char_bytes)
        ret = 8 * len(char_bytes)
        self._bit_counter += ret
        self._char_counter += len(char_bytes)
        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        char_bytes = c.encode(self._charset_name, "ignore")
        return 8 * len(char_bytes)

    def get_bytes(self) -> bytes:
        ret = bytearray(self._char_counter)

        for i, code_word in enumerate(self._code_words):
            ret[i] = code_word

        return bytes(ret)

    def in_subset(self, c: str) -> bool:
        return bool(c)

    def in_exclusive_subset(self, c: str) -> bool:
        if self._enc_alpha.in_subset(c):
            return False

        if self._enc_kanji and self._enc_kanji.in_subset(c):
            return False
        
        return self.in_subset(c)
