from ..encoding_mode import EncodingMode
from .alphanumeric_encoder import AlphanumericEncoder
from .kanji_encoder import KanjiEncoder
from .qrcode_encoder import QRCodeEncoder
from ..format.mode_indicator import ModeIndicator


class ByteEncoder(QRCodeEncoder):
    def __init__(self, encoding: str = "shift_jis") -> None:
        super().__init__()
        self._text_encoding = encoding

    @property
    def encoding_mode(self) -> int:
        return EncodingMode.EIGHT_BIT_BYTE

    @property
    def mode_indicator(self) -> int:
        return ModeIndicator.BYTE_VALUE

    def append(self, c: str) -> int:
        char_bytes = c.encode(self._text_encoding, "ignore")
        self._code_words.extend(char_bytes)
        ret = 8 * len(char_bytes)
        self._bit_counter += ret
        self._char_counter += len(char_bytes)
        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        char_bytes = c.encode(self._text_encoding, "ignore")
        return 8 * len(char_bytes)

    def get_bytes(self) -> bytes:
        ret = bytearray(self._char_counter)

        for i, code_word in enumerate(self._code_words):
            ret[i] = code_word

        return bytes(ret)

    @classmethod
    def in_subset(cls, c: str) -> bool:
        return bool(c)

    @classmethod
    def in_exclusive_subset(cls, c: str) -> bool:
        if AlphanumericEncoder.in_subset(c):
            return False
        
        if KanjiEncoder.in_subset(c):
            return False
        
        return ByteEncoder.in_subset(c)
