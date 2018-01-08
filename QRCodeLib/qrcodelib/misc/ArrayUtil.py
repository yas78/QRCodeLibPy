from typing import Sequence, MutableSequence


class ArrayUtil(object):

    @classmethod
    def copy(cls, 
             source_array: Sequence,
             source_index: int,
             destination_array: MutableSequence,
             destination_index: int,
             length: int):
        """
            一次元配列をコピーします。
        """
        dst_index = destination_index

        for src_index in range(source_index, source_index + length):
            destination_array[dst_index] = source_array[src_index]
            dst_index += 1
