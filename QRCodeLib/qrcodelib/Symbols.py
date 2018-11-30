from typing import List

from .Constants import Constants
from .EncodingMode import EncodingMode
from .ErrorCorrectionLevel import ErrorCorrectionLevel
from .Symbol import Symbol
from .encoder.AlphanumericEncoder import AlphanumericEncoder
from .encoder.ByteEncoder import ByteEncoder
from .encoder.KanjiEncoder import KanjiEncoder
from .encoder.NumericEncoder import NumericEncoder


class Symbols(object):
    """
        シンボルのコレクションを表します。
    """    
    def __init__(self, 
                 ec_level: int = ErrorCorrectionLevel.M,
                 max_version: int = Constants.MAX_VERSION,
                 allow_structured_append: bool = False,
                 byte_mode_encoding: str = "shift_jis") -> None:
        """
            インスタンスを初期化します。
        """
        if not (Constants.MIN_VERSION <= max_version <= Constants.MAX_VERSION):
            raise ValueError("max_version")
        
        self._items = []  # type: List[Symbol]

        self._min_version = 1
        self._max_version = max_version
        self._errorCorrectionLevel = ec_level
        self._structured_append_allowed = allow_structured_append
        self._byte_mode_encoding = byte_mode_encoding
        self._shift_jis_encoding = "shift_jis"

        self._structured_append_parity = 0

        self._curr_symbol = Symbol(self)
        self._items.append(self._curr_symbol)

    def __iter__(self):
        return iter(self._items)

    def item(self, index: int) -> Symbol:
        """
            インデックス番号を指定してSymbolオブジェクトを取得します。
        """
        return self._items[index]

    @property
    def count(self) -> int:
        """
            シンボル数を取得します。
        """
        return len(self._items)

    @property
    def min_version(self) -> int:
        """
            型番の下限を取得します。
        """
        return self._min_version

    @min_version.setter
    def min_version(self, value: int):
        """
            型番の下限を設定します。
        """
        self._min_version = value

    @property
    def max_version(self) -> int:
        """
            型番の上限を取得します。
        """
        return self._max_version

    @property
    def error_correction_level(self) -> int:
        """
            誤り訂正レベルを取得します。
        """
        return self._errorCorrectionLevel

    @property
    def structured_append_allowed(self) -> bool:
        """
            構造的連接モードの使用可否を取得します。
        """
        return self._structured_append_allowed

    @property
    def structured_append_parity(self) -> int:
        """
            構造的連接のパリティを取得します。
        """
        return self._structured_append_parity

    @property
    def byte_mode_encoding(self) -> str:
        """
            バイトモードの文字エンコーディングを取得します。
        """
        return self._byte_mode_encoding

    def _add(self) -> Symbol:
        """
            シンボルを追加します。
        """
        self._curr_symbol = Symbol(self)
        self._items.append(self._curr_symbol)
        return self._curr_symbol

    def append_text(self, data: str):
        """
            文字列を追加します。
        """
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
                    if (not self._structured_append_allowed 
                            or len(self._items) == 16):
                        raise OverflowError("String too long")
                    
                    self._add()
                    new_mode = self._select_initial_mode(data, i)
                    self._curr_symbol.try_set_encoding_mode(new_mode, c)
            
            if not self._curr_symbol.try_append(c):
                if (not self._structured_append_allowed 
                        or len(self._items) == 16):
                    raise OverflowError("String too long")
                
                self._add()
                new_mode = self._select_initial_mode(data, i)
                self._curr_symbol.try_set_encoding_mode(new_mode, c)
                self._curr_symbol.try_append(c)

    def _select_initial_mode(self, s: str, start_index: int) -> int:
        """
            初期モードを決定します。
        """
        version = self._curr_symbol.version

        if KanjiEncoder.in_subset(s[start_index]):
            return EncodingMode.KANJI
        
        if ByteEncoder.in_exclusive_subset(s[start_index]):
            return EncodingMode.EIGHT_BIT_BYTE
        
        if AlphanumericEncoder.in_exclusive_subset(s[start_index]):
            cnt = 0
            flg = False

            for i in range(start_index, len(s) - 1):
                if AlphanumericEncoder.in_exclusive_subset(s[i]):
                    cnt += 1
                else:
                    break
                
                if 1 <= version <= 9:
                    flg = cnt < 6
                elif 10 <= version <= 26:
                    flg = cnt < 7
                elif 27 <= version <= 40:
                    flg = cnt < 8
                else:
                    raise RuntimeError()

            if flg:
                if (start_index + cnt) < len(s):
                    if ByteEncoder.in_exclusive_subset(
                            s[start_index + cnt]):
                        return EncodingMode.EIGHT_BIT_BYTE
                    else:
                        return EncodingMode.ALPHA_NUMERIC
                else:
                    return EncodingMode.ALPHA_NUMERIC
            else:
                return EncodingMode.ALPHA_NUMERIC

        if NumericEncoder.in_subset(s[start_index]):
            cnt = 0
            flg1 = False
            flg2 = False

            for i in range(start_index, len(s) - 1):
                if NumericEncoder.in_subset(s[i]):
                    cnt += 1
                else:
                    break

                if 1 <= version <= 9:
                    flg1 = cnt < 4
                    flg2 = cnt < 7
                elif 10 <= version <= 26:
                    flg1 = cnt < 4
                    flg2 = cnt < 8
                elif 27 <= version <= 40:
                    flg1 = cnt < 5
                    flg2 = cnt < 9
                else:
                    raise RuntimeError()

            if flg1:
                if (start_index + cnt) < len(s):
                    flg1 = ByteEncoder.in_exclusive_subset(
                        s[start_index + cnt])
                else:
                    flg1 = False
            
            if flg2:
                if (start_index + cnt) < len(s):
                    flg2 = AlphanumericEncoder.in_exclusive_subset(
                        s[start_index + cnt])
                else:
                    flg2 = False

            if flg1:
                return EncodingMode.EIGHT_BIT_BYTE
            elif flg2:
                return EncodingMode.ALPHA_NUMERIC
            else:
                return EncodingMode.NUMERIC
       
        raise RuntimeError()

    def _select_mode_while_in_numeric(
            self, s: str, start_index: int) -> int:
        """
            数字モードから切り替えるモードを決定します。
        """
        if KanjiEncoder.in_subset(s[start_index]):
            return EncodingMode.KANJI

        if ByteEncoder.in_exclusive_subset(s[start_index]):
            return EncodingMode.EIGHT_BIT_BYTE

        if AlphanumericEncoder.in_exclusive_subset(s[start_index]):
            return EncodingMode.ALPHA_NUMERIC
        
        return EncodingMode.NUMERIC

    def _select_mode_while_in_alphanumeric(
            self, s: str, start_index: int) -> int:
        """
            英数字モードから切り替えるモードを決定します。
        """
        version = self._curr_symbol.version

        if KanjiEncoder.in_subset(s[start_index]):
            return EncodingMode.KANJI
        
        if ByteEncoder.in_exclusive_subset(s[start_index]):
            return EncodingMode.EIGHT_BIT_BYTE

        cnt = 0
        flg = False

        for i in range(start_index, len(s) - 1):
            if not AlphanumericEncoder.in_subset(s[i]):
                break
            
            if NumericEncoder.in_subset(s[i]):
                cnt += 1
            else:
                flg = True
                break
        
        if flg:
            if 1 <= version <= 9:
                flg = cnt >= 13
            elif 10 <= version <= 26:
                flg = cnt >= 15
            elif 27 <= version <= 40:
                flg = cnt >= 17
            else:
                raise RuntimeError()

            if flg:
                return EncodingMode.NUMERIC
            
        return EncodingMode.ALPHA_NUMERIC

    def _select_mode_while_in_byte(self, s: str, start_index: int) -> int:
        """
            バイトモードから切り替えるモードを決定します。
        """
        version = self._curr_symbol.version

        cnt = 0
        flg = False
            
        if KanjiEncoder.in_subset(s[start_index]):
            return EncodingMode.KANJI
        
        for i in range(start_index, len(s) - 1):
            if not ByteEncoder.in_subset(s[i]):
                break
            
            if NumericEncoder.in_subset(s[i]):
                cnt += 1
            elif ByteEncoder.in_exclusive_subset(s[i]):
                flg = True
                break
            else:
                break

        if flg:
            if 1 <= version <= 9:
                flg = cnt >= 6
            elif 10 <= version <= 26:
                flg = cnt >= 8
            elif 27 <= version <= 40:
                flg = cnt >= 9
            else:
                raise RuntimeError()

            if flg:
                return EncodingMode.NUMERIC
            
        cnt = 0
        flg = False

        for i in range(start_index, len(s) - 1):
            if not ByteEncoder.in_subset(s[i]):
                break
            
            if AlphanumericEncoder.in_exclusive_subset(s[i]):
                cnt += 1
            elif ByteEncoder.in_exclusive_subset(s[i]):
                flg = True
                break
            else:
                break

        if flg:
            if 1 <= version <= 9:
                flg = cnt >= 11
            elif 10 <= version <= 26:
                flg = cnt >= 15
            elif 27 <= version <= 40:
                flg = cnt >= 16
            else:
                raise RuntimeError()

            if flg:
                return EncodingMode.ALPHA_NUMERIC
            
        return EncodingMode.EIGHT_BIT_BYTE

    def update_parity(self, c: str):
        """
            構造的連接のパリティを更新します。
        """
        if KanjiEncoder.in_subset(c):
            char_bytes = c.encode(self._shift_jis_encoding, "ignore")
        else:
            char_bytes = c.encode(self._byte_mode_encoding, "ignore")

        for value in char_bytes:
            self._structured_append_parity ^= value
