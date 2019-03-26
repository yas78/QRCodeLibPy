from typing import List, Tuple

from io import BytesIO
import tkinter as tk

from .AlignmentPattern import AlignmentPattern
from .EncodingMode import EncodingMode
from .FinderPattern import FinderPattern
from .FormatInfo import FormatInfo
from .GaloisField256 import GaloisField256
from .GeneratorPolynomials import GeneratorPolynomials
from .Masking import Masking
from .QuietZone import QuietZone
from .RemainderBit import RemainderBit
from .Separator import Separator
from .TimingPattern import TimingPattern
from .VersionInfo import VersionInfo
from .encoder.QRCodeEncoderFactory import QRCodeEncoderFactory
from .format.CharCountIndicator import CharCountIndicator
from .format.Codeword import Codeword
from .format.DataCodeword import DataCodeword
from .format.ModeIndicator import ModeIndicator
from .format.Module import Module
from .format.RSBlock import RSBlock
from .format.StructuredAppend import StructuredAppend
from .format.SymbolSequenceIndicator import SymbolSequenceIndicator
from .image.BITMAPFILEHEADER import BITMAPFILEHEADER
from .image.BITMAPINFOHEADER import BITMAPINFOHEADER
from .image.RGBQUAD import RGBQUAD
from .misc.ArrayUtil import ArrayUtil
from .misc.BitSequence import BitSequence
from .misc.ColorCode import ColorCode


