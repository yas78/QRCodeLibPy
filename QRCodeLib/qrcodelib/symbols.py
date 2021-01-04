from typing import List
from .constants import Constants
from .encoding_mode import EncodingMode
from .error_correction_level import ErrorCorrectionLevel
from .symbol import Symbol
from .encoder import NumericEncoder, AlphanumericEncoder, KanjiEncoder, ByteEncoder


class Symbols:
    def __init__(self,
                 ec_level: int = ErrorCorrectionLevel.M,
                 max_version: int = Constants.MAX_VERSION,
                 allow_structured_append: bool = False,
                 byte_mode_encoding: str = "shift_jis") -> None:
        if not (Constants.MIN_VERSION <= max_version <= Constants.MAX_VERSION):
            raise ValueError("max_version")

        self._items = []  # type: List[Symbol]

        self._min_version = Constants.MIN_VERSION
        self._max_version = max_version
        self._error_correction_level = ec_level
        self._structured_append_allowed = allow_structured_append
        self._byte_mode_encoding = byte_mode_encoding
        self._shift_jis_encoding = "shift_jis"

        self._parity = 0

        self._curr_symbol = Symbol(self)
        self._items.append(self._curr_symbol)

    def __iter__(self):
        return iter(self._items)

    @property
    def count(self) -> int:
        return len(self._items)

    @property
    def min_version(self) -> int:
        return self._min_version

    @min_version.setter
    def min_version(self, value: int) -> None:
        self._min_version = value

    @property
    def max_version(self) -> int:
        return self._max_version

    @property
    def error_correction_level(self) -> int:
        return self._error_correction_level

    @property
    def structured_append_allowed(self) -> bool:
        return self._structured_append_allowed

    @property
    def parity(self) -> int:
        return self._parity

    @property
    def byte_mode_encoding(self) -> str:
        return self._byte_mode_encoding

    def item(self, index: int) -> Symbol:
        return self._items[index]

    def _add(self) -> Symbol:
        self._curr_symbol = Symbol(self)
        self._items.append(self._curr_symbol)
        return self._curr_symbol

    def append_text(self, data: str) -> None:
        if not data:
            raise ValueError("data")

        for i, c in enumerate(data):
            old_mode = self._curr_symbol.current_encoding_mode

            if old_mode == EncodingMode.UNKNOWN:
                new_mode = self._select_initial_mode(data, i)
            elif old_mode == EncodingMode.NUMERIC:
                new_mode = self._select_mode_while_in_numeric(data, i)
            elif old_mode == EncodingMode.ALPHA_NUMERIC:
                new_mode = self._select_mode_while_in_alphanumeric(data, i)
            elif old_mode == EncodingMode.EIGHT_BIT_BYTE:
                new_mode = self._select_mode_while_in_byte(data, i)
            elif old_mode == EncodingMode.KANJI:
                new_mode = self._select_initial_mode(data, i)
            else:
                raise RuntimeError()

            if new_mode != old_mode:
                if not self._curr_symbol.try_set_encoding_mode(new_mode, c):
                    if not self._structured_append_allowed or len(self._items) == 16:
                        raise OverflowError("String too long")

                    self._add()
                    new_mode = self._select_initial_mode(data, i)
                    self._curr_symbol.try_set_encoding_mode(new_mode, c)

            if not self._curr_symbol.try_append(c):
                if not self._structured_append_allowed or len(self._items) == 16:
                    raise OverflowError("String too long")

                self._add()
                new_mode = self._select_initial_mode(data, i)
                self._curr_symbol.try_set_encoding_mode(new_mode, c)
                self._curr_symbol.try_append(c)

    def _select_initial_mode(self, s: str, start: int) -> int:
        if KanjiEncoder.in_subset(s[start]):
            return EncodingMode.KANJI

        if ByteEncoder.in_exclusive_subset(s[start]):
            return EncodingMode.EIGHT_BIT_BYTE

        if AlphanumericEncoder.in_exclusive_subset(s[start]):
            return self._select_mode_when_initial_data_alphanumeric(s, start)

        if NumericEncoder.in_subset(s[start]):
            return self._select_mode_when_initial_data_numeric(s, start)

        raise RuntimeError()

    def _select_mode_when_initial_data_alphanumeric(self, s, start) -> int:
        cnt = 0

        for i in range(start, len(s) - 1):
            if AlphanumericEncoder.in_exclusive_subset(s[i]):
                cnt += 1
            else:
                break

        version = self._curr_symbol.version

        if 1 <= version <= 9:
            flg = cnt < 6
        elif 10 <= version <= 26:
            flg = cnt < 7
        elif 27 <= version <= 40:
            flg = cnt < 8
        else:
            raise RuntimeError()

        if flg:
            if (start + cnt) < len(s):
                if ByteEncoder.in_subset(s[start + cnt]):
                    return EncodingMode.EIGHT_BIT_BYTE

        return EncodingMode.ALPHA_NUMERIC

    def _select_mode_when_initial_data_numeric(self, s, start) -> int:
        cnt = 0

        for i in range(start, len(s) - 1):
            if NumericEncoder.in_subset(s[i]):
                cnt += 1
            else:
                break

        version = self._curr_symbol.version

        if 1 <= version <= 9:
            flg = cnt < 4
        elif 10 <= version <= 26:
            flg = cnt < 4
        elif 27 <= version <= 40:
            flg = cnt < 5
        else:
            raise RuntimeError()

        if flg:
            if (start + cnt) < len(s):
                if ByteEncoder.in_exclusive_subset(s[start + cnt]):
                    return EncodingMode.EIGHT_BIT_BYTE

        if 1 <= version <= 9:
            flg = cnt < 7
        elif 10 <= version <= 26:
            flg = cnt < 8
        elif 27 <= version <= 40:
            flg = cnt < 9
        else:
            raise RuntimeError()

        if flg:
            if (start + cnt) < len(s):
                if AlphanumericEncoder.in_exclusive_subset(s[start + cnt]):
                    return EncodingMode.ALPHA_NUMERIC

        return EncodingMode.NUMERIC

    @classmethod
    def _select_mode_while_in_numeric(cls, s: str, start: int) -> int:
        if KanjiEncoder.in_subset(s[start]):
            return EncodingMode.KANJI

        if ByteEncoder.in_exclusive_subset(s[start]):
            return EncodingMode.EIGHT_BIT_BYTE

        if AlphanumericEncoder.in_exclusive_subset(s[start]):
            return EncodingMode.ALPHA_NUMERIC

        return EncodingMode.NUMERIC

    def _select_mode_while_in_alphanumeric(self, s: str, start: int) -> int:
        if KanjiEncoder.in_subset(s[start]):
            return EncodingMode.KANJI

        if ByteEncoder.in_exclusive_subset(s[start]):
            return EncodingMode.EIGHT_BIT_BYTE

        if self._must_change_alphanumeric_to_numeric(s, start):
            return EncodingMode.NUMERIC

        return EncodingMode.ALPHA_NUMERIC

    def _must_change_alphanumeric_to_numeric(self, s: str, start: int) -> bool:
        ret = False
        cnt = 0

        for i in range(start, len(s) - 1):
            if not AlphanumericEncoder.in_subset(s[i]):
                break

            if NumericEncoder.in_subset(s[i]):
                cnt += 1
            else:
                ret = True
                break

        if ret:
            version = self._curr_symbol.version
            if 1 <= version <= 9:
                ret = cnt >= 13
            elif 10 <= version <= 26:
                ret = cnt >= 15
            elif 27 <= version <= 40:
                ret = cnt >= 17
            else:
                raise RuntimeError()

        return ret

    def _select_mode_while_in_byte(self, s: str, start: int) -> int:
        if KanjiEncoder.in_subset(s[start]):
            return EncodingMode.KANJI

        if self._must_change_byte_to_numeric(s, start):
            return EncodingMode.NUMERIC

        if self._must_change_byte_to_alphanumeric(s, start):
            return EncodingMode.ALPHA_NUMERIC

        return EncodingMode.EIGHT_BIT_BYTE

    def _must_change_byte_to_numeric(self, s, start) -> bool:
        ret = False
        cnt = 0

        for i in range(start, len(s) - 1):
            if not ByteEncoder.in_subset(s[i]):
                break

            if NumericEncoder.in_subset(s[i]):
                cnt += 1
            elif ByteEncoder.in_exclusive_subset(s[i]):
                ret = True
                break
            else:
                break

        if ret:
            version = self._curr_symbol.version
            if 1 <= version <= 9:
                ret = cnt >= 6
            elif 10 <= version <= 26:
                ret = cnt >= 8
            elif 27 <= version <= 40:
                ret = cnt >= 9
            else:
                raise RuntimeError()

        return ret

    def _must_change_byte_to_alphanumeric(self, s, start) -> bool:
        ret = False
        cnt = 0

        for i in range(start, len(s) - 1):
            if not ByteEncoder.in_subset(s[i]):
                break

            if AlphanumericEncoder.in_exclusive_subset(s[i]):
                cnt += 1
            elif ByteEncoder.in_exclusive_subset(s[i]):
                ret = True
                break
            else:
                break

        if ret:
            version = self._curr_symbol.version
            if 1 <= version <= 9:
                ret = cnt >= 11
            elif 10 <= version <= 26:
                ret = cnt >= 15
            elif 27 <= version <= 40:
                ret = cnt >= 16
            else:
                raise RuntimeError()

        return ret

    def update_parity(self, c: str) -> None:
        if KanjiEncoder.in_subset(c):
            char_bytes = c.encode(self._shift_jis_encoding, "ignore")
        else:
            char_bytes = c.encode(self._byte_mode_encoding, "ignore")

        for value in char_bytes:
            self._parity ^= value
