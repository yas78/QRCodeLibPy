from abc import ABCMeta, abstractmethod
from typing import List


class QRCodeEncoder(object):
    """
        エンコーダーの基本抽象クラス
    """
    __metaclass__ = ABCMeta
    
    def __init__(self) -> None:
        """
            インスタンスを初期化します。
        """
        self._code_words = []  # type: List[int]
        self._char_counter = 0
        self._bit_counter = 0
    
    @property
    def char_count(self) -> int:
        """
            文字数を取得します。
        """
        return self._char_counter

    @property
    def bit_count(self) -> int:
        """
            データビット数を取得します。
        """
        return self._bit_counter

    @property
    @abstractmethod
    def encoding_mode(self) -> int:
        """
            符号化モードを取得します。
        """
        pass

    @property
    @abstractmethod
    def mode_indicator(self) -> int:
        """
            モード指示子を取得します。
        """
        pass

    @abstractmethod
    def append(self, c: str) -> int:
        """
            文字を追加します。
        """
        pass

    @abstractmethod
    def get_codeword_bit_length(self, c: str) -> int:
        """
            指定の文字をエンコードしたコード語のビット数を返します。
        """
        pass

    @abstractmethod
    def get_bytes(self) -> bytearray:
        """
            エンコードされたデータのバイト配列を返します。
        """
        pass