class Symbol(object):
    """
        シンボルを表します。
    """
    def __init__(self, parent) -> None:
        self._parent = parent

        self._position = parent.count

        self._curr_encoder = None
        self._curr_encoding_mode = EncodingMode.UNKNOWN
        self._curr_version = parent.min_version

        self._data_bit_capacity = 8 * DataCodeword.get_total_number(
            parent.error_correction_level, parent.min_version)

        self._data_bit_counter = 0

        self._segments = []

        self._segment_counter = {
            EncodingMode.NUMERIC:        0,
            EncodingMode.ALPHA_NUMERIC:  0,
            EncodingMode.EIGHT_BIT_BYTE: 0,
            EncodingMode.KANJI:          0
        }

        if parent.structured_append_allowed:
            self._data_bit_capacity -= StructuredAppend.HEADER_LENGTH

    @property
    def parent(self):
        """
            親オブジェクトを取得します。
        """
        return self._parent

    @property
    def version(self) -> int:
        """
            型番を取得します。
        """
        return self._curr_version

    @property
    def current_encoding_mode(self) -> int:
        """
            現在の符号化モードを取得します。
        """
        return self._curr_encoding_mode

    def try_append(self, c: str) -> bool:
        """
            シンボルに文字を追加します。
            シンボル容量が不足している場合は false を返します。
        """
        bit_length = self._curr_encoder.get_codeword_bit_length(c)

        while self._data_bit_capacity < (self._data_bit_counter
                                         + bit_length):
            if self._curr_version >= self._parent.max_version:
                return False
            self._select_version()

        self._curr_encoder.append(c)
        self._data_bit_counter += bit_length
        self._parent.update_parity(c)
        return True

    def try_set_encoding_mode(self, enc_mode: int, c: str) -> bool:
        """
            符号化モードを設定します。
            引数cはシンボルに追加されません。
            シンボル容量が不足している場合は false を返します。
        """
        encoder = QRCodeEncoderFactory.create_encoder(
            enc_mode, self._parent.byte_mode_encoding)
        bit_length = encoder.get_codeword_bit_length(c)

        while self._data_bit_capacity < (
                self._data_bit_counter
                + ModeIndicator.LENGTH
                + CharCountIndicator.get_length(
                    self._curr_version, enc_mode)
                + bit_length):

            if self._curr_version >= self._parent.max_version:
                return False

            self._select_version()

        self._data_bit_counter += (
                ModeIndicator.LENGTH
                + CharCountIndicator.get_length(self._curr_version, enc_mode)
        )

        self._curr_encoder = encoder
        self._segments.append(self._curr_encoder)
        self._segment_counter[enc_mode] += 1
        self._curr_encoding_mode = enc_mode
        return True

    def _select_version(self):
        """
            型番を決定します。
        """
        for enc_mode in self._segment_counter.keys():
            num = self._segment_counter[enc_mode]
            self._data_bit_counter += (
                    num * CharCountIndicator.get_length(
                        self._curr_version + 1, enc_mode)
                    - num * CharCountIndicator.get_length(
                        self._curr_version + 0, enc_mode)
            )

        self._curr_version += 1
        self._data_bit_capacity = 8 * DataCodeword.get_total_number(
            self._parent.error_correction_level, self._curr_version)
        self._parent.min_version = self._curr_version

        if self._parent.structured_append_allowed:
            self._data_bit_capacity -= StructuredAppend.HEADER_LENGTH

    def _build_data_block(self) -> List[bytearray]:
        """
            データブロックを返します。
        """
        data_bytes = self._get_message_bytes()

        num_pre_blocks = RSBlock.get_total_number(
            self._parent.error_correction_level, self._curr_version, True)

        num_fol_blocks = RSBlock.get_total_number(
            self._parent.error_correction_level, self._curr_version, False)

        ret = [None] * (num_pre_blocks + num_fol_blocks)  # type: List[bytearray]

        index = 0

        num_pre_block_data_codewords = RSBlock.get_number_data_codewords(
            self._parent.error_correction_level, self._curr_version, True)

        for i in range(num_pre_blocks):
            data = bytearray(num_pre_block_data_codewords)
            ArrayUtil.copy(data_bytes, index, data, 0, len(data))
            index += len(data)
            ret[i] = data

        num_fol_block_data_codewords = RSBlock.get_number_data_codewords(
            self._parent.error_correction_level, self._curr_version, False)

        for i in range(num_pre_blocks, num_pre_blocks + num_fol_blocks):
            data = bytearray(num_fol_block_data_codewords)
            ArrayUtil.copy(data_bytes, index, data, 0, len(data))
            index += len(data)
            ret[i] = data

        return ret

    def _build_error_correction_block(self, data_block: List[bytearray]) -> List[bytearray]:
        """
            誤り訂正データ領域のブロックを生成します。
        """
        num_ec_codewords = RSBlock.get_number_ec_codewords(
            self._parent.error_correction_level, self._curr_version)
        num_pre_blocks = RSBlock.get_total_number(
            self._parent.error_correction_level, self._curr_version, True)
        num_fol_blocks = RSBlock.get_total_number(
            self._parent.error_correction_level, self._curr_version, False)

        ret = [None] * (num_pre_blocks + num_fol_blocks)  # type: List[bytearray]

        for i in range(len(ret)):
            ret[i] = bytearray(num_ec_codewords)

        gp = GeneratorPolynomials.item(num_ec_codewords)

        for block_index in range(len(data_block)):
            data = [0] * (len(data_block[block_index]) + len(ret[block_index]))
            ecc_index = len(data) - 1

            for block in data_block[block_index]:
                data[ecc_index] = block
                ecc_index -= 1

            for i in range(len(data) - 1, num_ec_codewords - 1, -1):
                if data[i] > 0:
                    exp = GaloisField256.to_exp(data[i])
                    ecc_index = i

                    for value in reversed(gp):
                        data[ecc_index] ^= GaloisField256.to_int((value + exp) % 255)
                        ecc_index -= 1

            ecc_index = num_ec_codewords - 1

            for i in range(len(ret[block_index])):
                ret[block_index][i] = data[ecc_index]
                ecc_index -= 1

        return ret

    def _get_encoding_region_bytes(self) -> bytearray:
        """
            符号化領域のバイトデータを返します。
        """
        data_block = self._build_data_block()
        ec_block = self._build_error_correction_block(data_block)

        num_codewords = Codeword.get_total_number(self._curr_version)
        num_data_codewords = DataCodeword.get_total_number(
            self._parent.error_correction_level, self._curr_version)

        ret = bytearray(num_codewords)
        index = 0

        n = 0
        while index < num_data_codewords:
            r = n % len(data_block)
            c = n // len(data_block)

            if c <= len(data_block[r]) - 1:
                ret[index] = data_block[r][c]
                index += 1

            n += 1

        n = 0
        while index < num_codewords:
            r = n % len(ec_block)
            c = n // len(ec_block)

            if c <= len(ec_block[r]) - 1:
                ret[index] = ec_block[r][c]
                index += 1

            n += 1

        return ret

    def _get_message_bytes(self) -> bytes:
        """
            コード語に変換するメッセージビット列を返します。
        """
        bs = BitSequence()

        if self._parent.count > 1:
            self._write_structured_append_header(bs)

        self._write_segments(bs)
        self._write_terminator(bs)
        self._write_padding_bits(bs)
        self._write_pad_codewords(bs)
        return bs.get_bytes()

    def _write_structured_append_header(self, bs: BitSequence):
        """
            構造的連接のヘッダーを追記します。
        """
        bs.append(ModeIndicator.STRUCTURED_APPEND_VALUE,
                  ModeIndicator.LENGTH)
        bs.append(self._position,
                  SymbolSequenceIndicator.POSITION_LENGTH)
        bs.append(self._parent.count - 1,
                  SymbolSequenceIndicator.TOTAL_NUMBER_LENGTH)
        bs.append(self._parent.structured_append_parity,
                  StructuredAppend.PARITY_DATA_LENGTH)

    def _write_segments(self, bs: BitSequence):
        """
            セグメントのデータを追記します。
        """
        for segment in self._segments:
            bs.append(segment.mode_indicator, ModeIndicator.LENGTH)
            bs.append(segment.char_count,
                      CharCountIndicator.get_length(
                          self._curr_version, segment.encoding_mode))

            data = segment.get_bytes()

            for i in range(len(data) - 1):
                bs.append(data[i], 8)

            codeword_bit_length = segment.bit_count % 8

            if codeword_bit_length == 0:
                codeword_bit_length = 8

            bs.append(data[-1] >> (
                    8 - codeword_bit_length), codeword_bit_length
                      )

    def _write_terminator(self, bs: BitSequence):
        """
            終端パターンを追記します。
        """
        terminator_length = self._data_bit_capacity - self._data_bit_counter

        if terminator_length > ModeIndicator.LENGTH:
            terminator_length = ModeIndicator.LENGTH

        bs.append(ModeIndicator.TERMINATOR_VALUE, terminator_length)

    def _write_padding_bits(self, bs: BitSequence):
        """
            埋め草ビットを追記します。
        """
        if bs.length % 8 > 0:
            bs.append(0x0, 8 - (bs.length % 8))

    def _write_pad_codewords(self, bs: BitSequence):
        """
            埋め草コード語を追記します。
        """
        num_data_codewords = DataCodeword.get_total_number(
            self._parent.error_correction_level, self._curr_version)

        flag = True
        while bs.length < 8 * num_data_codewords:
            bs.append(236 if flag else 17, 8)
            flag = not flag

    def _get_module_matrix(self) -> List[List[int]]:
        """
            シンボルの明暗パターンを返します。
        """
        num_modules_per_side = Module.get_num_modules_per_side(
            self._curr_version)

        module_matrix = [None] * num_modules_per_side  # type: List[List[int]]

        for i in range(len(module_matrix)):
            module_matrix[i] = [0] * len(module_matrix)

        FinderPattern.place(module_matrix)
        Separator.place(module_matrix)
        TimingPattern.place(module_matrix)

        if self._curr_version >= 2:
            AlignmentPattern.place(module_matrix, self._curr_version)

        FormatInfo.place_temp_blank(module_matrix)

        if self._curr_version >= 7:
            VersionInfo.place_temp_blank(module_matrix)

        self._place_symbol_char(module_matrix)
        RemainderBit.place(module_matrix)

        mask_pattern_reference = Masking.apply(
            module_matrix,
            self._curr_version,
            self._parent.error_correction_level
        )

        FormatInfo.place(module_matrix,
                         self._parent.error_correction_level,
                         mask_pattern_reference)

        if self._curr_version >= 7:
            VersionInfo.place(module_matrix, self._curr_version)

        return module_matrix

    def _place_symbol_char(self, module_matrix: List[List[int]]):
        """
            シンボルキャラクタを配置します。
        """
        data = self._get_encoding_region_bytes()

        r = len(module_matrix) - 1
        c = len(module_matrix[0]) - 1

        to_left = True
        row_direction = -1

        for value in data:
            bit_pos = 7

            while bit_pos >= 0:
                columns = module_matrix[r]

                if columns[c] == 0:
                    columns[c] = 1 if (value & (1 << bit_pos)) > 0 else -1

                    bit_pos -= 1

                if to_left:
                    c -= 1
                else:
                    if (r + row_direction) < 0:
                        r = 0
                        row_direction = 1
                        c -= 1

                        if c == 6:
                            c = 5

                    elif (r + row_direction) > (len(module_matrix) - 1):
                        r = len(module_matrix) - 1
                        row_direction = -1
                        c -= 1

                        if c == 6:
                            c = 5

                    else:
                        r += row_direction
                        c += 1

                to_left = not to_left

    def get_1bpp_dib(self,
                     module_size: int = 5,
                     fore_rgb: str = ColorCode.BLACK,
                     back_rgb: str = ColorCode.WHITE) -> bytes:
        """
            シンボル画像を1bpp DIB形式で返します。
        """
        if module_size < 1:
            raise ValueError("module_size")

        (fore_r, fore_g, fore_b) = ColorCode.to_rgb(fore_rgb)
        (back_r, back_g, back_b) = ColorCode.to_rgb(back_rgb)

        module_matrix = QuietZone.place(self._get_module_matrix())

        width = module_size * len(module_matrix)
        height = width

        h_byte_len = (width + 7) // 8

        pack_8bit = 0
        if width % 8 > 0:
            pack_8bit = 8 - (width % 8)

        pack_32bit = 0
        if h_byte_len % 4 > 0:
            pack_32bit = 8 * (4 - (h_byte_len % 4))

        bs = BitSequence()

        for columns in reversed(module_matrix):
            for i in range(module_size):
                for value in columns:
                    for j in range(module_size):
                        bs.append(0 if value > 0 else 1, 1)

                bs.append(0, pack_8bit)
                bs.append(0, pack_32bit)

        data_block = bs.get_bytes()

        bfh = BITMAPFILEHEADER(
            0x4D42,
            62 + len(data_block),
            0,
            0,
            62
        )

        bih = BITMAPINFOHEADER(
            40,
            width,
            height,
            1,
            1,
            0,
            0,
            3780,
            3780,
            0,
            0
        )

        palette1 = RGBQUAD(fore_b, fore_g, fore_r)
        palette2 = RGBQUAD(back_b, back_g, back_r)

        with BytesIO() as buffer:
            buffer.write(bfh)
            buffer.write(bih)
            buffer.write(palette1)
            buffer.write(palette2)
            buffer.write(data_block)
            ret = buffer.getvalue()

        return ret

    def get_24bpp_dib(self,
                      module_size: int = 5,
                      fore_rgb: str = ColorCode.BLACK,
                      back_rgb: str = ColorCode.WHITE) -> bytes:
        """
            シンボル画像を24bpp DIB形式で返します。
        """
        if module_size < 1:
            raise ValueError("module_size")

        (fore_r, fore_g, fore_b) = ColorCode.to_rgb(fore_rgb)
        (back_r, back_g, back_b) = ColorCode.to_rgb(back_rgb)

        module_matrix = QuietZone.place(self._get_module_matrix())

        width = module_size * len(module_matrix)
        height = width

        h_byte_len = width * 3

        pack_4byte = 0
        if h_byte_len % 4 > 0:
            pack_4byte = 4 - (h_byte_len % 4)

        data_block = bytearray((h_byte_len + pack_4byte) * height)

        idx = 0

        for columns in reversed(module_matrix):
            for i in range(module_size):
                for value in columns:
                    for j in range(module_size):
                        if value > 0:
                            data_block[idx + 0] = fore_b
                            data_block[idx + 1] = fore_g
                            data_block[idx + 2] = fore_r
                        else:
                            data_block[idx + 0] = back_b
                            data_block[idx + 1] = back_g
                            data_block[idx + 2] = back_r

                        idx += 3

                idx += pack_4byte

        bfh = BITMAPFILEHEADER(
            0x4D42,
            54 + len(data_block),
            0,
            0,
            54
        )

        bih = BITMAPINFOHEADER(
            40,
            width,
            height,
            1,
            24,
            0,
            0,
            3780,
            3780,
            0,
            0
        )

        with BytesIO() as buffer:
            buffer.write(bfh)
            buffer.write(bih)
            buffer.write(data_block)
            ret = buffer.getvalue()

        return ret

    def get_ppm(self,
                module_size: int = 5,
                fore_rgb: str = ColorCode.BLACK,
                back_rgb: str = ColorCode.WHITE) -> bytes:
        """
            シンボル画像をPPMバイナリ形式で返します。
        """
        if module_size < 1:
            raise ValueError("module_size")

        (fore_r, fore_g, fore_b) = ColorCode.to_rgb(fore_rgb)
        (back_r, back_g, back_b) = ColorCode.to_rgb(back_rgb)

        module_matrix = QuietZone.place(self._get_module_matrix())

        width = module_size * len(module_matrix)
        height = width
        ppm = bytearray()

        header = "P6\n" + str(width) + " " + str(height) + "\n255\n"

        for c in header:
            ppm.append(ord(c))

        for columns in module_matrix:
            for i in range(module_size):
                for value in columns:
                    for j in range(module_size):
                        if value > 0:
                            ppm.append(fore_r)
                            ppm.append(fore_g)
                            ppm.append(fore_b)
                        else:
                            ppm.append(back_r)
                            ppm.append(back_g)
                            ppm.append(back_b)
        return bytes(ppm)

    def get_xbm(self, module_size: int = 5) -> str:
        """
            シンボル画像をXBM形式で返します。
        """
        if module_size < 1:
            raise ValueError("module_size")

        module_matrix = QuietZone.place(self._get_module_matrix())

        width = module_size * len(module_matrix)
        height = width

        pack_8bit = 0
        if width % 8 > 0:
            pack_8bit = 8 - (width % 8)

        bs = BitSequence()

        for columns in module_matrix:
            for i in range(module_size):
                for value in columns:
                    for j in range(module_size):
                        bs.append(1 if value > 0 else 0, 1)

                bs.append(0, pack_8bit)

        data_block = bs.get_bytes()

        reversed_bits_array = bytearray()

        for data in data_block:
            reversed_bits_array.append(0)
            for i in range(8):
                reversed_bits_array[-1] |= (1 if (data & 1 << i) > 0 else 0) << 7 - i

        bits_chars = []

        for bits in reversed_bits_array:
            bits_chars.append(hex(bits))

        header = ("# define img_width " + str(width) + "\n" +
                  "# define img_height " + str(height) + "\n" +
                  "static char bits[] = {" + "\n")
        xbm = header + ", ".join(bits_chars) + "};"

        return xbm

    def get_rgb_bytes(self,
                      module_size: int = 5,
                      fore_rgb: str = ColorCode.BLACK,
                      back_rgb: str = ColorCode.WHITE) -> Tuple[bytes, int, int]:
        """
            シンボル画像のRGB値を返します。
        """
        if module_size < 1:
            raise ValueError("module_size")

        (fore_r, fore_g, fore_b) = ColorCode.to_rgb(fore_rgb)
        (back_r, back_g, back_b) = ColorCode.to_rgb(back_rgb)

        module_matrix = QuietZone.place(self._get_module_matrix())

        width = module_size * len(module_matrix)
        height = width
        rgb_bytes = bytearray()

        for columns in module_matrix:
            for i in range(module_size):
                for value in columns:
                    for j in range(module_size):
                        if value > 0:
                            rgb_bytes.append(fore_r)
                            rgb_bytes.append(fore_g)
                            rgb_bytes.append(fore_b)
                        else:
                            rgb_bytes.append(back_r)
                            rgb_bytes.append(back_g)
                            rgb_bytes.append(back_b)

        return bytes(rgb_bytes), width, height

    def tk_bitmap_image(self,
                        module_size: int = 5,
                        fore_rgb: str = ColorCode.BLACK,
                        back_rgb: str = ColorCode.WHITE) -> tk.BitmapImage:
        """
            tkinter BitmapImageオブジェクトを取得します。
        """
        xbm = self.get_xbm(module_size)

        return tk.BitmapImage(data=xbm, foreground=fore_rgb, background=back_rgb)

    def tk_photo_image(self,
                       module_size: int = 5,
                       fore_rgb: str = ColorCode.BLACK,
                       back_rgb: str = ColorCode.WHITE) -> tk.PhotoImage:
        """
            tkinter PhotoImageオブジェクトを取得します。
        """
        ppm = self.get_ppm(module_size=module_size, fore_rgb=fore_rgb, back_rgb=back_rgb)

        return tk.PhotoImage(data=ppm)

    def save_1bpp_dib(self,
                      file_name: str,
                      module_size: int = 5,
                      fore_rgb: str = ColorCode.BLACK,
                      back_rgb: str = ColorCode.WHITE):
        """
            シンボル画像を1bpp DIB形式でファイルに保存します。
        """
        if not file_name:
            raise ValueError("file_name")

        if module_size < 1:
            raise ValueError("module_size")

        dib = self.get_1bpp_dib(module_size, fore_rgb, back_rgb)

        with open(file_name, "wb") as fout:
            fout.write(dib)

    def save_24bpp_dib(self,
                       file_name: str,
                       module_size: int = 5,
                       fore_rgb: str = ColorCode.BLACK,
                       back_rgb: str = ColorCode.WHITE):
        """
            シンボル画像を24bpp DIB形式でファイルに保存します。
        """
        if not file_name:
            raise ValueError("file_name")

        if module_size < 1:
            raise ValueError("module_size")

        dib = self.get_24bpp_dib(module_size, fore_rgb, back_rgb)

        with open(file_name, "wb") as fout:
            fout.write(dib)

    def save_ppm(self,
                 file_name: str,
                 module_size: int = 5,
                 fore_rgb: str = ColorCode.BLACK,
                 back_rgb: str = ColorCode.WHITE):
        """
            シンボル画像をPPM形式でファイルに保存します。
        """
        if not file_name:
            raise ValueError("file_name")

        if module_size < 1:
            raise ValueError("module_size")

        ppm = self.get_ppm(module_size, fore_rgb, back_rgb)

        with open(file_name, "wb") as fout:
            fout.write(ppm)

    def save_xbm(self, file_name: str, module_size: int = 5):
        """
            シンボル画像をXBM形式でファイルに保存します。
        """
        if not file_name:
            raise ValueError("file_name")

        if module_size < 1:
            raise ValueError("module_size")

        xbm = self.get_xbm(module_size)

        with open(file_name, "wt") as fout:
            fout.write(xbm)
