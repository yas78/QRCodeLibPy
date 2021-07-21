from ..encoding_mode import EncodingMode
from .qrcode_encoder import QRCodeEncoder
from .alphanumeric_encoder import AlphanumericEncoder
from ..format.mode_indicator import ModeIndicator
from ..misc.bit_sequence import BitSequence


class KanjiEncoder(QRCodeEncoder):
    def __init__(self, charset_name: str) -> None:
        super().__init__(charset_name)
        self._encAlpha = AlphanumericEncoder(charset_name)

    @property
    def encoding_mode(self) -> int:
        return EncodingMode.KANJI

    @property
    def mode_indicator(self) -> int:
        return ModeIndicator.KANJI_VALUE

    def append(self, c: str) -> None:
        char_bytes = c.encode(self._charset_name, "ignore")
        wd = (char_bytes[0] << 8) | char_bytes[1]

        if 0x8140 <= wd <= 0x9FFC:
            wd -= 0x8140
        elif 0xE040 <= wd <= 0xEBBF:
            wd -= 0xC140
        else:
            raise ValueError("c")

        wd = ((wd >> 8) * 0xC0) + (wd & 0xFF)
        self._code_words.append(wd)

        self._bit_counter += self.get_codeword_bit_length(c)
        self._char_counter += 1

    def get_codeword_bit_length(self, c: str) -> int:
        return 13

    def get_bytes(self) -> bytes:
        bs = BitSequence()

        for wd in self._code_words:
            bs.append(wd, 13)

        return bs.get_bytes()

    def in_subset(self, c: str) -> bool:
        char_bytes = c.encode(self._charset_name, "ignore")

        if len(char_bytes) != 2:
            return False

        code = (char_bytes[0] << 8) | char_bytes[1]

        if (0x8140 <= code <= 0x9FFC or
                0xE040 <= code <= 0xEBBF):
            return (0x40 <= char_bytes[1] <= 0xFC and
                    0x7F != char_bytes[1])

        return False

    def in_exclusive_subset(self, c: str) -> bool:
        if self._encAlpha.in_subset(c):
            return False

        return self.in_subset(c)
