from ..encoding_mode import EncodingMode
from .qrcode_encoder import QRCodeEncoder
from .numeric_encoder import NumericEncoder
from ..format.mode_indicator import ModeIndicator
from ..misc.bit_sequence import BitSequence


class AlphanumericEncoder(QRCodeEncoder):
    def __init__(self, charset_name: str) -> None:
        super().__init__(charset_name)
        self._encNumeric = NumericEncoder(charset_name)

    @property
    def encoding_mode(self) -> int:
        return EncodingMode.ALPHA_NUMERIC

    @property
    def mode_indicator(self) -> int:
        return ModeIndicator.ALPHANUMERIC_VALUE

    def append(self, c: str) -> None:
        wd = self._convert_char_code(c)

        if self._char_counter % 2 == 0:
            self._code_words.append(wd)
        else:
            self._code_words[-1] *= 45
            self._code_words[-1] += wd

        self._bit_counter += self.get_codeword_bit_length(c)
        self._char_counter += 1

    def get_codeword_bit_length(self, c: str) -> int:
        if self._char_counter % 2 == 0:
            return 6
        else:
            return 5

    def get_bytes(self) -> bytes:
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
        char_bytes = c.encode("ascii", "ignore")

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
        if "0" <= c <= "9":
            return char_bytes[0] - 48
        if c == ":":
            return 44
        if "A" <= c <= "Z":
            return char_bytes[0] - 55

        return -1
    
    def in_subset(self, c: str) -> bool:
        return self._convert_char_code(c) > -1

    def in_exclusive_subset(self, c: str) -> bool:
        if self._encNumeric.in_subset(c):
            return False
        
        return self.in_subset(c)
