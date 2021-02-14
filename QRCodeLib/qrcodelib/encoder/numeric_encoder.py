from ..encoding_mode import EncodingMode
from .qrcode_encoder import QRCodeEncoder
from ..format.mode_indicator import ModeIndicator
from ..misc.bit_sequence import BitSequence


class NumericEncoder(QRCodeEncoder):
    def __init__(self, charset_name: str) -> None:
        super().__init__(charset_name)

    @property
    def encoding_mode(self) -> int:
        return EncodingMode.NUMERIC

    @property
    def mode_indicator(self) -> int:
        return ModeIndicator.NUMERIC_VALUE

    def append(self, c: str) -> int:
        wd = int(c)

        if self._char_counter % 3 == 0:
            self._code_words.append(wd)
        else:
            self._code_words[-1] *= 10
            self._code_words[-1] += wd

        ret = self.get_codeword_bit_length(c)
        self._bit_counter += ret
        self._char_counter += 1

        return ret

    def get_codeword_bit_length(self, c: str) -> int:
        if self._char_counter % 3 == 0:
            return 4
        else:
            return 3

    def get_bytes(self) -> bytes:
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

    def in_subset(self, c: str) -> bool:
        return "0" <= c <= "9"

    def in_exclusive_subset(self, c: str) -> bool:
        return self.in_subset(c)
