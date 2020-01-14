class BitSequence(object):
    """
        ビット列の生成機能を提供します。
    """    
    def __init__(self) -> None:
        self._buffer = bytearray()
        self._bit_counter = 0
        self._space = 0

    @property
    def length(self) -> int:
        """
            ビット数を取得します。
        """
        return self._bit_counter

    def append(self, data: int, length: int) -> None:
        """
            指定のビット数でデータを追加します。
        """
        remaining_length = length
        remaining_data = data

        while remaining_length > 0:
            if self._space == 0:
                self._space = 8
                self._buffer.append(0x0)

            temp = self._buffer[-1]

            if self._space < remaining_length:
                temp |= remaining_data >> (remaining_length - self._space)
                remaining_data &= (1 << (remaining_length - self._space)) - 1
                self._bit_counter += self._space
                remaining_length -= self._space
                self._space = 0
            else:
                temp |= remaining_data << (self._space - remaining_length)
                self._bit_counter += remaining_length
                self._space -= remaining_length
                remaining_length = 0
            
            self._buffer[-1] = temp

    def get_bytes(self) -> bytes:
        """
            データのバイト配列を返します。
        """
        return bytes(self._buffer)
