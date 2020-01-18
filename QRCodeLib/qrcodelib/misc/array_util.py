from typing import List
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
        
    @classmethod
    def rotate90(cls, arg: List[List[int]]) -> List[List[int]]:
        ret = [[0] * len(arg[0]) for _ in range(len(arg[0]))]
        k = len(ret) - 1

        for i in range(len(ret)):
            for j in range(len(ret[i])):
                ret[i][j] = arg[j][k - i]

        return ret
