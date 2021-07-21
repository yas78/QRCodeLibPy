from typing import List
from abc import ABCMeta, abstractmethod


class QRCodeEncoder:
    __metaclass__ = ABCMeta

    def __init__(self, charset_name: str) -> None:
        self._code_words = []  # type: List[int]
        self._char_counter = 0
        self._bit_counter = 0

        self._charset_name = charset_name

    @property
    def char_count(self) -> int:
        return self._char_counter

    @property
    def bit_count(self) -> int:
        return self._bit_counter

    @property
    def charset_name(self):
        return self._charset_name

    @property
    @abstractmethod
    def encoding_mode(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def mode_indicator(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def append(self, c: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_codeword_bit_length(self, c: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_bytes(self) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def in_subset(self, c: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def in_exclusive_subset(self, c: str) -> bool:
        raise NotImplementedError()
