from typing import Sequence, MutableSequence


class ArrayUtil(object):

    @classmethod
    def copy(cls,
             src_array: Sequence,
             src_index: int,
             dest_array: MutableSequence,
             dest_index: int,
             length: int) -> None:
        """
            一次元配列をコピーします。
        """
        dest_array[dest_index:dest_index + length] = src_array[src_index:src_index + length]
