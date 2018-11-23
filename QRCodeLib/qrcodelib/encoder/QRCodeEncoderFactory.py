from ..EncodingMode import EncodingMode
from .AlphanumericEncoder import AlphanumericEncoder
from .ByteEncoder import ByteEncoder
from .KanjiEncoder import KanjiEncoder
from .NumericEncoder import NumericEncoder
from .QRCodeEncoder import QRCodeEncoder


class QRCodeEncoderFactory(object):

    @classmethod
    def create_encoder(cls,  enc_mode: int, byte_mode_encoding: str) -> QRCodeEncoder:
        if enc_mode == EncodingMode.NUMERIC:
            return NumericEncoder()

        if enc_mode == EncodingMode.ALPHA_NUMERIC:
            return AlphanumericEncoder()

        if enc_mode == EncodingMode.EIGHT_BIT_BYTE:
            return ByteEncoder(byte_mode_encoding)

        if enc_mode == EncodingMode.KANJI:
            return KanjiEncoder()
        
        raise ValueError("enc_mode")
